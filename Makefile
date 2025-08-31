.PHONY: help install test lint format clean

# Default target
help:
	@echo "Available commands:"
	@echo "  make install     Install dependencies"
	@echo "  make migrate     Run database migrations"
	@echo "  make superuser   Create a superuser"
	@echo "  make test        Run tests"
	@echo "  make lint        Run linters"
	@echo "  make format      Format code"
	@echo "  make clean       Remove Python and build artifacts"

# Install dependencies
install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

# Run database migrations
migrate:
	python manage.py migrate

# Create superuser
superuser:
	python manage.py createsuperuser

# Run tests
test:
	pytest --cov=.

# Run linters
lint:
	flake8 .
	black --check .
	isort --check-only .

# Format code
format:
	black .
	isort .

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -r {} \;
	find . -type d -name ".pytest_cache" -exec rm -r {} \;
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} \;
	docker-compose down -v
	rm -rf build/ dist/ .coverage htmlcov/
