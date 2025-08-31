# Django E-commerce with ML Recommendations

A high-performance e-commerce platform built with Django, featuring machine learning-based recommendations, secure payments, and modern development practices.

## Features

- **User System**: Registration, authentication, password management
- **Product Catalog**: Categories, products, search, and filtering
- **Shopping Experience**:
  - Shopping cart with session management
  - Wishlists and saved items
  - Product reviews and ratings
- **Checkout & Payments**:
  - Secure checkout flow
  - Stripe payment integration
  - Order tracking
- **AI/ML Features**:
  - Personalized product recommendations
  - Real-time behavior analysis
  - Cython-optimized performance
- **Admin Dashboard**:
  - Comprehensive product management
  - Order processing
  - Sales analytics

## 🛠 Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: PostgreSQL (production), SQLite (development)
- **Search**: Django Haystack with Whoosh
- **Caching**: Redis
- **Async Tasks**: Celery with Redis
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Testing**: pytest, Factory Boy, Selenium

##  Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- Node.js 16+ (for frontend assets)
- Docker & Docker Compose (optional)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/django-ecommerce.git
   cd django-ecommerce
   ```

2. **Set up environment**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   
   # Set up pre-commit hooks
   pre-commit install
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load sample data** (optional)
   ```bash
   python manage.py load_sample_data
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

### Using Docker

```bash
# Build and start containers
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=.

# Run specific test
pytest path/to/test_file.py::TestClass::test_method
```

## 🧹 Code Quality

```bash
# Format code
make format

# Run linters
make lint

# Run security checks
safety check
bandit -r .
```

## 📦 Deployment

### Production

1. Set up a production-ready database (PostgreSQL)
2. Configure environment variables in production
3. Set up a production web server (Nginx + Gunicorn)
4. Configure SSL certificates (Let's Encrypt)

Example Gunicorn command:
```bash
gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000 --workers 4 --worker-class gthread --threads 2
```

### Docker Production

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## 📚 Documentation

- [API Documentation](/docs/API.md)
- [Frontend Guide](/docs/FRONTEND.md)
- [Deployment Guide](/docs/DEPLOYMENT.md)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django Software Foundation
- Bootstrap Team
- Stripe for payment processing
- Redis Labs for caching
- All contributors who helped improve this project```

6. **Compile Cython extensions** (optional):
   ```bash
   python setup_recsys.py
   ```
   
   Or use the setup script:
   ```bash
   python setup_project.py
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
ecommerce/
├── core/                    # Main application
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   ├── recommendations/     # ML recommendation system
│   ├── static/              # Static files (CSS, JS, images)
│   ├── __init__.py
│   ├── admin.py            # Admin configuration
│   ├── apps.py             # App configuration
│   ├── models.py           # Database models
│   ├── urls.py             # URL routing
│   └── views.py            # View functions
├── ecommerce/              # Project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # Project settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py
├── media/                  # User-uploaded files
├── static/                 # Collected static files
├── templates/              # Base templates
├── tests/                  # Test files
├── .gitignore
├── manage.py              # Django management script
├── README.md              # This file
├── requirements_updated.txt # Project dependencies
└── setup_project.py       # Setup script
```

## Recommendation System

The recommendation system uses collaborative filtering with Cython-optimized similarity calculations. It provides:

- Personalized product recommendations
- Real-time updates based on user interactions
- Fallback to popular items when insufficient data

### How It Works

1. **Data Collection**: Tracks user interactions (views, cart additions, purchases)
2. **Similarity Calculation**: Uses cosine similarity to find similar users/items
3. **Recommendation Generation**: Suggests items based on user behavior and similarity
4. **Performance Optimization**: Cython-accelerated calculations for better performance

## Testing

Run the test suite with:
```bash
pytest
```

## Deployment

For production deployment:

1. Set `DEBUG = False` in `ecommerce/settings.py`
2. Configure a production database (PostgreSQL recommended)
3. Set up a production web server (Nginx + Gunicorn)
4. Configure environment variables
5. Set up SSL/TLS for secure connections

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django Framework
- Bootstrap 5
- scikit-learn
- Cython
- Stripe for payments
