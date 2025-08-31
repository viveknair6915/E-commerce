""
Views for handling recommendations.
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Count, Avg

from core.models import Product, Review, OrderItem
from core.recommendations.recommender import Recommender

# Global recommender instance
recommender = None

def init_recommender():
    """Initialize the recommender with existing data."""
    global recommender
    
    if recommender is not None:
        return
    
    # Get all user-item interactions from reviews and orders
    reviews = Review.objects.values('user_id', 'product_id').annotate(
        avg_rating=Avg('rating')
    )
    
    # Convert to list of tuples (user_id, item_id, rating)
    interactions = [
        (r['user_id'], r['product_id'], float(r['avg_rating']))
        for r in reviews
    ]
    
    # Add order data as implicit feedback
    orders = OrderItem.objects.values('order__user_id', 'product_id').annotate(
        count=Count('id')
    )
    
    # Add implicit feedback (purchases) with a default rating of 4.0
    for order in orders:
        interactions.append((order['order__user_id'], order['product_id'], 4.0))
    
    # Initialize and fit the recommender
    if interactions:
        recommender = Recommender(use_cython=True)
        recommender.fit(interactions)

@login_required
def get_recommendations(request):
    """Get personalized product recommendations for the current user."""
    global recommender
    
    if recommender is None:
        init_recommender()
    
    user_id = request.user.id
    recommended = []
    
    if recommender is not None:
        # Get top 6 recommendations
        recommendations = recommender.recommend(user_id, n=6)
        
        # Get product details for recommended items
        product_ids = [item_id for item_id, _ in recommendations]
        products = Product.objects.filter(id__in=product_ids).in_bulk()
        
        # Create list of recommended products with scores
        recommended = [
            {
                'product': products[item_id],
                'score': score
            }
            for item_id, score in recommendations
            if item_id in products
        ]
    
    # If no recommendations or not enough, fall back to popular items
    if len(recommended) < 3:
        popular = Product.objects.annotate(
            num_orders=Count('order_items')
        ).order_by('-num_orders')[:6]
        
        for product in popular:
            if not any(r['product'].id == product.id for r in recommended):
                recommended.append({'product': product, 'score': 0.0})
            if len(recommended) >= 6:
                break
    
    return recommended

@login_required
def recommendation_view(request):
    """View for displaying recommendations."""
    recommended = get_recommendations(request)
    return render(request, 'recommendations.html', {'recommended': recommended})

@require_http_methods(["POST"])
@login_required
def rate_product(request, product_id):
    """Handle product rating and update recommendations."""
    global recommender
    
    try:
        rating = float(request.POST.get('rating'))
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
            
        # Save the rating
        product = get_object_or_404(Product, id=product_id)
        review, created = Review.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={'rating': rating}
        )
        
        # Update the recommender with the new rating
        if recommender is not None:
            # Re-initialize the recommender with updated data
            init_recommender()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Rating saved successfully',
            'created': created,
            'rating': rating
        })
        
    except (ValueError, TypeError) as e:
        return JsonResponse(
            {'status': 'error', 'message': str(e)},
            status=400
        )
