# Nabil Canan
import sys
import requests
import sqlite3
import pytest
from secrets import wufoo_key
from requests.auth import HTTPBasicAuth
import json


def get_wufoo_data() -> dict:  # comment to test workflow
    url = "https://nabilcanan.wufoo.com/api/v3/forms/zhc4c2c17puvvi/entries/json"
    response = requests.get(url, auth=HTTPBasicAuth(wufoo_key, 'pass'))

    if response.status_code != 200:
        print(f"Failed to get data, response code:{response.status_code} and error message: {response.reason} ")
        sys.exit(-1)

    jsonresponse = response.json()
    return jsonresponse['Entries']


def write_wufoo_data():
    conn = sqlite3.connect('wufoo_data.db')
    c = conn.cursor()

    # Creates the table making sure it is if not exists and creating the column names
    c.execute('''CREATE TABLE IF NOT EXISTS entries (Entry_ID text, Title text, First_Name text,
    Last_Name text, Org_Title text, Organization text, Email text, Org_Website text, Phone_Number text,
    Time_Period text, Permission text, Opportunities text, Date_Created text, Created_By text, Date_Updated text,
    Updated_By text)''')

    data = get_wufoo_data()

    for item in data:
        opportunities = ', '.join([item.get('Field101', ''), item.get('Field102', ''), item.get('Field103', ''),
                                   item.get('Field104', ''), item.get('Field105', ''), item.get('Field106', ''),
                                   item.get('Field107', '')])

        c.execute("INSERT INTO entries VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  (item['EntryId'],
                   item.get('Field0', ''),
                   item.get('Field1', ''),
                   item.get('Field2', ''),
                   item.get('Field8', ''),
                   item.get('Field9', ''),
                   item.get('Field5', ''),
                   item.get('Field6', ''),
                   item.get('Field7', ''),
                   ', '.join([item.get('Field12', ''),
                              item.get('Field13', ''),
                              item.get('Field14', ''),
                              item.get('Field15', ''),
                              item.get('Field16', '')]),
                   item.get('Field212', ''),
                   opportunities,
                   item.get('DateCreated', ''),
                   item.get('CreatedBy', ''),
                   item.get('DateUpdated', ''),
                   item.get('UpdatedBy', '')))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    write_wufoo_data()
