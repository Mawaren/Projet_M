import base64
import io
import urllib

from matplotlib import pyplot as plt
from matplotlib.pyplot import savefig
import plotly.graph_objects as go

def tableau(df):

    df = df.style.bar(subset=['% du portefeuille'], color='#d65f5f').set_properties(**{'border': '1.3px solid green',
                                                                                  'color': 'magenta'})

    return df


def tableau2(df):

    df = df.style.bar(subset=['PdP'], color='#d65f5f').set_properties(**{'border': '1.3px solid green',
                                                                                  'color': 'green'})

    return df


class Creation_graph:
    def __init__(self, df):
        self.buf = io.BytesIO()
        self.df = df

    def plot(self):
        self.df.plot.bar(rot=0)
        savefig(self.buf, format='png')
        self.buf.seek(0)
        string = base64.b64encode(self.buf.read())
        uri2 = 'data:image/png;base64,' + urllib.parse.quote(string)

        return uri2

    def pie(self):
        labels = self.df.iloc[:,0]
        values = self.df.iloc[:,4]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

        return fig


