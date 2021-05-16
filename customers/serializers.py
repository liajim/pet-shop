from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pets.models import Pet
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer"""
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Customer
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'address', 'phone_number', 'password')

    @transaction.atomic()
    def create(self, validated_data):
        """Set Password after create a new user"""
        password = validated_data.pop('password')
        customer = super().create(validated_data)
        customer.set_password(password)
        customer.save()
        return customer


class InternalCustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer"""
    pet_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Customer
        fields = ('pet_id',)

    @transaction.atomic()
    def update(self, instance, validated_data):
        """add or remove pets from hearted"""
        pet_id = validated_data['pet_id']
        pets = instance.hearted_pets.filter(id=pet_id)
        if pets.exists():
            pet = pets.first()
            pet.delete()
        else:
            try:
                pet = Pet.objects.get(pk=pet_id)
                instance.hearted_pets.add(pet)
            except Pet.DoesNotExist as e:
                raise ValidationError(_('Pet does not exists'))
        return instance
