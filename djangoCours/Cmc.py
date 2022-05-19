import sqlite3
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
    dj.set_index('symbol', inplace=True)

    dj = dj.round(4)

    dj = dj.rename(columns= {'quote.USD.price': 'price', 'quote.USD.market_cap': 'Market_cap'})

    print(dj)
    return dj


import_data()
