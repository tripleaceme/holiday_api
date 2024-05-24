import pandas as pd
import pymysql as py
import configparser as cf
import matplotlib.pyplot as plt
import seaborn as sns
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


# Fetch the data
#query = "SELECT *  FROM events"
#df = pd.read_sql(query, conn)

# Close the connection
#conn.close()
#print(df.head())

### 1.  Number of holidays per month
query = """     select month, holiday_count from (
                Select monthname(occured_date) as month ,month(occured_date) month_number ,count(*) as holiday_count 
                 FROM events 
                group by month , month_number
                order by month_number) all_month;
        """

df_month = pd.read_sql(query,conn)
print(df_month)

plt.figure(figsize=(10,6))
sns.barplot(x='month',y='holiday_count',data=df_month,palette='viridis')
plt.title("Number fo holidays per Month")
plt.xlabel('Month')
plt.ylabel('Number of Holidays')
plt.xticks(range(12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.show()


### 2. Public vs. Non-public Holidays

query = "SELECT is_public, COUNT(*) AS count FROM events GROUP BY is_public;"
df_public = pd.read_sql(query, conn)

# Plot
plt.figure(figsize=(6, 4))
sns.barplot(x='is_public', y='count', data=df_public, palette='viridis')
plt.title('Public vs. Non-public Holidays')
plt.xlabel('Is Public Holiday')
plt.ylabel('Number of Holidays')
plt.xticks([0, 1], ['Non-public', 'Public'])
plt.show()


### 3. Number of Holidays per Weekday

query = "SELECT DAYNAME(occured_date) AS weekday, COUNT(*) AS count FROM events GROUP BY weekday ORDER BY FIELD(weekday, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');"
df_weekday = pd.read_sql(query, conn)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(x='weekday', y='count', data=df_weekday, palette='viridis')
plt.title('Number of Holidays per Weekday')
plt.xlabel('Weekday')
plt.ylabel('Number of Holidays')
plt.show()


### 4. Number of Holidays by Holiday Name

query = "SELECT holiday_name, COUNT(*) AS count FROM events GROUP BY holiday_name ORDER BY count DESC;"
df_holiday_name = pd.read_sql(query, conn)

# Plot
plt.figure(figsize=(12, 8))
sns.barplot(x='count', y='holiday_name', data=df_holiday_name, palette='viridis')
plt.title('Number of Holidays by Holiday Name')
plt.xlabel('Number of Holidays')
plt.ylabel('Holiday Name')
plt.show()


### 5. Number of Holidays by Year

query = "SELECT year, COUNT(*) AS count FROM events GROUP BY year ORDER BY year;"
df_year = pd.read_sql(query, conn)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(x='year', y='count', data=df_year, palette='viridis')
plt.title('Number of Holidays by Year')
plt.xlabel('Year')
plt.ylabel('Number of Holidays')
plt.show()


### 6. Number of Holidays by Month and Year

query = "SELECT YEAR(occured_date) AS year, MONTH(occured_date) AS month, COUNT(*) AS count FROM events GROUP BY year, month ORDER BY year, month;"
df_month_year = pd.read_sql(query, conn)

# Pivot table for heatmap
df_pivot = df_month_year.pivot("month", "year", "count")

# Plot
plt.figure(figsize=(12, 8))
sns.heatmap(df_pivot, cmap="viridis", annot=True, fmt="d")
plt.title('Number of Holidays by Month and Year')
plt.xlabel('Year')
plt.ylabel('Month')
plt.show()


### 7. Average Number of Holidays per Month

query = """
SELECT MONTH(occured_date) AS month, AVG(count) AS avg_count
FROM (
    SELECT occured_date, COUNT(*) AS count
    FROM events
    GROUP BY occured_date
) AS daily_holidays
GROUP BY month
ORDER BY month;
"""
df_avg_month = pd.read_sql(query, conn)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(x='month', y='avg_count', data=df_avg_month, palette='viridis')
plt.title('Average Number of Holidays per Month')
plt.xlabel('Month')
plt.ylabel('Average Number of Holidays')
plt.xticks(range(12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.show()


### 8. Holidays with United Nations Participation

query = "SELECT holiday_name, COUNT(*) AS count FROM events WHERE FIND_IN_SET('United Nations', organizations) > 0 GROUP BY holiday_name ORDER BY count DESC;"
df_un = pd.read_sql(query, conn)

# Plot
plt.figure(figsize=(12, 8))
sns.barplot(x='count', y='holiday_name', data=df_un, palette='viridis')
plt.title('Holidays with United Nations Participation')
plt.xlabel('Number of Holidays')
plt.ylabel('Holiday Name')
plt.show()


### 9. Holidays in the First Half vs. Second Half of the Year

query = "SELECT CASE WHEN MONTH(occured_date) <= 6 THEN 'First Half' ELSE 'Second Half' END AS half_year, COUNT(*) AS count FROM events GROUP BY half_year;"
df_half_year = pd.read_sql(query, conn)

# Plot
plt.figure(figsize=(8, 6))
sns.barplot(x='half_year', y='count', data=df_half_year, palette='viridis')
plt.title('Holidays in the First Half vs. Second Half of the Year')
plt.xlabel('Half of the Year')
plt.ylabel('Number of Holidays')
plt.show()


### 10. Number of Holidays per Organization


query = "SELECT organizations, COUNT(*) AS count FROM events GROUP BY organizations ORDER BY count DESC;"
df_organization = pd.read_sql(query, conn)

# Plot
plt.figure(figsize=(12, 8))
sns.barplot(x='count', y='organizations', data=df_organization, palette='viridis')
plt.title('Number of Holidays per Organization')
plt.xlabel('Number of Holidays')
plt.ylabel('Organization')
plt.show()


### 11. Holidays by Type (Public vs. Non-public) Over the Year

query = "SELECT MONTH(occured_date) AS month, is_public, COUNT(*) AS count FROM events GROUP BY month, is_public ORDER BY month, is_public;"
df_public_month = pd.read_sql(query, conn)

# Plot
plt.figure(figsize=(12, 8))
sns.catplot(x='month', y='count', hue='is_public', kind='bar', data=df_public_month, palette='viridis', height=6, aspect=2)
plt.title('Holidays by Type (Public vs. Non-public) Over the Year')
plt.xlabel('Month')
plt.ylabel('Number of Holidays')
plt.xticks(range(12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.show()


### 12. Distribution of Public Holidays by Weekday

query = "SELECT DAYNAME(occured_date) AS weekday, COUNT(*) AS count FROM events WHERE is_public = TRUE GROUP BY weekday ORDER BY FIELD(weekday, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');"
df_public_weekday = pd.read_sql(query, conn)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(x='weekday', y='count', data=df_public_weekday, palette='viridis')
plt.title('Distribution of Public Holidays by Weekday')
plt.xlabel('Weekday')
plt.ylabel('Number of Holidays')
plt.show()


### 13. Number of Holidays in Each Quarter


query = "SELECT CASE WHEN MONTH(occured_date) BETWEEN 1 AND 3 THEN 'Q1' WHEN MONTH(occured_date) BETWEEN 4 AND 6 THEN 'Q2' WHEN MONTH(occured_date) BETWEEN 7 AND 9 THEN 'Q3' ELSE 'Q4' END AS quarter, COUNT(*) AS count FROM events GROUP BY quarter;"
df_quarter = pd.read_sql(query, conn)

# Plot
plt.figure(figsize=(8, 6))
sns.barplot(x='quarter', y='count', data=df_quarter, palette='viridis')
plt.title('Number of Holidays in Each Quarter')
plt.xlabel('Quarter')
plt.ylabel('Number of Holidays')
plt.show()


### 14. Trend of Holidays Over the Years

query = "SELECT year, COUNT(*) AS count FROM events GROUP BY year ORDER BY year;"
df_trend = pd.read_sql(query, conn)

# Plot
plt.figure(figsize=(10, 6))
sns.lineplot(x='year', y='count', data=df_trend, marker='o', palette='viridis')
plt.title('Trend of Holidays Over the Years')
plt.xlabel('Year')
plt.ylabel('Number of Holidays')
plt.show()


### 15. Most Common Month for Public Holidays

query = "SELECT MONTH(occured_date) AS month, COUNT(*) AS count FROM events WHERE is_public = TRUE GROUP BY month ORDER BY count DESC LIMIT 1;"
df_common_public_month = pd.read_sql(query, conn)

# Plot
plt.figure(figsize=(8, 6))
sns.barplot(x='month', y='count', data=df_common_public_month, palette='viridis')
plt.title('Most Common Month for Public Holidays')
plt.xlabel('Month')
plt.ylabel('Number of Public Holidays')
plt.xticks([0], ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.show()