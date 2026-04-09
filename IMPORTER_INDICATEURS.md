# 📊 Importer les Indicateurs depuis Excel vers Neon

## 🎯 Objectif

Importer tous les indicateurs du fichier `Indicateurs_ProSMAT_Complet.xlsx` vers la base de données Neon PostgreSQL.

---

## 📋 Prérequis

### 1. Installer pandas et openpyxl
```bash
pip install pandas openpyxl
```

### 2. Configurer DATABASE_URL
Dans ton fichier `.env`:
```env
DATABASE_URL=postgresql://neondb_owner:npg_KAWbvj8u0HlY@ep-little-morning-ab9ty32l-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require
```

### 3. Avoir le fichier Excel
Chemin: `C:\Users\HP\Downloads\prosmat_se\Indicateurs_ProSMAT_Complet.xlsx`

---

## 🚀 Utilisation

### Méthode 1: Avec le chemin par défaut
```bash
python importer_indicateurs_excel.py
```

Le script utilisera automatiquement:
`C:\Users\HP\Downloads\prosmat_se\Indicateurs_ProSMAT_Complet.xlsx`

### Méthode 2: Avec un autre fichier
```bash
python importer_indicateurs_excel.py "C:\chemin\vers\ton\fichier.xlsx"
```

---

## 📊 Format du Fichier Excel

### Colonnes Attendues

| Colonne | Obligatoire | Description | Exemple |
|---------|-------------|-------------|---------|
| Code | ✅ Oui | Code unique de l'indicateur | IND-1.1.1 |
| Libellé | ✅ Oui | Description de l'indicateur | Nombre de bénéficiaires directs |
| Composante | ⚠️ Optionnel | Nom de la composante | Composante 1: Amélioration... |
| Sous-composante | ⚠️ Optionnel | Nom de la sous-composante | 1.1 Infrastructures agricoles |
| Type | ⚠️ Optionnel | QUANTITATIF ou QUALITATIF | QUANTITATIF |
| Niveau | ⚠️ Optionnel | IMPACT, EFFET, EXTRANT, etc. | IMPACT |
| Unité | ⚠️ Optionnel | Unité de mesure | Personnes |
| Cible | ⚠️ Optionnel | Valeur cible | 50000 |

### Variantes de Noms de Colonnes Acceptées

Le script accepte plusieurs variantes:
- **Libellé**: `Libellé`, `libelle`, `Libelle`
- **Sous-composante**: `Sous-composante`, `Sous_composante`
- **Unité**: `Unité`, `Unite`
- **Cible**: `Cible`, `cible`

---

## 🔄 Ce que fait le Script

### 1. Lecture du Fichier
- ✅ Lit le fichier Excel
- ✅ Affiche le nombre de lignes
- ✅ Liste les colonnes disponibles

### 2. Traitement des Données
Pour chaque ligne:
- ✅ Nettoie et normalise les textes
- ✅ Trouve ou crée la composante
- ✅ Trouve ou crée la sous-composante
- ✅ Crée ou met à jour l'indicateur

### 3. Gestion des Doublons
- Si le **code existe déjà** → Met à jour l'indicateur
- Si le **code est nouveau** → Crée un nouvel indicateur

### 4. Résumé
- ✅ Nombre d'indicateurs créés
- 🔄 Nombre d'indicateurs mis à jour
- ❌ Nombre d'erreurs
- 📊 État final de la base

---

## 📊 Exemple de Sortie

```
======================================================================
IMPORTATION DES INDICATEURS DEPUIS EXCEL
======================================================================

📂 Lecture du fichier: C:\Users\HP\Downloads\prosmat_se\Indicateurs_ProSMAT_Complet.xlsx
✅ 45 lignes trouvées dans le fichier

📋 Colonnes disponibles: ['Code', 'Libellé', 'Composante', 'Sous-composante', 'Type', 'Niveau', 'Unité', 'Cible']

📊 État actuel de la base:
   - Composantes: 4
   - Sous-composantes: 6
   - Indicateurs: 3

🔄 Importation en cours...
----------------------------------------------------------------------
✅ Créé: IND-1.1.1 - Nombre de bénéficiaires directs du projet
✅ Créé: IND-1.1.2 - Nombre d'hectares aménagés
🔄 Mis à jour: IND-1.2.1 - Nombre de producteurs ayant reçu des intrants
✅ Créé: IND-2.1.1 - Nombre d'unités de transformation créées
...

======================================================================
✅ IMPORTATION TERMINÉE
======================================================================

📊 Résultats:
   ✅ Créés: 42
   🔄 Mis à jour: 3
   ❌ Erreurs: 0
   📈 Total traité: 45

📊 État final de la base:
   - Composantes: 4
   - Sous-composantes: 8
   - Indicateurs: 45

🎉 Les indicateurs sont maintenant sur Neon!
```

---

## ✅ Vérification après Import

### Méthode 1: Script Python
```bash
python verifier_neon.py
```

### Méthode 2: Neon Console
1. Va sur https://console.neon.tech
2. SQL Editor
3. Exécute:
```sql
SELECT COUNT(*) as total_indicateurs FROM monitoring_indicateur;
SELECT code, libelle FROM monitoring_indicateur ORDER BY code;
```

### Méthode 3: Application Web
1. Va sur ton URL Render
2. Connecte-toi comme admin
3. Va sur `/admin/monitoring/indicateur/`
4. Vérifie que tous les indicateurs sont là

---

## 🔧 Dépannage

### Problème: "Fichier non trouvé"

**Solution**: Vérifie le chemin
```bash
# Afficher le chemin complet
dir "C:\Users\HP\Downloads\prosmat_se\Indicateurs_ProSMAT_Complet.xlsx"
```

### Problème: "Erreur de lecture du fichier"

**Solutions**:
1. Ferme Excel si le fichier est ouvert
2. Vérifie que c'est bien un fichier .xlsx
3. Essaie de l'ouvrir dans Excel pour vérifier qu'il n'est pas corrompu

### Problème: "Colonne manquante"

**Solution**: Le script affiche les colonnes disponibles. Vérifie que ton Excel a au moins:
- Une colonne `Code`
- Une colonne `Libellé` (ou `libelle`)

### Problème: "Erreur de connexion à la base"

**Solution**: Vérifie DATABASE_URL dans `.env`
```bash
python verifier_neon.py
```

---

## 🔄 Réimporter les Données

Si tu veux réimporter (par exemple après avoir modifié l'Excel):

### Option 1: Mise à jour (RECOMMANDÉ)
```bash
python importer_indicateurs_excel.py
```
→ Met à jour les indicateurs existants, crée les nouveaux

### Option 2: Suppression puis réimport
```sql
-- Dans Neon Console SQL Editor
DELETE FROM monitoring_indicateur;
```
Puis:
```bash
python importer_indicateurs_excel.py
```

---

## 📝 Notes Importantes

### Sécurité des Données
- ✅ Le script utilise des **transactions**
- ✅ Si une erreur survient, **rien n'est importé**
- ✅ Les données existantes sont **préservées**

### Composantes et Sous-composantes
- Si une composante n'existe pas → Elle est créée automatiquement
- Si une sous-composante n'existe pas → Elle est créée automatiquement
- Recherche par nom partiel (20 premiers caractères)

### Types et Niveaux
Le script normalise automatiquement:
- **Types**: QUANTITATIF, QUALITATIF
- **Niveaux**: IMPACT, EFFET, EXTRANT, INTRANT, PROCESSUS

---

## 🎯 Workflow Complet

### 1. Préparer
```bash
pip install pandas openpyxl
```

### 2. Configurer
Ajouter DATABASE_URL dans `.env`

### 3. Importer
```bash
python importer_indicateurs_excel.py
```

### 4. Vérifier
```bash
python verifier_neon.py
```

### 5. Tester sur l'application
- Connecte-toi sur Render
- Va sur `/admin/monitoring/indicateur/`
- Vérifie que tous les indicateurs sont là

---

## 🚀 Après l'Import

Tes indicateurs sont maintenant:
- ✅ Sur Neon (base de données permanente)
- ✅ Accessibles depuis Render
- ✅ Disponibles pour la saisie des réalisations
- ✅ Prêts pour les rapports

---

**Développé avec ❤️ pour ProSMAT - Togo**

*Mis à jour le: 11 février 2026*
