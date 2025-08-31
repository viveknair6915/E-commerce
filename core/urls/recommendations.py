""
URLs for the recommendation system.
"""
from django.urls import path
from .views import recommendations as recommendation_views

app_name = 'recommendations'

urlpatterns = [
    path('', recommendation_views.recommendation_view, name='recommendations'),
    path('rate/<int:product_id>/', recommendation_views.rate_product, name='rate_product'),
]
