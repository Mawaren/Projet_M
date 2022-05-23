from django.contrib import admin
from accounts.models import Trader
from blog.models import Wallets, historiques

# Enregistrement des modèles ici
admin.site.register(Trader)
admin.site.register(Wallets)
admin.site.register(historiques)
