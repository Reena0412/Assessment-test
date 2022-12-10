from django.urls import path
from . import views

urlpatterns = [
    path('', views.accept_csv, name='accept_csv')
]
