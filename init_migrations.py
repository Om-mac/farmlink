"""
Run this script to populate initial migrations
python manage.py shell < init_migrations.py
"""

import os
import django

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from django.core.management import call_command
from django.apps import apps

print("🗂️  Generating migrations for all apps...")

# Get all app configs
apps_to_migrate = ['farmers', 'buyers', 'products', 'orders', 'smartcontracts']

for app in apps_to_migrate:
    print(f"\n📝 Creating migrations for {app}...")
    try:
        call_command('makemigrations', app)
        print(f"✓ Migrations created for {app}")
    except Exception as e:
        print(f"⚠️  Error creating migrations for {app}: {e}")

print("\n🔄 Applying all migrations...")
try:
    call_command('migrate')
    print("✓ All migrations applied successfully!")
except Exception as e:
    print(f"❌ Error applying migrations: {e}")

print("\n✅ Migration setup complete!")
