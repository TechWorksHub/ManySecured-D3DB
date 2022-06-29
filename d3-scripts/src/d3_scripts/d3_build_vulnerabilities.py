import requests
import json
import urllib.parse as urllp


def encodeURIComponent(s): return urllp.quote(s, safe="~()*!.'")
def json_stringify(s): return json.dumps(s, separators=(',', ':'))


string_to_search_for = "apple"

ndJSON = False
datasetId = "Efl8dagnBm"
pipeline = [{"$match": {"search_string": {"$regex": string_to_search_for, "$options": "i"}}}]
format = "aggregate"
if ndJSON:
    format = "ndaggregate"
pipeline = encodeURIComponent(json_stringify(pipeline))
endpoint = f"resources/{datasetId}/{format}?pipeline={pipeline}"
queryServer = "https://q.nqm-2.com/v1/"
query = endpoint
request = f"{queryServer}{query}"
print(request)
response_API = requests.get(request)
data = json.loads(response_API.text)
print(data)
