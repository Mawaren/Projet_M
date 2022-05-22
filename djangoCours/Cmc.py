import sqlite3
import pandas as pd
import seaborn as sns


def import_data():
    conn = sqlite3.connect('/Users/marwanebelaid/djangoCours/db.sqlite3')
    curr = conn.cursor()
    sql_query = pd.read_sql_query(''' SELECT * FROM prices ''',
                                  conn)
    conn.commit()
    curr.close()
    conn.close()
    dj = pd.DataFrame(sql_query, columns=['symbol', 'quote.USD.price','quote.USD.market_cap'])


    dj = dj.round(4)

    dj = dj.rename(columns= {'quote.USD.price': 'price', 'quote.USD.market_cap': 'Market_cap'})

    return dj



def transform_data():
    dj = import_data()

    dj = dj.style.set_properties(**{'border': '1.3px solid green',
                          'color': 'magenta'})

    return dj

