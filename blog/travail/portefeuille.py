
import pandas as pd
from requests import Session
import json

from datetime import datetime
import sqlite3


import time

'''Classe Portefeuille.
on définit dans le init , la connexion au serveur sql, un dictionnaire contenant les différentes clefs API pour les 
différentes blockchains.
Une variable today pour obtenir la date d'aujourd'hui
Une liste contenant les symboles des layers
Une liste contenant les noms des layers'''


class Portefeuille:
    def __init__(self, adresse):
        self.conn = sqlite3.connect('db.sqlite3')
        self.curr = self.conn.cursor()

        self.session = Session()
        self.adresse = adresse
        self.blockchain = {'api.etherscan.com': 'MMW7FUW6EZ5YGSSINYR7NMCTDXV69XKKPF',
                           'api.ftmscan.com': '46NU3E7MB8EUBMWACBGT3B3KBK4ZS2GJFC',
                           'api.polygonscan.com': 'RB4ACXDV6HPNFUF38G8QF65BIIJXMDWMWF',
                           'api.bscscan.com': 'MPSX84G1YFA87FAD8N4QVAB1GFE6DU8SM5',
                           'api.arbiscan.io': 'VC2I8ZW7QH4HCX39WWFEF5P2GRH3BQ2C7H',
                           'api.snowtrace.io': 'IM4CBYMSZPP2YD8NWTSZ3QRP14SGXTP4K7',
                           'blockscout.com/xdai/mainnet': ''}

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
                .format(x, self.adresse, str(0), str(self.today), y)

            response1 = self.session.get(url1)


            if response1.ok == True:
                historique = (json.loads(response1.text)['result'])

                self.histo.append((json.loads(response1.text)['result']))

                for index in range(len(historique)):
                    if '.io' in historique[index]['tokenName']:
                        pass
                    else:
                        token.append(historique[index]['tokenSymbol'])
                        address.append(historique[index]['contractAddress'])
                        token_name.append(historique[index]['tokenName'])
                        blockchains.append(x)
                        if not historique[index]['tokenDecimal']:
                            decimal.append(0)
                        else:
                            decimal.append(float(historique[index]['tokenDecimal']))

            #else:
               # continue à vérifier

        # nettoyage des données récupérée
        token = list(map(lambda x: x.lower(), token))

        dl = pd.DataFrame({'blockchains': blockchains, 'tokens': token, 'address': address, 'decimal': decimal,
                           'token_name': token_name})
        dl = dl.drop_duplicates()
        dt = pd.DataFrame({'blockchains': self.layer, 'tokens': self.layer, 'address': ad, 'decimal': dec,
                           'token_name': self.layer_name})

        df = pd.concat([dl, dt])

        df = df.reset_index()
        df.pop('index')

        return df

    def df_transactions(self):
        hist = self.get_histo()

        date = []
        dates = []
        value_send = []
        value_received = []
        token_send = []
        token_received = []
        for x in self.histo:
            # index sont les élements des x
            for index in range(len(x)):
                a = x[index].keys()
                if 'value' in a:
                # recuperation dans le dictionnaire json de historique_portefeuille des tokens envoyés et recus avec leur date de
                # transactions

                    if x[index]['from'] == self.adresse:

                        token_send.append(x[index]['tokenSymbol'])
                        date.append(datetime.fromtimestamp(float(x[index]['timeStamp'])))
                        if not x[index]['tokenDecimal']:
                            value_send.append(float(x[index]['value']))

                        else:
                            value_send.append(float(x[index]['value']) / 10 ** float(x[index]['tokenDecimal']))

                    else:
                        dates.append(datetime.fromtimestamp(float(x[index]['timeStamp'])))
                        token_received.append(x[index]['tokenSymbol'])

                        if not x[index]['tokenDecimal']:
                            value_received.append(float(x[index]['value']))
                        else:
                            value_received.append(float(x[index]['value']) / 10 ** float(x[index]['tokenDecimal']))

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

        return transactions, hist


# get_balance récupère le nombre de tokens possédés pour l'adresse wallet.
# Un meme token peut etre présent sur plusieurs blockchain et une adresse sur une blockchain ne vise pas le même objet
# Il faut donc itérer sur chcaune des apis, pour d'abord récuperer la balance du token de gouvernance ( ex: eth)
# Puis pour récuperer la balance de chacun des tokens sur cette blockchain, on fait une deuxième boucle dans le dataframe
# et a chaque fois que la clef du dictionnaire match avec la blockchain on cherche la balance.
    def get_balance(self):

        transactions, df = self.df_transactions()

        balance = []
        eth = 0

        for key, value in self.blockchain.items():
            counter = 0
            start = datetime.now()
            for index in range(len(df)):

                counter += 1
                end = datetime.now()
                s = (end-start).seconds
                if counter == 5 and s < 1:
                    time.sleep(0.5)
                    counter = 0
                    start = datetime.now()

                if df['blockchains'][index] == key:
                    url2 = 'https://{}/api?module=account&action=tokenbalance&contractaddress={}' \
                           '&address={}&tag=latest&apikey={}' \
                        .format(key, df['address'][index], self.adresse, value)

                    response2 = self.session.get(url2)
                    if json.loads(response2.text)["message"] == "OK":

                        balance.append(json.loads(response2.text)['result'])
                    else:
                        balance.append('0')


        for key, value in self.blockchain.items():

            url3 = 'https://{}/api?module=account&action=balance&address={}&tag=latest&apikey={}' \
                .format(key, self.adresse, value)
            response3 = self.session.get(url3)

            if json.loads(response3.text)["message"] == "OK":
                if key == 'api.arbiscan.io':
                    balance.append('0')
                    eth += float((json.loads(response3.text)['result']))
                else:
                    balance.append(json.loads(response3.text)['result'])
            else:
                balance.append('0')


        for index, value in enumerate(balance):
            balance[index] = float(value) / (10 ** (df['decimal'][index]))


        balance[-6] += float(eth) / (10 ** 18)
        df['balance'] = balance

        df = df[df['balance'] > 0]

        return transactions, df

    def get_price(self):

        transactions, df = self.get_balance()
        tokens2 = {}

        for index, row in df.iterrows():

            if df['tokens'][index] not in tokens2.keys():
                tokens2[df['tokens'][index]] = df['balance'][index]
            else:

                tokens2[df['tokens'][index]] += df['balance'][index]
                df['balance'][index] = tokens2[df['tokens'][index]]


        df['tokens'] = df['tokens'].apply(lambda x: x.upper())

        pp = []

        sql_query = pd.read_sql_query(''' SELECT * FROM prices ''',
                                        self.conn)



        dj = pd.DataFrame(sql_query, columns=['symbol', 'quote.USD.price'])
        dj = dj.set_index('symbol')

        dj.columns = ['prices']


        df = df.merge( dj, how='inner', left_on='tokens', right_on='symbol')



        # création de la valeur en USD des tokens que l'on détient puis grâce à cette valeur, de la part du token dans le
        # portefeuille

        df['USD_value'] = df['balance'] * df['prices']

        for x in df['USD_value']:
            y = x / sum(df['USD_value']) * 100
            pp.append(y)


        df['% du portefeuille'] = pp


        #df = df.set_index('blockchains').sort_values(by=['blockchains'], ascending=False)
        df = df[['tokens', 'USD_value','prices','balance','% du portefeuille']]



        self.curr.close()
        self.conn.close()
        df.drop_duplicates(subset='tokens', keep='last', inplace=True)
        df = df[df["% du portefeuille"] > 1.1]
        df = df.reset_index()
        df.pop('index')

        return transactions, df



marwane= Portefeuille('0xde23d846b7247c72944722e7d0a59258c8595a29')
marwane.get_price()
