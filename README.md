# cis6930sp24-assignment0

Name: VEDANT UPGANLAWAR

## Project Description

## How to install

pipenv install

## How to run

pipenv run ...
![video](video)

## Functions

#### main.py \

has_lowercase(text) - This is a helper function which is used to prcess the string seperation of the columns 'Location' and 'Nature'

extractincidents() - This functions has the url parameter which it further processes to get the response of the url and extract the incidents which can further be received in the format of dataframes which we further insert into the database row-wise

## Database Development

create_db() - Creates the sqlite3 database for the given schema

populate_db(row) - This function is responsible for inserting the data into the table where it gets the data from the "row" argument

fetch_db() - This function shoots the query "SELECT \* FROM table_name" to get all the rows of the table

delete_data() - This function deletes all the data from the table keeping the table schema untouched

group_by() - This function returns the result of the "group by" query

## Bugs and Assumptions

Bug1 : The code inserts a row even if one of the column has a non Null value
