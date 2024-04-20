import os
import pandas as pd
import glob


# THIS SCRIPT TRANSFORMS THE DOWNLOADED CENSUS DATA VALUES INTO PERCENTS FOR EACH DATASET


### LIST ALL DATASETS FROM 2011 CENSUS DATA
try:
    metadata_2011 = pd.read_csv(r'.\data\raw\api\msoa\counts\c2011\metadata.csv')
except:  
    os.chdir("..")
    metadata_2011 = pd.read_csv(r'.\data\raw\api\msoa\counts\c2011\metadata.csv')
metadata_2011['clean_mnemonic'] = metadata_2011['mnemonic'].str.extract('(c2011ks\d*).*')
metadata_2011 = metadata_2011[metadata_2011['geoglevel'].str.contains('oa')]
metadata_2011_mnemonics = list(set(metadata_2011['clean_mnemonic']))
metadata_2011['geoglevel']


### LIST ALL DATASETS FROM 2021 CENSUS DATA
metadata_2021 = pd.read_csv(r'.\data\raw\api\msoa\counts\c2021\metadata.csv')
metadata_2021['clean_mnemonic'] = metadata_2021['mnemonic'].str.extract('(c2021ts.*)')
metadata_2021 = metadata_2021[metadata_2021['geoglevel'].str.contains('msoa')]
metadata_2021_mnemonics = list(set(metadata_2021['clean_mnemonic']))
len(metadata_2021_mnemonics)


### IMPORT ALL CENSUS 2011 DATASETS AND STORE IN A LIST OF DATAFRAMES
c2011_dfs = []

for mnemonic in metadata_2011_mnemonics:

    root_dir = r'.\data\raw\api\msoa\counts\c2011'
    mnemonic_tables = glob.glob(mnemonic+'*', root_dir=root_dir)
    mnemonic_dfs = []

    for table in mnemonic_tables:
        df = pd.read_csv(rf"{root_dir}\{table}")
        mnemonic_dfs.append(df)

    mnemonic_df = pd.concat(mnemonic_dfs)

    mnemonic_df = mnemonic_df.drop(columns=['Unnamed: 0', 'GEOGRAPHY_TYPE', 'GEOGRAPHY_TYPECODE', 'DATE'])
    mnemonic_df['OBS_VALUE'] = mnemonic_df['OBS_VALUE'].astype(float)
    mnemonic_df = mnemonic_df[mnemonic_df['OBS_VALUE'] > 0]
    cols = list(mnemonic_df.columns)
    var_col = [col for col in cols if col not in ['GEOGRAPHY_CODE', 'OBS_VALUE']][0]
    mnemonic_df = mnemonic_df.pivot_table(index='GEOGRAPHY_CODE', columns=var_col, values='OBS_VALUE', aggfunc='mean', fill_value=0)
    mnemonic_df = mnemonic_df.reset_index(drop=False)
    c2011_dfs.append(mnemonic_df)
c2011_dfs[0]


### IMPORT ALL CENSUS 2021 DATASETS AND STORE IN A LIST OF DATAFRAMES
c2021_dfs = []

for mnemonic in metadata_2021_mnemonics:
    root_dir = r'.\data\raw\api\msoa\counts\c2021'
    mnemonic_tables = glob.glob(mnemonic+'*', root_dir=root_dir)
    mnemonic_dfs = []

    for table in mnemonic_tables:
        df = pd.read_csv(rf"{root_dir}\{table}")
        mnemonic_dfs.append(df)

    mnemonic_df = pd.concat(mnemonic_dfs)

    mnemonic_df = mnemonic_df.drop(columns=['Unnamed: 0', 'GEOGRAPHY_TYPE', 'GEOGRAPHY_TYPECODE', 'DATE'])
    mnemonic_df['OBS_VALUE'] = mnemonic_df['OBS_VALUE'].astype(float)
    mnemonic_df = mnemonic_df[mnemonic_df['OBS_VALUE'] > 0]
    cols = list(mnemonic_df.columns)
    var_col = [col for col in cols if col not in ['GEOGRAPHY_CODE', 'OBS_VALUE']][0]
    mnemonic_df = mnemonic_df.pivot_table(index='GEOGRAPHY_CODE', columns=var_col, values='OBS_VALUE', aggfunc='mean', fill_value=0)
    mnemonic_df = mnemonic_df.reset_index(drop=False)
    c2021_dfs.append(mnemonic_df)
c2021_dfs[37]


### CONVERT NON-AGGREGATE DATA INTO PERCENTS
for df in c2011_dfs:
    print(df.columns)
    total_col = df.filter(regex='(^All categories.*)|(.*All households.*)|(All usual residents.*)|(All lone parent housholds.*)').columns[0]
    total_cols = list(df.filter(regex='(^All categories.*)|(.*All households.*)|(All usual residents.*)|(All lone parent housholds.*)').columns)
    agg_cols = list(df.filter(regex='.*([Aa]verage)|([Mm]ean)|([Mm]edian)|([Nn]umber of).*').columns)
    geo_col = 'GEOGRAPHY_CODE'
    val_cols = [col for col in df.columns if col not in total_cols and col not in agg_cols and col != geo_col]
    for col in val_cols:
        df[col] = df[col] / df[total_col]

for df in c2021_dfs:
    geo_col = 'GEOGRAPHY_CODE'
    try:
        total_col = df.filter(regex='Total.*').columns[0]
    except:
        total_col = [col for col in df.columns if col not in [geo_col]][0]
    total_cols = list(df.filter(regex='Total.*').columns)
    agg_cols = list(df.filter(regex='.*([Aa]verage)|([Mm]ean)|([Mm]edian)|([Nn]umber of)|(\d\sbedrooms?)|(more\sbedrooms).*').columns)
    geo_col = 'GEOGRAPHY_CODE'
    val_cols = [col for col in df.columns if col not in total_cols and col not in agg_cols and col != geo_col and col != total_col]
    for col in val_cols:
        df[col] = df[col] / df[total_col]


### STORE PERCENT DATA IN PERCENTS FOLDER
for mnemonic, df in zip(metadata_2011_mnemonics, c2011_dfs):
    df.to_csv(rf'.\data\raw\api\msoa\percents\c2011\{mnemonic}.csv')

for mnemonic, df in zip(metadata_2021_mnemonics, c2021_dfs):
    df.to_csv(rf'.\data\raw\api\msoa\percents\c2021\{mnemonic}.csv')