import csv
from io import TextIOWrapper

from django.contrib import admin
from django.forms import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.translation import gettext_lazy as _


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response
    export_as_csv.short_description = _("Export Selected")


class CSVAdmin(admin.ModelAdmin, ExportCsvMixin):
    change_list_template = "entities/override_changelist.html"
    actions = ["export_as_csv"]
    encoding_utf8 = True

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def add_object_csv(self, row):
        pass

    def import_csv(self, request):
        if request.method == "POST":
            if self.encoding_utf8:
                csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding="utf8")
            else:
                csv_file = TextIOWrapper(request.FILES['csv_file'].file)
            reader = csv.reader(csv_file)
            for row in reader:
                self.add_object_csv(row)
            self.message_user(request, _("Your csv file has been imported"))
            return redirect("..")

        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/pet_csv_form.html", payload
        )
