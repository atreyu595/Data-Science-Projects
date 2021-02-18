# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 22:04:30 2020
@author: Atreyu Jasper Laxa Cortez
"""

"""
Data Manipulation and Wrangling project
Objective: In which Metro/Cities do Field Engineers earn the most?
"""
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_excel(r'C:\Users\Atrey\Documents\JMR_data-2020-11.xlsx')

df = pd.DataFrame(data)

print(df['Value'].describe())

#metro checking
def findNoMetro(metro):
    if 'Chicago' in metro:
        return 'Chicago'  
    elif 'Philadelphia' in metro:
        return 'Phil'
    elif 'Los Angeles' in metro:
        return 'LA'
    elif 'Seattle' in metro:
        return 'S'
    elif 'New York City' in metro:
        return 'NYC'
    elif 'National' in metro:
        return 'National'
    elif 'Washington DC' in metro:
        return 'DC'
    elif 'Boston' in metro:
        return 'Boston'
    elif 'San Francisco' in metro:
        return 'SF'
    elif 'Atlanta' in metro:
        return 'A'
    elif 'Houston' in metro:
        return 'H'
    elif 'U.S' in metro:
        return 'U.S'
    else: 
        return 'Other'

#job type

df['Dimension'] = df['Dimension'].astype(str)

#find all fields with 'Engineer' title
def findAreaOfWork(listing):
    if 'Engineer' in listing:
        return listing
    else: 
        return 'Other'

countsEngineer = df['Dimension'].apply(findAreaOfWork)

#find metro where engineers work
def findMetroEngineers(location):
    if 'Engineer' in location:
        return location 
    else:
        return 'Other'

#create column for engineers only
df['Engineers'] = countsEngineer

data = pd.DataFrame(df.loc[df['Engineers'] == 'Software Engineer'])
dataSystem = pd.DataFrame(df.loc[df['Engineers'] == 'Systems Engineer'])
dataCivil = pd.DataFrame(df.loc[df['Engineers'] == 'Civil Engineer'])
dataElec = pd.DataFrame(df.loc[df['Engineers'] == 'Electrical Engineer'])
dataMech = pd.DataFrame(df.loc[df['Engineers'] == 'Mechanical Engineer'])
dataProcess = pd.DataFrame(df.loc[df['Engineers'] == 'Process Engineer'])
dataManufacture = pd.DataFrame(df.loc[df['Engineers'] == 'Manufacturing Engineer'])
dataDesign = pd.DataFrame(df.loc[df['Engineers'] == 'Design Engineer'])
dataField = pd.DataFrame(df.loc[df['Engineers'] == 'Field Engineer'])
dataQuality = pd.DataFrame(df.loc[df['Engineers'] == 'Quality Engineer'])
dataArchitecture = pd.DataFrame(df.loc[df['Engineers'] == 'Architecture & Civil Engineering'])

frame = [data, dataCivil, dataSystem, dataMech, dataProcess, 
         dataManufacture, dataDesign, dataField, dataQuality, dataArchitecture]

#create new dataframe for engineers only
result = pd.concat(frame)

#YoY parsing

#display data type for verfication 
result['YoY'] = result['YoY'].astype(str)

minusPercentage = result['YoY'].apply(lambda x: x.replace('%',''))

#replace NAN values with zero
def replaceNAN(col):
    if 'nan' in col.lower():
        return 0
    else: 
        return col 
    
minusNAN = minusPercentage.apply(replaceNAN)

minusNAN.astype(float)

result['YoY'] = minusNAN

#salary parsing
result['Value'] = result['Value'].astype(str)

minusSalary = result['Value'].apply(lambda x: x.replace(',','')) 

minusSalaryDollar = minusSalary.apply(lambda x: x.replace('$', '').replace(' ', ''))

result['Salary'] = minusSalaryDollar

result = result.drop(['Engineers', 'Value'], axis = 1)

cleanedResultArchitectureEng = pd.DataFrame(result.loc[df['Engineers'] == 'Architecture & Civil Engineering'])

cleanedResult = pd.DataFrame(cleanedResultArchitectureEng[['Metro', 'Dimension', 'Salary']])

countsMetroCleaned = cleanedResult['Metro'].apply(findNoMetro)

arc = cleanedResult.loc[cleanedResult["Dimension"] == 'Architecture & Civil Engineering']

arc = arc.loc[arc['Metro'] == 'Seattle']  

arc['Salary'] = arc['Salary'].astype(int)

avgSalary = (arc['Salary'].sum(axis = 0))/2


#find range of values of salary for median pay
medianMeasureField = result.loc[result['Dimension'] == 'Field Engineer']

medianMeasureField['Salary'] = medianMeasureField['Salary'].astype(int)

#Plot results for Field Engineer Salaries 
plt.ylabel('Salary', fontsize=30)

plt.suptitle('Field Engineer Salary: Glassdoor Listing', fontsize=40)

plt.bar(medianMeasureField['Metro'],medianMeasureField['Salary'])
plt.xlabel('City', fontsize=30)


plt.ylabel('Salary', fontsize=30)

plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.legend(loc=2, prop={'size': 15})

