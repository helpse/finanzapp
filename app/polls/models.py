from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Account(models.Model):
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

class Cashier(models.Model):
    account = models.ForeignKey(Account,db_index=True, on_delete=models.CASCADE)

class Registry(models.Model):
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)

class Transaction(models.Model):
