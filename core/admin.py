from django.contrib import admin
from .models import Category, Product, Review, Cart, CartItem, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    list_filter = ['created_at', 'updated_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created_at', 'updated_at']
    list_filter = ['available', 'created_at', 'updated_at', 'category']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    date_hierarchy = 'created_at'

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at', 'total_items', 'total_price']
    list_filter = ['created_at', 'updated_at']
    inlines = [CartItemInline]
    readonly_fields = ['created_at', 'updated_at', 'total_items', 'total_price']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['get_cost']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email', 'status', 'paid', 'created_at']
    list_filter = ['status', 'paid', 'created_at', 'updated_at']
    search_fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at', 'get_total_cost']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at', 'likes', 'dislikes']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__name', 'user__username', 'comment']
