import pandas as pd


# defines a function for reformating world bank data
def reformatDF(DF, *, feature_name='', round_to=2):
    ''' a function to reformat world bank data '''

    # removes unnecessary columns
    DF.drop(columns=['Indicator Name', 'Indicator Code', 'Unnamed: 63'],
            inplace=True)

    # only keeps columns for years between 1960 and 2016
    DF.drop(columns=list(DF.loc[:, '1960':'1989'].columns), inplace=True)
    DF = DF.drop(columns=['2017', '2018'])

    # rounds numerical values to given number of decimals
    DF = DF.round(decimals=round_to)

    # reformats DF to have one year feature instead of a feature for each year
    newDF = pd.DataFrame()
    for year in range(1990, 2017):
        tempDF = DF[['Country Name', 'Country Code', f'{year}']]
        tempDF = tempDF.rename(columns={f'{year}': feature_name})
        tempDF['Year'] = year
        tempDF = tempDF[['Country Name', 'Country Code',
                         'Year', feature_name]]
        newDF = pd.concat([newDF, tempDF])

    return(newDF)


def mergeDFs(list_of_dfs):
    '''
    a function to merge a list of dfs all formated with the reformatDF function
    '''

    # removes first df from list and uses it as start of the mergedDF
    mergedDF = list_of_dfs.pop(0)

    # merges the rest of the dataframes with the first one
    for DF in list_of_dfs:
        mergedDF = mergedDF.merge(DF,
                                  on=['Country Code', 'Year', 'Country Name'])

    return(mergedDF)


# importing dataframes
DF1 = pd.read_csv('forest_percent.csv', skiprows=3)
DF2 = pd.read_csv('forest_area.csv', skiprows=3)
DF3 = pd.read_csv('agriculture_percent.csv', skiprows=3)
DF4 = pd.read_csv('population.csv', skiprows=3)
DF5 = pd.read_csv('gdp.csv', skiprows=3)

# reformats dataframes
newDF1 = reformatDF(DF1, feature_name='Forest Land Percent')
newDF2 = reformatDF(DF2, feature_name='Forest Area (sq km)', round_to=0)
newDF3 = reformatDF(DF3, feature_name='Agriculture Land Percentage')
newDF4 = reformatDF(DF4, feature_name='Population', round_to=0)
newDF5 = reformatDF(DF5, feature_name='GDP Per Capita (2019 USD)', round_to=0)

# creates list of dataframes
DFlist = [newDF1, newDF2, newDF3, newDF4, newDF5]

# merges the dataframes for past data
df0 = mergeDFs(DFlist)

# imports prediction data
predDF = pd.read_csv('forest_predictions.csv', index_col=0)


# creates a dictionary for country codes/names
oneYear = df0[df0['Year'] == 1990]
countries = oneYear[['Country Code', 'Country Name']]
codeList = list(countries['Country Code'])
nameList = list(countries['Country Name'])
countryDict = dict(zip(codeList, nameList))

# creates list of countries
countryList = list(predDF.columns)[1:]

# reformats prediction dataframe to apend to other dataframe
newPredDF = pd.DataFrame()
for country in countryList:
    tempDF = predDF[['Year', f'{country}']]
    tempDF = tempDF.rename(columns={f'{country}': 'Forest Land Percent'})
    tempDF['Country Code'] = f'{country}'
    tempDF['Country Name'] = countryDict[f'{country}']
    tempDF['Forest Land Percent']
    newPredDF = pd.concat([newPredDF, tempDF])
newPredDF['Forest Land Percent'] = newPredDF['Forest Land Percent'].astype('float')  # noqa
newPredDF.sort_values(by='Year', inplace=True)

# sets prediction dataframe
predictionDF = newPredDF.copy()

# adds prediction data to past data
df = pd.concat([df0, newPredDF], sort=False).reset_index(drop=True)

# fills null vlaues
df = df.fillna('NODATA')

df.to_csv('dataframe.csv', index=0)
