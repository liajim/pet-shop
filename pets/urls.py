from django.urls import path

from pets.views import index

urlpatterns = [
    path('', index),
]
