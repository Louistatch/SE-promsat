#!/usr/bin/env bash
set -o errexit

echo "📦 Installation des dépendances..."
pip install -r requirements.txt

echo "🔐 Configuration Firebase..."
if [ ! -z "$FIREBASE_CREDENTIALS_BASE64" ]; then
    echo "$FIREBASE_CREDENTIALS_BASE64" | base64 -d > firebase-credentials.json
    echo "✅ Credentials Firebase OK"
else
    echo "⚠️  Firebase non configuré (mode dev)"
fi

echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --no-input

echo "🗄️  Migrations..."
python manage.py migrate

echo "✅ Build terminé!"
