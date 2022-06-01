def resolve_behaviour_rules(claim, claim_tree):
    """
    Resolve rules which apply for behaviour claim, and checks that any named rules exist and that
    there are no duplicate rule names in claim behaviour.

    Args:
        claim: The D3 behaviour claim to resolve behaviour for (dict)
        claim_tree: The claim inheritance tree for the claim (array of array of dict)

    Returns:
        The rules which apply to the behaviour claim. (array of dicts)

    """
    aggregated_rules = []
    rules = claim["credentialSubject"].get("rules", [])
    aggregated_rules += rules
    for index, behaviours in enumerate(claim_tree[0:-1]):
        for behaviour in behaviours:
            behaviour_parents = behaviour["credentialSubject"].get("parents", [])
            for parent in behaviour_parents:
                id = parent["id"]
                parent_behaviour = find_behaviour(id, claim_tree[index + 1])
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
