from django.contrib import admin

from .models import ProductCategory, Product, ProductDetail, ProductImage, ProductReview


class ProductDetailInline(admin.TabularInline):
    model = ProductDetail


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductReviewInline(admin.TabularInline):
    model = ProductReview


@admin.register(ProductCategory)
class ProductCategoryModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'id')
    search_fields = ('title',)

    prepopulated_fields = {'slug': ('title',)}


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'quantity', 'available', 'final_price', 'discount_percent')
    list_filter = ('available',)
    search_fields = ('title', 'description')
    inlines = (ProductDetailInline, ProductImageInline, ProductReviewInline)


@admin.register(ProductDetail)
class ProductDetailModelAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    search_fields = ('key', 'value')


@admin.register(ProductReview)
class ProductReviewModelAdmin(admin.ModelAdmin):
    list_display = ('product__title', 'owner__username', 'status', 'rate')
    list_filter = ('status', 'rate')
    search_fields = ('body', 'owner__username')
