from .models import Coupon


def get_all_coupons() -> list[Coupon]:
    return Coupon.objects.all()
