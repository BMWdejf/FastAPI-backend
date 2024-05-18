import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_urls():
    auth = (os.getenv("FLEXB_USER"), os.getenv("FLEXB_PASS"))
    response = requests.get("https://sas-technologi.flexibee.eu:5434/c/einteriors_s_r_o_/cenik.json?detail=custom:id&limit=1&order=id@D", auth=auth)
    data = response.json()['winstrom']['cenik']

    max_id = data[0]["id"]

    # Create an empty list to store the URLs
    urls =[]

    for id_value in range(1, int(max_id) + 1):
        url = f"https://sas-technologi.flexibee.eu:5434/c/einteriors_s_r_o_/cenik/{id_value}.json?detail=custom:id,kod,nazev,exportNaEshop,prilohy(nazSoub,%20content,%20link,%20typK)&relations=prilohy"
        # Add the URL to the list
        urls.append(url)

    return urls # Return the list with the URLs
