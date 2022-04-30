
import pandas as pd
from requests import Session
import json
import matplotlib.pyplot as plt
from datetime import datetime
import sqlite3






class Portefeuille:
    def __init__(self, adresse):
        self.conn = sqlite3.connect('/Users/marwanebelaid/djangoCours/db.sqlite3')
        self.curr = self.conn.cursor()
        self.session = Session()
        self.adresse = adresse
        self.blockchain = {'api.etherscan.com': 'MMW7FUW6EZ5YGSSINYR7NMCTDXV69XKKPF',
                           'api.ftmscan.com': '46NU3E7MB8EUBMWACBGT3B3KBK4ZS2GJFC',
                           'api.polygonscan.com': 'RB4ACXDV6HPNFUF38G8QF65BIIJXMDWMWF',
                           'api.bscscan.com': 'MPSX84G1YFA87FAD8N4QVAB1GFE6DU8SM5',
                           'api.arbiscan.io': 'VC2I8ZW7QH4HCX39WWFEF5P2GRH3BQ2C7H',
                           'api.snowtrace.io': 'IM4CBYMSZPP2YD8NWTSZ3QRP14SGXTP4K7', 'blockscout.com/xdai/mainnet': ''}
        self.layer = ['eth', 'ftm', 'matic', 'bnb', 'eth', 'avax', 'gno']
        self.layer_name = ['Ethereum', 'Fantom', 'Matic', 'Bnb', 'Ethereum', 'Avalanche', 'Gnosis']

        self.today = datetime.today().strftime('%Y-%m-%d')

        # créer une fonction pour vérifier qu'une adresse crypto existe avec un try dans la view
    def get_histo(self):
        token_name = []
        token = []
        address = []
        decimal = []
        blockchains = []
        ad = [self.adresse, self.adresse, self.adresse, self.adresse, self.adresse, self.adresse, self.adresse]
        self.histo = []
        dec = [18, 18, 18, 18, 18, 18, 18]
        for x, y in self.blockchain.items():
            url1 = 'https://{}/api?module=account&action=tokentx&address={}&startblock={}&endblock={}' \
                   '&sort=asc&apikey={}' \
                .format(x, self.adresse, str(self.today), str(self.today), y)

            response2 = self.session.get(url1)

            if response2.ok == True:
                historique = (json.loads(response2.text)['result'])
                self.histo.append((json.loads(response2.text)['result']))
                for index in range(len(historique)):
                    token.append(historique[index]['tokenSymbol'])
                    address.append(historique[index]['contractAddress'])
                    token_name.append(historique[index]['tokenName'])
                    blockchains.append(x)
                    if historique[index]['tokenDecimal'] is None:
                        decimal.append(0)
                    else:
                        decimal.append(float(historique[index]['tokenDecimal']))

            else:
                continue

        # nettoyage des données récupérée

        token = list(map(lambda x: x.lower(), token))

        dl = pd.DataFrame({'blockchains': blockchains, 'tokens': token, 'address': address, 'decimal': decimal,
                           'token_name': token_name})
        dl = dl.drop_duplicates()
        dt = pd.DataFrame({'blockchains': self.layer, 'tokens': self.layer, 'address': ad, 'decimal': dec,
                           'token_name': self.layer_name})

        df = pd.concat([dl, dt])
        # suppression des données
        df = df.reset_index()
        df.pop('index')

        return df

    def df_transactions(self):
        self.get_histo()



        date = []
        dates = []
        value_send = []
        value_received = []
        token_send = []
        token_received = []

        for x in self.histo:
            # index sont les élements des x
            for index in range(len(x)):
                # recuperation dans le dictionnaire json de historique_portefeuille des tokens envoyés et recus avec leur date de
                # transactions
                if x[index]['from'] == self.adresse:

                    token_send.append(x[index]['tokenSymbol'])
                    value_send.append(float(x[index]['value']) / 10 ** float(x[index]['tokenDecimal']))
                    date.append(datetime.fromtimestamp(float(x[index]['timeStamp'])))
                else:
                    dates.append(datetime.fromtimestamp(float(x[index]['timeStamp'])))
                    value_received.append(float(x[index]['value']) / 10 ** float(x[index]['tokenDecimal']))
                    token_received.append(x[index]['tokenSymbol'])
        # création du dataframe de l'historique des transactions
        # création du data frame de l'historique de transactions
        df_send = pd.DataFrame({'date': date, 'token_send': token_send, 'value_send': value_send})
        df_receive = pd.DataFrame({'date': dates, 'value_received': value_received, 'token_received': token_received})

        transactions = pd.merge(df_send, df_receive, on='date', how='outer')
        transactions = transactions.set_index('date').sort_values(by=['date'], ascending=False)
        transactions['token_send'] = transactions['token_send'].fillna('CEX/pool')
        transactions['token_received'] = transactions['token_received'].fillna('CEX/pool')
        transactions['value_send'] = transactions['value_send'].fillna(0)
        transactions['value_received'] = transactions['value_received'].fillna(0)

        transactions.to_sql('Transactions_Adresse', con = self.conn, if_exists = 'replace')

        self.conn.commit()



        return transactions



    def get_balance(self):
        df = self.get_histo()
        balance = []
        eth = 0
        for key, value in self.blockchain.items():
            for index in range(len(df)):
                if df['blockchains'][index] == key:

                    url2 = 'https://{}/api?module=account&action=tokenbalance&contractaddress={}' \
                           '&address={}&tag=latest&apikey={}' \
                        .format(key, df['address'][index], self.adresse, value)

                    response2 = self.session.get(url2)

                    if json.loads(response2.text)['result'] == 'Max rate limit reached':
                        balance.append('0')
                    elif json.loads(response2.text)['result'] == 'Max rate limit reached, rate limit of 5/1sec applied':
                        balance.append('0')
                    elif json.loads(response2.text)['result'] == '':
                        balance.append('0')

                    else:
                        balance.append(json.loads(response2.text)['result'])

        for key, value in self.blockchain.items():
            url3 = 'https://{}/api?module=account&action=balance&address={}&tag=latest&apikey={}' \
                .format(key, self.adresse, value)
            response3 = self.session.get(url3)

            if key == 'api.arbiscan.io':
                balance.append('0')
                eth += float((json.loads(response3.text)['result']))
            elif json.loads(response3.text)['result'] == '':
                balance.append('0')
            else:
                balance.append(json.loads(response3.text)['result'])

        for index, value in enumerate(balance):
            balance[index] = float(value) / (10 ** (df['decimal'][index]))

        balance[-6] += float(eth) / (10 ** 18)
        df['balance'] = balance

        df = df[df['balance'] > 0]

        return df

    def get_price(self):

        df = self.get_balance()



        df['tokens'] = df['tokens'].apply(lambda x: x.upper())

        pp = []

        sql_query = pd.read_sql_query(''' SELECT * FROM prices ''',
                                        self.conn)



        dj = pd.DataFrame(sql_query, columns=['symbol', 'quote.USD.price'])
        dj = dj.set_index('symbol')

        dj.columns = ['prices']


        df = df.merge( dj, how='inner', left_on='tokens', right_on='symbol')
        df = df.drop_duplicates('balance')

        # création de la valeur en USD des tokens que l'on détient puis grâce à cette valeur, de la part du token dans le
        # portefeuille

        df['USD_value'] = df['balance'] * df['prices']

        for x in df['USD_value']:
            y = x / sum(df['USD_value']) * 100
            pp.append(y)

        df['% du portefeuille'] = pp
        df = df[df["% du portefeuille"] > 1.1]

        df = df.set_index('blockchains').sort_values(by=['blockchains'], ascending=False)
        df = df[['tokens', 'USD_value','balance','prices']]

        df.to_sql('Wallet', con=self.conn, if_exists = 'replace')

        self.conn.commit()

        self.curr.close()
        self.conn.close()
        return df



    def camembert(self):
        df = self.get_price()


        sizes = df["% du portefeuille"]
        fig, ax1 = plt.subplots()
        ax1.pie(sizes, labels=df["tokens"], autopct='%1.1f%%')
        ax1.axis('equal')









        total = [self.today, sum(df['USD_value'])]
        print(total)

marwane= Portefeuille('0xde23d846b7247c72944722e7d0a59258c8595a29')
marwane.get_price()

