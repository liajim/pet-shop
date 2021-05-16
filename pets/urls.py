from django.conf.urls import url

from pets.views import index

urlpatterns = [
    url('^$', index, name="index"),
]
