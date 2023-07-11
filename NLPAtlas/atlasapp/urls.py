from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('update_collections', views.update_collections, name='update_collections'),
]