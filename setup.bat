@echo off
REM FarmLink Setup Script for Windows

echo.
echo 🌾 FarmLink Setup Script (Windows)
echo ==================================
echo.

REM Check Python version
python --version
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.9+ first.
    exit /b 1
)

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env file
if not exist .env (
    echo ⚙️  Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Please edit .env with your AWS credentials
)

REM Run migrations
echo 🗄️  Running database migrations...
python manage.py migrate

REM Create superuser
echo 👤 Creating superuser...
python manage.py createsuperuser --noinput --username admin --email admin@farmlink.local

REM Collect static files
echo 📁 Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file with your AWS credentials
echo 2. Run: venv\Scripts\activate.bat
echo 3. Run: python manage.py runserver
echo 4. Visit: http://localhost:8000/admin/
echo.
