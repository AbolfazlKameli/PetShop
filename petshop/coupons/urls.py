from django.urls import path

from . import views

app_name = 'coupons'

urlpatterns = [
    path('', views.CouponsListAPI.as_view(), name='coupons-list'),
    path('create/', views.CouponCreateAPI.as_view(), name='coupon-create'),
    path('<int:coupon_id>/', views.CouponRetrieveAPI.as_view(), name='coupon-retrieve'),
    path('<int:coupon_id>/update/', views.CouponUpdateAPI.as_view(), name='coupon-update'),
    path('<int:coupon_id>/delete/', views.CouponDeleteAPI.as_view(), name='coupon-delete'),
    path('apply/', views.CouponApplyAPI.as_view(), name='coupon-apply'),
]
