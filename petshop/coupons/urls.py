from django.urls import path

from . import views

app_name = 'coupons'

urlpatterns = [
    path('<int:coupon_id>/', views.CouponRetrieveAPI.as_view(), name='coupon-retrieve'),
]
