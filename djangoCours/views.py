
from django.shortcuts import render


from blog.models import Wallets
from blog.travail.portefeuille import Portefeuille



def index(request):


    if request.GET.keys():
        user = request.user
        users = user.id
        instance = Wallets.objects.filter(user_id=user)
        instance.delete()
        for adresses in request.GET.values():
                a = adresses

        if not a:
            return render(request, 'index.html')

        elif a[0] == '0' and a[1] == 'x':

            marwane = Portefeuille(a)


            df = marwane.df_transactions()
            dt = marwane.get_price()


            i = 0
            while i < len(dt):
                new_obj = Wallets.objects.create(user = user, blockchains='eth', tokens=dt['tokens'][i], USD_value = dt['USD_value'][i], balance=dt['balance'][i], prices = dt['prices'][i])
                new_obj.save()
                i+=1




        if df.empty == False:

                context = {
                    'df': df.to_html(),
                    'dt':dt.to_html()
                }

                return render(request, 'index-blog.html', context=context)
        else:
            return render(request, 'index.html')
    return render(request, 'index.html')

