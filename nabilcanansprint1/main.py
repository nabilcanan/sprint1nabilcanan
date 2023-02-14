# Nabil Canan
import json
import sys
import requests
import sqlite3
from secrets import wufoo_key
from requests.auth import HTTPBasicAuth


def get_wufoo_data() -> dict:  # comment to test workflow
    url = "https://nabilcanan.wufoo.com/api/v3/forms/m16i9gqh089msfx/entries/json"
    response = requests.get(url, auth=HTTPBasicAuth(wufoo_key, 'pass'))

    if response.status_code != 200:
        print(f"Failed to get data, response code:{response.status_code} and error message: {response.reason} ")
        sys.exit(-1)

    jsonresponse = response.json()
    return jsonresponse['Entries']


def write_wufoo_data():
    try:
        db_connection = sqlite3.connect('wufoo_data.db')
        db_cursor = db_connection.cursor()

        db_cursor.execute('''CREATE TABLE IF NOT EXISTS entries (Entry_Id text, First_Name text, 
        Last_Name text, Attendance text, Num_Guest text,
         Meat_eater text , vegan_or text, gluten_free text, 
         dairy_free text, nothing_here text, other_info text, 
         restrictions text, untitles_here text,  
         Date_Created text, Created_By text, Date_Updated text, Updated_By text)''')

    except sqlite3.Error as db_error:
        print(f'A Database Error has occurred: {db_error}')

    finally:
        if db_connection:
            db_connection.close()
            print('Database connection closed.')
    insert_database()


def insert_database():
    data = get_wufoo_data()
    try:
        db_connection = sqlite3.connect('wufoo_data.db')
        db_cursor = db_connection.cursor()

        db_cursor.execute('DELETE FROM entries')

        for item in data:
            db_cursor.execute("INSERT INTO entries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                              (item['EntryId'],
                               # first name
                               item.get('Field1', ''),
                               # last name
                               item.get('Field2', ''),
                               # attendance
                               item.get('Field3', ''),
                               # num_guest
                               item.get('Field4', ''),
                               # vegetarian
                               item.get('Field5', ''),
                               # vegan
                               item.get('Field6', ''),
                               # gluten free
                               item.get('Field7', ''),
                               # dairy free
                               item.get('Field8', ''),
                               # no restrictions
                               item.get('Field9', ''),
                               # other restriction
                               item.get('Field10', ''),
                               # user input
                               item.get('Field105', ''),
                               # untitled
                               item.get('Field107', ''),
                               item.get('DateCreated'),
                               item.get('CreatedBy'),
                               item.get('DateUpdated'),
                               item.get('UpdatedBy')))

        db_connection.commit()

    except sqlite3.Error as db_error:
        print(f'A Database Error has occurred: {db_error}')

    finally:
        if db_connection:
            db_connection.close()
    print('Database connection closed.')


if __name__ == "__main__":
    write_wufoo_data()
