"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from customers import api_urls as customer_api_urls
from customers import urls as customer_urls
from customers import internal_urls as internal_customer_urls
from pets import api_urls as pet_api_urls
from pets import urls as pet_urls
from django.contrib.auth import views

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('api/', include(customer_api_urls)),
    path('api/', include(pet_api_urls)),
    path('api/internal/', include((internal_customer_urls, 'internal-api'), 'internal-api')),
    path('', include(customer_urls)),
    path('', include(pet_urls)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
