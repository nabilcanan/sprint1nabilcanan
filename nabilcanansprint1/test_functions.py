import json
from urllib import response

import pytest
from _pytest import monkeypatch
import requests


def test_entries():
    url = 'https://nabilcanan.wufoo.com/api/v3/forms/zhc4c2c17puvvi/entries/json'
    response = requests.get(url)
    assert response.status_code == 200, f"Failed to retrieve data. Response status code: {response.status_code}"
    data = response.json()
    entries = data['Entries']
    for entry in entries:
        for key, value in entry.items():
            assert value != '', f"Error: The field {key} is empty"

def test_retrieve_data(self):
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.text)
    self.assertGreater(len(data["Entries"]), 10)