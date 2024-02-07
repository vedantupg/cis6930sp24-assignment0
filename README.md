# cis6930sp24-assignment0

Name: VEDANT UPGANLAWAR

## Project Description
Creating a Python application to extract incident data from PDF files released by the Norman, Oklahoma police department is the task at hand. The programme gathers important data, including date/time, incident number, location, type, and incident ORI, from incident summaries downloaded from a given URL. It then stores the information in a SQLite database. It also has the ability to print an overview of the different incident kinds and their corresponding counts. The project intends to demonstrate proficiency in database management, command-line parameter parsing, and data extraction. Following best practices, the code is arranged in a Python package and comes with extensive documentation in the README file.

# How to Install:
1. Clone the repository on your system:
    ```sh
    $ git clone https://github.com/vedantupg/cis6930sp24-assignment0.git
    $ cd cis6930sp24-assignment0
    ```

# How to run
1. To run the program, use the following command:
    ```sh
    $ pipenv run python assignment0/main.py --incidents <url>
    ```
    

## Functions

## main.py \

has_lowercase(text) - This is a helper function which is used to prcess the string seperation of the columns 'Location' and 'Nature'

extractincidents() - This functions has the url parameter which it further processes to get the response of the url and extract the incidents which can further be received in the format of dataframes which we further insert into the database row-wise

## Database Development

**create_db()** - Creates the sqlite3 database for the given schema

**populate_db(row)** - This function is responsible for inserting the data into the table where it gets the data from the "row" argument

**fetch_db()** - This function shoots the query "SELECT \* FROM table_name" to get all the rows of the table

**delete_data()** - This function deletes all the data from the table keeping the table schema untouched

**group_by()** - This function returns the result of the "group by" query

## Bugs and Assumptions

Bug1 : The code inserts a row even if one of the column has a non-Null value
