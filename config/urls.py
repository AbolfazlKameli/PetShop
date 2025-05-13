from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('users/', include('petshop.users.urls', namespace='users')),
    path('products/', include('petshop.products.urls', namespace='products')),
    path('orders/', include('petshop.orders.urls', namespace='orders')),
    path('coupons/', include('petshop.coupons.urls', namespace='coupons')),
]
