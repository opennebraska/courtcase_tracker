"""
Usage: python3 ./test_add_data.py YYYY-MM-DD

Connects to the flask host and triggers adddata for the provided date

Set the following environment variables to match your test setup:
TEST_FLASK_HOST = example: http://127.0.0.1
TEST_FLASK_PORT = example: 5000
"""

import sys
import requests
import os
import datetime as dt
import json

TEST_FLASK_HOST = os.getenv("TEST_FLASK_HOST")
TEST_FLASK_PORT = os.getenv("TEST_FLASK_PORT")

formatted_today = dt.datetime.now().strftime("%Y-%m-%d")


def trigger_add_data(date=formatted_today):
    """
    Triggers the adddata endpoint using the provided date
    :param date: string containing the date to pull in the format YYYY-MM-DD
    :return: None
    """
    parameters = {
        "date": date
    }

    print(f"Pulling data for {date} (This may take a minute...)")

    response = requests.get(f"http://{TEST_FLASK_HOST}:{TEST_FLASK_PORT}/adddata/", params=parameters)
    print(response.text)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        try:
            dt.datetime.strptime(sys.argv[1], "%Y-%m-%d")
        except ValueError:
            print("Invalid date. Required format is YYYY-MM-DD")
        else:
            trigger_add_data(sys.argv[1])
    else:
        print("Usage: python3 ./test_add_data.py YYYY-MM-DD")