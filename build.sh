#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Début du build ProSMAT..."

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements.txt

# Décoder les credentials Firebase depuis base64
echo "🔐 Configuration Firebase..."
if [ ! -z "$FIREBASE_CREDENTIALS_BASE64" ]; then
    echo "$FIREBASE_CREDENTIALS_BASE64" | base64 -d > firebase-credentials.json
    echo "✅ Credentials Firebase créés"
else
    echo "⚠️  FIREBASE_CREDENTIALS_BASE64 non défini"
fi

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --no-input

# Effectuer les migrations
echo "🗄️  Exécution des migrations..."
python manage.py migrate

# Charger les données initiales (seulement si la base est vide)
echo "📊 Chargement des données initiales..."
python manage.py charger_donnees

echo "✅ Build terminé avec succès!"
