import pandas as pd


# read the countries data 
country_info = pd.read_csv('raw_data/raw_countries_info.tsv', sep='\t')

# cleaning countries
new_cols = {'Codes':'country_code','Name':'country_name','Organizations':'organizations'}
country_info.rename(columns=new_cols, inplace=True)
country_info['organizations'].fillna("Coming Soon", inplace=True)

if country_info['country_name'].str.contains('Namibia').any() == True:
    # Replace for Namibia country code
    country_info['country_code'].fillna("NA", inplace=True)
else:
    # don't do anything
    pass

# read the countries holiday data
country_holiday = pd.read_csv('raw_data/raw_countries_holiday.csv')

# Merge the two datasets together
country_data = pd.merge(country_holiday, country_info, how='left', on='country_code')

#country_data = pd.merge(country_info, country_holiday, how='right', on='country_code')

# Basic transformation on final dataset
country_data.to_csv('cleaned_data/country_holidays.csv', index=None)


