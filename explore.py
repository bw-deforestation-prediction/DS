import pandas as pd
import json
import requests

df = pd.read_csv('test.csv')


jStr = df[df['Country Name'] == 'Aruba'][['Year', 'Forest Land Percent']].to_json(  # noqa
    orient='table', index=False)

j1 = json.loads(jStr)


str(j1['data'])

jStr2 = df[df['Country Name'] == 'Aruba'][
    ['Year',
     'Forest Land Percent',
     'Agriculture Land Percentage',
     'Population',
     'GDP Per Capita (2019 USD)']].to_json(orient='table',
                                           index=False)
