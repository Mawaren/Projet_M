import pandas as pd
from requests import Session
import json
from datetime import datetime, timedelta
import sqlite3
import time
session = Session()

today = datetime.today()



def get_prices():
    #a = 0
    #while a==0:

    conn = sqlite3.connect('/Users/marwanebelaid/djangoCours/db.sqlite3')
    curr = conn.cursor()


    url4 ='https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit=5000'
    parameters = {
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '02cc6aa0-8a27-4e7d-b2e3-bd68c838dd89'
    }
    session.headers.update(headers)
    response4 = session.get(url4, params=parameters)
    price = (json.loads(response4.text))
    price = pd.json_normalize(price, 'data').assign(**price['status'])
    price = price[['symbol','quote.USD.price']]


    price.to_sql('prices', con = conn, if_exists= 'replace')
    conn.commit()
    curr.close()
    conn.close()
    #time.sleep(86400)

get_prices()