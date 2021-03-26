"""
Usage: python3 ./test_cases.py [raw]

Connects to the flask host and triggers cases. Outputs the response as either formatted(default) or raw data.

Set the following environment variables to match your test setup:
TEST_FLASK_HOST = example: http://127.0.0.1
TEST_FLASK_PORT = example: 5000
"""

import sys
import requests
import os
import json

TEST_FLASK_HOST = os.getenv("TEST_FLASK_HOST")
TEST_FLASK_PORT = os.getenv("TEST_FLASK_PORT")


def show_cases(formatted=True):
    """
    Triggers the cases endpoint and outputs the response as either formatted or raw data.
    :param formatted: Boolean. True(default) - Output will be formatted / False - Output will be un-formatted
    :return: None
    """
    print(f"Pulling cases in database...")
    response = requests.get(f"http://{TEST_FLASK_HOST}:{TEST_FLASK_PORT}/cases/")
    if formatted is True:
        print(json.dumps(response.json(), indent=4))
        print(f"Number of Cases: {len(response.json())}")
    else:
        print(response.json())


if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "raw":
            show_cases(formatted=False)
        else:
            print("Unrecognized argument. Usage: python3 ./test_cases.py [raw]")
    else:
        show_cases(formatted=True)
