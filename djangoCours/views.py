from django.shortcuts import render, redirect
from blog.models import Wallets
from blog.travail.get_prices import get_prices
from blog.travail.portefeuille import Portefeuille
from blog.travail.tableau import Tableur, Creation_graph
from djangoCours.Cmc import import_data, transform


def index(request):
    valeur = ["Tokens", "Price", "Market_cap"]
    config = {'displayModeBar': False}

    dj = import_data()
    table = Tableur(dj, valeur,title='Prix et Capitalisations des Cryptomonnaies')
    graph1 = table.tableau()


    #graph2 = Creation_graph(dj[:50], dj[:50]['tokens'], dj[:50]['Market_cap'], title='Top 30 capitalisations', xaxis_title='Tokens'
                            #, yaxis_title='Market_cap')
    #graph2 = graph2.histogramme()

    graph = Creation_graph(dj[:10], ['tokens'], dj[:10]['Market_cap'], title='Top 10 capitalisations')
    graph = graph.treemap()

    graph3 = Creation_graph(dj[10:100], ['tokens'], dj[10:100]['Market_cap'], title='Top 100 capitalisations '
                                                                                    'sans les 10 premiers')
    graph3 = graph3.treemap()

    context1 = {
        'graph1': graph1.to_html(config,default_width = '100%',default_height='25em'),
        #'graph2': graph2.to_html(config,default_width = '100%',default_height='20em'),
        'graph': graph.to_html(config, default_width = '100%',default_height='18em'),
        'graph3': graph3.to_html(config, default_width='100%', default_height='18em')
    }

    if request.GET.keys():
        user = request.user

        instance = Wallets.objects.filter(user_id=user)
        instance.delete()

        for adresses in request.GET.values():
            a = adresses
        if not a:

            return render(request, 'index.html', context=context1)

        elif a[0] == '0' and a[1] == 'x':

            marwane = Portefeuille(a)

            df, dt = marwane.get_price()

            for i in range(len(dt)):
                new_obj = Wallets.objects.create(user=user, blockchains=a, tokens=dt['tokens'][i],
                                                 USD_value=dt['USD_value'][i], balance=dt['balance'][i],
                                                 prices=dt['prices'][i],
                                                 PdP=dt['PdP'][i])
                new_obj.save()

        if not df.empty:

            total = int(sum(dt['USD_value']))

            graph1 = Creation_graph(dt, dt['tokens'], dt['PdP'], title='Composition du Portefeuille')
            uri = graph1.pie()

            valeur3 = ["date", "token_send", "value_send", 'value_received', 'token_received']
            table = Tableur(df, valeur3)
            df_img = table.tableau()

            valeur2 = ["tokens", "USD_value", "prices", 'balance', 'PdP']
            table2 = Tableur(dt, valeur2)
            dt_img = table2.tableau()

            transac = transform(df)

            ts = Creation_graph(df, df['date'], transac, title='Activité du portefeuille', xaxis_title='Date',
                                yaxis_title= "Type")
            uri2 = ts.t_series()

            context = {
                "a": a,
                'total': total,
                'df': df_img.to_html(config),
                'dt': dt_img.to_html(config),
                'imgdata': uri.to_html(config),
                'imgdata2': uri2.to_html(config)
            }

            return render(request, 'index-blog.html', context=context)
        else:
            return render(request, 'index.html', context=context1)
    return render(request, 'index.html', context=context1)


def prix(request):
    get_prices()

    return redirect('index')
