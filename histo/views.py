import pandas as pd
from django.shortcuts import render, redirect

from blog.models import historiques
from blog.travail.tableau import Tableur, Creation_graph


def historique(request):
    user = request.user
    qs = historiques.objects.select_related().filter(user_id=user)

    q = qs.values('tokens', 'prices', 'USD_value', 'balance', 'PdP', 'blockchains')

    if q.exists():
        dt = pd.DataFrame.from_records(q)
        a = dt['blockchains'][0]

        dt.pop('blockchains')
        total = int(sum(dt['USD_value']))

        graph1 = Creation_graph(dt, dt['tokens'], dt['PdP'])
        uri = graph1.pie()
        uri2 = graph1.bubbles(dt['prices'],dt['USD_value'])
        df = dt
        df = df.set_index('tokens')
        df.pop('prices')
        df.pop('PdP')

        valeur = ["tokens", "prices", "USD_value", 'balance', 'PdP']
        table = Tableur(dt, valeur)
        dt = table.tableau()


        context = {
            'a': a,
            'dt': dt.to_html(),
            'imgdata': uri.to_html(),
            'total': total,
            'imgdata2':uri2.to_html()
        }
        return render(request, 'historique.html', context=context)
    else:
        return redirect('index')
