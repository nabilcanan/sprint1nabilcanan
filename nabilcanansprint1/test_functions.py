import pytest
from _pytest import monkeypatch
import requests


def test_get_requests():
    url = "https://nabilcanan.wufoo.com/api/v3/forms/zhc4c2c17puvvi/entries/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("Data has been received", data)
        return True
    else:
        print("Failed to get data", response.status_code)
        return False


