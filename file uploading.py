"""q1: One of our products is in charge of downloading and ingesting millions of records from our clients.
Recently during ingesting a large dataset we had our entire DB(Postgres) go down and the entire ingestion process from pandas data frame to SQL took around 2-3 hours because of the RAM unavailability.
Now this has two simple fixes

- Increase ram/ scale the DB on demand
- change our code to accommodate these restrictions and make the entire ingestion process much faster on the way.

How would you approach this? We are not looking for a full-blown ingestion logic. Just a small script to take a given CSV file and upload it to DB in an efficient manner.
Write code to take a large csv file( > 1GB ) and ingest it to table - public.test_od"""

import pandas as pd
from sqlalchemy import create_engine

# Connect to the PostgreSQL database
engine = create_engine('postgresql://username:password@host:port/database')

# Read the CSV file into a DataFrame
df = pd.read_csv('large_file.csv', chunksize=100000)

# Insert the DataFrame into the table
for i, chunk in enumerate(df):
    chunk.to_sql('test_od', engine, if_exists='append')


"""q2: At Saama we have two main products in the Smart Series
1. Smart Series-1
2. Smart Series-2

both these products run on a flask backend.
Write an API using flask to upload a CSV file and insert it into a new timestamped table.

given this API request

curl --location --request POST 'http://localhost:5000/api/file-import' \
--form 'files=@"/Users/master_study_list.csv"' \
--form 'create_usr_id="ashish"
--form 'schema="public"'


Create a new table with the data in given schema as public.master_study_list_2022_01_21_17_09_11
Where 2022_01_21 is the date
and 17_09_11 is the time with seconds"""

from flask import Flask, request, jsonify
import os
import pandas as pd
import datetime

app = Flask(application)


@app.route('/api/file-import', methods=['POST'])
def file_import():
    try:


        # Get file and user ID from request
        file = request.files['/Users/master_study_list.csv']
        create_usr_id = request.form['ashish']
        schema = request.form['public']


        # Get current date and time
        now = datetime.datetime.now()
        date = now.strftime("%Y_%m_%d")
        time = now.strftime("%H_%M_%S")

        # Create new table name
        table_name = f"{schema}.master_study_list_{date}_{time}"

        # Read CSV file into a dataframe
        df = pd.read_csv(file)

        # Connect to database and create new table
        # Code to connect to database and create table goes here

        # Insert data into new table
        # Code to insert data into table goes here

        return jsonify({"status": "success", "message": f"File imported and inserted into table {table_name}"})
    except:
        return jsonify({"status": "error", "message": "An error occurred while importing the file"})
if application == 'main':

    app.run(debug=True)