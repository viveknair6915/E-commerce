from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-ecommerce',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=4.2.10',
        'Pillow>=11.0.0',
        'django-crispy-forms>=2.1',
        'crispy-bootstrap5>=2023.10',
        'stripe>=7.6.0',
        'python-dotenv>=1.0.0',
    ],
    python_requires='>=3.8',
    author='Your Name',
    author_email='your.email@example.com',
    description='A Django e-commerce application with ML recommendations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/django-ecommerce',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
