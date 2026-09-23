# openCost JSON Metadata Schemas

This directory contains a [JSON Schema variant](https://github.com/opencost-de/opencost/blob/main/doc/json/opencost.json)
of the original openCost metadata schema which can be used to validate
JSON documents containing openCost data. 

## Converter

The schema has been automatically transformed using a python
[converter](https://github.com/opencost-de/opencost/blob/main/doc/json/tools/convert_to_json_schema.py).
Usage:

```bash
`python convert_to_json_schema.py ../../opencost.xsd ../../opencost_types.xsd
```

This will generate an output file `json_schema_out.json`. 

The converter has been tested with Python 3.12 and 3.14 and does not rely on any external modules. Please note that it has been implemented specifically with the openCost schema in mind and will probably not work with other XSD files.

## Examples

The `examples` directory contains openCost JSON documents which have been converted from the [XML examples](https://github.com/opencost-de/opencost/tree/main/doc/examples) and are valid against the JSON schema. Using a CLI validator like [check-jsonschema](https://github.com/python-jsonschema/check-jsonschema), the directory's content may be valiated like this:

```bash
check-jsonschema --schemafile opencost.json examples/*.json
```
