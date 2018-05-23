from django.urls import path
from django.conf.urls import include, url
from . import views
from app.polls.views import *

urlpatterns = [
    path('', views.index, name='index'),
    # url(r'^/app/get_accounts', get_accounts),
    path('login', views.login),
    # path('/register_payment', views.register_payment),
    # path('get_accounts', views.get_accounts),
    # path('/get_')
]