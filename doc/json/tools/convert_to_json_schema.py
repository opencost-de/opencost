#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Basic converter to transform the openCost XSD schema into a JSON schema.

This is no general JSON to XSD converter and only implements a specific 
subset of XSD element combinations used in openCost. It also relies on all
types definitions being stored as top-level elements in the XSD.
"""

import argparse
import json
import sys
import xml.etree.ElementTree as ET

from collections import OrderedDict

class UnsupportedXSDStructure(Exception):

    def __init__(self, type_element, children_allowed):
        elem_name = type_element.attrib.get("name")
        elem_name = "(" + elem_name + ")" if elem_name is not None else ""
        elem_tag = type_element.tag
        msg = "Element '{}' {}: Only the following children of this element are currently supported: {}"
        msg = msg.format(elem_tag, elem_name, ", ".join(children_allowed))
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
# 5) Store completely converted complex types in a lookup table.
#
# Additional remarks:
# - sequence/choice structures in the openCost XSD are usually applied to allow free element ordering.
# - In contrast to XML child elements, JSON objects properties are unordered. This means we can usually treat <xs:all> and <xs:sequence> as identical.
# - Converting these directly may lead to very complicated allOf/OneOf JSON constructs. If possible, these should be simplified after conversion.

# XSD types converted to JSON structures

CONVERTED_TYPES = {
    "xs:boolean": OrderedDict(
        {"enum": ["1", "0", True, False]}
    ),
    "xs:decimal": OrderedDict(
        {"type": "number"}
    ),
}

RESTRICTION_BASE_TYPES = {
    "xs:string": "string"
}

XSD_COMPLEX_TYPES = {}
XSD_SIMPLE_TYPES = {}

def convert_element(elem, tle=False):
    ret = OrderedDict()
    elem_type = elem.attrib.get("type")
    elem_name = elem.attrib.get("name")
    if elem_type is not None:
        if elem_type not in CONVERTED_TYPES:
            CONVERTED_TYPES[elem_type] = convert_complex_type(XSD_COMPLEX_TYPES[elem_type])
        type_structure = CONVERTED_TYPES[elem_type]
        if tle:
            ret[elem_name] = type_structure
        else:
            ret = type_structure
    return ret

def convert_sequence_indicator(seq_elem):
    ret = OrderedDict({
        "type": "object",
        "additionalProperties": False,
        "properties": {}
    })
    sequence_skippable = False
    if seq_elem.attrib.get("minOccurs") == "0":
        sequence_skippable = True
    elements = seq_elem.findall("xs:element", namespaces)
    if len(elements) > 0:
        required_list = []
        for element in elements:
            name = element.attrib["name"]
            min_occurs = element.attrib.get("minOccurs", "1")
            max_occurs = element.attrib.get("maxOccurs", "1")
            max_occurs_number = 1
            if max_occurs.isdecimal():
                max_occurs_number = int(max_occurs)
            if max_occurs == "unbounded" or max_occurs_number > 1:
                ret["properties"][name] = OrderedDict({
                    "type": "array",
                    "minItems": 1,
                    "contains": convert_element(element)
                })
            else:
                ret["properties"][name] = convert_element(element)
            if min_occurs == "0" or sequence_skippable:
                pass
            else:
                required_list.append(OrderedDict({"required": [name]}))
        if len(required_list) > 0:
            ret["allOf"] = required_list
    sub_sequences = seq_elem.findall("xs:sequence", namespaces)
    if len(sub_sequences) > 0:
        for sequence in sub_sequences:
            seq_structure = convert_sequence_indicator(sequence)
            for name, elem_structure in seq_structure["properties"].items():
                ret["properties"][name] = elem_structure
            if "allOf" in seq_structure:
                if "allOf" in ret:
                    ret["allOf"] += seq_structure["allOf"]
                else:
                    ret["allOf"] = [seq_structure["allOf"]]
    sub_choices = seq_elem.findall("xs:choice", namespaces)
    if len(sub_choices) > 0:
        for choice in sub_choices:
            choice_structure = convert_choice_indicator(choice)
            #print(json.dumps(choice_structure, indent=2))
            for name, elem_structure in choice_structure["properties"].items():
                ret["properties"][name] = elem_structure
            if "allOf" in choice_structure:
                if "allOf" in ret:
                    ret["allOf"] += choice_structure["allOf"]
                else:
                    ret["allOf"] = [choice_structure["allOf"]]
            elif "anyOf" in choice_structure:
                any_of = OrderedDict({"anyOf": choice_structure["anyOf"]})
                if "allOf" in ret:
                    ret["allOf"] += any_of
                else:
                    ret["allOf"] = [any_of]
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
            min_occurs = element.attrib.get("minOccurs", "1")
            ret["properties"][name] = convert_element(element)
            if min_occurs == "0":
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
    })
    max_occurs = choice_elem.attrib.get("maxOccurs", "1")
    max_occurs_number = 1
    if max_occurs.isdecimal():
        max_occurs_number = int(max_occurs)
    elements = choice_elem.findall("xs:element", namespaces)
    sequences = choice_elem.findall("xs:sequence", namespaces)
    if len(elements) > 0:
        ret["oneOf"] = []
        if max_occurs == "unbounded" or max_occurs_number > 1:
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
    elif len(sequences) > 0:
        all_ofs = []
        for sequence in sequences:
            seq_structure = convert_sequence_indicator(sequence)
            for name, elem_structure in seq_structure["properties"].items():
                ret["properties"][name] = elem_structure
            if "allOf" in seq_structure:
                all_ofs.append(seq_structure["allOf"])
        if len(all_ofs) > 0:
            # If all all_ofs dicts are identical, we can merge them into a single structure
            if all_ofs.count(all_ofs[0]) == len(all_ofs):
                ret["allOf"] = all_ofs[0]
            else:
                ret["anyOf"] = [elem[0] for elem in all_ofs]
    else:
        raise UnsupportedXSDStructure(choice_elem, ["xs:element", "xs:sequence"])
    return ret

def convert_complex_type(complex_element):
    choice_elem = complex_element.find("xs:choice", namespaces)
    all_elem = complex_element.find("xs:all", namespaces)
    seq_elem = complex_element.find("xs:sequence", namespaces)
    if choice_elem is not None:
        return convert_choice_indicator(choice_elem)
    elif all_elem is not None:
        return convert_all_indicator(all_elem)
    elif seq_elem is not None:
        return convert_sequence_indicator(seq_elem)
    else:
        raise UnsupportedXSDStructure(complex_element, ["xs:choice", "xs:all", "xs:sequence"])

def convert_simple_type(simple_element):
    ret = OrderedDict()
    res_elem = simple_element.find("xs:restriction", namespaces)
    if res_elem is None:
        raise UnsupportedXSDStructure(simple_element, ["xs:restriction"])
    type_restriction = RESTRICTION_BASE_TYPES.get(res_elem.attrib.get("base", ""), None)
    if type_restriction is not None:
        ret["type"] = type_restriction
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
        raise UnsupportedXSDStructure(res_elem, ["xs:enumeration", "xs:pattern", "xs:minLength"])
    return ret

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("xsd_files", nargs="+", help=HELP_MSGS["xsd_files"])
    args = parser.parse_args()

    top_level_element = None

    for xsd_file in args.xsd_files:
        tree = ET.parse(xsd_file)
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

    json_schema["properties"] = convert_element(top_level_element, tle=True)
    json_schema["required"] = [top_level_element.attrib["name"]]

    with open("json_schema_out.json", "w", encoding="utf-8") as out:
        out.write(json.dumps(json_schema, indent=2))

if __name__ == '__main__':
    main()
