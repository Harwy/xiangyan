from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.itemCreate, name='create'),
    path('buy/', views.itemBuy, name='buy'),
    path('sellList/', views.itemSellList, name='sellList'),
    path('download/', views.download_file, name='download'),  # 下载导入txt api
    path('mission-add/', views.itemNowAdd, name='mission-add'),  # api
    path('insert/', views.itemInsert, name='insert'),  # 导入操作，未完善，慎用
    path('mission/', views.mission, name='mission'),
    path('loglist/', views.loglist, name='loglist'),
    path('log/<int:pk>/', views.log, name='log'),
]
