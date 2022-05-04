# Options:
#  a) Download from web link and populate into ./db folder:
#     python3 d3_populate.py https://gitlab.com/wireshark/wireshark/-/raw/master/manuf ./db
#  b) Retrieve from file and populate into ./db folder:
#     python3 d3_populate.py ../examples/manuf.txt ./db

import re
import csv
import requests
import sys
import os
import yaml
import uuid

GIT_REPO_ADDRESS = "https://gitlab.com/wireshark/wireshark/-/raw/master/manuf"
POPULATE_FOLDER_PATH = "./db"
DEVICE_TYPE_FILENAME = "device.type.d3.yaml"

def get_web_file(url: str):
    data = requests.get(url, allow_redirects=True)
    csv_out = csv.reader(data.text.splitlines(), delimiter='\t')
    return csv_out

def get_storage_file(path: str):
    try:
        with open(path, 'r') as f: 
            content = f.read()
            csv_out = csv.reader(content.splitlines(), delimiter='\t')
        return csv_out
    except OSError:
        pass

def generate_d3_type(mac: str, short_name: str, long_name: str):
    return {
        "type": "d3-device-type-assertion",
        "credentialSubject": {
            "id": str(uuid.uuid4()),
            "manufacturer": long_name,
            "manufacturer-uri": "https://device-type.com",
            "name": short_name,
            "mac-addresses": []
        }
    }

def dump_yaml_files(populate_folder: str, d3_dict):
    for key in d3_dict:
        company_folder_path = "{}/{}".format(populate_folder, key)

        # Create the folder with the given short company name
        os.makedirs(company_folder_path, exist_ok=True)

        yaml_file_path = "{}/{}".format(company_folder_path, DEVICE_TYPE_FILENAME)

        d3_type = d3_dict[key]
        with open(yaml_file_path, mode="wt", encoding="utf-8") as file:
            yaml.dump(d3_type, file)
            print("Added {}".format(yaml_file_path))

def d3_populate(csv_data, populate_folder: str):
    print('Populating with data from {}'.format(git_repo))
    print('Populating to {}'.format(populate_folder))

    hp = "[0-9a-fA-F]{2}"
    manuf_re = re.compile(r'^({}:{}:{})((:{})*)(/[0-9][0-9])*$'.format(hp, hp, hp, hp))

    d3_dict = {}

    for row in csv_out:
        # Only process rows that have a MAC address and company assigned
        if len(row) >= 2:
            m = manuf_re.match(row[0])
            if m != None:
                if m.group(2) == "":
                    mac = m.group(1) + ":00:00:00/24"
                else:
                    mac = m.group(1) + m.group(2) + m.group(4)

                # Create the folder with the company name
                short_name = row[1]

                
                try:
                    long_name = row[2]
                except:
                    long_name = ""

                if short_name in d3_dict:
                    d3_type = d3_dict[short_name]
                else:
                    d3_type = generate_d3_type(mac, short_name, long_name)

                # Add the mac address to the corresponding company
                d3_type["credentialSubject"]["mac-addresses"].append(mac)
                d3_dict[short_name] = d3_type

    # Save the yaml/json object to files
    dump_yaml_files(populate_folder, d3_dict)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        git_repo = GIT_REPO_ADDRESS
        populate_folder = POPULATE_FOLDER_PATH
    elif len(sys.argv) == 2:
        git_repo = sys.argv[1]
        populate_folder = POPULATE_FOLDER_PATH
    else:
        git_repo = sys.argv[1]
        populate_folder = sys.argv[2]

    csv_out = get_storage_file(git_repo)
    if csv_out == None:
        csv_out = get_web_file(git_repo)

    d3_populate(csv_out, populate_folder)