d3_type_codes = {
    "behaviour": "d3-device-type-behaviour",
    "firmware": "d3-firmware-assertion",  # TODO: check definition
    "inheritance": "d3-device-type-inheritance",
    "type": "d3-device-type-assertion",
    "vuln": "d3-device-instance-vuln",
}

d3_type_codes_to_schemas = {
    d3_type_code: schema_name
    for schema_name, d3_type_code in d3_type_codes.items()
}

d3_types = d3_type_codes.keys()
d3_codes = d3_type_codes.values()
