import sqlite3
import numpy as np
import pandas as pd


def import_data():
    conn = sqlite3.connect('/Users/marwanebelaid/djangoCours/db.sqlite3')
    curr = conn.cursor()
    sql_query = pd.read_sql_query(''' SELECT * FROM prices ''',
                                  conn)
    conn.commit()
    curr.close()
    conn.close()
    dj = pd.DataFrame(sql_query, columns=['symbol', 'quote.USD.price','quote.USD.market_cap'])

    #dj.loc[:, 'quote.USD.market_cap'] = dj['quote.USD.market_cap'].map('{:,d}'.format)

    dj = dj.rename(columns= {'symbol':'tokens', 'quote.USD.price': 'price', 'quote.USD.market_cap': 'Market_cap'})

    return dj


def ln(x):

    return np.log(x)




