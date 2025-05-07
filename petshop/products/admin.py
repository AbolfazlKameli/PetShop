from django.contrib import admin

from .models import ProductCategory, Product, ProductDetail, ProductImage


class ProductDetailInline(admin.TabularInline):
    model = ProductDetail


class ProductImageInline(admin.TabularInline):
    model = ProductImage


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
    inlines = (ProductDetailInline, ProductImageInline)


@admin.register(ProductDetail)
class ProductDetailModelAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    search_fields = ('key', 'value')
