import boto3
import pandas as pd
from dotenv import load_dotenv
import os
from io import StringIO
from datetime import datetime
import requests

# Initialize environment variables
load_dotenv()

USERNAME_SMTP = os.environ.get("USERNAME_SMTP")
PASSWORD = os.environ.get("PASSWORD")
URL_OBTAIN_LOGIN_TOKEN = os.environ.get("URL_OBTAIN_LOGIN_TOKEN")
URL_DEVICE_STATUS = os.environ.get('URL_DEVICE_STATUS')
BUCKET_NAME = os.getenv('BUCKET_NAME')



# Logs into API to obtain bearer token required for status update
# and passes it into the next function to run
def get_ClearStream_login_token():
    
    payload = {
        "username":USERNAME_SMTP,
        "password": PASSWORD
    }
    headers = {
        'Content-Type': 'text/plain'       
    }

    response = requests.request("POST", URL_OBTAIN_LOGIN_TOKEN, headers=headers, json=payload)
    token_response = response.json()
    BEARER_TOKEN = token_response['token']

    if BEARER_TOKEN:
        print('Login Successful!')
        
    get_ClearStream_JSON_data(BEARER_TOKEN)


# Uses the token obtained from login to access the status of the devices and see 
# if DVA3 devices are currently offline and then sends email with devices listed
devices_list = []
def get_ClearStream_JSON_data(BEARER_TOKEN):

    # HTTP GET request with token
    headers = {
        'Content-Type': 'text/plain',
        'Authorization': f'Bearer {BEARER_TOKEN}'
    }
    response = requests.request("GET", URL_DEVICE_STATUS, headers=headers )

    # Filter down response result
    top = response.json()
    devices = top['devices']

    devices_list.append(devices)
get_ClearStream_login_token()



# Format to pandas dataframe
df=pd.DataFrame(devices_list[0])

# Send the file up to the S3 buckets
resource = boto3.resource(
    's3',
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_CODE'),
    region_name = os.getenv('AWS_REGION')
)

# Name files and determine location
timestamp = str(datetime.now().replace(microsecond=0))
current = 'current/device_status_info.csv'
history = f'history/device_status_info_{timestamp}.csv'

# Add to both current and historical folders
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)
resource.Object(BUCKET_NAME, current).put( Body=csv_buffer.getvalue())
resource.Object(BUCKET_NAME, history).put( Body=csv_buffer.getvalue())






    












