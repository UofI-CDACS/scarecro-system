from jsonschema import validate
import json 

instance_name = "example_instances/gateway_1.json"

with open(instance_name) as f:
    sample_instance = json.load(f)


with open("schemas/instance_schema.json") as f:
    instance_schema = json.load(f)

validate(instance=sample_instance, schema=instance_schema)