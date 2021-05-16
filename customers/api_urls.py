from django.urls import path, include
from rest_framework import routers
from . import views

customerRouter = routers.DefaultRouter()
customerRouter.register(r'customers', views.CustomerView, 'customer')

urlpatterns = [
    path('', include(customerRouter.urls)),
]