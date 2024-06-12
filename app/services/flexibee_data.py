import requests
import os
from dotenv import load_dotenv
import asyncio
load_dotenv()

async def get_data(url: object) -> object:
    auth = (os.getenv("FLEXB_USER"), os.getenv("FLEXB_PASS"))
    response = await asyncio.to_thread(requests.get, url, auth=auth)
    #response = requests.get(url, auth=auth)
    data = response.json()['winstrom']['cenik']
    #TODO: Write for cycle for import data to database
    #print(data)
    return data
