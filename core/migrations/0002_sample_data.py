from django.db import migrations


def create_sample_data(apps, schema_editor):
    # Get models
    Category = apps.get_model('core', 'Category')
    Product = apps.get_model('core', 'Product')
    
    # Create categories
    electronics = Category.objects.create(
        name='Electronics',
        description='Latest electronic gadgets and devices.'
    )
    
    clothing = Category.objects.create(
        name='Clothing',
        description='Fashionable clothing for all occasions.'
    )
    
    books = Category.objects.create(
        name='Books',
        description='Bestselling books in various genres.'
    )
    
    # Create sample products
    Product.objects.create(
        name='Wireless Earbuds',
        description='High-quality wireless earbuds with noise cancellation.',
        price=99.99,
        category=electronics,
        stock=50,
        available=True
    )
    
    Product.objects.create(
        name='Smartwatch',
        description='Feature-rich smartwatch with health tracking.',
        price=199.99,
        category=electronics,
        stock=30,
        available=True
    )
    
    Product.objects.create(
        name='Cotton T-Shirt',
        description='Comfortable cotton t-shirt for everyday wear.',
        price=24.99,
        category=clothing,
        stock=100,
        available=True
    )
    
    Product.objects.create(
        name='Jeans',
        description='Classic blue jeans for a casual look.',
        price=59.99,
        category=clothing,
        stock=75,
        available=True
    )
    
    Product.objects.create(
        name='Python Programming Book',
        description='Comprehensive guide to Python programming.',
        price=39.99,
        category=books,
        stock=25,
        available=True
    )


def delete_sample_data(apps, schema_editor):
    # Get models
    Category = apps.get_model('core', 'Category')
    Product = apps.get_model('core', 'Product')
    
    # Delete all data
    Product.objects.all().delete()
    Category.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sample_data, delete_sample_data),
    ]
