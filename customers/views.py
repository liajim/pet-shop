from annoying.decorators import render_to
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .serializers import CustomerSerializer, InternalCustomerSerializer
from .models import Customer


class InternalCustomerView(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           GenericViewSet):
    """Viewset for authenticated customer"""
    http_method_names = ['get', 'patch']
    serializer_class = InternalCustomerSerializer
    queryset = Customer.objects.all()


class CustomerView(mixins.CreateModelMixin,
                   GenericViewSet):
    """Viewset for customer signup"""
    http_method_names = ['post']
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = []


@render_to('signup.html')
def signup(request):
    return {}