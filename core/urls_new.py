"""
URLs for the core application.
"""
from django.urls import path, include
from django.views.generic import TemplateView
from . import views
from .views import test_recommendations

app_name = 'core'

urlpatterns = [
    # Home page
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # Product URLs
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    
    # Cart URLs
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    
    # Order URLs
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # Recommendation URLs
    path('recommendations/', include('core.urls.recommendations')),
    path('test-recommendations/', test_recommendations.test_recommendations, name='test_recommendations'),
]
