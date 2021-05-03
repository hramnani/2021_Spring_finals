import pandas as pd
import plotly.express as px
pd.options.plotting.backend = "plotly"
import plotly.graph_objs as go
import glob as glob


def cleancensus(file):
    """

    :param file:
    :return:
    """
    cleaned = pd.read_csv(file)
    year_cols = []
    for col in cleaned.columns:
        if col.startswith('20'):
            year_cols.append(col)

    cleaned = cleaned.groupby('Geographic Area').sum()[year_cols]
    cleaned['State'] = cleaned.index
    cleaned2 = cleaned.reset_index().melt(id_vars=['State'])
    census = cleaned2[cleaned2['variable'] != 'Geographic Area'].copy()
    census['Year'] = census['variable']
    census.drop('variable', 1, inplace=True)
    census.columns = ['State', 'Population', 'Year']
    census['Population'] = census['Population'].str.replace(',', '').astype(str).astype(int)
    census['Year'] = census['Year'].astype(str).astype(int)
    return census


def cleanhatecrime(datafile):
    read = pd.read_csv(datafile)
    table = read.groupby(['STATE_NAME', 'DATA_YEAR']).sum()[['VICTIM_COUNT']]
    table.reset_index(inplace=True)

    return table

def combine(dataframe1, dataframe2):
    joined = dataframe1.merge(dataframe2, how='left', left_on= ['State', 'Year'], right_on= ['STATE_NAME', 'DATA_YEAR'])
    joined.drop(['STATE_NAME', 'DATA_YEAR'], 1, inplace=True)
    return joined

def all_years(df1, df2):
    decade1 = df1[df1['VICTIM_COUNT'].notna()]
    decade2 = df2[df2['VICTIM_COUNT'].notna()]
    decade1 = decade1.groupby('Year')[['Population', 'VICTIM_COUNT']].sum()
    decade2 = decade2.groupby('Year')[['Population', 'VICTIM_COUNT']].sum()
    decade1['Victims per mil'] = (decade1['VICTIM_COUNT'] / decade1['Population']) * 1000000
    decade2['Victims per mil'] = (decade2['VICTIM_COUNT'] / decade2['Population']) * 1000000
    all_years_table = decade1.groupby('Year')['Victims per mil'].sum().append(decade2.groupby('Year')['Victims per mil'].sum())
    return all_years_table

if __name__ == '__main__':
    file1 = './pop_2000-2009.csv'
    file2 = './pop_2010-2019.csv'
    datafile = './hate_crime.csv'
    #decade1 = cleancensus(file1)
    #decade2 = cleancensus(file2)
    #hate_crime = cleanhatecrime(datafile)
    #print(hate_crime)
    dataframe1 = cleancensus(file1)
    dataframe2 = cleanhatecrime(datafile)
    dataframe3 = cleancensus(file2)
    decade1 = combine(dataframe1, dataframe2)
    decade2 = combine(dataframe3, dataframe2)
    all_years_df = all_years(decade1, decade2)
    print(all_years_df)

