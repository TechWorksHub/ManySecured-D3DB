import validators
import requests
import logging


def check_uri_resolve(json_data: dict, schema: dict) -> None:
    """Checks uri resolves in a JSON object, provids soft warning if not.
    Args:
        json_data: The JSON object to check
        schema: The JSON schema to use
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
            response = requests('GET', uri, retries=False)
            if(response.status != 200):
                raise ValueError()
        except Exception:
            logging.warning("URI " + uri + " cannot be resolved")
