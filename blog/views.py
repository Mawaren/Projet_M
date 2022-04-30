

from django.shortcuts import render

from blog.models import Wallets
from blog.models import historiques



def histo(request):
    user = request.user


    instance = Wallets.objects.values()
    for dico in instance:

        if dico['user_id'] != user.id:
            pass

        else:
            print(dico)
            new_obj = historiques.objects.create(user=user, blockchains='eth', tokens=dico['tokens'],
                                             USD_value=dico['USD_value'], balance=dico['balance'],
                                             prices=dico['prices'])
            new_obj.save()






    return render(request, 'index.html')





# Create your views here.`



