
import pandas as pd
from django.shortcuts import render, redirect

from blog.models import historiques
from blog.travail.tableau import tableau2, Creation_graph


def historique(request):

    user = request.user
    qs = historiques.objects.select_related().filter(user_id=user)

    q = qs.values('tokens', 'prices', 'USD_value', 'balance','PdP','blockchains')

    if q.exists():
        dt = pd.DataFrame.from_records(q)
        a = dt['blockchains'][0]

        dt.pop('blockchains')
        total = int(sum(dt['USD_value']))

        graph1 = Creation_graph(dt)
        uri = graph1.pie()

        df = dt
        df = df.set_index('tokens')
        df.pop('prices')
        df.pop('PdP')

        graph2 = Creation_graph(df)
        uri2 = graph2.plot()

        dt = tableau2(dt)

        context = {
            'a': a,
            'dt': dt.to_html(),
            'imgdata': uri.to_html(),
            'total':total,
            'imgdata2':uri2
        }
        return render(request, 'historique.html', context=context)
    else:
        return redirect('index')






