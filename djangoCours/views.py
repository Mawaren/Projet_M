import base64
import io
import urllib


from django.shortcuts import render
import matplotlib
from matplotlib import pyplot as plt

from blog.models import Wallets
from blog.travail.portefeuille import Portefeuille
from djangoCours.Cmc import import_data

matplotlib.use('Agg')




def index(request):
    dj = import_data()

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
            return render(request, 'index.html')

        elif a[0] == '0' and a[1] == 'x':

            marwane = Portefeuille(a)

            df, dt = marwane.get_price()
            i = 0

            while i < len(dt):
                new_obj = Wallets.objects.create(user = user, blockchains=a, tokens=dt['tokens'][i], USD_value = dt['USD_value'][i], balance=dt['balance'][i], prices = dt['prices'][i],
                                                 PdP = dt['% du portefeuille'][i])
                new_obj.save()
                i += 1

        if df.empty == False:

            total = int(sum(dt['USD_value']))

            sizes = dt['% du portefeuille']

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
                "a":a,
                'total': total,
                'df': df.to_html(),
                'dt': dt.to_html(),
                'imgdata': uri,
            }

            return render(request, 'index-blog.html', context=context)
        else:
            return render(request, 'index.html', context= context1)
    return render(request, 'index.html', context= context1)

