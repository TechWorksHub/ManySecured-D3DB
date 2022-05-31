import functools
import logging
import typing
import warnings
from pathlib import Path
import multiprocessing

import tqdm

from .yaml_tools import is_valid_yaml_claim, load_claim, lint_yaml
from .json_tools import is_json_unchanged, get_json_file_name, write_json
from .validate_schemas import (
    get_schema_validator_from_path,
    validate_claim_meta_schema,
    validate_d3_claim_schema,
)
from .check_uri_resolve import check_uri
from .check_behaviours_resolve import check_behaviours_resolve, BehaviourJsons
from .check_parents_resolve import check_parents_resolve
from .d3_constants import d3_type_codes


def _validate_d3_claim_uri(yaml_file_path: str, **check_uri_kwargs):
    """Checks whether the given YAML file has valid URIs.

    Raises:
        Exception: If the YAML file has a URI that is not valid/resolveable.
    """
    # import yaml claim to Python dict (JSON)
    claim = load_claim(yaml_file_path)
    schema = get_schema_validator_from_path(yaml_file_path).schema
    # check URIs and other refs resolve
    check_uri(
        claim["credentialSubject"],
        schema,
        **check_uri_kwargs,
    )


def validate_d3_claim_files(
    yaml_file_names: typing.Sequence[str],
    check_uri_resolves: bool = False
):
    """Checks whether D3 claim files are valid.

    Performs each check sequentially, (e.g. like a normal CI task)
    so if one fails, the rest are not checked.
    """
    stages = {
        "Checking if D3 files have correct filename": is_valid_yaml_claim,
        "Linting D3 files": lint_yaml,
        "Checking whether D3 files match JSONSchema": validate_d3_claim_schema,
        "Checking whether URIs/refs resolve": functools.partial(
            _validate_d3_claim_uri, check_uri_resolves=check_uri_resolves,
        ),
    }

    with multiprocessing.Pool() as pool:
        for description, function in stages.items():
            # use imap so that progress bar only updates when each chunk is done
            result_generator = pool.imap(function, yaml_file_names, chunksize=16)
            for _result in tqdm.tqdm(
                result_generator,
                unit="files",
                desc=description,
                disable=logging.getLogger().getEffectiveLevel() > logging.INFO,
                delay=0.5,  # delay to show progress bar
                total=len(yaml_file_names),
            ):
                pass

    return True


def process_claim_file(
    yaml_file_name: str, behaviour_jsons: BehaviourJsons,
    check_uri_resolves: bool,
    pass_on_failure: bool,
) -> typing.List[Warning]:
    """Processes a single D3 claim file.
    Checks include:
    - is unchanged claim
    - is valid claim relative to JSONSchema for type
    - are all URIs/refs resolveable/valid
    - behaviour statements are valid

    Args:
        yaml_file_name: The filepath to the YAML file
        check_uri_resolves: Whether to check URIs/refs resolveable/valid

    Returns:
        List of warnings. If empty, no warnings.
        Warnings are hidden by default in multiprocessing.
    """
    json_file_name = get_json_file_name(yaml_file_name)
    Path(json_file_name).parent.mkdir(parents=True, exist_ok=True)

    # import yaml claim to Python dict (JSON)
    claim = load_claim(yaml_file_name)

    # if JSON already exists and is unchanged then skip
    # (unless it's a behaviour claim)
    if is_json_unchanged(json_file_name, claim) and claim["type"] != d3_type_codes["behaviour"]:
        return []

    # validate schema
    validate_claim_meta_schema(claim)

    try:
        schema_validator = get_schema_validator_from_path(yaml_file_name)
        schema = schema_validator.schema
        schema_validator.validate(claim["credentialSubject"])

        # check URIs and other refs resolve
        with warnings.catch_warnings(record=True) as uri_warnings:
            check_uri(
                claim["credentialSubject"],
                schema,
                check_uri_resolves=check_uri_resolves
            )

        # check behaviour statement is valid, if so add to claim
        claim["credentialSubject"] = check_behaviours_resolve(
            claim["credentialSubject"],
            schema,
            behaviour_jsons)

        if claim["type"] == d3_type_codes["behaviour"]:
            # Checks all parent behaviours exist, checks for circular dependencies and retrieves parent behaviour claims
            parents = check_parents_resolve(claim, behaviour_jsons)
            # Gets aggregated rules, checking that specified parent rules exist and that no rule names are duplicated
            aggregated_rules = resolve_behaviour_rules(claim, parents)
            # Replace claim rules with aggregated rules from parents
            claim["credentialSubject"]["rules"] = aggregated_rules

        # write JSON if valid
        write_json(json_file_name, claim)

        return [*uri_warnings]
    except FileNotFoundError as err:
        if (pass_on_failure):
            print(f"\nWARNING! Skipping claim {yaml_file_name} due to error: ${err}")
            return []
        else:
            raise err


def resolve_behaviour_rules(claim, parents):
    aggregated_rules = []
    rules = claim["credentialSubject"].get("rules", [])
    aggregated_rules += rules
    for index, behaviours in enumerate(parents[0:-1]):
        for behaviour in behaviours:
            behaviour_parents = behaviour["credentialSubject"].get("parents", [])
            for parent in behaviour_parents:
                id = parent["id"]
                parent_behaviour = find_behaviour(id, parents[index + 1])
                parent_rules = parent_behaviour["credentialSubject"].get("rules", [])
                rules_to_inherit = parent.get("rules", [])
                if len(rules_to_inherit) > 0:
                    for rule in rules_to_inherit:
                        inherited_rule = find_rule(rule, parent_rules)
                        if not inherited_rule:
                            behaviour_id = behaviour["credentialSubject"]["id"]
                            raise ValueError(f"""Non-Existant Rule Error: Behaviour {behaviour_id}
                            attempted to inherit non-existent rule {rule} from behaviour {id}""")
                        existing_rule = find_rule(rule, aggregated_rules)
                        if existing_rule:
                            behaviour_id = behaviour["credentialSubject"]["id"]
                            raise ValueError(f"""Duplicate Rule Error: Behaviour {behaviour_id}
                            attempted to inherit duplicate rule {rule} from behaviour {id}""")
                        aggregated_rules += [inherited_rule]
                else:
                    aggregated_rules += parent_rules
    return aggregated_rules


def find_behaviour(id, behaviours):
    return next((item for item in behaviours if item["credentialSubject"]["id"] == id), None)


def find_rule(name, rules):
    return next((item for item in rules if item["name"] == name), None)
