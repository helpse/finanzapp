from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

class Cashier(models.Model):
    account = models.ForeignKey(Account,db_index=True, on_delete=models.CASCADE)

class Registry(models.Model):
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)

class Transaction(models.Model):
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    registry = models.ForeignKey(Registry, db_index=True, on_delete=models.CASCADE)
    payment = models.FloatField(default=0)
    accounts = models.ManyToManyField(Account)

class TransactionDetail(models.Model):
    transaction = models.ForeignKey(Transaction, db_index=True, on_delete=models.CASCADE)


