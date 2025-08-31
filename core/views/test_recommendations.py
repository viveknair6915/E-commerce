""
Test views for the recommendation system.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from ..models import Product, Review
from ..recommendations.recommender import Recommender
import random

@never_cache
@login_required
def test_recommendations(request):
    """Test view to verify recommendation system functionality."""
    # Generate some test data if needed
    if not Review.objects.exists():
        products = list(Product.objects.all())
        users = [request.user]
        
        # Create some test reviews
        for user in users:
            for product in random.sample(products, min(5, len(products))):
                Review.objects.create(
                    user=user,
                    product=product,
                    rating=random.randint(1, 5),
                    comment=f"Test review for {product.name}"
                )
    
    # Initialize recommender
    recommender = Recommender(use_cython=True)
    
    # Get interactions from reviews
    reviews = Review.objects.values('user_id', 'product_id').annotate(
        avg_rating=Avg('rating')
    )
    
    interactions = [
        (r['user_id'], r['product_id'], float(r['avg_rating']))
        for r in reviews
    ]
    
    # Fit the recommender
    if interactions:
        recommender.fit(interactions)
        
        # Get recommendations for current user
        recommendations = recommender.recommend(request.user.id, n=5)
        
        # Get recommended products
        recommended_products = []
        for product_id, score in recommendations:
            try:
                product = Product.objects.get(id=product_id)
                recommended_products.append({
                    'product': product,
                    'score': score
                })
            except Product.DoesNotExist:
                pass
    else:
        recommended_products = []
    
    # Get user's reviewed products
    user_reviews = Review.objects.filter(user=request.user).select_related('product')
    
    return render(request, 'test_recommendations.html', {
        'recommended_products': recommended_products,
        'user_reviews': user_reviews,
    })
