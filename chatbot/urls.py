from django.urls import path

from . import blenderbot

urlpatterns = [
    path('blenderbot', blenderbot.index, name='index'),
]
