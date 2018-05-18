from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/register_user', views.register),
    path('/login', views.login),
    path('/'
]