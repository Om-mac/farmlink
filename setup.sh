#!/bin/bash

# FarmLink Setup Script
# Run this after cloning to set up the development environment

echo "🌾 FarmLink Setup Script"
echo "========================"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version found"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your AWS credentials and settings"
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Create superuser
echo "👤 Creating superuser..."
python manage.py createsuperuser --noinput --username admin --email admin@farmlink.local || true

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create sample data (optional)
echo "🌱 Creating sample data..."
python manage.py shell < sample_data.py || true

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your AWS credentials"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python manage.py runserver"
echo "4. Visit: http://localhost:8000/admin/"
echo "5. Use credentials from superuser creation"
echo ""
