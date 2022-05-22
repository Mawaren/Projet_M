
import io

import plotly.graph_objects as go
import plotly.express as px


class Tableur():

    def __init__(self, df, valeur):
        self.df = df
        self.valeur = valeur
        self.value = []

    def tableau(self):

        for label, content in self.df.items():
            self.value.append(self.df[label])

        fig = go.Figure(data=[go.Table(
            header=dict(
                values=self.valeur,
                font=dict(size=10),
                align="left"
            ),
            cells=dict(
                values=self.value,
                align="left"))
        ])

        return fig



class Creation_graph:
    def __init__(self, label, value):
        self.buf = io.BytesIO()

        self.label = label
        self.value = value



    def pie(self):

        fig = go.Figure(data=[go.Pie(labels=self.label, values=self.value)])

        return fig

    def t_series(self):

        fig = px.line(self.label, x='date', y=self.value)
        return fig


