import requests
import pandas as pd
from bs4 import BeautifulSoup

# Getting the webpage
r = requests.get('https://www.worldometers.info/coronavirus/?utm_campaign=homeAdvegas1?%22%20%5Cl%20%22countries')
soup = BeautifulSoup(r.content,'html5lib')

# Getting the table out of webpage
table_list = soup.find('table',{'id':'main_table_countries_today'})

# Getting required rows based on HTML code
rows_list = table_list.find_all('tr',{'style':''})

# Getting the data from the rows
rowsdata = []
for tr in rows_list:

    td = tr.find_all('td',{'data-continent':''})
    row = [tr.text for tr in td]
    #print(row)
    rowsdata.append(row)

# Creating a Data Frame out of the rows for further cleaning our data
df = pd.DataFrame(rowsdata, columns=list(range(0,21)))

# Cleaning the data frame
df.drop(df.iloc[:,-6:],axis=1,inplace=True)
df.drop(df.iloc[:,0:2],axis=0,inplace=True)
df.drop(df.tail(1).index,axis=0,inplace=True)

# Adding column names to the data frame
df.columns = ['Index','Country','Total Cases','New Cases','Total Deaths','New Deaths','Total Recovered','New Recovered','Active Cases','Serious Critical','Total Cases/1M pop','Deaths/1M Pop','Total Tests','Tests/1M Pop','Population']

#Replacing N/A Values to empty
df['Total Recovered'] = df['Total Recovered'].str.replace('N/A','')
df['New Recovered'] = df['New Recovered'].str.replace('N/A','')
df['Active Cases'] = df['Active Cases'].str.replace('N/A','')


#print(df.head())
#print(df.tail())

# Exporting data frame to CSV
df.to_csv(r'D:\DataAnalysisProjects\Covid19Reports\Covid19Data.csv', index = False)