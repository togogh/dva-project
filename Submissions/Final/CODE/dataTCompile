import os
import pandas as pd
import glob
import math
import numpy as np
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


# THIS SCRIPT COMPILES ALL CENSUS, INCOME, AND HOUSE PRICING DATA INTO ONE DATASET FOR MODELING


### FUNCTION TO ADJUST PRICES AND INCOME TO INFLATION
annual_inflation = {
    # https://www.rateinflation.com/inflation-rate/uk-historical-inflation-rate/
    2002: 1.259 / 100,
    2003: 1.362 / 100,
    2004: 1.344 / 100,
    2005: 2.057 / 100,
    2006: 2.329 / 100,
    2007: 2.323 / 100,
    2008: 3.602 / 100,
    2009: 2.165 / 100,
    2010: 3.298 / 100,
    2011: 4.464 / 100,
    2012: 2.828 / 100,
    2013: 2.565 / 100,
    2014: 1.461 / 100,
    2015: 0.040 / 100,
    2016: 0.660 / 100,
    2017: 2.683 / 100,
    2018: 2.478 / 100,
    2019: 1.791 / 100,
    2020: 0.851 / 100,
    2021: 2.588 / 100,
}

def inflation_adjustment(year, pv):
    try:
        fv = int(pv)
    except:
        return np.nan
    while year < 2021:
        year += 1
        r = annual_inflation[year]
        fv = fv * (1 + r)
    return fv


### CREATE BASE TABLES FOR 2011 AND 2021 DATA
base2011_df = pd.read_csv(r'.\data\raw\geoportal\Middle_Layer_Super_Output_Area_(2011)_to_Major_Towns_and_Cities_(December_2015)_Lookup_in_England_and_Wales.csv')
base2011_df = base2011_df.dropna(axis=0, how='any', ignore_index=True)
base2011_df = base2011_df.drop(columns='FID')
base2011_df

base2021_df = pd.read_csv(r'.\data\raw\geoportal\MSOA_(2011)_to_MSOA_(2021)_to_Local_Authority_District_(2022)_Lookup_for_England_and_Wales_(Version_2).csv')
base2021_df = base2021_df[['MSOA21CD', 'MSOA11CD']]
base2021_df = base2021_df.merge(base2011_df, on='MSOA11CD')
base2021_df


### IMPORT CENSUS DATA
c2011_census_df = base2011_df.copy()
c2011_dfs = []

root_dir = r'.\data\raw\api\percents\c2011'
tables = glob.glob('*', root_dir=root_dir)

for table in tables:
    df = pd.read_csv(rf'{root_dir}\{table}')
    c2011_dfs.append(df)
    c2011_census_df = c2011_census_df.merge(df, how='left', left_on='MSOA11CD', right_on='GEOGRAPHY_CODE', suffixes=('', '_y'))
    c2011_census_df_cols = list(c2011_census_df.columns)
    c2011_census_df_dup_cols = [col for col in c2011_census_df_cols if '_y' in col]
    c2011_census_df_dup_cols.append('GEOGRAPHY_CODE')
    c2011_census_df = c2011_census_df.drop(columns=c2011_census_df_dup_cols)
c2011_census_df = c2011_census_df.dropna(axis=1, how='all')
c2011_census_df

c2021_census_df = base2021_df.copy()
c2021_dfs = []

root_dir = r'.\data\raw\api\percents\c2021'
tables = glob.glob('*', root_dir=root_dir)

for table in tables:
    df = pd.read_csv(rf'{root_dir}\{table}')
    c2021_dfs.append(df)
    c2021_census_df = c2021_census_df.merge(df, how='left', left_on='MSOA11CD', right_on='GEOGRAPHY_CODE', suffixes=('', '_y'))
    c2021_census_df_cols = list(c2021_census_df.columns)
    c2021_census_df_dup_cols = [col for col in c2021_census_df_cols if '_y' in col]
    c2021_census_df_dup_cols.append('GEOGRAPHY_CODE')
    c2021_census_df = c2021_census_df.drop(columns=c2021_census_df_dup_cols)
c2021_census_df = c2021_census_df.dropna(axis=1, how='all')
c2021_census_df


### MERGE CENSUS DATA WITH BASE TABLES
c2011_census_df = base2011_df.copy()
for df in c2011_dfs:
    c2011_census_df = c2011_census_df.merge(df, how='left', left_on='MSOA11CD', right_on='GEOGRAPHY_CODE', suffixes=('', '_y'))
    c2011_census_df_cols = list(c2011_census_df.columns)
    c2011_census_df_dup_cols = [col for col in c2011_census_df_cols if '_y' in col]
    c2011_census_df_dup_cols.append('GEOGRAPHY_CODE')
    c2011_census_df = c2011_census_df.drop(columns=c2011_census_df_dup_cols)
c2011_census_df = c2011_census_df.dropna(axis=1, how='all')
c2011_census_df


### IMPORT INCOME DATA AND MERGE WITH BASE TABLE
income2011_df = pd.read_excel(r'.\data\raw\govuk\1smallareaincomeestimatesdatatcm77420299.xls', sheet_name='Total weekly income', header=4)
income2011_df = income2011_df[['MSOA code', 'Total weekly income (£)']]
income2011_df = income2011_df.dropna(axis=0, how='any')
income2011_df['Total weekly income (£)'] = income2011_df['Total weekly income (£)'].apply(lambda x: inflation_adjustment(2011, x))
income2011_df

c2011_income_df = c2011_census_df.copy()
c2011_income_df = c2011_income_df.merge(income2011_df, how='left', left_on='MSOA11CD', right_on='MSOA code')
c2011_income_df = c2011_income_df.drop(columns='MSOA code')
c2011_income_df

income2021_df = pd.read_excel(r'.\data\raw\ons\saiefy1920finalqaddownload280923.xlsx', sheet_name='Total annual income', header=4)
income2021_df = income2021_df[['MSOA code', 'Total annual income (£)']]
income2021_df = income2021_df.dropna(axis=0, how='any')
income2021_df

c2021_income_df = c2021_census_df.copy()
c2021_income_df = c2021_income_df.merge(income2021_df, how='left', left_on='MSOA21CD', right_on='MSOA code')
c2021_income_df = c2021_income_df.drop(columns='MSOA code')
c2021_income_df


### IMPORT HOUSE PRICING DATA AND MERGE WITH BASE TABLE
housing2011_df = pd.read_excel(r'.\data\raw\ons\hpssamedianpricebymsoa.xlsx', sheet_name='1a', header=2)
housing2011_df = housing2011_df[['MSOA code', 'Year ending Dec 2011']]
housing2011_df = housing2011_df.rename(columns={'Year ending Dec 2011': 'Median house price'})
housing2011_df['Median house price'] = housing2011_df['Median house price'].apply(lambda x: inflation_adjustment(2011, x))
housing2011_df

c2011_housing_df = c2011_income_df.copy()
c2011_housing_df = c2011_housing_df.merge(housing2011_df, how='left', left_on='MSOA11CD', right_on='MSOA code')
c2011_housing_df = c2011_housing_df.drop(columns='MSOA code')
c2011_housing_df

housing2021_df = pd.read_excel(r'.\data\raw\ons\hpssamedianpricebymsoa.xlsx', sheet_name='1a', header=2)
housing2021_df = housing2021_df[['MSOA code', 'Year ending Dec 2021']]
housing2021_df = housing2021_df.rename(columns={'Year ending Dec 2021': 'Median house price'})
housing2021_df

c2021_housing_df = c2021_income_df.copy()
c2021_housing_df = c2021_housing_df.merge(housing2021_df, how='left', left_on='MSOA21CD', right_on='MSOA code')
c2021_housing_df = c2021_housing_df.drop(columns='MSOA code')
c2021_housing_df


### GENERATE ADDITIONAL COLUMNS FOR NORMALIZATION AND SAVE DATASET FOR EACH YEAR
c2011_df = c2011_housing_df.copy()
c2011_df = c2011_df.dropna(axis=1, how='all')
c2011_df["Central and South America"] = c2011_df["South America"] + c2011_df["Central America"]
c2011_df["3 or more cars or vans in household"] = c2011_df["3 cars or vans in household"] + c2011_df["4 or more cars or vans in household"]
c2011_df["Married or in a registered civil partnership"] = c2011_df["Married"] + c2011_df["In a registered same-sex civil partnership"]
c2011_df["Age 15 to 19 years"] = c2011_df["Age 15"] + c2011_df["Age 16 to 17"] + c2011_df["Age 18 to 19"]
c2011_df["Aged 5 to 9 years"] = c2011_df["Age 5 to 7"] + c2011_df["Age 8 to 9"]
c2011_df["Aged 85 years and over"] = c2011_df["Age 85 to 89"] + c2011_df["Age 90 and over"]
c2011_df["Age: 16 years and over"] = c2011_df["All usual residents aged 16 to 74"] + c2011_df["Age 75 to 84"] + c2011_df["Aged 85 years and over"]
c2011_df.to_csv(r'.\data\clean\c2011_percent.csv', index=False)

c2021_df = c2021_housing_df.copy()
c2021_df = c2021_df.dropna(axis=1, how='all')
c2021_df["Average number of bedrooms per household"] = (c2021_df["1 bedroom"] + c2021_df["2 bedrooms"] * 2 + c2021_df["3 bedrooms"] * 3 + c2021_df["4 or more bedrooms"] * 5) / c2021_df["Number of households"]
c2021_df["Other combination of skills in Welsh"] = c2021_df["Can read and write but cannot speak Welsh"] + c2021_df["Can read but cannot speak or write Welsh"] + c2021_df["Can speak and other combinations of skills in Welsh"] + c2021_df["Can speak, read and write Welsh"] + c2021_df["Can understand spoken Welsh only"] + c2021_df["Can write but cannot speak or read Welsh"]
c2021_df["Economically active: Self-employed"] = c2021_df["Economically active and a full-time student:In employment:Self-employed with employees"] + c2021_df["Economically active and a full-time student:In employment:Self-employed without employees"]
c2021_df["Economically active"] = c2021_df["Economically active and a full-time student"] + c2021_df["Economically active (excluding full-time students)"]
c2021_df["Medical and care establishment: Local Authority: Care home or other home"] = c2021_df["Medical and care establishment: Local Authority: Care home with nursing"] + c2021_df["Medical and care establishment: Local Authority: Care home without nursing"] + c2021_df["Medical and care establishment: Local Authority: Other home"]
c2021_df["Age 30 to 44"] = c2021_df["Aged 30 to 34 years"] + c2021_df["Aged 35 to 39 years"] + c2021_df["Aged 40 to 44 years"]
c2021_df["Age 45 to 59"] = c2021_df["Aged 45 to 49 years"] + c2021_df["Aged 50 to 54 years"] + c2021_df["Aged 55 to 59 years"]
c2021_df["Age 65 to 74"] = c2021_df["Aged 65 to 69 years"] + c2021_df["Aged 70 to 74 years"]
c2021_df["Age 75 to 84"] = c2021_df["Aged 75 to 79 years"] + c2021_df["Aged 80 to 84 years"]
c2021_df.to_csv(r'.\data\clean\c2021_percent.csv', index=False)


### IMPORT GOOGLE SHEETS WITH COLUMN MAPPER TO NORMALIZE COLUMN NAMES ACROSS BOTH YEARS
normalizer_df = pd.read_csv('https://docs.google.com/spreadsheets/d/' + 
                   '1nLWtw-6VwOgKvADQEhwIa0s9zst_-_aY5CVGEoCoKpU' +
                   '/export?gid=508974035&format=csv')
final_cols = list(normalizer_df['var_final'])
var_types = list(normalizer_df['var_type'])


### NORMALIZE COLUMNS
normcols_2011 = list(normalizer_df['var_2011'])
multcols_2011 = list(normalizer_df['multiplier_2011'])

fin2011_df = pd.DataFrame()

for final_col, var_type, normcol, multcol in zip(final_cols, var_types, normcols_2011, multcols_2011):
    if var_type == 'disc':
        fin2011_df[final_col] = c2011_df[normcol]
    else:
        if not math.isnan(multcol):
            fin2011_df[final_col] = c2011_df[normcol] * multcol
        else:
            fin2011_df[final_col] = 0

fin2011_df['Year'] = 2011
fin2011_df

normcols_2021 = list(normalizer_df['var_2021'])
multcols_2021 = list(normalizer_df['multiplier_2021'])

fin2021_df = pd.DataFrame()

for final_col, var_type, normcol, multcol in zip(final_cols, var_types, normcols_2021, multcols_2021):
    if var_type == 'disc':
        fin2021_df[final_col] = c2021_df[normcol]
    else:
        if not math.isnan(multcol):
            fin2021_df[final_col] = c2021_df[normcol] * multcol
        else:
            fin2021_df[final_col] = None

fin2021_df['Year'] = 2021
fin2021_df


### CLEAN NULL VALUES AND COMPILE BASE TABLES INTO FINAL DATASET
fin_df = pd.concat([fin2011_df, fin2021_df])
id_cols = ["MSOA Code", "MSOA Name", "City Code", "City Name", "Year"]
val_cols = [col for col in list(fin_df.columns) if col not in id_cols]
val_cols = sorted(val_cols)
fin_cols = id_cols + val_cols
fin_df = fin_df[fin_cols]
fin_df = fin_df.groupby(id_cols).sum().reset_index()
fin_df = fin_df.replace([np.inf, -np.inf], 0)
fin_df.to_csv(r".\data\clean\normalized_percents.csv", index=False)
fin_df