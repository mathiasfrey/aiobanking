from django.db import models
from django.db.models.fields import IntegerField

# Create your models here.

class CurrentAccount(models.Model):
    account = models.CharField(max_length=32, unique=True)
    balance = IntegerField()

    def __str__(self):
        return self.account