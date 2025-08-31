""
Script to update Django settings with recommendation system configurations.
Run this script after checking the changes.
"""
import os

def update_settings():
    settings_path = os.path.join('ecommerce', 'settings.py')
    
    # Read the current settings
    with open(settings_path, 'r') as f:
        content = f.read()
    
    # Add context processor if not exists
    if 'core.context_processors.recommendations' not in content:
        context_processors_start = content.find("'context_processors': [")
        if context_processors_start != -1:
            insert_pos = content.find(']', context_processors_start)
            if insert_pos != -1:
                content = (
                    content[:insert_pos] + 
                    "\n                'core.context_processors.recommendations'," +
                    content[insert_pos:]
                )
    
    # Add login URL if not exists
    if 'LOGIN_URL' not in content:
        content += '\n\n# Authentication\nLOGIN_URL = "login"\nLOGIN_REDIRECT_URL = "core:home"\nLOGOUT_REDIRECT_URL = "core:home"\n'
    # Add cache settings if not exists
    if 'CACHES' not in content:
        content += '\n\n# Cache settings\nCACHES = {\n    "default": {\n        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",\n        "LOCATION": "unique-snowflake",\n    }\n}\n'
    
    # Add session settings if not exists
    if 'SESSION_ENGINE' not in content:
        content += '\n# Session settings\nSESSION_ENGINE = "django.contrib.sessions.backends.cache"\nSESSION_CACHE_ALIAS = "default"\n'
    
    # Write the updated content back
    with open(settings_path, 'w') as f:
        f.write(content)
    
    print("Settings updated successfully!")

if __name__ == '__main__':
    update_settings()
