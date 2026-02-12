# 🔍 Comment Vérifier les Données sur Neon

## Méthode 1: Via Script Python (RECOMMANDÉ)

### Configuration
1. Ajoutez DATABASE_URL dans `.env`:
```env
DATABASE_URL=postgresql://neondb_owner:npg_KAWbvj8u0HlY@ep-little-morning-ab9ty32l-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require
```

2. Exécutez le script:
```bash
python verifier_neon.py
```

### Ce que le script vérifie:
- ✅ Connexion à Neon
- ✅ Version PostgreSQL
- ✅ Nom de la base de données
- ✅ Liste des tables
- ✅ Nombre d'enregistrements par table
- ✅ Exemples de données
- ✅ Comptes admin (tatchida@gmail.com, admin@prosmat.tg)

---

## Méthode 2: Via Neon Console (Interface Web)

### Étapes:
1. Allez sur: https://console.neon.tech
2. Connectez-vous avec votre compte
3. Sélectionnez votre projet: **neondb**
4. Cliquez sur **SQL Editor** dans le menu de gauche
5. Exécutez ces requêtes:

### Vérifier les tables:
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;
```

### Compter les données:
```sql
-- Utilisateurs
SELECT COUNT(*) as total_users FROM accounts_user;

-- Composantes
SELECT COUNT(*) as total_composantes FROM monitoring_composante;

-- Indicateurs
SELECT COUNT(*) as total_indicateurs FROM monitoring_indicateur;

-- Périodes
SELECT COUNT(*) as total_periodes FROM monitoring_periode;

-- Réalisations
SELECT COUNT(*) as total_realisations FROM monitoring_realisation;
```

### Vérifier les admins:
```sql
SELECT email, username, role, is_staff, is_superuser 
FROM accounts_user 
WHERE email IN ('tatchida@gmail.com', 'admin@prosmat.tg');
```

### Voir toutes les données:
```sql
-- Toutes les composantes
SELECT * FROM monitoring_composante ORDER BY ordre;

-- Tous les indicateurs
SELECT code, libelle, type_indicateur, niveau 
FROM monitoring_indicateur 
ORDER BY code;

-- Tous les utilisateurs
SELECT email, username, role, is_staff 
FROM accounts_user 
ORDER BY email;
```

---

## Méthode 3: Via psql (Ligne de commande)

### Installation psql:
- **Windows**: Téléchargez PostgreSQL depuis https://www.postgresql.org/download/windows/
- **Mac**: `brew install postgresql`
- **Linux**: `sudo apt install postgresql-client`

### Connexion:
```bash
psql "postgresql://neondb_owner:npg_KAWbvj8u0HlY@ep-little-morning-ab9ty32l-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require"
```

### Commandes utiles:
```sql
-- Lister les tables
\dt

-- Compter les enregistrements
SELECT 
  'users' as table_name, COUNT(*) FROM accounts_user
UNION ALL
SELECT 'composantes', COUNT(*) FROM monitoring_composante
UNION ALL
SELECT 'indicateurs', COUNT(*) FROM monitoring_indicateur
UNION ALL
SELECT 'periodes', COUNT(*) FROM monitoring_periode;

-- Quitter
\q
```

---

## Méthode 4: Via Render Logs

### Étapes:
1. Allez sur: https://dashboard.render.com
2. Sélectionnez votre service **prosmat**
3. Cliquez sur **Logs** dans le menu
4. Cherchez les lignes du build:

```
📊 Chargement des données initiales...
✅ Créé: Composante 1: Amélioration de la productivité agricole
✅ Créé: Composante 2: Développement des chaînes de valeur
...
✅ DONNÉES INITIALES CHARGÉES AVEC SUCCÈS!
Résumé:
   - Composantes: 4
   - Sous-composantes: 6
   - Indicateurs: 5
   - Périodes: 9
   - Utilisateurs: 2
```

Si vous voyez:
```
⚠️  Des données existent déjà. Chargement ignoré.
```
→ Les données sont déjà dans Neon!

---

## Méthode 5: Via l'Application Render

### Une fois déployé:
1. Allez sur votre URL Render (ex: https://prosmat-xxx.onrender.com)
2. Connectez-vous avec **admin@prosmat.tg** / **ProSMAT2026!**
3. Allez sur **/admin/**
4. Vérifiez les sections:
   - **Accounts** → **Users** (devrait avoir 2 utilisateurs)
   - **Monitoring** → **Composantes** (devrait avoir 4 composantes)
   - **Monitoring** → **Indicateurs** (devrait avoir 5 indicateurs)
   - **Monitoring** → **Périodes** (devrait avoir 9 périodes)

---

## Résultats Attendus

### Si les données sont chargées:
```
✅ Utilisateurs: 2 enregistrements
   - admin@prosmat.tg (ADMIN)
   - tatchida@gmail.com (ADMIN)

✅ Composantes: 4 enregistrements
   - Composante 1: Amélioration de la productivité agricole
   - Composante 2: Développement des chaînes de valeur
   - Composante 3: Renforcement des capacités
   - Composante 4: Coordination et gestion du projet

✅ Sous-composantes: 6 enregistrements

✅ Indicateurs: 5 enregistrements
   - IND-1.1.1: Nombre de bénéficiaires directs du projet
   - IND-1.1.2: Nombre d'hectares aménagés
   - IND-1.2.1: Nombre de producteurs ayant reçu des intrants
   - IND-2.1.1: Nombre d'unités de transformation créées
   - IND-3.1.1: Nombre de producteurs formés

✅ Périodes: 9 enregistrements
   - 2024 T1, T2, T3, T4
   - 2025 T1, T2, T3, T4
   - 2026 T1

✅ Réalisations: 0 enregistrements (normal au début)
```

### Si la base est vide:
```
⚠️  Utilisateurs: 0 enregistrements
⚠️  Composantes: 0 enregistrements
⚠️  Indicateurs: 0 enregistrements
⚠️  Périodes: 0 enregistrements
```

→ Il faut exécuter: `python manage.py charger_donnees`

---

## Dépannage

### Problème: "Aucune donnée trouvée"

**Solution 1**: Vérifier les logs Render
- Les données ont-elles été chargées au build?
- Y a-t-il eu des erreurs?

**Solution 2**: Charger manuellement (si shell disponible)
```bash
python manage.py charger_donnees
```

**Solution 3**: Vérifier DATABASE_URL
- Est-ce que Render utilise bien Neon?
- DATABASE_URL est-il correctement configuré?

### Problème: "Connexion refusée"

**Solution**: Vérifier DATABASE_URL
```bash
# Dans .env
DATABASE_URL=postgresql://neondb_owner:npg_KAWbvj8u0HlY@ep-little-morning-ab9ty32l-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require
```

### Problème: "Tables n'existent pas"

**Solution**: Exécuter les migrations
```bash
python manage.py migrate
```

---

## Commandes Rapides

### Vérification complète:
```bash
python verifier_neon.py
```

### Charger les données:
```bash
python manage.py charger_donnees
```

### Compter rapidement:
```bash
python manage.py shell
>>> from monitoring.models import *
>>> from accounts.models import User
>>> print(f"Users: {User.objects.count()}")
>>> print(f"Composantes: {Composante.objects.count()}")
>>> print(f"Indicateurs: {Indicateur.objects.count()}")
>>> exit()
```

---

## Checklist de Vérification

- [ ] Connexion à Neon réussie
- [ ] Tables créées (django_migrations, accounts_user, monitoring_*, etc.)
- [ ] 2 utilisateurs admin (tatchida@gmail.com, admin@prosmat.tg)
- [ ] 4 composantes
- [ ] 6 sous-composantes
- [ ] 5 indicateurs
- [ ] 9 périodes
- [ ] Comptes admin ont role='ADMIN', is_staff=True, is_superuser=True

---

**Développé avec ❤️ pour ProSMAT - Togo**

*Mis à jour le: 11 février 2026*
