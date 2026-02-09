#!/bin/bash

echo "🚀 Démarrage de ProSMAT..."

# Exécuter les migrations
echo "📊 Exécution des migrations..."
python manage.py migrate --noinput

# Créer les utilisateurs par défaut
echo "👥 Création des utilisateurs par défaut..."
python manage.py init_users

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Démarrer Gunicorn
echo "🌐 Démarrage du serveur..."
gunicorn config.wsgi --log-file - --bind 0.0.0.0:$PORT
