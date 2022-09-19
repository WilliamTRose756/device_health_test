import json
import boto3
import pandas as pd

# This is where the API call will happen
# For now I am using hardcoded data
with open('data.json') as data_1:
    read_content_1 = json.load(data_1)
devices = read_content_1['devices']

offline_devices = []
offline_devices_dictionaries = []

# Filter down to be a list of dictionaries
for device in devices:
    if device['online'] == '0':
        offline_devices.append(device)


# Filter out keys in the dictionaries that that match in include_keys
include_keys = ['name', 'deviceid', 'lastseen']
for i in offline_devices:
        newdictionary = {}
        for k,v in i.items():
            if k in include_keys:
                newdictionary[k] = v
        offline_devices_dictionaries.append(newdictionary)

print(offline_devices_dictionaries)

# Format to pandas dataframe
df=pd.DataFrame(offline_devices_dictionaries)
df.to_csv('sliced_data.csv')

# Upload to s3 bucket
s3 = boto3.resource('s3')
s3.meta.client.upload_file()







    





