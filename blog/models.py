from djangoCours.settings import AUTH_USER_MODEL
from django.db import models





class Wallets(models.Model):

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    blockchains = models.TextField()
    tokens = models.TextField()
    USD_value = models.FloatField()
    balance = models.FloatField()
    prices = models.FloatField()


    def __str__(self):
        return self.user.username

class historiques(models.Model):

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    blockchains = models.TextField()
    tokens = models.TextField()
    USD_value = models.FloatField()
    balance = models.FloatField()
    prices = models.FloatField()

    def __str__(self):
        return self.user.username







