import plotly.graph_objects as go
import plotly.express as px


class Tableur:

    def __init__(self, df, valeur, title=None, xaxis_title=None, yaxis_title=None):
        self.df = df
        self.valeur = valeur
        self.value = []
        self.title = title
        self.xaxis_title = xaxis_title
        self.yaxis_title = yaxis_title

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
        fig.update_layout(
            title=self.title,
            xaxis_title=self.xaxis_title,
            yaxis_title=self.yaxis_title,
        )
        return fig


class Creation_graph:

    def __init__(self, df, label, value, title=None, xaxis_title=None, yaxis_title=None):
        self.df = df
        self.label = label
        self.value = value
        self.title = title
        self.xaxis_title = xaxis_title
        self.yaxis_title = yaxis_title

    def pie(self):
        fig = go.Figure(data=[go.Pie(labels=self.label, values=self.value)])
        fig.update_layout(
            title=self.title,
            xaxis_title=self.xaxis_title,
            yaxis_title=self.yaxis_title,
        )
        return fig

    def t_series(self):
        fig = px.scatter(self.df, x=self.label, y=self.value)
        fig.update_layout(
            title=self.title,
            xaxis_title=self.xaxis_title,
            yaxis_title=self.yaxis_title,
        )
        return fig

    def bubbles(self, value2, value3):
        fig = px.scatter(self.df, x=value2, y=value3,
                         size=self.value, color=self.label,
                         hover_name=self.label, log_x=True, size_max=90)
        fig.update_layout(
            title=self.title,
            xaxis_title=self.xaxis_title,
            yaxis_title=self.yaxis_title,
        )

        return fig

    def histogramme(self):
        fig = px.histogram(self.df, x=self.label, y=self.value, title=self.title)

        fig.update_layout(
            title=self.title,
            xaxis_title=self.xaxis_title,
            yaxis_title=self.yaxis_title,

        )

        return fig

    def treemap(self, color_continuous_scale='RdBu'):
        self.color = color_continuous_scale

        fig = px.treemap(self.df, path=self.label, values=self.value, color=self.value,
                         color_continuous_scale=self.color)

        fig.update_layout(
            title=self.title,
            xaxis_title=self.xaxis_title,
            yaxis_title=self.yaxis_title,

        )
        return fig
