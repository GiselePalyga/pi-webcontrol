#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "==> Preparando ambiente virtual"
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate

echo "==> Instalando dependencias"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "==> Criando projeto Django"
if [ ! -f "manage.py" ]; then
  django-admin startproject config .
fi

echo "==> Criando estrutura base"
mkdir -p apps templates static/css static/js database
touch apps/__init__.py

for app in core accounts fornecedores produtos notas financeiro; do
  if [ ! -d "apps/$app" ]; then
    python manage.py startapp "$app" "apps/$app"
  fi
done

echo "==> Proximos passos manuais"
echo "1. Ajustar config/settings.py:"
echo "   - adicionar os apps criados em INSTALLED_APPS"
echo "   - configurar DIRS de templates"
echo "   - configurar STATICFILES_DIRS"
echo "   - definir LOGIN_URL e LOGIN_REDIRECT_URL"
echo "2. Criar os models com base em database/schema.sql"
echo "3. Rodar: python manage.py makemigrations"
echo "4. Rodar: python manage.py migrate"
echo "5. Rodar: python manage.py createsuperuser"
echo "6. Subir servidor: python manage.py runserver"

