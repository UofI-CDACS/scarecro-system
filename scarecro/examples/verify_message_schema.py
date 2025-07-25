from jsonschema import validate
import json 


message_name = "example_messages/weather_rack.json"
with open(message_name) as f:
    sample_message = json.load(f)

with open("schemas/message_schema.json") as f:
    message_schema = json.load(f)

with open("schemas/field_schema.json") as f:
    field_schema = json.load(f)


message_schema["properties"]["fields"] = {
    "type": "array",
    "items": field_schema
    }

validate(instance=sample_message, schema=message_schema)