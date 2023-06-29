import pandas as pd
import json
from datetime import datetime
# Read the dataframe
df = pd.read_csv('models.csv')

def extract_id(json_str, key):
    data_dict = json.loads(json_str)
    return data_dict.get(key, None)

# Extract 'id' from 'data' column
df['id'] = df['data'].apply(extract_id, key="id")
df['created'] = df['data'].apply(extract_id, key="created")
df['created_d'] = df['created'].apply(lambda x: datetime.fromtimestamp(x) )
df = df.sort_values(by="created")
df[['created_d', 'id']]

df2003= df[df['created_d'] > "2023-01-01 00:00:00"]['id'].to_numpy()