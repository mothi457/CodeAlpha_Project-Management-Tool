#!/bin/bash
echo "🚀 Setting up TaskFlow — Project Management Tool..."

pip install -r requirements.txt

python manage.py makemigrations projects
python manage.py migrate

python setup_data.py

echo ""
echo "✅ Done! Run: python manage.py runserver"
echo "🌐 Open: http://127.0.0.1:8000"
echo "🔐 Admin: http://127.0.0.1:8000/admin (admin / admin123)"
