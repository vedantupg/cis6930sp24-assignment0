import argparse
import requests
import io
import sqlite3
from pypdf import PdfReader


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


# def populatedb(row):

#     connection = sqlite3.connect("resources/normanpd.db")
#     cursor = connection.cursor()
#     query = """INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori)
#                 VALUES (?, ?, ?, ?, ?)"""

#     words = row.split(" ")
#     if (len(words) > 3):
#         date_time = words[0]+" "+words[1]
#         incidentNo = words[2]
#         incidentORI = words[-1]

#         location_Nature = words[3:-1]
#         location = ""
#         nature = ""
#         for word in location_Nature:
#             if has_lowercase(word) or word == "MVA" or word == "COP" or word == "EMS" or word == "DDACTS" or word == "/" or word == "911":
#                 nature += word + " "
#             else:
#                 location += word + " "

#         location = location.rstrip()
#         nature = nature.rstrip()

#         cursor.execute(
#             query, (date_time, incidentNo, location, nature, incidentORI))

#     connection.commit()
#     connection.close()

def populatedb(row):

    connection = sqlite3.connect("resources/normanpd.db")
    cursor = connection.cursor()
    query = """INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori)
                VALUES (?, ?, ?, ?, ?)"""
    string = ''
    try:
        words = row.split(' ')
        final_dict = {'Date / Time': words[0] + ' ' + words[1],
                      'Incident Number': words[2],
                      'Incident ORI': words[-1],
                      'Location': '',
                      'Incident Type': ''}

        words.remove(words[0])
        words.remove(words[0])
        words.remove(words[0])
        words.remove(words[-1])

        for j in range(0, len(words)):
            if any(c.islower() for c in words[j]):
                for a in range(j, len(words)):
                    if words[a-1] == '911':
                        string += words[a-1] + ' '
                    string += words[a] + ' '
                break
            elif words[j] == 'COP':
                string += words[j] + ' '
            elif words[j] == 'EMS':
                string += words[j] + ' '
            elif words[j] == 'DDACTS':
                string += words[j] + ' '
            elif words[j] == 'MVA':
                string += words[j] + ' '

        final_dict['Incident Type'] = string.strip()
        final_dict['Location'] = ' '.join(
            words).replace(string.strip(), '').strip()

        cursor.execute(query, (final_dict['Date / Time'], final_dict['Incident Number'],
                               final_dict['Location'], final_dict['Incident Type'], final_dict['Incident ORI']))

        connection.commit()  # Commit changes
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()      # Close cursor
        connection.close()   # Close connection


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
    cursor.execute("""SELECT nature, COUNT(*) AS count
FROM incidents
GROUP BY nature
ORDER BY COUNT(*) DESC, nature ASC;                             
 """)

    for row in cursor.fetchall():
        print(*row, sep="|")

    connection.commit()
    connection.close()


def extract_incidents(url):
    response = requests.get(url)
    response.raise_for_status()

    remote_file = io.BytesIO(response.content)
    tables = PdfReader(remote_file)

    return tables  # list of dataframes


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True,
                        help="Incident summary url.")

    args = parser.parse_args()
    if args.incidents:

        create_db()
        # Iterating the tables extracted and populating the data

        tables = extract_incidents(args.incidents)
        pages = len(tables.pages)
        for i in range(0, pages):
            page = tables.pages[i]
            text = page.extract_text()
            rows = text.split("\n")
            for row in rows:
                populatedb(row)

        # fetch_db()
        # delete_data()
        groupBy()
