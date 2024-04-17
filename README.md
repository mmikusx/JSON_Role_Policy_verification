# JSON Policy Verification

This project is a Python application that verifies JSON policy documents against a predefined schema. It includes a set of unit tests to ensure the verification process works as expected.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Needed

- Python 3.6 or higher
- `jsonschema` Python package

### Installing

1. Clone the repository / copy files to your local machine.
2. Install the required Python packages using pip:

```bash
pip3 install jsonschema
```

## Usage

To use this application, you need to have a JSON policy document that you want to verify. The `verify_policy_json` function in `verify_json.py` takes the path to a JSON file as its argument and returns `True` if the JSON document is valid according to the schema, and `False` otherwise.

Here's an example of how to use it:

```python
from verify_json import verify_policy_json

is_valid = verify_policy_json('path_to_your_json_file.json')

if is_valid:
    print("The JSON document is valid.")
else:
    print("The JSON document is invalid.")
```

Replace `'path_to_your_json_file.json'` with the path to your JSON file.

## Running the tests

The tests for this project are written using the `unittest` module in Python. To run the tests, navigate to the project directory and run the following command:

```bash
python -m unittest test_verify_json.py
```

## Built With

- [Python](https://www.python.org/) - The programming language used.
- [jsonschema](https://python-jsonschema.readthedocs.io/en/stable/) - The Python library used for validating JSON documents against a schema.