import pandas as pd
from django.shortcuts import render, redirect

from blog.models import historiques
from blog.travail.tableau import Tableur, Creation_graph


def historique(request):
    user = request.user
    qs = historiques.objects.select_related().filter(user_id=user)
    config = {'displayModeBar': False}

    q = qs.values('tokens', 'prices', 'USD_value', 'balance', 'PdP', 'blockchains')

    if q.exists():
        dt = pd.DataFrame.from_records(q)
        a = dt['blockchains'][0]

        dt.pop('blockchains')
        total = int(sum(dt['USD_value']))

        graph1 = Creation_graph(dt, dt['tokens'], dt['PdP'])
        graph2 = Creation_graph(dt, dt['tokens'], dt['PdP'], title='Part des différents tokens dans le Portefeuille',
                                xaxis_title='Prix', yaxis_title='Valeur du token dans le Portefeuille (USD)')
        uri = graph1.pie()
        uri2 = graph2.bubbles(dt['prices'],dt['USD_value'])
        df = dt
        df = df.set_index('tokens')
        df.pop('prices')
        df.pop('PdP')

        valeur = ["tokens", "prices", "USD_value", 'balance', 'PdP']
        table = Tableur(dt, valeur)
        dt = table.tableau()


        context = {
            'a': a,
            'dt': dt.to_html(config),
            'imgdata': uri.to_html(config),
            'total': total,
            'imgdata2':uri2.to_html(config)
        }
        return render(request, 'historique.html', context=context)
    else:
        return redirect('index')
