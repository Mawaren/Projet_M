import pandas as pd
from decouple import config
from requests import Session
import json
import sqlite3





def get_prices():
    session = Session()

    conn = sqlite3.connect('db.sqlite3')

    url4 = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit=5000'
    parameters = {
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': config('CMCKEY')
    }
    session.headers.update(headers)
    response4 = session.get(url4, params=parameters)
    price = (json.loads(response4.text))
    price = pd.json_normalize(price, 'data').assign(**price['status'])  # recopé d'internet pas trop compris

    price = price[['symbol', 'quote.USD.price', 'quote.USD.market_cap']]

    price.to_sql('prices', con=conn, if_exists='replace')
    conn.commit()

    conn.close()
    # pas de fermeture de la connexion car sinon impossible de la réouvrir
    # connexion auto-gérée par django ?


get_prices()