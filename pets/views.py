from annoying.decorators import render_to
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from utils.database_functions import query_pets_by_args
from .models import Pet
from .serializers import PetSerializer


class PetView(mixins.ListModelMixin,
              GenericViewSet):
    """Viewset for pet list public and for authenticated users"""
    http_method_names = ['get']
    serializer_class = PetSerializer
    queryset = Pet.objects.all()
    permission_classes = []

    def list(self, request, **kwargs):
        """List of pets"""
        pets = query_pets_by_args(**request.query_params)
        kwargs['request'] = request
        serializer = PetSerializer(pets['items'], many=True, context=kwargs)
        result = dict()
        result['data'] = serializer.data
        result['draw'] = pets['draw']
        result['recordsTotal'] = pets['total']
        result['recordsFiltered'] = pets['count']
        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)


@render_to('index.html')
def index(request):
    return {'current_year': 2021}
