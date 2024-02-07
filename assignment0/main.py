import argparse
import requests
import io
import tabula
import sqlite3
import pandas as pd


def has_lowercase(text):
    return any(char.islower() for char in text)


def create_db():

    connection = sqlite3.connect("resources/normanpd.db")
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE incidents (
    incident_time TEXT,
    incident_number TEXT,
    incident_location TEXT,
    nature TEXT,
    incident_ori TEXT
);""")

    connection.commit()
    connection.close()


def populatedb(row):
    row.iloc[3] = str(row.iloc[3])

    connection = sqlite3.connect("resources/normanpd.db")
    cursor = connection.cursor()
    query = """INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori)
                VALUES (?, ?, ?, ?, ?)"""

    if row.iloc[3] == "nan":
        words = row[2].split(" ")
        row.iloc[2] = ""
        row.iloc[3] = ""
        for word in words:
            if has_lowercase(word):
                row.iloc[3] = row.iloc[3] + word + " "
            else:
                row.iloc[2] = row.iloc[2] + word + " "

    row.iloc[3] = row.iloc[3].rstrip()

    if not pd.isna(row.iloc[0]):
        cursor.execute(
            query, (row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4]))
    connection.commit()
    connection.close()


def fetch_db():

    connection = sqlite3.connect("resources/normanpd.db")
    cursor = connection.cursor()
    results = cursor.execute("""SELECT * FROM incidents;
 """)

    rows = results.fetchall()

# Loop through each row and print its values
    for row in rows:
        for column in row:
            print(column, end=" | ")
        print("")

    connection.commit()
    connection.close()


def delete_data():

    connection = sqlite3.connect("resources/normanpd.db")
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM incidents;
 """)

    connection.commit()
    connection.close()


def groupBy():

    connection = sqlite3.connect("resources/normanpd.db")
    cursor = connection.cursor()
    results = cursor.execute("""SELECT nature, COUNT(*) AS count
FROM incidents
GROUP BY nature
ORDER BY nature ASC;                             
 """)

    rows = results.fetchall()

# Loop through each row and print its values
    for row in rows:
        for column in row:
            print(column, end=" | ")
        print("")

    results = cursor.execute("""SELECT COUNT(*) FROM incidents;""")
    row = results.fetchone()  # Fetch the single row
    count = row[0]           # Access the count value from the first element
    print(count)

    connection.commit()
    connection.close()


def extract_incidents(url):
    response = requests.get(url)
    response.raise_for_status()

    with io.BytesIO(response.content) as pdf_file:  # Create a file-like object

        tables = tabula.read_pdf(
            pdf_file, guess=False, pages="all", stream=True, encoding="utf-8")

        return tables  # list of dataframes


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True,
                        help="Incident summary url.")

    args = parser.parse_args()
    if args.incidents:

        # Iterating the tables extracted and populating the data
        #
        tables = extract_incidents(args.incidents)
        for table_index, table in enumerate(tables):
            for row_index, row in table.iterrows():
                populatedb(row)

        # create_db()

        # delete_data()

        fetch_db()

        groupBy()
