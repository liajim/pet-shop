from django.contrib import admin
from django.db import transaction

from utils.database_classes import CSVAdmin
from .models import Pet, Specie, Breed


@admin.register(Pet)
class PetAdmin(CSVAdmin):
    list_display = ('name', 'specie', 'breed', 'age', 'for_adoption', 'price')

    @transaction.atomic()
    def add_object_csv(self, row):
        """ Add a row to Pet model avoid first line """
        if row[0] == 'image_url':
            return

        specie, _ = Specie.objects.get_or_create(name=row[4])
        breed, _ = Breed.objects.get_or_create(name=row[3], specie=specie)
        data = {
            'image_url': row[0],
            'name': row[1],
            'sex': row[2],
            'breed': breed,
            'for_adoption': row[5] == "1",
            'years': row[6],
            'months': row[7]
        }
        if row[8].strip() != '':
            data['price'] = row[8]
        Pet.objects.create(**data)


admin.site.register(Breed)
admin.site.register(Specie)
