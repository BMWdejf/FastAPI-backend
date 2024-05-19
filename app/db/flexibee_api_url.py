import requests
import os
from dotenv import load_dotenv
from app.db.flexibee_data import get_data
import functools
import time
from typing import Callable, Any
import asyncio

load_dotenv()

def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f'starting {func} with args {args} {kwargs}')
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f'finished {func} in {total:.4f} second(s)')

        return wrapped

    return wrapper

@async_timed()
async def get_urls():
    auth = (os.getenv("FLEXB_USER"), os.getenv("FLEXB_PASS"))
    response = requests.get("https://sas-technologi.flexibee.eu:5434/c/einteriors_s_r_o_/cenik.json?detail=custom:id&limit=1&order=id@D", auth=auth)
    data = response.json()['winstrom']['cenik']

    max_id = data[0]["id"]
    #print(max_id)

    requests_data = []
    last_index = 1
    try:
        for id_value in range(1, 10 + 1):
            last_index = id_value
            url = f"https://sas-technologi.flexibee.eu:5434/c/einteriors_s_r_o_/cenik/{id_value}.json?detail=custom:id,kod,nazev,exportNaEshop,prilohy(nazSoub,%20content,%20link,%20typK)&relations=prilohy"
            requests_data.append(get_data(url))
            #requests_data.append(asyncio.to_thread(get_data, url))

        #print(requests_data)
        results = await asyncio.gather(*requests_data)

        for row in results:
            print(row)
    except Exception as e:
        print(e)
        print(last_index)

if __name__ == "__main__":
    asyncio.run(get_urls())
