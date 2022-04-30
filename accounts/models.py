from django.db import models
from django.contrib.auth.models import AbstractUser

from djangoCours.settings import AUTH_USER_MODEL


class Trader(AbstractUser):
    pass

