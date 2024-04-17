import json
import unittest
import os
from verify_json import verify_policy_json


def write_to_file(json_data, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(json_data, file)
        return True
    except Exception as e:
        print(f"Error writing to file: {e}")
        return False


class TestVerifyJson(unittest.TestCase):
    def setUp(self):
        self.files_to_remove = []

    def tearDown(self):
        for file_path in self.files_to_remove:
            try:
                os.remove(file_path)
            except OSError:
                pass

    def test_valid_json(self):
        valid_json = {
            "PolicyName": "root",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "IamListAccess",
                        "Effect": "Allow",
                        "Action": [
                            "iam:ListRoles",
                            "iam:ListUsers"
                        ],
                        "Resource": "arn:aws:iam::123456789012:user/*"
                    }
                ]
            }
        }
        write_to_file(valid_json, 'valid.json')
        self.assertTrue(verify_policy_json('valid.json'))
        self.files_to_remove.append('valid.json')

    def test_invalid_schema(self):
        invalid_schema_json = {
            "PolicyName": "root",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "IamListAccess",
                        "Effect": "Allow",
                        "Action": [
                            "iam:ListRoles",
                            "iam:ListUsers"
                        ]
                    }
                ]
            }
        }
        write_to_file(invalid_schema_json, 'invalid_schema.json')
        self.assertFalse(verify_policy_json('invalid_schema.json'))
        self.files_to_remove.append('invalid_schema.json')

    def test_single_asterisk(self):
        single_asterisk_json = {
            "PolicyName": "root",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "IamListAccess",
                        "Effect": "Allow",
                        "Action": [
                            "iam:ListRoles",
                            "iam:ListUsers"
                        ],
                        "Resource": "*"
                    }
                ]
            }
        }
        write_to_file(single_asterisk_json, 'single_asterisk.json')
        self.assertFalse(verify_policy_json('single_asterisk.json'))
        self.files_to_remove.append('single_asterisk.json')

    def test_missing_resource(self):
        missing_resource_json = {
            "PolicyName": "root",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "IamListAccess",
                        "Effect": "Allow",
                        "Action": [
                            "iam:ListRoles",
                            "iam:ListUsers"
                        ]
                    }
                ]
            }
        }
        write_to_file(missing_resource_json, 'missing_resource.json')
        self.assertFalse(verify_policy_json('missing_resource.json'))
        self.files_to_remove.append('missing_resource.json')

    def test_invalid_resource_type(self):
        invalid_resource_type_json = {
            "PolicyName": "root",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "IamListAccess",
                        "Effect": "Allow",
                        "Action": [
                            "iam:ListRoles",
                            "iam:ListUsers"
                        ],
                        "Resource": 123
                    }
                ]
            }
        }
        write_to_file(invalid_resource_type_json, 'invalid_resource_type.json')
        self.assertFalse(verify_policy_json('invalid_resource_type.json'))
        self.files_to_remove.append('invalid_resource_type.json')

    def test_invalid_resource_value(self):
        invalid_resource_value_json = {
            "PolicyName": "root",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "IamListAccess",
                        "Effect": "Allow",
                        "Action": [
                            "iam:ListRoles",
                            "iam:ListUsers"
                        ],
                        "Resource": ["arn:aws:iam::123456789012:user/*", 123]
                    }
                ]
            }
        }
        write_to_file(invalid_resource_value_json, 'invalid_resource_value.json')
        self.assertFalse(verify_policy_json('invalid_resource_value.json'))
        self.files_to_remove.append('invalid_resource_value.json')


if __name__ == '__main__':
    unittest.main()
