from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_thumbs.fields import ImageThumbsField

from utils.constants import MIN_MONTH_AGE, SIZES
from utils.utils import open_and_treat_image


class Specie(models.Model):
    """Model for species."""
    name = models.CharField(max_length=100, verbose_name=_('name'))

    def __str__(self):
        """String Representation of the Specie."""
        return self.name


class Breed(models.Model):
    """Model for breeds."""
    specie = models.ForeignKey(Specie, verbose_name=_('name'), on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=_('name'))

    def __str__(self):
        """String Representation of the Breed."""
        return '%s %s' % (self.name, self.specie.name)


class Pet(models.Model):
    """Model for pets."""
    image = ImageThumbsField(upload_to='pets', sizes=SIZES, blank=True, null=True, verbose_name=_('image'))
    image_url = models.URLField(blank=True, null=True, verbose_name=_('image url'))
    name = models.CharField(max_length=100, verbose_name=_('name'))
    sex = models.CharField(max_length=6, choices=(('male', 'male'), ('female', 'female')))
    breed = models.ForeignKey(Breed, verbose_name=_('breed'), on_delete=models.PROTECT)
    for_adoption = models.BooleanField(verbose_name=_('for adoption'), default=False)
    years = models.SmallIntegerField(verbose_name=_('years'))
    months = models.SmallIntegerField(verbose_name=_('months'))
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_('price'),
                                blank=True, null=True)

    def __str__(self):
        """String Representation of the Pet."""
        return self.name

    def clean(self):
        """Validate info pet"""
        # Don't allow pets that have less than 2 months of age.
        if self.years == 0 and self.months < MIN_MONTH_AGE:
            raise ValidationError(_('Age of Pet cannot be less than 2 months'))
        # Verify pet has image
        with_image = True
        try:
            self.image.file
        except ValueError as e:
            with_image = False
        if not self.image_url and not with_image:
            raise ValidationError(_('Pet without image'))
        # Verify is for adoption or has price
        if not self.for_adoption and (self.price is None or self.price.compare(Decimal(0)) == 1):
            raise ValidationError(_('If pet is not for adoption need a price greater than 0'))
        # if it is for adoption price is None
        if self.for_adoption and self.price is not None:
            self.price = None

    @property
    def specie(self):
        """Name of the specie."""
        return self.breed.specie

    @property
    def age(self):
        """String representation of age."""
        years_str = ''
        if self.years > 0:
            if self.years == 1:
                years_str += str(_('%s year' % self.years))
            else:
                years_str += str(_('%s years' % self.years))
        months_str = ''
        if self.months > 0:
            if years_str != '':
                months_str = ' %s ' % str(_('and'))
            if self.months == 1:
                months_str += str(_('%s month' % self.months))
            else:
                months_str += str(_('%s months' % self.months))
        return years_str + months_str

    def save(self, *args, **kwargs):
        if self.image:
            data = open_and_treat_image(self.image)
            self.image = ContentFile(data, name=self.image.name)
        super(Pet, self).save(*args, **kwargs)