from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.itemCreate, name='create'),
    path('buy/', views.itemBuy, name='buy'),
    path('sellList/', views.itemSellList, name='sellList'),
    path('download/list/', views.downloadList, name='download-list'),
    path('download/<int:pk>/', views.downloadFile, name='download'),  # 下载导入txt api
    path('mission-add/', views.itemNowAdd, name='mission-add'),  # api
    path('mission/', views.mission, name='mission'),
    path('loglist/', views.loglist, name='loglist'),
    path('log/<int:pk>/', views.log, name='log'),
    path('file/upload/', views.fileUpload, name='upload'),  # 上传文件api
    path('mission/delete/', views.missionDelete, name='delete'),
]
