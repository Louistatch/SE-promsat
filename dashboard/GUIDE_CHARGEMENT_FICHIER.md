# Guide de Chargement de Fichier Excel

## 📤 Nouvelle Fonctionnalité : Chargement de Fichier Personnalisé

Le dashboard permet maintenant de charger vos propres fichiers Excel pour analyser vos données de coopératives.

---

## 🚀 Comment Utiliser

### Étape 1 : Lancer le Dashboard
```bash
streamlit run dashboard_sig_streamlit.py
```

### Étape 2 : Choisir la Source de Données

Dans la barre latérale gauche, vous verrez une section **"Chargement des Données"** avec deux options :

1. **Fichier par défaut** : Utilise `MISSION_DE_SUIVI_cleaned.xlsx`
2. **Charger un fichier Excel** : Permet de charger votre propre fichier

### Étape 3 : Télécharger le Template (Nouveau !)

Lorsque vous sélectionnez **"Charger un fichier Excel"**, un bouton apparaît automatiquement :

**📥 Télécharger le Template Excel**

1. Cliquez sur ce bouton pour télécharger le fichier template
2. Le fichier `TEMPLATE_ProSMAT_Cooperatives.xlsx` sera téléchargé
3. Ouvrez-le dans Excel
4. Remplissez-le avec vos données (vous pouvez supprimer les exemples)
5. Sauvegardez le fichier

### Étape 4 : Charger Votre Fichier

1. Sélectionnez **"Charger un fichier Excel"**
2. **Téléchargez le template** en cliquant sur le bouton "📥 Télécharger le Template Excel"
3. Remplissez le template avec vos données
4. Cliquez sur **"Browse files"** ou glissez-déposez votre fichier
5. Le fichier doit être au format `.xlsx` ou `.xls`
6. Une fois chargé, le nom du fichier s'affiche avec un message de confirmation

### Étape 5 : Analyser Vos Données

Le dashboard charge automatiquement vos données et vous pouvez :
- Utiliser tous les filtres
- Visualiser les cartes
- Générer des analyses
- Exporter les résultats

---

## 📋 Format du Fichier Excel

### Colonnes Obligatoires

Votre fichier Excel doit contenir au minimum :

**Géographie :**
- `2.1. Région`
- `prefectures`
- `Commune`
- `2.5. Village`

**Coopérative :**
- `3.1. Nom de la coopérative`
- `3.2.1.Effectif total des membres `

**Coordonnées GPS :**
- `_6.3. Coordonnées géographiques delaparcelle_latitude`
- `_6.3. Coordonnées géographiques delaparcelle_longitude`

### Colonnes Optionnelles

- `3.2.2.Nombre de Jeune (moins de 35 ans)`
- `3.2.3.Nombre de femmes`
- `3.2.4.Nombre de personnes vivant avec un handicap`
- `3.4. Êtes-vous immatriculé ? `
- `4.1. Avez-vous organisé la restitution de la formation ? `
- `4.1.6. Y-a-t-il eu des engagements fermes d'adoption des pratiques agroécologiques par les membres ?`
- `6.1. Avez-vous déjà choisi la parcelle d'apprentissage ?`
- `Nom et prénoms du CRP`

---

## ✅ Validation des Données

Le dashboard effectue automatiquement :

1. **Nettoyage des coordonnées GPS**
   - Suppression des coordonnées invalides (0, 0)
   - Vérification des limites géographiques du Togo
   - Latitude : entre 5 et 12
   - Longitude : entre -1 et 2

2. **Conversion des types**
   - Effectifs convertis en nombres entiers
   - Valeurs manquantes remplacées par 0 ou "Non renseigné"

3. **Normalisation**
   - "Centrale" → "Centre"
   - Nettoyage des espaces
   - Standardisation des réponses Oui/Non

---

## 🎯 Cas d'Usage

### Cas 1 : Nouvelle Mission de Terrain
Vous avez collecté de nouvelles données sur le terrain et voulez les analyser immédiatement.

**Solution :**
1. Exportez vos données au format Excel
2. Assurez-vous que les colonnes correspondent au format requis
3. Chargez le fichier dans le dashboard
4. Analysez et exportez les résultats

### Cas 2 : Comparaison de Périodes
Vous voulez comparer les données de deux missions différentes.

**Solution :**
1. Chargez le fichier de la première mission
2. Exportez les analyses (PNG, Excel, CSV)
3. Chargez le fichier de la deuxième mission
4. Exportez les analyses
5. Comparez les résultats

### Cas 3 : Données Partielles
Vous avez des données pour une seule région ou préfecture.

**Solution :**
1. Préparez votre fichier Excel avec les données disponibles
2. Chargez le fichier
3. Le dashboard s'adapte automatiquement au nombre de coopératives

---

## 🔧 Résolution de Problèmes

### Problème : "Veuillez charger un fichier Excel"
**Solution :** Vous avez sélectionné "Charger un fichier Excel" mais n'avez pas encore uploadé de fichier. Cliquez sur "Browse files" pour charger votre fichier.

### Problème : Erreur lors du chargement
**Causes possibles :**
- Format de fichier incorrect (doit être .xlsx ou .xls)
- Colonnes manquantes ou mal nommées
- Données corrompues

**Solution :**
1. Vérifiez que votre fichier est au format Excel
2. Comparez les noms de colonnes avec `MISSION_DE_SUIVI_cleaned.xlsx`
3. Consultez `TEMPLATE_EXCEL_FORMAT.md` pour le format détaillé

### Problème : Aucune coopérative affichée sur la carte
**Cause :** Coordonnées GPS manquantes ou invalides

**Solution :**
1. Vérifiez que les colonnes latitude/longitude existent
2. Assurez-vous que les coordonnées sont dans les limites du Togo
3. Vérifiez qu'il n'y a pas de valeurs (0, 0)

### Problème : Certaines colonnes manquent dans les analyses
**Cause :** Colonnes optionnelles absentes du fichier

**Solution :**
- Le dashboard remplit automatiquement les colonnes manquantes avec des valeurs par défaut
- Pour des analyses complètes, ajoutez toutes les colonnes recommandées

---

## 📊 Exemple de Fichier

Téléchargez `MISSION_DE_SUIVI_cleaned.xlsx` comme template de référence.

Structure minimale :

| 2.1. Région | prefectures | Commune | 3.1. Nom de la coopérative | latitude | longitude |
|-------------|-------------|---------|----------------------------|----------|-----------|
| Kara        | Kozah       | Kara    | Coopérative Test           | 9.5511   | 1.1864    |

---

## 💡 Conseils

1. **Utilisez le fichier par défaut comme template**
   - Copiez la structure exacte
   - Remplacez les données par les vôtres

2. **Vérifiez vos coordonnées GPS**
   - Utilisez un GPS ou Google Maps
   - Format décimal (ex: 9.5511, 1.1864)

3. **Testez avec un petit fichier d'abord**
   - Chargez 5-10 coopératives pour tester
   - Vérifiez que tout fonctionne
   - Puis chargez le fichier complet

4. **Sauvegardez vos fichiers**
   - Gardez une copie de vos données originales
   - Le dashboard ne modifie pas votre fichier

---

## 📚 Documentation Complémentaire

- **TEMPLATE_EXCEL_FORMAT.md** - Format détaillé du fichier Excel
- **GUIDE_DEMARRAGE_RAPIDE.md** - Guide général du dashboard
- **README_COMPLET.md** - Documentation technique complète

---

## 👨‍💻 Support

Pour toute question sur le chargement de fichiers :

**TATCHIDA Louis**
- MSc Agronomie
- MSc Ingénierie Financière adaptée à l'Agriculture
- Data Analyst

---

**Version** : 3.1  
**Date** : Février 2025  
**Fonctionnalité** : Chargement de fichier Excel personnalisé
