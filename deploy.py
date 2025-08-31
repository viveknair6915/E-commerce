#!/usr/bin/env python
"""
Deployment Script for E-commerce Application
-----------------------------------------
Helps deploy the application to a production environment.
"""
import os
import sys
import subprocess
import shutil
import argparse
from pathlib import Path

# Configuration
PROJECT_NAME = 'ecommerce'
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / '.env'
REQUIREMENTS = 'requirements_updated.txt'

def run_command(command, cwd=None, shell=True):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd or BASE_DIR,
            shell=shell,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None

def check_prerequisites():
    """Check if all prerequisites are installed."""
    print("Checking prerequisites...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        return False
    
    print("✓ Python version is compatible")
    return True

def setup_environment():
    """Set up the production environment."""
    print("\nSetting up environment...")
    
    # Create .env file if it doesn't exist
    if not ENV_FILE.exists():
        with open(ENV_FILE, 'w') as f:
            f.write("""# Django Settings
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=example.com,www.example.com

# Database
DB_NAME=ecommerce_db
DB_USER=ecommerce_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=your-email@example.com

# Stripe
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
""")
        print(f"✓ Created {ENV_FILE} - Please update with your configuration")
    else:
        print(f"✓ {ENV_FILE} already exists")

def install_dependencies():
    """Install required dependencies."""
    print("\nInstalling dependencies...")
    run_command(f"pip install -r {REQUIREMENTS}")
    print("✓ Dependencies installed")

def setup_database():
    """Set up the production database."""
    print("\nSetting up database...")
    run_command("python manage.py migrate")
    run_command("python manage.py collectstatic --noinput")
    print("✓ Database and static files set up")

def setup_web_server(server_type='nginx'):
    """Set up the web server configuration."""
    print(f"\nSetting up {server_type.upper()} configuration...")
    
    if server_type == 'nginx':
        config = f"""
server {{
    listen 80;
    server_name example.com www.example.com;

    location = /favicon.ico {{ access_log off; log_not_found off; }}
    
    location /static/ {{
        root {BASE_DIR};
    }}
    
    location /media/ {{
        root {BASE_DIR};
    }}
    
    location / {{
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }}
}}
"""
        config_path = f"/etc/nginx/sites-available/{PROJECT_NAME}"
        
        try:
            with open(config_path, 'w') as f:
                f.write(config)
            
            # Create symlink if it doesn't exist
            if not os.path.exists(f"/etc/nginx/sites-enabled/{PROJECT_NAME}"):
                os.symlink(
                    f"/etc/nginx/sites-available/{PROJECT_NAME}",
                    f"/etc/nginx/sites-enabled/{PROJECT_NAME}"
                )
            
            print(f"✓ {server_type.upper()} configuration created at {config_path}")
            print("  Don't forget to update the server_name and other settings")
            
        except PermissionError:
            print(f"✗ Permission denied when writing to {config_path}")
            print(f"Run this script with sudo or as a user with appropriate permissions")
    else:
        print(f"✗ Unsupported server type: {server_type}")

def setup_gunicorn():
    """Set up Gunicorn configuration."""
    print("\nSetting up Gunicorn...")
    
    config = f"""[Unit]
Description=gunicorn daemon for {PROJECT_NAME}
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory={BASE_DIR}
ExecStart={sys.executable} -m gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock {PROJECT_NAME}.wsgi:application

[Install]
WantedBy=multi-user.target
"""
    
    service_path = f"/etc/systemd/system/{PROJECT_NAME}.service"
    
    try:
        with open(service_path, 'w') as f:
            f.write(config)
        
        run_command("systemctl daemon-reload")
        run_command(f"systemctl enable {PROJECT_NAME}.service")
        run_command(f"systemctl start {PROJECT_NAME}.service")
        
        print(f"✓ Gunicorn service created at {service_path}")
        print("  You can manage the service with:")
        print(f"  sudo systemctl start|stop|restart {PROJECT_NAME}.service")
        
    except PermissionError:
        print(f"✗ Permission denied when writing to {service_path}")
        print("Run this script with sudo or as a user with appropriate permissions")

def setup_ssl():
    """Set up SSL certificates with Let's Encrypt."""
    print("\nSetting up SSL with Let's Encrypt...")
    
    if not shutil.which('certbot'):
        print("Certbot is not installed. Installing...")
        run_command("sudo apt-get update")
        run_command("sudo apt-get install -y certbot python3-certbot-nginx")
    
    print("Running Certbot to obtain SSL certificate...")
    run_command("sudo certbot --nginx -d example.com -d www.example.com")
    
    # Set up automatic renewal
    run_command("(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -")
    
    print("✓ SSL certificate set up successfully")

def deploy():
    """Run the full deployment process."""
    print("=" * 70)
    print(f"Deploying {PROJECT_NAME.upper()} to Production")
    print("=" * 70)
    
    if not check_prerequisites():
        sys.exit(1)
    
    setup_environment()
    install_dependencies()
    setup_database()
    
    if input("\nSet up Nginx configuration? (y/n): ").lower() == 'y':
        setup_web_server('nginx')
    
    if input("\nSet up Gunicorn service? (y/n): ").lower() == 'y':
        setup_gunicorn()
    
    if input("\nSet up SSL with Let's Encrypt? (y/n): ").lower() == 'y':
        setup_ssl()
    
    print("\n" + "=" * 70)
    print("Deployment completed successfully!")
    print("Next steps:")
    print("1. Update the .env file with your configuration")
    print("2. Configure your domain's DNS settings")
    print("3. Start the services:")
    print("   sudo systemctl start nginx")
    print(f"   sudo systemctl start {PROJECT_NAME}.service")
    print("\nAccess your site at: https://your-domain.com")
    print("=" * 70)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deploy the e-commerce application')
    parser.add_argument('--setup-nginx', action='store_true', help='Set up Nginx configuration')
    parser.add_argument('--setup-gunicorn', action='store_true', help='Set up Gunicorn service')
    parser.add_argument('--setup-ssl', action='store_true', help='Set up SSL with Let\'s Encrypt')
    
    args = parser.parse_args()
    
    if args.setup_nginx:
        setup_web_server('nginx')
    elif args.setup_gunicorn:
        setup_gunicorn()
    elif args.setup_ssl:
        setup_ssl()
    else:
        deploy()
