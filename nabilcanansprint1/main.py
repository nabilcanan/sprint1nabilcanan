# Nabil Canan
import json
import sys
import requests
import sqlite3
from secrets import wufoo_key
from requests.auth import HTTPBasicAuth


def get_wufoo_data() -> dict:  # comment to test workflow
    url = "https://nabilcanan.wufoo.com/api/v3/forms/zhc4c2c17puvvi/entries/json"
    response = requests.get(url, auth=HTTPBasicAuth(wufoo_key, 'pass'))

    if response.status_code != 200:
        print(f"Failed to get data, response code:{response.status_code} and error message: {response.reason} ")
        sys.exit(-1)

    jsonresponse = response.json()
    # print(jsonresponse['Entries'])
    return jsonresponse['Entries']


def write_wufoo_data():
    try:
        db_connection = sqlite3.connect('wufoo_data.db')
        db_cursor = db_connection.cursor()

        db_cursor.execute('''CREATE TABLE IF NOT EXISTS entries (Entry_Id text, noFirst_Name text, Last_Name text, Attendance text, Num_Guest text,
         Meat_eater text , vegan_or text, gluten_free text, dairy_free text, nothing_here text, other_info text, restrictions text,
        untitles_here text)''')

    except sqlite3.Error as db_error:
        print(f'A Database Error has occurred: {db_error}')

    finally:
        if db_connection:
            db_connection.close()
            print('Database connection closed.')


def insert_database(data):
        try:
            db_connection = sqlite3.connect('wufoo_data.db')
            db_cursor = db_connection.cursor()

            db_cursor.execute('DELETE FROM entries')

            for item in data:
                db_cursor.execute("INSERT INTO entries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                  (item['EntryId'],
                                  #first name
                                  item.get('Field1', ''),
                                  #last name
                                  item.get('Field2', ''),
                                  item.get('Field3', ''),
                                  item.get('Field4', ''),
                                   item.get('Field5', ''),
                                   item.get('Field6', ''),
                                   item.get('Field7', ''),
                                   item.get('Field8', ''),
                                   item.get('Field9', ''),
                                   item.get('Field10', ''),
                                   item.get('Field105', ''),
                                   item.get('Field107', ''),

                                )

        except sqlite3.Error as db_error:
        # print the error description
        print(f'A Database Error has occurred: {db_error}')

        finally:
            # close the database connection whether an error happened or not (if a connection exists)
            if db_connection:
                db_connection.close()
                print('Database connection closed.')


if __name__ == "__main__":
    get_wufoo_data()
