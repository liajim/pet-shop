from django.urls import path, include
from rest_framework import routers
from . import views

petRouter = routers.DefaultRouter()
petRouter.register(r'pets', views.PetView, 'pet')


urlpatterns = [
    path('', include(petRouter.urls)),
]
