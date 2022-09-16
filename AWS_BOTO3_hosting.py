import json
import smtplib
import pandas as pd

sender_email = "william.rose@modjoul.com"
rec_email = "william.rose@modjoul.com"
password = ""


with open('data.json') as data_1:
    read_content_1 = json.load(data_1)



devices = read_content_1['devices']
offline_devices = []
for device in devices:

    if device['online'] == '0':
        offline_device_name = device
        offline_devices.append(offline_device_name)

df=pd.DataFrame(offline_devices)
df.to_csv('test_1.csv')



print(len(offline_devices))

    





