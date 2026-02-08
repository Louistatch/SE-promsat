# 🚀 Guide de Déploiement en Production

## ⚠️ Avant de Déployer

### Checklist de Sécurité

- [ ] Changer la SECRET_KEY
- [ ] Définir DEBUG = False
- [ ] Configurer ALLOWED_HOSTS
- [ ] Utiliser PostgreSQL (pas SQLite)
- [ ] Configurer HTTPS
- [ ] Changer tous les mots de passe par défaut
- [ ] Configurer les sauvegardes automatiques
- [ ] Configurer les logs
- [ ] Tester en environnement de staging

## 🔧 Configuration de Production

### 1. Créer settings_local.py

```bash
cp config/settings_production.py config/settings_local.py
```

Modifiez `settings_local.py` avec vos valeurs:

```python
SECRET_KEY = 'votre-cle-secrete-unique'
DEBUG = False
ALLOWED_HOSTS = ['prosmat.tg', 'www.prosmat.tg']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'prosmat_db',
        'USER': 'prosmat_user',
        'PASSWORD': 'mot_de_passe_fort',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 2. Modifier settings.py

À la fin de `config/settings.py`, ajoutez:

```python
# Import local settings if exists
try:
    from .settings_local import *
except ImportError:
    pass
```

## 🗄️ Base de Données PostgreSQL

### Installation PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**Windows:**
Téléchargez depuis: https://www.postgresql.org/download/windows/

### Créer la Base de Données

```bash
sudo -u postgres psql

CREATE DATABASE prosmat_db;
CREATE USER prosmat_user WITH PASSWORD 'mot_de_passe_fort';
ALTER ROLE prosmat_user SET client_encoding TO 'utf8';
ALTER ROLE prosmat_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE prosmat_user SET timezone TO 'Africa/Lome';
GRANT ALL PRIVILEGES ON DATABASE prosmat_db TO prosmat_user;
\q
```

### Installer le Driver PostgreSQL

```bash
pip install psycopg2-binary
```

### Migrer les Données

```bash
python manage.py migrate
python manage.py init_prosmat
```

## 🌐 Serveur Web avec Gunicorn et Nginx

### 1. Installer Gunicorn

```bash
pip install gunicorn
```

### 2. Tester Gunicorn

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### 3. Créer un Service Systemd

Créez `/etc/systemd/system/prosmat.service`:

```ini
[Unit]
Description=ProSMAT Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/prosmat_se
Environment="PATH=/var/www/prosmat_se/venv/bin"
ExecStart=/var/www/prosmat_se/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/prosmat_se/prosmat.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 4. Activer le Service

```bash
sudo systemctl start prosmat
sudo systemctl enable prosmat
sudo systemctl status prosmat
```

### 5. Installer et Configurer Nginx

**Installation:**
```bash
sudo apt install nginx
```

**Configuration** `/etc/nginx/sites-available/prosmat`:

```nginx
server {
    listen 80;
    server_name prosmat.tg www.prosmat.tg;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/prosmat_se/staticfiles/;
    }
    
    location /media/ {
        alias /var/www/prosmat_se/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/prosmat_se/prosmat.sock;
    }
}
```

**Activer le site:**
```bash
sudo ln -s /etc/nginx/sites-available/prosmat /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🔒 HTTPS avec Let's Encrypt

### 1. Installer Certbot

```bash
sudo apt install certbot python3-certbot-nginx
```

### 2. Obtenir un Certificat SSL

```bash
sudo certbot --nginx -d prosmat.tg -d www.prosmat.tg
```

### 3. Renouvellement Automatique

```bash
sudo certbot renew --dry-run
```

Le renouvellement automatique est configuré via cron.

## 📦 Fichiers Statiques

### Collecter les Fichiers Statiques

```bash
python manage.py collectstatic --noinput
```

### Configuration Nginx pour les Statiques

Déjà inclus dans la configuration Nginx ci-dessus.

## 🔐 Sécurité Supplémentaire

### 1. Firewall (UFW)

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

### 2. Fail2Ban

```bash
sudo apt install fail2ban
sudo systemctl start fail2ban
sudo systemctl enable fail2ban
```

### 3. Changer les Mots de Passe

Connectez-vous à l'admin et changez tous les mots de passe par défaut:

```bash
python manage.py changepassword admin
python manage.py changepassword coordonnateur
# etc.
```

## 💾 Sauvegardes

### Script de Sauvegarde Automatique

Créez `/var/www/prosmat_se/backup.sh`:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/prosmat"

# Créer le dossier de sauvegarde
mkdir -p $BACKUP_DIR

# Sauvegarder la base de données
pg_dump -U prosmat_user prosmat_db > $BACKUP_DIR/db_$DATE.sql

# Sauvegarder les fichiers media
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/prosmat_se/media/

# Supprimer les sauvegardes de plus de 30 jours
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Sauvegarde terminée: $DATE"
```

### Rendre le Script Exécutable

```bash
chmod +x /var/www/prosmat_se/backup.sh
```

### Cron pour Sauvegarde Quotidienne

```bash
sudo crontab -e
```

Ajoutez:
```
0 2 * * * /var/www/prosmat_se/backup.sh >> /var/log/prosmat_backup.log 2>&1
```

## 📊 Monitoring

### 1. Logs Django

Créez le dossier:
```bash
mkdir -p /var/www/prosmat_se/logs
```

Les logs seront dans `/var/www/prosmat_se/logs/django.log`

### 2. Logs Nginx

```bash
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 3. Logs Gunicorn

```bash
sudo journalctl -u prosmat -f
```

## 🔄 Mise à Jour de l'Application

### Script de Déploiement

Créez `deploy.sh`:

```bash
#!/bin/bash

echo "Déploiement ProSMAT..."

# Activer l'environnement virtuel
source venv/bin/activate

# Récupérer les dernières modifications
git pull origin main

# Installer les dépendances
pip install -r requirements.txt

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Appliquer les migrations
python manage.py migrate

# Redémarrer Gunicorn
sudo systemctl restart prosmat

echo "Déploiement terminé!"
```

## 📧 Configuration Email

### Gmail (pour les notifications)

1. Activez l'authentification à deux facteurs
2. Générez un mot de passe d'application
3. Configurez dans `settings_local.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'votre-email@gmail.com'
EMAIL_HOST_PASSWORD = 'mot-de-passe-app'
```

## 🧪 Tests en Production

### 1. Vérifier les URLs

```bash
curl -I https://prosmat.tg
curl -I https://prosmat.tg/admin
```

### 2. Tester la Connexion

- Ouvrez https://prosmat.tg
- Connectez-vous avec un compte
- Testez la saisie d'une réalisation

### 3. Vérifier les Logs

```bash
sudo journalctl -u prosmat -n 50
tail -f /var/www/prosmat_se/logs/django.log
```

## 📱 Performance

### 1. Activer la Compression Gzip (Nginx)

Ajoutez dans `/etc/nginx/nginx.conf`:

```nginx
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;
```

### 2. Cache Django

Dans `settings_local.py`:

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

## 🆘 Dépannage Production

### Service ne démarre pas

```bash
sudo systemctl status prosmat
sudo journalctl -u prosmat -n 100
```

### Erreur 502 Bad Gateway

- Vérifier que Gunicorn tourne
- Vérifier les permissions du socket
- Vérifier les logs Nginx

### Base de données inaccessible

```bash
sudo -u postgres psql
\l  # Lister les bases
\du # Lister les utilisateurs
```

### Fichiers statiques ne chargent pas

```bash
python manage.py collectstatic --noinput
sudo chown -R www-data:www-data /var/www/prosmat_se/staticfiles
```

## 📞 Support Production

Pour les problèmes en production:
1. Consultez les logs
2. Vérifiez les services (systemctl status)
3. Testez les connexions (base de données, réseau)
4. Contactez l'équipe technique

## ✅ Checklist Post-Déploiement

- [ ] Application accessible via HTTPS
- [ ] Tous les comptes par défaut ont de nouveaux mots de passe
- [ ] Sauvegardes automatiques configurées
- [ ] Monitoring en place
- [ ] Logs configurés
- [ ] Firewall activé
- [ ] SSL/TLS configuré
- [ ] Email configuré
- [ ] Tests de charge effectués
- [ ] Documentation à jour

## 🎉 Félicitations !

Votre application ProSMAT est maintenant en production et sécurisée !
