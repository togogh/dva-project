import requests
import json
import pandas as pd
import time
import os


# THIS SCRIPT DOWNLOADS UK CENSUS DATA FOR 2011 AND 2021 FROM NOMIS 


### EXPLORE GEOGRAPHY DATASETS FROM NOMIS API
root_url = 'http://www.nomisweb.co.uk'

# api_url = '/api/v01/dataset/NM_1_1/geography.def.sdmx.json' # list all possible geography datasets
# api_url = '/api/v01/dataset/NM_1_1/geography/2092957697.def.sdmx.json' # list of all geography datasets in UK
api_url = '/api/v01/dataset/NM_1_1/geography/2092957697TYPE441.def.sdmx.json' # major towns and cities within United Kingdom

url = root_url + api_url
response = requests.get(url)
json.loads(response.text)


### DOWNLOAD MAJOR TOWNS AND CITIES DATASET AND STORE AS DATAFRAME
api_url = '/api/v01/dataset/NM_1_1/geography/2092957697TYPE441.def.sdmx.json' # major towns and cities within United Kingdom
url = root_url + api_url

response = requests.get(url)
cities_json = json.loads(response.text)
cities_json = cities_json['structure']['codelists']['codelist'][0]['code']
cities_list = []
for city in cities_json:
    geog_code = city['annotations']['annotation'][2]['annotationtext']
    name = city['description']['value']
    id = city['value']
    city_dict = {
        'id': id,
        'name': name,
        'geog_code': geog_code
    }
    cities_list.append(city_dict)
cities_df = pd.DataFrame(cities_list)
cities_df


### IMPORT LOOKUP TABLE MATCHING 2011 MSOA CODES WITH CITIES
try:
    c2011_lookup = pd.read_csv(r'.\data\raw\geoportal\Middle_Layer_Super_Output_Area_(2011)_to_Major_Towns_and_Cities_(December_2015)_Lookup_in_England_and_Wales.csv')
except:
    os.chdir('..')
    c2011_lookup = pd.read_csv(r'.\data\raw\geoportal\Middle_Layer_Super_Output_Area_(2011)_to_Major_Towns_and_Cities_(December_2015)_Lookup_in_England_and_Wales.csv')
c2011_lookup = c2011_lookup.dropna(subset=['TCITY15NM'])
c2011_lookup


### IMPORT LOOKUP TABLE MATCHING MSOA CODES FOR 2011 AND 2021
### CREATE BASE TABLE FOR 2021 USING 2011 MSOA CODES
c2021_lookup = pd.read_csv(r'.\data\raw\geoportal\MSOA_(2011)_to_MSOA_(2021)_to_Local_Authority_District_(2022)_Lookup_for_England_and_Wales_(Version_2).csv')
c2021_lookup = c2021_lookup[['MSOA11CD', 'MSOA21CD']]
c2021_lookup = c2021_lookup.merge(c2011_lookup, on='MSOA11CD', how='inner')
c2021_lookup = c2021_lookup.drop('MSOA11CD', axis=1)
c2021_lookup = c2021_lookup.rename(columns={'MSOA11NM': 'MSOA21NM'})
c2021_lookup


### GET A LIST OF ALL CENSUS DATASETS FOR 2021 AND STORE THIS METADATA IN A CSV
api_url = '/api/v01/dataset/def.sdmx.json?search=C2021TS*'
url = root_url + api_url
response = requests.get(url)

c2021_datasets_json = json.loads(response.text)
c2021_datasets_json = c2021_datasets_json['structure']['keyfamilies']['keyfamily']
c2021_datasets_metadata_list = []
for dataset in c2021_datasets_json:
    annotations = dataset['annotations']['annotation']
    for annotation in annotations:
        if annotation['annotationtitle'] == 'contenttype/geoglevel':
            geoglevel = annotation['annotationtext']
        if annotation['annotationtitle'] == 'Mnemonic':
            mnemonic = annotation['annotationtext']
        if annotation['annotationtitle'] == 'MetadataText0':
            description = annotation['annotationtext']
    id = dataset['id']
    metadata = {
        'id': id,
        'mnemonic': mnemonic,
        'description': description,
        'geoglevel': geoglevel
    }
    c2021_datasets_metadata_list.append(metadata)
c2021_datasets_metadata_df = pd.DataFrame(c2021_datasets_metadata_list)
c2021_datasets_metadata_df.to_csv(r'.\data\raw\api\msoa\counts\c2021\metadata.csv')
c2021_datasets_metadata_df


### DOWNLOAD ALL 2021 DATASETS THAT HAVE MSOA AS A LEVEL OF DETAIL
record_limit = 25000    # The API has a limit of 25000 records for each download
offset = 0

for dataset in c2021_datasets_metadata_list:
    id = dataset['id']
    mnemonic = dataset['mnemonic']
    geoglevel = dataset['geoglevel'].split(',')
    if 'msoa' not in geoglevel:
        continue

    print("downloading", mnemonic)

    ### Download a small snapshot of the dataset for troubleshooting whenever the download fails
    api_url = f'/api/v01/dataset/{id}.data.csv?recordlimit=10'
    url = root_url + api_url
    try:
        dataset_df = pd.read_csv(url)
    except:
        time.sleep(60)
        dataset_df = pd.read_csv(url)
    dataset_df.to_csv('test.csv')

    try:
        stat_name = dataset_df.filter(regex='^C2021.*NAME$', axis=1).columns[0].lower()
    except:
        try:
            stat_name = dataset_df.filter(regex='^CELL.*NAME$', axis=1).columns[0].lower()
        except:
            stat_name = dataset_df.filter(regex='^C_.*NAME$', axis=1).columns[0].lower()

    last_record = offset

    for i in range(1000):
        print(f"trying records {last_record} - {last_record + record_limit}")
        api_url = f'/api/v01/dataset/{id}.data.csv?geography=TYPE152&measures=20100&select=date,geography_code,geography_type,geography_typecode,{stat_name},obs_value&recordlimit={record_limit}&recordoffset={last_record}'
        url = root_url + api_url

        print(url)

        try:
            batch_df = pd.read_csv(url)
        except pd.errors.EmptyDataError:
            print("empty dataset")
            break
        except:
            time.sleep(60)
            batch_df = pd.read_csv(url)

        if len(batch_df) == 0:
            break

        dest_file = f'./data/raw/api/msoa/counts/c2021/{mnemonic}_{i:02}.csv'
        batch_df.to_csv(dest_file)
        print(f"chunk {i} saved in {dest_file}")

        last_record += record_limit


### GET A LIST OF ALL CENSUS DATASETS FOR 2011 AND STORE THIS METADATA IN A CSV
api_url = '/api/v01/dataset/def.sdmx.json?search=c2011ks*'
url = root_url + api_url
response = requests.get(url)

c2011_datasets_json = json.loads(response.text)
c2011_datasets_json = c2011_datasets_json['structure']['keyfamilies']['keyfamily']
c2011_datasets_metadata_list = []
for dataset in c2011_datasets_json:
    annotations = dataset['annotations']['annotation']
    for annotation in annotations:
        if annotation['annotationtitle'] == 'contenttype/geoglevel':
            geoglevel = annotation['annotationtext']
        if annotation['annotationtitle'] == 'Mnemonic':
            mnemonic = annotation['annotationtext']
        if annotation['annotationtitle'] == 'MetadataText0':
            description = annotation['annotationtext']
    id = dataset['id']
    metadata = {
        'id': id,
        'mnemonic': mnemonic,
        'description': description,
        'geoglevel': geoglevel
    }
    c2011_datasets_metadata_list.append(metadata)
c2011_datasets_metadata_df = pd.DataFrame(c2011_datasets_metadata_list)
c2011_datasets_metadata_df.to_csv('./data/raw/api/msoa/counts/c2011/metadata.csv')
c2011_datasets_metadata_df


### DOWNLOAD ALL 2011 DATASETS THAT HAVE MSOA AS A LEVEL OF DETAIL
for dataset in c2011_datasets_metadata_list[22:]:
    id = dataset['id']
    mnemonic = dataset['mnemonic']
    geoglevel = dataset['geoglevel'].split(',')
    if 'oa' not in geoglevel:
        continue

    print("downloading", mnemonic)
    api_url = f'/api/v01/dataset/{id}.data.csv?recordlimit=10'
    url = root_url + api_url
    try:
        dataset_df = pd.read_csv(url)
    except:
        time.sleep(60)
        dataset_df = pd.read_csv(url)
    dataset_df.to_csv('test.csv')
    try:
        stat_name = dataset_df.filter(regex='^C2011.*NAME$', axis=1).columns[0].lower()
    except:
        try:
            stat_name = dataset_df.filter(regex='^CELL.*NAME$', axis=1).columns[0].lower()
        except:
            try:
                stat_name = dataset_df.filter(regex='^C_.*NAME$', axis=1).columns[0].lower()
            except:
                stat_name = dataset_df.filter(regex='RURAL_URBAN_TYPE', axis=1).columns[0].lower()

    last_record = offset

    for i in range(1000):
        print(f"trying records {last_record} - {last_record + record_limit}")
        api_url = f'/api/v01/dataset/{id}.data.csv?geography=TYPE297&measures=20100&select=date,geography_code,geography_type,geography_typecode,{stat_name},obs_value&recordlimit={record_limit}&recordoffset={last_record}'
        url = root_url + api_url

        print(url)

        try:
            batch_df = pd.read_csv(url)
        except pd.errors.EmptyDataError:
            print("empty dataset")
            break
        except:
            time.sleep(60)
            batch_df = pd.read_csv(url)

        if len(batch_df) == 0:
            break

        dest_file = f'./data/raw/api/msoa/counts/c2011/{mnemonic}_{i:02}.csv'
        batch_df.to_csv(dest_file)
        print(f"chunk {i} saved in {dest_file}")

        last_record += record_limit