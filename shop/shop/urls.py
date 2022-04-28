"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib.auth.views import LoginView
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('shop/', shop, name='shop'),  # Магазин без передачи параметров
    path('shop/<str:filter>/', shop, name='shop'),  # Магазин с передачей параметров
    path('contact/', contact, name='contact'),
    path('shop-single/', shop_single, name='shop-single'),
    path('shop-single/<str:product>/', shop_single, name='shop-single'),
    path('add_to_basket/', add_to_basket, name='add_to_basket'),
    path('basket/', basket, name='basket'),
    path('order/', order, name='order'),
    path('order_accept/', order_accept, name='order_accept'),

    path('accounts/login/', LoginView.as_view(), name="login"),
    path('accounts/profile/', ProfilePage.as_view(), name="profile"),
    path('accounts/register/', RegisterView.as_view(), name="register"),
    path('accounts/logout/', exit, name='exit'),
]


# ----------------------------------------------------------------------
# Без этой настройки из админки не открывались фотографии
# from django.conf import settings
# from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



