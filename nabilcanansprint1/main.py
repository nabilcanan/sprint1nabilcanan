import json
import sys
import requests
from secrets import wufoo_key
from requests.auth import HTTPBasicAuth


def get_wufoo_data() -> dict:
    url = "http://{subdomain}.wufoo.com/api/v3/forms/{identifier}/entries/count.{format}"
    response = requests.get(url, auth=HTTPBasicAuth(wufoo_key, 'pass'))

    if response.status_code != 200:  # if we don't get an ok response we have trouble
        print(f"Failed to get data, response code:{response.status_code} and error message: {response.reason} ")
        sys.exit(-1)
    jsonresponse = response.json()
    return jsonresponse  # json response will be either a dictionary or a list of dictionaries


def write_wufu_data():
    data = get_wufoo_data()['Entries']

    with open("data.txt", "w") as outfile:
        # write the JSON key-value pairs to the file
        for item in data:
            for key, value in item.items():
                outfile.write(f"{key}: {value}\n")

    print_file("datafile.txt")


def print_file(file_name):
    with open(file_name) as f:
        print(f.read())


if __name__ == "__main__":
    write_wufu_data()
