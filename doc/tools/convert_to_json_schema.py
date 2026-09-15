#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import json
import sys
import xml.etree.ElementTree as ET

from collections import OrderedDict

class UnsupportedXSDStructure(Exception):
    
    def __init__(self, type_element, parent, children_allowed):
        elem_name = type_element.attrib["name"]
        msg = "Type '{}': Only the following children of {} are currently supported: {}"
        msg = msg.format(elem_name, parent, ", ".join(children_allowed))
        super().__init__(msg)

HELP_MSGS = {
    "xsd_files": "One or more XSD Schema files which should be converted to JSON Schema"
}

namespaces = {
    "opencost": "https://opencost.de",
    "xs": "http://www.w3.org/2001/XMLSchema"
}

json_schema = OrderedDict({
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://opencost.de",
    "title": "openCost JSON Schema",
    "description": "Validates openCost records in JSON. Automatically transformed from the original openCost XSD Schema.",
    "type": "object",
    "additionalProperties": False
})

# General approach to XSD conversion:
# 1) From the XSD files extract a top-level element and all top-level types
# 2) Convert all SimpleTypes to JSON Schema Structures
# 3) Start constructing the JSON Schema recursively from the TLE
# 4) When encountering a type definition, convert the corresponding XSD type to JSON. Apply recursion if encountering more types during the process.
# 5) Store completely converted JSON structures in a lookup table. 
#
# Additional insights:
# In contrast to XML child elements, JSON objects properties are unordered. This means we can treat <xs:all> and <xs:sequence> as identical.

# XSD types converted to JSON structures

CONVERTED_TYPES = {
    "xs:boolean": OrderedDict({
        "enum": ["1", "0", True, False]
    }),
}
XSD_COMPLEX_TYPES = {}
XSD_SIMPLE_TYPES = {}

def convert_element(elem, tle=False):
    ret = OrderedDict()
    elem_type = elem.attrib.get("type")
    elem_name = elem.attrib.get("name")
    print(elem_type)
    if elem_type is not None:
        if elem_type not in CONVERTED_TYPES:
            CONVERTED_TYPES[elem_type] = convert_complex_type(XSD_COMPLEX_TYPES[elem_type])
        type_structure = CONVERTED_TYPES[elem_type]
        if tle:
            ret[elem_name] = type_structure
        else:
            ret = type_structure
    return ret

def convert_all_indicator(all_elem):
    ret = OrderedDict({
        "type": "object",
        "additionalProperties": False,
        "properties": {}
    })
    elements = all_elem.findall("xs:element", namespaces)
    if len(elements) > 0:
        required_list = []
        for element in elements:
            name = element.attrib["name"]
            minOccurs = element.attrib.get("minOccurs", "1")
            ret["properties"][name] = convert_element(element)
            if minOccurs == "0":
                pass
            else:
                required_list.append(OrderedDict({"required": [name]}))
        if len(required_list) > 0:
            ret["allOf"] = required_list
    return ret

def convert_choice_indicator(choice_elem):
    ret = OrderedDict({
        "type": "object",
        "additionalProperties": False,
        "properties": OrderedDict(),
        "oneOf": []
    })
    maxOccurs = choice_elem.attrib.get("maxOccurs", "1")
    maxOccursNumber = 1
    if maxOccurs.isdecimal():
        maxOccursNumber = int(maxOccurs)
    elements = choice_elem.findall("xs:element", namespaces)
    if maxOccurs == "unbounded" or maxOccursNumber > 1:
        for element in elements:
            name = element.attrib["name"]
            ret["properties"][name] = OrderedDict({
                "type": "array",
                "minItems": 1,
                "contains": convert_element(element)
            })
            ret["oneOf"].append(OrderedDict({"required": [name]}))
    else:
        for element in elements:
            name = element.attrib["name"]
            ret["properties"][name] = convert_element(element)
            ret["oneOf"].append(OrderedDict({"required": [name]}))
    return ret

def convert_complex_type(complex_element):
    choice_elem = complex_element.find("xs:choice", namespaces)
    all_elem = complex_element.find("xs:all", namespaces)
    if choice_elem is not None:
        return convert_choice_indicator(choice_elem)
    elif all_elem is not None:
        return convert_all_indicator(all_elem)
    return {}

def convert_simple_type(simple_element):
    ret = OrderedDict()
    res_elem = simple_element.find("xs:restriction", namespaces)
    if res_elem is None:
        raise UnsupportedXSDStructure(simple_element, "xs:simpleType", ["xs:restriction"])
    enums = res_elem.findall("xs:enumeration", namespaces)
    pattern = res_elem.find("xs:pattern", namespaces)
    minlength = res_elem.find("xs:minLength", namespaces)
    if len(enums) > 0:
        ret["enum"] = []
        for enum_elem in enums:
            value = enum_elem.attrib["value"]
            ret["enum"].append(value)
    elif pattern is not None:
        value = pattern.attrib["value"]
        ret["pattern"] = value
    elif minlength is not None:
        value = minlength.attrib["value"]
        ret["minLength"] = int(value)
    else:
        raise UnsupportedXSDStructure(simple_element, "xs:restriction", ["xs:enumeration", "xs:pattern", "xs:minLength"])
    return ret

parser = argparse.ArgumentParser()
parser.add_argument("xsd_files", nargs="+", help=HELP_MSGS["xsd_files"])
args = parser.parse_args()

top_level_element = None

for xsd_file in args.xsd_files:
    tree = ET.parse(xsd_file)
    root = tree.getroot()
    complex_type_elems = tree.findall("./xs:complexType", namespaces)
    for comp_type_elem in complex_type_elems:
        type_name = comp_type_elem.attrib["name"]
        XSD_COMPLEX_TYPES[type_name] = comp_type_elem
    simple_type_elems = tree.findall("./xs:simpleType", namespaces)
    for simp_type_elem in simple_type_elems:
        type_name = simp_type_elem.attrib["name"]
        XSD_SIMPLE_TYPES[type_name] = simp_type_elem
    tle = tree.find("./xs:element", namespaces)
    if tle is not None:
        if top_level_element is None:
            top_level_element = tle
        else:
            print("ERROR: More than one top-level xs:element found!")
            sys.exit()

for type_name, simp_type_elem in XSD_SIMPLE_TYPES.items():
    CONVERTED_TYPES[type_name] = convert_simple_type(simp_type_elem)

print(json.dumps(CONVERTED_TYPES, indent=2))
#print(XSD_COMPLEX_TYPES['data_type'].tag)
#print(XSD_COMPLEX_TYPES['data_type'].tag == "xs:complexType")
#print(json.dumps(convert_complex_type(XSD_COMPLEX_TYPES['data_type']), indent=2))
json_schema["properties"] = convert_element(top_level_element, tle=True)
json_schema["required"] = [top_level_element.attrib["name"]]
print(json.dumps(json_schema, indent=2))
with open("json_schema_out.json", "w") as out:
        out.write(json.dumps(json_schema, indent=2))
