from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('file', views.result, name='result'),
    path('download', views.download, name='download'),
]