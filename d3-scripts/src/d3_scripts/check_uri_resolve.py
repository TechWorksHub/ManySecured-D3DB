import validators
import requests
import warnings


def check_uri(json_data: dict, schema: dict, check_uri_resolves: bool) -> None:
    """Checks uri resolves in a JSON object, provids soft warning if not.

    Args:
        json_data: The JSON object to check
        schema: The JSON schema to use
        check_uri_resolves: Whether to check if the uri resolves.

    Returns:
        None
    """
    properties = schema["properties"]
    uri_fields = [key for key in properties.keys()
                  if properties[key].get("format") == "uri"]

    for uri_field in uri_fields:
        uri = json_data.get(uri_field)
        if(uri is not None):
            is_valid_uri(uri)
            if check_uri_resolves:
                uri_resolves(uri)


def is_valid_uri(uri: str) -> None:
    """Checks if a URI is valid.
    Args:
        uri: The URI to check
    Returns:
        None
    """
    if (not validators.url(uri)):
        raise ValueError(uri + " is not a valid URI")


def uri_resolves(uri: str) -> None:
    """Checks if a URI resolves, provides a soft warning if not
    Args:
        uri: The URI to check
    Returns:
        None
    """

    # TODO: Temporary bypass for example uri
    if(not uri == "https://device-type.com"):
        try:
            # timeout of 5 seconds is pretty slow, but so are some people's servers
            response = requests.head(uri, timeout=5)
            # throws an error if HTTP Code >= 400
            response.raise_for_status()
        except Exception as error:
            warnings.warn(f"URI {uri} cannot be resolved: {error}")
