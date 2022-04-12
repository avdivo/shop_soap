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

]
# https://learntutorials.net/ru/django/topic/3299/%D0%BC%D0%B0%D1%80%D1%88%D1%80%D1%83%D1%82%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F-url
# urlpatterns = [
#     url(r'^$', home, name='home'),
#     url(r'^about/$', about, name='about'),
#     url(r'^blog/(?P<id>\d+)/$', blog_detail, name='blog-detail'),
# ]


# ----------------------------------------------------------------------
# Без этой настройки из админки не открывались фотографии
# from django.conf import settings
# from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



