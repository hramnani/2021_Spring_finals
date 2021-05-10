# 2021_Spring_finals

#### Team members: 
Hina Ramnani (ramnani2)
Shraddha Tiwari (tiwari5)   

## Story of Hate Crimes- A Decade-wise analysis of hate crimes in the US

The purpose of our project is to look at how Hate Crimes in the USA have an association with various factors.
We came up with topic as the social issue about Hate Crimes is more relevant now, than ever, and the Hypotheses here help us understand how Hate Crimes have changed over the two decades.

We came up with 2 Major Hypothesis, and upon discussion with our Professor, we decided to include a 3rd and a 4th Hypothesis as well to better capture the data.

### Hypothesis 1:
The comparison of hate crime victims' count over a time-series of the past 2 decades:
The rate of hate crimes was higher between 2000-2010 vs between 2010-2019
![2021-03-17-hate-crime-la](https://user-images.githubusercontent.com/77983281/116895024-5c143780-abf8-11eb-826d-e907408220e3.jpeg)

### Conclusion for Hypothesis 1:
From the below graph, we can see that we fail to reject our Hypothesis 1. There is infact a dip in the crime rates in the decade of 2010-2019
![H1](https://user-images.githubusercontent.com/77983353/117689927-e1ab6080-b17f-11eb-9dc3-45ef4e1aaa41.png)



### Hypothesis 2:
There is a correlation between States with different race population and hate crimes victims, the races being- White, Black, Hispanic, Asian, American Indian/Alaska Native, Native Hawaiian/Other Pacific Islander as well as Multiple Races
![resized-iStock-1158476263](https://user-images.githubusercontent.com/77983281/116894833-22dbc780-abf8-11eb-9041-fdb7a5fd6d8a.jpg)

### Conclusion for Hypothesis 2:
From the below graph as an example of one of the Races that we analyze here, we can see that we fail to reject our Hypothesis 2.
![H2](https://user-images.githubusercontent.com/77983353/117689966-eb34c880-b17f-11eb-831e-24d060e84a9b.png)






### Hypothesis 3:
Testing association between unemployment rate and hate crime based on the correaltion value.
![Unemployment](https://user-images.githubusercontent.com/77983281/116894968-4868d100-abf8-11eb-98fc-ba856b2c8100.jpg)

### Conclusion for Hypothesis 3:
As we can see from the below graph as one example of a State, there is no strong pattern that can be deduced here for determining whether there is an association between Unemployment Rate and Victim Counts. Hence, here we Reject our Hypothesis.
![H3](https://user-images.githubusercontent.com/77983353/117689987-f25bd680-b17f-11eb-9d22-2cbbc2b57440.png)




### Hypothesis 4:
Since 1991, Anti-white hate crimes have increased, while crimes against other races (Black, Asian, Multiple) have decreased.
![Bias](https://user-images.githubusercontent.com/77983353/117680118-7e690080-b176-11eb-9331-eec8ad8a258a.jpg)


### Conclusion for Hypothesis 4:
As we can see from the Stacked Bar Plot, the hate crimes towards races mostly remain unchanged. Hence, we Reject our Hypothesis.
![H4](https://user-images.githubusercontent.com/77983353/117690007-f7b92100-b17f-11eb-8147-16eda28c2c64.png)



### Conclusion:
From all our above Hypothesis, we aim to understand how Hate Crimes have changed over the decades, and whether the Racial Population plays a part in the Victim Count of Hate Crimes being committed over the years, along with an Unemployment and a Bias factor that is analysed against the Data.



### Contributions:
Hina Ramnani (ramnani2):
- Completed Doctests, Docstrings, Plots and functions for Hypothesis 1 and 3

Shraddha Tiwari (tiwari5):
- Completed Doctests, Docstrings, Plots and functions for Hypothesis 2 and 4



### Data Sources:
#### Census data 2010-2019 https://www.census.gov/data/tables/time-series/demo/popest/2010s-state-total.html
#### Census data 2000-2009 https://www.census.gov/data/tables/time-series/demo/popest/intercensal-2000-2010-state.html
#### Hate crime data https://crime-data-explorer.fr.cloud.gov/pages/downloads
#### Unemployment data https://www.icip.iastate.edu/tables/employment/unemployment-states
#### Race data https://www.kff.org/other/state-indicator/distribution-by-raceethnicity/?dataView=1&currentTimeframe=9&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D


### Other helpful links used:
#### #https://stackoverflow.com/questions/28988627/pandas-correlation-groupbyfor_
#### #https://thispointer.com/python-pandas-select-rows-in-dataframe-by-conditions-on-multiple-columns/


#### The following is an excerpt from the Readme provided along with the hate_crime data from the FBI:
"The Hate Crime Statistics Program of the FBIís Uniform Crime Reporting (UCR) Program collects data regarding criminal offenses that were motivated, in whole or in part, by the offenderís bias against a race, gender, gender identity, religion, disability, sexual orientation, or ethnicity, and were committed against persons, property, or society. Because motivation is subjective, it is sometimes difficult to know with certainty whether a crime resulted from the offenderís bias. Moreover, the presence of bias alone does not necessarily mean that a crime can be considered a hate crime. Only when a law enforcement investigation reveals sufficient evidence to lead a reasonable and prudent person to conclude that the offenderís actions were motivated, in whole or in part, by his or her bias, should an agency report an incident as a hate crime. 
Addition of Animal Cruelty, Fraud Offenses, and a Cyberspace Location to NIBRS 

The UCR Program began permitting law enforcement agencies that contribute their data via NIBRS to report offenses of animal cruelty, identity theft, and hacking/computer invasion, as well as the location of cyberspace in 2016. 

Offense types 

The law enforcement agencies that voluntarily participate in the Hate Crime Statistics Program collect details about offendersí bias motivations associated with 13 offense types already being reported to the UCR Program: murder and nonnegligent manslaughter, rape (revised and legacy definitions), aggravated assault, simple assault, intimidation, human traffickingócommercial sex acts, and human traffickingóinvoluntary servitude (crimes against persons); and robbery, burglary, larceny-theft, motor vehicle theft, arson, and destruction/damage/vandalism (crimes against property). The law enforcement agencies that participate in the UCR Program via NIBRS collect data about additional offenses for crimes against persons and crimes against property. These data appear in Hate Crime Statistics in the category of other. These agencies also collect hate crime data for the category called crimes against society, which includes drug or narcotic offenses, gambling offenses, prostitution offenses, weapon law violations, and animal cruelty offenses. Together, the offense classification other and the crime category crimes against society include 39 Group A offenses that are captured in NIBRS, which also collects the previously mentioned 13 offense types. (The NIBRS User Manual provides an explanation of the 52 Group A offenses.)

Beginning in 2015, all law enforcement agencies could report human trafficking offenses. However, no human trafficking offenses with a bias motivation were reported during 2016. 

Crimes against persons, property, or society 

The UCR Programís data collection guidelines stipulate that a hate crime may involve multiple offenses, victims, and offenders within one incident; therefore, the Hate Crime Statistics Program is incident-based. According to UCR counting guidelines:
  * One offense is counted for each victim in crimes against persons.
  * One offense is counted for each offense type in crimes against property.
  * One offense is counted for each offense type in crimes against society. "
