from rest_framework import serializers
from .models import Pet


class PetSerializer(serializers.ModelSerializer):
    """Serializer for List of Pets"""
    photo_url = serializers.SerializerMethodField()
    breed = serializers.CharField(source='breed.name')
    specie = serializers.CharField(source='breed.specie.name')
    is_hearted = serializers.SerializerMethodField()

    def get_photo_url(self, pet):
        request = self.context.get('request')
        try:
            photo_url = pet.image.url
        except ValueError as e:
            photo_url = pet.image_url
        return request.build_absolute_uri(photo_url)

    def get_is_hearted(self, obj):
        """Verify if the pet was hearted by current customer"""
        request = self.context['request']
        if not hasattr(request.user, 'customer') or not request.user.customer:
            return False
        customer_hearted_pets = request.user.customer.hearted_pets.filter(id=obj.id)
        return customer_hearted_pets.exists()

    class Meta:
        model = Pet
        fields = ('id', 'photo_url', 'name', 'specie', 'breed', 'sex', 'age', 'for_adoption', 'price', 'is_hearted')
