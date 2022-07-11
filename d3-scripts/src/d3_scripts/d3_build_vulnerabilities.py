import requests
import json
import urllib.parse as urllp
import re


def encodeURIComponent(s): return urllp.quote(s, safe="~()*!.'")
def json_stringify(s): return json.dumps(s, separators=(',', ':'))


def reproject(vuln):
    return {
            "type": "d3-device-type-vuln",
            "credentialSubject": {
                "id": vuln["CVE_data_meta"]["ID"],
                "vulnerability": f"https://nvd.nist.gov/vuln/detail/{vuln['CVE_data_meta']['ID']}"
            }
        }


def get_vulnerabilities(string_to_search_for, projection={"CVE_data_meta": 1}):
    ndJSON = False
    datasetId = "Efl8dagnBm"
    filter = {"$text": {"$search": string_to_search_for}}
    filterStr = encodeURIComponent(json_stringify(filter))
    projectionStr = ""
    if projection is not None:
        projectionStr = encodeURIComponent(json_stringify(projection))
    format = "data"
    if ndJSON:
        format = "nddata"
    endpoint = f"resources/{datasetId}/{format}"
    queryServer = "https://q.nqm-2.com/v1/"
    query = f"{endpoint}?filter={filterStr}&proj={projectionStr}"
    request = f"{queryServer}{query}"
    response_API = requests.get(request)
    data = json.loads(response_API.text)["data"]
    return data


def build_vulnerabilities(type_jsons, pbar=None, percentage_total=None):
    retrieved_cve_vulnerabilities = []
    for i, type_json in enumerate(type_jsons):
        progress_increment = 1/len(type_jsons)
        pbar.update(progress_increment * percentage_total/100)
        search_term = type_json["credentialSubject"].get("modelNumber", None)
        if search_term is None:
            search_term = type_json["credentialSubject"].get("name", None)
        if search_term is not None:
            cve_vulnerabilities = get_vulnerabilities(re.escape(search_term))
            cve_vulnerabilities = [reproject(vuln) for vuln in cve_vulnerabilities]
            current_vulnerabilities = []
            try:
                current_vulnerabilities = type_json["credentialSubject"]["vulnerabilities"]
            except KeyError:
                pass
            cve_vulnerability_ids = [entry["credentialSubject"]["id"] for entry in cve_vulnerabilities]
            type_json["credentialSubject"]["vulnerabilities"] = current_vulnerabilities + cve_vulnerability_ids
            retrieved_cve_vulnerabilities += cve_vulnerabilities
    return retrieved_cve_vulnerabilities
