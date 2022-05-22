
from django.shortcuts import render, redirect
import matplotlib


from blog.models import Wallets
from blog.travail.get_prices import get_prices

from blog.travail.portefeuille import Portefeuille
from blog.travail.tableau import tableau, Creation_graph
from djangoCours.Cmc import transform_data

matplotlib.use('Agg')

def index(request):
    dj = transform_data()

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
                                                 PdP = dt['% du portefeuille'][i])
                new_obj.save()


        if df.empty == False:

            total = int(sum(dt['USD_value']))

            graph1 = Creation_graph(dt)
            uri = graph1.pie()

            dt = tableau(dt)

            context = {
                "a":a,
                'total': total,
                'df': df.to_html(),
                'dt': dt.to_html(),
                'imgdata': uri.to_html(),
            }

            return render(request, 'index-blog.html', context=context)
        else:
            return render(request, 'index.html', context= context1)
    return render(request, 'index.html', context= context1)

def prix(request):
    get_prices()

    return redirect('index')