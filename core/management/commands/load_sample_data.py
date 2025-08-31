"""
Sample Data Generator for E-commerce Application
--------------------------------------------
Generates sample products, categories, and user interactions.
"""
import os
import random
from datetime import datetime, timedelta
from django.core.files import File
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Category, Product, Review, Cart, CartItem, Order, OrderItem

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate sample data for the e-commerce application'

    def handle(self, *args, **options):
        self.stdout.write('Generating sample data...')
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Category.objects.all().delete()
        Product.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        # Create categories
        categories = [
            'Electronics', 'Clothing', 'Books', 'Home & Kitchen', 'Toys', 'Sports'
        ]
        
        category_objs = []
        for name in categories:
            cat = Category.objects.create(
                name=name,
                slug=name.lower().replace(' ', '-')
            )
            category_objs.append(cat)
            self.stdout.write(f'Created category: {name}')
        
        # Create sample products
        products = [
            {'name': 'Wireless Headphones', 'price': 99.99, 'category': 'Electronics'},
            {'name': 'Smart Watch', 'price': 199.99, 'category': 'Electronics'},
            {'name': 'Cotton T-Shirt', 'price': 19.99, 'category': 'Clothing'},
            {'name': 'Python Programming Book', 'price': 39.99, 'category': 'Books'},
            {'name': 'Coffee Maker', 'price': 49.99, 'category': 'Home & Kitchen'},
            {'name': 'Football', 'price': 29.99, 'category': 'Sports'}
        ]
        
        for prod in products:
            category = Category.objects.get(name=prod['category'])
            product = Product.objects.create(
                name=prod['name'],
                slug=prod['name'].lower().replace(' ', '-'),
                description=f'This is a sample {prod["name"]}. Great product with amazing features!',
                price=prod['price'],
                category=category,
                stock=random.randint(10, 100),
                available=True
            )
            self.stdout.write(f'Created product: {product.name}')
        
        # Create a test user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.stdout.write('Created test user: testuser / testpass123')
        
        self.stdout.write(self.style.SUCCESS('Successfully generated sample data!'))
