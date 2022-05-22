import numpy as np
from django.shortcuts import render, redirect



from blog.models import Wallets
from blog.travail.get_prices import get_prices

from blog.travail.portefeuille import Portefeuille
from blog.travail.tableau import Tableur, Creation_graph
from djangoCours.Cmc import import_data, ln


def index(request):
    valeur = ["Symbol", "Price", "Market_cap"]
    dj = import_data()
    table = Tableur(dj,valeur)
    dj = table.tableau()
    context1 = {
        'dj': dj.to_html()
    }


    if request.GET.keys():
        user = request.user

        instance = Wallets.objects.filter(user_id=user)
        instance.delete()

        for adresses in request.GET.values():
                a = adresses
        if not a:

            return render(request, 'index.html', context = context1)

        elif a[0] == '0' and a[1] == 'x':

            marwane = Portefeuille(a)

            df, dt = marwane.get_price()


            for i in range(len(dt)):
                new_obj = Wallets.objects.create(user = user, blockchains=a, tokens=dt['tokens'][i], USD_value = dt['USD_value'][i], balance=dt['balance'][i], prices = dt['prices'][i],
                                                 PdP = dt['PdP'][i])
                new_obj.save()


        if df.empty == False:

            total = int(sum(dt['USD_value']))

            graph1 = Creation_graph(dt['tokens'], dt['PdP'])
            uri = graph1.pie()


            valeur3 = ["date", "token_send", "value_send", 'value_received', 'token_received']
            table = Tableur(df, valeur3)
            df_img = table.tableau()

            valeur2 = ["tokens", "USD_value", "prices", 'balance', 'PdP']
            table2 = Tableur(dt, valeur2)
            dt_img = table2.tableau()

            df['value_send'] = df['value_send'].apply(ln)
            ts = Creation_graph(df,'value_send')
            uri2 = ts.t_series()

            context = {
                "a":a,
                'total': total,
                'df': df_img.to_html(),
                'dt': dt_img.to_html(),
                'imgdata': uri.to_html(),
                'imgdata2': uri2.to_html()
            }

            return render(request, 'index-blog.html', context=context)
        else:
            return render(request, 'index.html', context= context1)
    return render(request, 'index.html', context= context1)

def prix(request):
    get_prices()

    return redirect('index')