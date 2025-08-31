""
Context processors for the core application.
"""
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .views.recommendations import get_recommendations

def recommendations(request):
    ""
    Add recommendations to the template context for authenticated users.
    """
    context = {}
    
    if request.user.is_authenticated:
        # Cache recommendations for 1 hour (3600 seconds)
        @method_decorator(cache_page(3600))
        def get_cached_recommendations():
            return get_recommendations(request)
            
        try:
            context['recommended_products'] = get_cached_recommendations()
        except Exception as e:
            # Log error but don't break the page
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error getting recommendations: {e}")
            context['recommended_products'] = []
    
    return context
