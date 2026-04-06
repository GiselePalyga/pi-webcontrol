#!/bin/sh
set -e

echo "==> Aplicando migrações..."
python manage.py migrate --noinput

echo "==> Criando superusuário (se necessário)..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@webcontrol.local')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'webcontrol@2025')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superusuário criado: {username}')
else:
    print(f'Superusuário já existe: {username}')
"

echo "==> Iniciando servidor Gunicorn..."
exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 2 \
  --threads 2 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile -
