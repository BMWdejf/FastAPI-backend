import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_data(url):
    auth = (os.getenv("FLEXB_USER"), os.getenv("FLEXB_PASS"))
    response = requests.get(url, auth=auth)
    data = response.json()['winstrom']['cenik']
    #TODO: Write for cycle for import data to database
    print(data)
