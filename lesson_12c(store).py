import pandas as pd
import pymysql as py
import configparser as cf

# set up your db
"""
create user 'data_engineer'@'localhost' IDENTIFIED BY 'training';

CREATE DATABASE IF NOT EXISTS countries_holiday;

USE countries_holiday;

GRANT ALL PRIVILEGES ON countries_holiday.* TO 'data_engineer'@'localhost';
			

CREATE TABLE IF NOT EXISTS events (
    holiday_name VARCHAR(255),
    occured_date DATE,
    observed_date DATE,
    is_public BOOLEAN,
    country_code CHAR(2),
    occured_weekday VARCHAR(10),
    observed_weekday VARCHAR(10),
    year INT,
    country_name VARCHAR(255),
    organizations VARCHAR(255)
    )

"""



# Load the data from the CSV file
data = pd.read_csv('cleaned_data/cleaned_country_holidays.csv')

# Connect to MySQL server
"""conn = py.connect(
    host='localhost',
    user='data_engineer',
    password='training',
    database='countries_holiday'  # Use the existing database
)"""

# configure mysql credential
parser = cf.ConfigParser()
parser.read('cred.conf')
host = parser.get('mysql_creds','host')
user = parser.get('mysql_creds','user')
password = parser.get('mysql_creds','password')
database = parser.get('mysql_creds','database')


# Connect to MySQL server
conn = py.connect(
    host=host,
    user=user,
    password=password,
    database=database 
    )

# Create a cursor object
cursor = conn.cursor()

# Initialize a counter for the number of rows inserted
rows_inserted = 0

# Insert data into the database using cursor
for index, row in data.iterrows():

    insert_cols = """INSERT INTO events (holiday_name, occured_date, observed_date, is_public, country_code, occured_weekday, observed_weekday, year,country_name, organizations) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    # Group all values together so SQL doesn't throw error -- list(row) or tuple(row)
    cursor.execute(insert_cols,list(row) )
    rows_inserted += 1

# Commit changes
conn.commit()

# Print the total number of rows inserted
print("Total number of rows inserted:", rows_inserted)

# Close connection
conn.close()