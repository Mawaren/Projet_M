import base64
import io
import urllib

import pandas as pd
from django.shortcuts import render
from matplotlib import pyplot as plt
from blog.models import historiques


def historique(request):
    user = request.user

    qs = historiques.objects.select_related().filter(user_id=user)
    q = qs.values('USD_value', 'balance', 'prices', 'tokens','PdP','blockchains')
    dt = pd.DataFrame.from_records(q)
    a  = dt['blockchains'][0]

    dt.pop('blockchains')

    total = int(sum(dt['USD_value']))
    sizes = dt['PdP']
    fig, ax1 = plt.subplots()
    ax1.pie(sizes, labels=dt["tokens"], autopct='%1.1f%%')
    ax1.axis('equal')

    plt.gcf()
    plt.close()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())

    uri = 'data:image/png;base64,' + urllib.parse.quote(string)

    context = {
        'a': a,
        'dt': dt.to_html(),
        'imgdata': uri,
        'total':total,
    }
    return render(request, 'historique.html', context=context)





