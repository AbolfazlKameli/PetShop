from django.urls import path

from . import views

app_name = 'coupons'

urlpatterns = [
    path('', views.CouponsListAPI.as_view(), name='coupons-list'),
    path('<int:coupon_id>/', views.CouponRetrieveAPI.as_view(), name='coupon-retrieve'),
]
