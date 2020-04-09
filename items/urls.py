from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.itemCreate, name='create'),
    path('buy/', views.itemBuy, name='buy'),
    path('sellList/', views.itemSellList, name='sellList'),
    path('createTXT/', views.itemCreateTXT, name='createTXT'),
]