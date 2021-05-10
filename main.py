import pandas as pd
import plotly.express as px
pd.options.plotting.backend = "plotly"
import plotly.graph_objs as go
import glob as glob
import numpy as np


def hypo1_trendline_decadewise(year_df: pd.DataFrame):
    """
    This function takes in the Dataframe containing the Victims per million of the population against all years
    spanning two decades and uses Trend Line Plot to display the trend line for victim count spanning two decades.
    :param year_df: Dataframe containing the value for victim count against its year
    :return: Trend Line Plot
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=year_df[:11], x=year_df[:11].index, name='2000s'))
    fig.add_trace(go.Scatter(y=year_df[10:], x=year_df[10:].index, name='2010s'))
    fig.update_layout(title="Hate crime victim counts in the past 2 decades", xaxis_title="Year",
                      yaxis_title="Victim count")
    fig.show()


def cleancensus(file: str) -> pd.DataFrame:
    """
    The input parameter for this function is the pathname of the census file. After passing it through the function,
    the cleancensus() reads the file, converts it to a dataframe and cleans the file based on the output
    required to be used in further calculations.
    :param file: Input file path
    :return: A Dataframe of cleaned census data
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
    The input is a path string, which when passed to the function of cleanhatecrime() will read the .csv file and
    convert it to a Dataframe. Further cleaning is done on this dataframe to analyze relevant columns from the
    hate crime data.
    :param datafile: Input string pathname of csv file
    :return: A Dataframe
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
    For our first Hypothesis, we need to merge the two dataframes containing clean census data and the cleaned
    crime data. Passing these two dataframes as parameters within this function. The return Dataframe is a
    joined dataframe of these two files
    :param dataframe1: Cleaned Dataframe of census data
    :param dataframe2: Cleaned Dataframe of hate crime data
    :return: Merged Dataframe containing census and hate crime data
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
    This function takes in the two decades worth of data through dataframes as an input parameter and calculates
    Victims per million within the population. The output is a Dataframe containing the value of the calculated
    Victims, against the year it has been calculated for.
    :param df1: Dataframe containing decade wise data with victim count information
    :param df2: Dataframe containing decade wise data with victim count information
    :return: Dataframe containing victim counts per million of the population for the year it has been calculated
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
    The function will accept a list as a parameter containing the races we want to compare our Victim Counts
    of Hate Crime for against its recorded state. The output will display a Scatter Plots for each of the
    races inputted in the list.
    :param all_races: List with all races mentioned for comparison
    :return: A cascade of Scatter Plots for each race in the list
    """
    for indx, one_race in enumerate(all_races):
        race_hate = races.merge(dataframe2, right_on=['STATE_NAME', 'DATA_YEAR'], left_on=['Location', 'Timeframe'])[['Location', one_race, 'Total', 'VICTIM_COUNT']]
        race_hate_all = race_hate.groupby('Location').sum().reset_index()
        fig = race_hate_all.plot.scatter(x=one_race, y='VICTIM_COUNT', hover_name='Location')
        fig.update_layout(title="Association between Hate crime count and Race population",
                          yaxis_title="Victim count")
        fig.show()


def unemp_data(unempfile: str):
    """
    The function will accept the path of the unemployment file data stored in csv format as the input in the form
    of a string. The function will read the csv file, convert the file into a dataframe and clean the file
    to get relevant columns for further analysis of the unemployment rate in a State - Year wise unemployment rate
    format.
    :param unempfile: File path of the unemployment file data
    :return: Cleaned Dataframe containing unemployment Data State-Year wise
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
    The input parameter is a string pathname that will be accepted byt he function. Using this pathname the
    Crime Dataframe is created with the Crime - State - Victim count view for the Dataframe.
    :param hc: Hate Crime data csv file pathname
    :return: Crime Name Dataframe with Victim Counts and State analysis
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
    The input parameters are the Dataframes containing the unemployment rate against a State - Year wise view in
    the Frame1 Dataframe. The Frame2 Dataframe consists of the Offense name against the state and the Year wise
    victim counts mapped. The putput Dataframe is a merged view of Frame1 and Frame2.
    :param frame1: Dataframe with State - Year wise unemployment rate
    :param frame2: Dataframe with Offense Name against State - Year wise view with Victim Counts
    :return: Merged Dataframe
    >>> f2 = pd.DataFrame(np.array([['Illinois','2016','5.8'],['Maryland','2016','4.5'],['Florida','2016','4.8'],['Illinois','2017','4.9'],['Maryland','2017','4.3'],['Florida','2017','4.2'],['Illinois','2018','4.3'],['Maryland','2018','3.9'],['Florida','2018','3.6']]), columns=['State','Year','Unemployment Rate'])
    >>> f1 = pd.DataFrame(np.array([['Motor Vehicle Theft','Florida','2','2017'],['Robbery','Florida','4','2018'],['Robbery','Illinois','2','2017'],['Robbery','Illinois','1','2018'],['Robbery','Illinois','2','2019'],['Robbery','Maryland','1','2017'],['Robbery','Maryland','1','2018'],['Robbery','Maryland','2','2019'],['Shoplifting','Maryland','1','2017'],['Theft From Building','Maryland','2','2017']]), columns=['OFFENSE_NAME','STATE_NAME','VICTIM_COUNT','DATA_YEAR'])
    >>> unempcrimedf= unemp_hate_crime(f1, f2)
    >>> unempcrimedf
              OFFENSE_NAME     State  Year VICTIM_COUNT Unemployment Rate
    0  Motor Vehicle Theft   Florida  2017            2               4.2
    1              Robbery   Florida  2018            4               3.6
    2              Robbery  Illinois  2017            2               4.9
    3              Robbery  Illinois  2018            1               4.3
    4              Robbery  Maryland  2017            1               4.3
    5          Shoplifting  Maryland  2017            1               4.3
    6  Theft From Building  Maryland  2017            2               4.3
    7              Robbery  Maryland  2018            1               3.9

    """
    group_crime_unemp = frame1.merge(frame2, left_on=['STATE_NAME', 'DATA_YEAR'], right_on=['State', 'Year'])
    group_crime_unemp = group_crime_unemp[['OFFENSE_NAME', 'State', 'Year', 'VICTIM_COUNT', 'Unemployment Rate']]
    return group_crime_unemp



def plot_unemp_hatecrime(offense_name: str, state: str):
    """
    The input parameters are the Offense Name and the State against which we need to see the unemployment data
    along with its victim count rate. The output Scatter Plot displays the relevant results.
    :param offense_name: String of the Offense Name
    :param state: String of the State to be analysed
    :return: Scatter Plot for the Offense Name and State
    """
    unemp_hate_crime_state= unemp_crime_df.loc[(unemp_crime_df['OFFENSE_NAME'] == offense_name) & (unemp_crime_df['State'] == state)]
    scatter = unemp_hate_crime_state.plot.scatter(x='Unemployment Rate', y='VICTIM_COUNT', hover_name='Year')
    scatter.show()



# skipping for now do last##################################################################################
def unemp_hate_crime_corr(unemp_crime_df: pd.DataFrame):
    """
    This function accepts the input parameter as a Dataframe containing offense and their details like State,
    Year, Victim Count, Unemployment Rate. Using this information, the function filters out only those rows with
    Aggravated Assault as the Offense Name to be analysed against rest of the columns. The output is a Dataframe
    with correlation numbers for each of the States.
    :param unemp_crime_df: Dataframe containing crime and unemployment data
    :return: Grouped Dataframe showing correlation numbers for States against Hate Crime and Unemployment Rate
    #>>> unempcrimedf = pd.DataFrame(np.array([['Motor Vehicle Theft','Florida','2017','2','4.2'],['Aggravated Assault','Florida','2018','4','3.6'],['Aggravated Assault','Illinois','2017','2','4.9'],['Aggravated Assault','Illinois','2018','1','4.3'],['Robbery','Maryland','2017','1','4.3'],['Shoplifting','Maryland','2017','1','4.3'],['Theft From Building','Maryland','2017','2','4.3'],['Robbery','Maryland','2018','1','3.9']]), columns=['OFFENSE_NAME','State','Year','VICTIM_COUNT','Unemployment Rate'])
    #>>> unempcrimecorr = unemp_hate_crime_corr(unempcrimedf)
    #>>> unempcrimecorr

    """
    for_corr = unemp_crime_df.groupby(['State', 'OFFENSE_NAME', 'Year']).sum().reset_index()
    for_corr = for_corr.loc[(for_corr['OFFENSE_NAME'] == 'Aggravated Assault')]
    corr = for_corr.groupby('State')[['VICTIM_COUNT', 'Unemployment Rate']].corr().unstack().iloc[:, 1]
    return corr



def corr_plot(state_unemp_crime_corr):
    """
    The function will accept the unemployment and crime rate correlation dataframe as an input. This Dataframe is
    used to filter out relevant rows with significant correlation values and plot such rows.
    :param state_unemp_crime_corr: Dataframe containing unemployment and crime rate correlation values
    :return: Scatter Plot based on the input Dataframe
    """
    states = state_unemp_crime_corr[(state_unemp_crime_corr > 0.5) | (state_unemp_crime_corr < -0.5)]
    for_corr = unemp_crime_df.groupby(['State', 'OFFENSE_NAME', 'Year']).sum().reset_index()
    for_corr = for_corr.loc[(for_corr['OFFENSE_NAME'] == 'Aggravated Assault')]
    for state in states.index.to_list():
        fig = for_corr[for_corr['State'] == state].plot.scatter(x='Unemployment Rate', y='VICTIM_COUNT', title=state)
        fig.update_layout(yaxis_title='Victim count')
        fig.show()



def hate_crime_race_bias(hate_crime_df: pd.DataFrame):
    """
    The function will input the Hate Crime Dataframe as its input parameter. Based on this Dataframe, the function
    will perform calculations to analyze the hate crimes against specific biases mentioned in the original Dataframe.
    Using this calculation, a Stacked Bar Chart is plotted to view the Bias Offense Victim Count.
    :param hate_crime_df: The Hate Crime Dataframe
    :return: Bar Chart plotted for the Bias Offense and Victim Counts
    """
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