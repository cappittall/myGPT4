import os

import json
from datetime import datetime
import pandas as pd

def load_env():
    for k in open('.env', 'r').read().splitlines():
        if k != "":
            envs = k.split('=')
            os.environ[envs[0]]=envs[1]
        

def read_models():
    # Read the dataframe
    df = pd.read_csv('data/models.csv')

    def extract_id(json_str, key):
        data_dict = json.loads(json_str)
        return data_dict.get(key, None)

    # Extract 'id' from 'data' column
    df['id'] = df['data'].apply(extract_id, key="id")
    df['created'] = df['data'].apply(extract_id, key="created")
    df['created_d'] = df['created'].apply(lambda x: datetime.fromtimestamp(x) )
    df = df.sort_values(by="created")
    df[['created_d', 'id']]

    return df[df['created_d'] > "2023-01-01 00:00:00"]['id'].to_numpy()