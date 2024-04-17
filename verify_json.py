import json
from jsonschema import validate, ValidationError


schema = {
    "type": "object",
    "properties": {
        "PolicyName": {"type": "string"},
        "PolicyDocument": {
            "type": "object",
            "properties": {
                "Version": {"type": "string"},  # opt
                "Statement": {
                    "type": "array",
                    "minItems": 1,  # min 1 statement
                    "items": {
                        "type": "object",
                        "properties": {
                            "Sid": {"type": "string"},  # opt
                            "Effect": {"type": "string", "enum": ["Allow", "Deny"]},
                            "Action": {"oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]},
                            "Resource": {"oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]},
                            "Condition": {"type": "object"}  # opt
                        },
                        "required": ["Effect", "Action", "Resource"]
                    }
                }
            },
            "required": ["Statement"]
        }
    },
    "required": ["PolicyName", "PolicyDocument"]
}


def verify_policy_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            validate(instance=data, schema=schema)

            policy_document = data['PolicyDocument']
            for statement in policy_document['Statement']:
                resource = statement.get('Resource')
                if resource is None:
                    return False
                if isinstance(resource, str):
                    if resource.strip() == '*':
                        return False
                elif isinstance(resource, list):
                    if any(not isinstance(r, str) or r.strip() == '*' for r in resource):
                        return False
                else:
                    return False
            return True
    except (json.JSONDecodeError, ValidationError, KeyError, TypeError) as e:
        # print(f"Validation error: {e}") # to see where the error is uncomment this line
        return False
