import pandas as pd
import plotly.express as px
pd.options.plotting.backend = "plotly"
import plotly.graph_objs as go
import glob as glob
import numpy as np


def hypo1_trendline_decadewise(year_df: pd.DataFrame):
    """
    :param year_df:
    :return:
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=year_df[:11], x=year_df[:11].index, name='2000s'))
    fig.add_trace(go.Scatter(y=year_df[10:], x=year_df[10:].index, name='2010s'))
    fig.show()


def cleancensus(file: str) -> pd.DataFrame:
    """
    :param file:
    :return:
    >>> c_file = 'censussample.csv'
    >>> c_df = cleancensus(c_file)
    >>> c_df
           State  Population  Year
    3    Florida    20963613  2017
    4   Illinois    12778828  2017
    5   Maryland     6023868  2017
    6    Florida    21244317  2018
    7   Illinois    12723071  2018
    8   Maryland     6035802  2018
    9    Florida    21477737  2019
    10  Illinois    12671821  2019
    11  Maryland     6045680  2019
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


def cleanhatecrime(datafile: str) -> pd.DataFrame:
    """
    :param datafile:
    :return:
    >>> h_file = 'hatesample.csv'
    >>> h_df = cleanhatecrime(h_file)
    >>> h_df
      STATE_NAME  DATA_YEAR  VICTIM_COUNT
    0    Florida       2017           172
    1    Florida       2018           171
    2    Florida       2019           139
    3   Illinois       2017           104
    4   Illinois       2018           144
    5   Illinois       2019            97
    6   Maryland       2017           115
    7   Maryland       2018            62
    8   Maryland       2019            22
    """
    read = pd.read_csv(datafile)
    table = read.groupby(['STATE_NAME', 'DATA_YEAR']).sum()[['VICTIM_COUNT']]
    table.reset_index(inplace=True)

    return table

def combine(dataframe1: pd.DataFrame, dataframe2: pd.DataFrame) -> pd.DataFrame:
    """
    :param dataframe1:
    :param dataframe2:
    :return:
    >>> h_df = pd.DataFrame(np.array([['Florida','2017','172'],['Florida','2018','171'],['Florida','2019','139'],['Illinois','2017','104'],['Illinois','2018','144'],['Illinois','2019','97'],['Maryland','2017','115'],['Maryland','2018','62'],['Maryland','2019','22']]),columns=['STATE_NAME','DATA_YEAR','VICTIM_COUNT'])
    >>> c_df = pd.DataFrame(np.array([['Florida','20963613','2017'],['Illinois','12778828','2017'],['Maryland','6023868','2017'],['Florida','21244317','2018'],['Illinois','12723071','2018'],['Maryland','6035802','2018'],['Florida','21477737','2019'],['Illinois','12671821','2019'],['Maryland','6045680','2019']]), columns=['State','Population','Year'])
    >>> decade2 = combine(c_df, h_df)
    >>> decade2
          State Population  Year VICTIM_COUNT
    0   Florida   20963613  2017          172
    1  Illinois   12778828  2017          104
    2  Maryland    6023868  2017          115
    3   Florida   21244317  2018          171
    4  Illinois   12723071  2018          144
    5  Maryland    6035802  2018           62
    6   Florida   21477737  2019          139
    7  Illinois   12671821  2019           97
    8  Maryland    6045680  2019           22
    """
    joined = dataframe1.merge(dataframe2, how='left', left_on= ['State', 'Year'], right_on= ['STATE_NAME', 'DATA_YEAR'])
    joined.drop(['STATE_NAME', 'DATA_YEAR'], 1, inplace=True)
    return joined


# skipping for now do last##################################################################################
def all_years(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """
    :param df1:
    :param df2:
    :return:
    """
    decade1 = df1[df1['VICTIM_COUNT'].notna()]
    decade2 = df2[df2['VICTIM_COUNT'].notna()]
    decade1 = decade1.groupby('Year')[['Population', 'VICTIM_COUNT']].sum()
    decade2 = decade2.groupby('Year')[['Population', 'VICTIM_COUNT']].sum()
    decade1['Victims per mil'] = (decade1['VICTIM_COUNT'] / decade1['Population']) * 1000000
    decade2['Victims per mil'] = (decade2['VICTIM_COUNT'] / decade2['Population']) * 1000000
    all_years_table = decade1.groupby('Year')['Victims per mil'].sum().append(decade2.groupby('Year')['Victims per mil'].sum())
    return all_years_table


def race_hypo2(all_races: list):
    """
    :param all_races:
    :type all_races:
    :return:
    :rtype:
    """
    for indx, one_race in enumerate(all_races):
        race_hate = races.merge(dataframe2, right_on=['STATE_NAME', 'DATA_YEAR'], left_on=['Location', 'Timeframe'])[['Location', one_race, 'Total', 'VICTIM_COUNT']]
        race_hate_all = race_hate.groupby('Location').sum().reset_index()
        fig = race_hate_all.plot.scatter(x=one_race, y='VICTIM_COUNT', hover_name='Location')
        fig.show()


def unemp_data(unempfile: str):
    """
    :param unempfile:
    :type unempfile:
    :return:
    :rtype:
    >>> u_file = 'unempsample.csv'
    >>> unempdf = unemp_data(u_file)
    >>> unempdf
          State  Year  Unemployment Rate
    0  Illinois  2016                5.8
    1  Maryland  2016                4.5
    2   Florida  2016                4.8
    3  Illinois  2017                4.9
    4  Maryland  2017                4.3
    5   Florida  2017                4.2
    6  Illinois  2018                4.3
    7  Maryland  2018                3.9
    8   Florida  2018                3.6
    """
    uefile = pd.read_csv(unempfile)
    uefile.drop('Fips', 1, inplace=True)
    unemp = uefile.melt(id_vars='Area')
    unemp.columns = ['State', 'Year', 'Unemployment Rate']
    unemp['Year'] = unemp['Year'].astype('int')
    return unemp



def state_hatecrime(hc: str) -> pd.DataFrame:
    """
    :param hc:
    :type hc:
    :return:
    :rtype:
    >>> hcdf = pd.read_csv('h_sam2.csv')
    >>> datacrimesstate = state_hatecrime(hcdf)
    >>> datacrimesstate
              OFFENSE_NAME STATE_NAME  VICTIM_COUNT  DATA_YEAR
    0  Motor Vehicle Theft    Florida             2       2017
    1              Robbery    Florida             4       2018
    2              Robbery   Illinois             2       2017
    3              Robbery   Illinois             1       2018
    4              Robbery   Illinois             2       2019
    5              Robbery   Maryland             1       2017
    6              Robbery   Maryland             1       2018
    7              Robbery   Maryland             2       2019
    8          Shoplifting   Maryland             1       2017
    9  Theft From Building   Maryland             2       2017
    """
    data_crimes_state = hc.groupby([hc.OFFENSE_NAME, 'STATE_NAME', 'DATA_YEAR']).sum().reset_index()
    data_crimes_state = data_crimes_state[['OFFENSE_NAME', 'STATE_NAME', 'VICTIM_COUNT', 'DATA_YEAR']]
    return data_crimes_state




def unemp_hate_crime(frame1: pd.DataFrame, frame2: pd.DataFrame) -> pd.DataFrame:
    """
    :param frame1:
    :type frame1:
    :param frame2:
    :type frame2:
    :return:
    :rtype:
    """
    group_crime_unemp = frame1.merge(frame2, left_on=['STATE_NAME', 'DATA_YEAR'], right_on=['State', 'Year'])
    group_crime_unemp = group_crime_unemp[['OFFENSE_NAME', 'State', 'Year', 'VICTIM_COUNT', 'Unemployment Rate']]
    return group_crime_unemp



def plot_unemp_hatecrime(offense_name: str, state: str):
    """
    :param offense_name:
    :type offense_name:
    :param state:
    :type state:
    :return:
    :rtype:
    """
    unemp_hate_crime_state= unemp_crime_df.loc[(unemp_crime_df['OFFENSE_NAME'] == offense_name) & (unemp_crime_df['State'] == state)]
    scatter = unemp_hate_crime_state.plot.scatter(x='Unemployment Rate', y='VICTIM_COUNT', hover_name='Year')
    scatter.show()



def unemp_hate_crime_corr(unemp_crime_df: pd.DataFrame):
    """
    :param unemp_crime_df:
    :type unemp_crime_df:
    :return:
    :rtype:
    """
    for_corr = unemp_crime_df.groupby(['State', 'OFFENSE_NAME', 'Year']).sum().reset_index()
    for_corr = for_corr.loc[(for_corr['OFFENSE_NAME'] == 'Aggravated Assault')]
    corr = for_corr.groupby('State')[['VICTIM_COUNT', 'Unemployment Rate']].corr().unstack().iloc[:, 1]
    return corr



def corr_plot(state_unemp_crime_corr):
    """
    :param state_unemp_crime_corr:
    :type state_unemp_crime_corr:
    :return:
    :rtype:
    """
    states = state_unemp_crime_corr[(state_unemp_crime_corr > 0.5) | (state_unemp_crime_corr < -0.5)]
    for_corr = unemp_crime_df.groupby(['State', 'OFFENSE_NAME', 'Year']).sum().reset_index()
    for_corr = for_corr.loc[(for_corr['OFFENSE_NAME'] == 'Aggravated Assault')]
    for state in states.index.to_list():
        fig = for_corr[for_corr['State'] == state].plot.scatter(x='Unemployment Rate', y='VICTIM_COUNT', title=state)
        fig.show()



def hate_crime_race_bias(hate_crime_df: pd.DataFrame):
    hate_crimes_races = hate_crime_df[['DATA_YEAR', 'STATE_NAME', 'VICTIM_COUNT', 'BIAS_DESC']]
    hate_crimes_races = hate_crimes_races[hate_crimes_races['BIAS_DESC'].isin(['Anti-White', 'Anti-Black or African American', 'Anti-Asian', 'Anti-Multiple Races, Group'])]
    hate_crimes_bias_perc = hate_crimes_races.groupby('DATA_YEAR').sum()
    hate_crimes_bias_perc.columns = ['YEARLY_VICTIM_COUNT']
    hate_crimes_race_bias_group = hate_crimes_races.groupby(['DATA_YEAR', 'BIAS_DESC']).sum()
    hate_crimes_race_bias_group.index.to_list()
    hate_crimes_race_bias_group.reset_index()
    bias_perc_merge = hate_crimes_race_bias_group.reset_index().merge(hate_crimes_bias_perc, left_on='DATA_YEAR', right_on='DATA_YEAR')
    bias_perc_merge['VICTIM_COUNT_PERC'] = bias_perc_merge['VICTIM_COUNT'] / bias_perc_merge['YEARLY_VICTIM_COUNT']
    fig = px.bar(bias_perc_merge.reset_index(), x="DATA_YEAR", y="VICTIM_COUNT_PERC",
                 color='BIAS_DESC')
    fig.show()


if __name__ == '__main__':
    file1 = 'pop_2000-2009.csv'
    file2 = 'pop_2010-2019.csv'
    datafile = 'hate_crime.csv'
    #decade1 = cleancensus(file1)
    #decade2 = cleancensus(file2)
    #hate_crime = cleanhatecrime(datafile)
    #print(hate_crime)
    dataframe1 = cleancensus(file1)
    dataframe2 = cleanhatecrime(datafile)
    dataframe3 = cleancensus(file2)
    decade1 = combine(dataframe1, dataframe2)
    decade2 = combine(dataframe3, dataframe2)
    # all_years_df = all_years(decade1, decade2)
    #print(all_years_df)
    #hypo1_trendline_decadewise(all_years_df)
    temp = []
    for files in glob.glob("./csv/*.csv"):
        df = pd.read_csv(files, index_col=None, header=0)
        temp.append(df)
    races = pd.concat(temp, axis=0, ignore_index=True)
    #print(races.columns)
    #race_hypo2(['White', 'Black', 'Hispanic', 'Asian', 'American Indian/Alaska Native',
               #'Native Hawaiian/Other Pacific Islander', 'Multiple Races'])

    unempfile = 'unemp.csv'
    unemp_df = unemp_data(unempfile)
    #print(unemp_df)


    hc_df = pd.read_csv('hate_crime.csv')
    data_crimes_state = state_hatecrime(hc_df)
    #print(data_crimes_state)

    frame1 = data_crimes_state
    frame2 = unemp_df
    unemp_crime_df= unemp_hate_crime(frame1, frame2)
    #print(unemp_crime_df)

    #plot_unemp_hatecrime('Aggravated Assault', 'Illinois')
    state_unemp_crime_corr = unemp_hate_crime_corr(unemp_crime_df)
    #print(state_unemp_crime_corr)


    #print(corr_plot(state_unemp_crime_corr))

    hate_crime_df= pd.read_csv('hate_crime.csv')
    hc_race_bias_plot= hate_crime_race_bias(hate_crime_df)
    #print(hc_race_bias_plot)