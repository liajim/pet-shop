from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'address', 'phone_number', 'pets_hearted')

    def pets_hearted(self, obj):
        return mark_safe("<br>".join([p.name for p in obj.hearted_pets.all()]))


admin.site.register(Customer, CustomerAdmin)
