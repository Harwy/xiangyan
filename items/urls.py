from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.itemCreate, name='create'),
    path('buy/', views.itemBuy, name='buy'),
    path('sellList/', views.itemSellList, name='sellList'),
    path('download/', views.download_file, name='download'),
    path('mission-add/', views.itemNowAdd, name='mission'),
    path('insert/', views.itemInsert, name='insert'),
    path('mission/', views.mission, name='mission'),
]
