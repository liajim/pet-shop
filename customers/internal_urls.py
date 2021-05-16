from django.urls import path, include
from rest_framework import routers
from . import views

internalCustomerRouter = routers.DefaultRouter()
internalCustomerRouter.register(r'customers', views.InternalCustomerView, 'customer')


urlpatterns = [
    path('', include(internalCustomerRouter.urls)),
]