# 🔍 DÉBOGAGE ERREUR 500 SUR RENDER

## Étape 1: Vérifier les Logs

Sur Render:
1. Allez dans votre Web Service
2. Cliquez sur "**Logs**"
3. Cherchez les erreurs (lignes rouges)

**Erreurs courantes**:
- `ModuleNotFoundError` - Module manquant
- `ImproperlyConfigured` - Configuration Django incorrecte
- `OperationalError` - Problème base de données
- `ALLOWED_HOSTS` - Domaine non autorisé

---

## Étape 2: Vérifications Rapides

### A. Variables d'Environnement

Vérifiez que TOUTES ces variables sont configurées:

```
DJANGO_SETTINGS_MODULE=config.settings_deploy
SECRET_KEY=[votre clé générée]
DEBUG=False
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=[URL PostgreSQL]
PYTHON_VERSION=3.11.9
```

### B. ALLOWED_HOSTS

L'erreur 500 est souvent causée par ALLOWED_HOSTS.

**Solution**: Ajoutez votre domaine exact:

```
ALLOWED_HOSTS=prosmat-se.onrender.com,.onrender.com,localhost
```

---

## Étape 3: Solutions Rapides

### Solution 1: Activer DEBUG Temporairement

**⚠️ TEMPORAIRE SEULEMENT**

Dans les variables d'environnement:
```
DEBUG=True
```

Cela affichera l'erreur exacte. **Remettez à False après!**

### Solution 2: Vérifier DATABASE_URL

1. Allez dans votre base PostgreSQL
2. Copiez l'URL "**Internal Database URL**" (pas External)
3. Collez-la dans la variable `DATABASE_URL`

### Solution 3: Collecter les Fichiers Statiques

Dans le Shell Render:
```bash
python manage.py collectstatic --noinput
```

### Solution 4: Vérifier les Migrations

Dans le Shell Render:
```bash
python manage.py migrate
```

---

## Étape 4: Configuration settings_deploy.py

Le problème peut venir de `config/settings_deploy.py`.

**Vérifiez**:
1. `ALLOWED_HOSTS` inclut votre domaine
2. `DATABASE_URL` est bien configuré
3. `STATIC_ROOT` est défini

---

## Étape 5: Commandes de Diagnostic

Dans le Shell Render, exécutez:

```bash
# Vérifier la configuration
python manage.py check

# Vérifier les migrations
python manage.py showmigrations

# Tester la connexion DB
python manage.py dbshell
```

---

## 🆘 Si Rien ne Fonctionne

### Option A: Utiliser settings.py Standard

Changez la variable d'environnement:
```
DJANGO_SETTINGS_MODULE=config.settings
```

Au lieu de `config.settings_deploy`

### Option B: Simplifier ALLOWED_HOSTS

Dans `config/settings_deploy.py`, changez:
```python
ALLOWED_HOSTS = ['*']  # Temporaire pour tester
```

---

## 📋 Checklist de Vérification

- [ ] Logs consultés
- [ ] Variables d'environnement vérifiées
- [ ] DATABASE_URL correct (Internal URL)
- [ ] ALLOWED_HOSTS inclut le domaine
- [ ] Migrations exécutées
- [ ] Fichiers statiques collectés
- [ ] DEBUG=True temporairement pour voir l'erreur

---

## 🔧 Configuration Recommandée

### Variables d'Environnement Minimales

```env
DJANGO_SETTINGS_MODULE=config.settings
SECRET_KEY=votre-cle-secrete
DEBUG=False
ALLOWED_HOSTS=prosmat-se.onrender.com,.onrender.com
DATABASE_URL=postgresql://...
```

---

**Dites-moi ce que vous voyez dans les logs Render!**
