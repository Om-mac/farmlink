"""Main URL Configuration for FarmLink"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import api_root, home

urlpatterns = [
    path('', home, name='home'),
    path('api/', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/farmers/', include('farmers.urls')),
    path('api/buyers/', include('buyers.urls')),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/smartcontracts/', include('smartcontracts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
