from django.urls import path

from . import dialogpt

urlpatterns = [
    path('dialogpt', dialogpt.index, name='index'),
]