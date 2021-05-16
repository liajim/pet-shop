from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(User):
    """Model for customers."""
    address = models.CharField(max_length=256, verbose_name=_('address'))
    phone_number = models.CharField(max_length=30, verbose_name=_('phone number'))
    hearted_pets = models.ManyToManyField('pets.Pet')

    def _str_(self):
        """String Representation of the Customer."""
        return (self.first_name or '') + (self.last_name or '')