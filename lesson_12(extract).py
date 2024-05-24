import pandas as pd
import requests as re
#import json as js
import numpy as np
import configparser as cf


#pip install configparser


# read the countries data so we can dynamically choose our country codes
dynamic_country = pd.read_csv('raw_data/raw_countries_info.tsv', sep='\t')

# Rename the column names
new_cols = {'Codes':'country_code','Name':'country_name','Organizations':'organizations'}
dynamic_country.rename(columns=new_cols, inplace=True)

# convert the numpy array to a list  
country_code = list(dynamic_country['country_code'].values)


# List to store extracted values
extracted_data = []
# set the value for the year being pulled
last_year = 2023

# configure api credential
parser = cf.ConfigParser()
parser.read('cred.conf')
key = parser.get('api_key','key')

for code in country_code:
    
    parameters = {
                    'key': key,
                    'year': last_year,
                    'country': code
                    }

    url = f'https://holidayapi.com/v1/holidays?pretty&'
    data = re.get(url, params=parameters)


    if data.status_code == 200:
        # save the raw data for backup
        #with open(code+'.json', 'w') as c_hol:
         #   js.dump(data.json(), c_hol)
        
        data_pulled = data.json()
        # Extract information and store in the list
        for holiday in data_pulled["holidays"]:

            holiday_info = {
                "holiday_name": holiday["name"],
                "occured_date": holiday["date"],
                "observed_date": holiday["observed"],
                "is_public": holiday["public"],
                "country_code": holiday["country"],
                "occured_weekday": holiday["weekday"]["date"]["name"],
                "observed_weekday": holiday["weekday"]["observed"]["name"],
                "year": last_year
            }
            extracted_data.append(holiday_info)

    else:
        print(data.status_code)


# Convert list of dictionaries to a pandas DataFrame
df = pd.DataFrame(extracted_data)

# Print the DataFrame
print(df.head())
print(df.shape)

df.to_csv('raw_data/raw_countries_holiday.csv', index=None)