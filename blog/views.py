from django.shortcuts import redirect
from blog.models import Wallets
from blog.models import historiques


def histo(request):
    user = request.user
    instance = historiques.objects.filter(user_id=user)
    instance.delete()

    instance = Wallets.objects.values()
    for dico in instance:

        if dico['user_id'] != user.id:
            pass

        else:
            new_obj = historiques.objects.create(user=user, blockchains=dico['blockchains'], tokens=dico['tokens'],
                                                 USD_value=dico['USD_value'], balance=dico['balance'],
                                                 prices=dico['prices'], PdP=dico['PdP'])
            new_obj.save()

    return redirect('index')
