import requests
import os
from dotenv import load_dotenv
from app.db.flexibee_data import get_data
import functools
import time
from typing import Callable, Any
import asyncio
from app.models.models import Products
from app.db.base import SessionLocal
import re

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

def extract_drive_id(link):
    pattern = r"https://drive\.google\.com/file/d/([^/]+)/view\?usp=share_link"
    match = re.search(pattern, link)
    return match.group(1) if match else None

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
        for id_value in range(6328, int(max_id) + 1):
            last_index = id_value
            url = f"https://sas-technologi.flexibee.eu:5434/c/einteriors_s_r_o_/cenik/{id_value}.json?detail=custom:id,kod,nazev,exportNaEshop,prilohy(nazSoub,%20content,%20link,%20typK)&relations=prilohy"
            requests_data.append(get_data(url))
            #requests_data.append(asyncio.to_thread(get_data, url))

        #print(requests_data)
        results = await asyncio.gather(*requests_data)

        #print(results)

        db = SessionLocal()  # Start database session
        for item_list in results:
            for item in item_list:
                export_on_eshop = item['exportNaEshop'] == 'true'
                link = item['prilohy'][0]['link'] if 'prilohy' in item and item['prilohy'] else None
                drive_id = extract_drive_id(link) if link else None

                #print(f"Original link: {link}")
                #print(f"Extracted drive_id: {drive_id}")

                existing_product = db.query(Products).filter_by(fx_id=item['id']).first()

                if export_on_eshop:
                    if existing_product:
                        # Update existing product
                        existing_product.code = item['kod']
                        existing_product.name = item['nazev']
                        existing_product.exportOnEshop = 1
                        existing_product.link = drive_id
                    else:
                        # Add new product
                        product = Products(
                            fx_id=item['id'],
                            code=item['kod'],
                            name=item['nazev'],
                            exportOnEshop=1,
                            link=drive_id
                        )
                        db.add(product)
                else:
                    if existing_product:
                        # Delete product if exportNaEshop is false
                        db.delete(existing_product)

        db.commit()
        db.close()

    except Exception as e:
        print(e)
        print(last_index)

if __name__ == "__main__":
    asyncio.run(get_urls())
