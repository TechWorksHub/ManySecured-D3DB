import requests
import logging
import urllib.parse


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
            # technically, this checks if the URI is valid URL,
            # but they're close enough that this will probably be okay
            urllib.parse.urlparse(uri) # throws if invalid
            uri_resolves(uri)


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
