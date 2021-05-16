from django.conf.urls import url

from customers.views import signup

urlpatterns = [
    url('^signup$', signup, name="signup"),
]

