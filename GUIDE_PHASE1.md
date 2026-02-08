# 🚀 Guide Rapide - Phase 1

## 🎯 Nouvelles Fonctionnalités

### 1. Désagrégation par Genre

**Comment l'utiliser :**
1. Allez dans **Saisie**
2. Remplissez le formulaire :
   - Valeur Réalisée : 100
   - Hommes : 45
   - Femmes : 55
3. Enregistrez

**Validation automatique :**
- ✅ Si Total = Hommes + Femmes → OK
- ⚠️ Si Total ≠ Hommes + Femmes → Alerte créée

---

### 2. Synthèse Nationale

**Comment y accéder :**
1. Connectez-vous comme **coordonnateur** ou **evaluateur**
2. Menu : **Synthèse Nationale** 🌍
3. Sélectionnez une période

**Ce que vous voyez :**
- 📊 Agrégation des 5 régions
- 🎯 % d'atteinte par indicateur
- 👥 Désagrégation Hommes/Femmes
- 📈 Écarts par rapport aux cibles
- 🎨 Codes couleur :
  - 🟢 Vert : ≥ 100% (Atteint)
  - 🟠 Orange : 50-99% (En cours)
  - 🔴 Rouge : < 50% (En retard)

---

### 3. Contrôle Qualité

**Comment y accéder :**
1. Menu : **Contrôle Qualité** 🛡️

**Types d'alertes :**
- ⚠️ **EXCÈS** : Réalisé > Cible
- 🔴 **NÉGATIF** : Valeurs négatives
- ❓ **VIDE** : Données manquantes
- ⚠️ **INCOHÉRENT** : Total ≠ Hommes + Femmes

**Actions possibles :**
- ✏️ Modifier la réalisation
- ✅ Marquer comme résolu
- 🔍 Filtrer par région/période/type

---

### 4. Calculs Automatiques

**Automatiquement calculés :**
- 📊 **Cumul** : Somme des périodes précédentes
- 📈 **% Atteinte** : (Réalisé / Cible) × 100
- 📉 **Écart** : Cible - Réalisé
- 👥 **% Femmes** : (Femmes / Total) × 100

**Aucune action requise !** Tout est automatique.

---

## 🧪 Tester avec Données de Test

**Créer des données de test :**
```bash
.\venv_prosmat\Scripts\python.exe manage.py creer_donnees_test
```

**Résultat :**
- 25 réalisations créées
- 5 indicateurs × 5 régions
- Désagrégation par genre incluse
- Contrôle qualité effectué

---

## 👥 Comptes à Utiliser

### Pour Synthèse Nationale et Contrôle Qualité
```
Username: coordonnateur
Password: prosmat2026
```
ou
```
Username: evaluateur
Password: prosmat2026
```

### Pour Saisie Régionale
```
Username: charge_maritime
Password: prosmat2026
```

---

## 🔧 Commandes Utiles

### Créer des données de test
```bash
python manage.py creer_donnees_test
```

### Réimporter les indicateurs
```bash
python manage.py import_excel
```

### Vérifier le système
```bash
python manage.py check
```

---

## 🐛 Résolution de Problèmes

### Erreur "NoneType"
**Solution :** Corrigée dans `monitoring/utils.py`
Rafraîchissez la page.

### Pas de données dans Synthèse
**Solution :** Créez des données de test
```bash
python manage.py creer_donnees_test
```

### Alertes ne s'affichent pas
**Solution :** Les alertes sont créées automatiquement à la saisie.
Saisissez une réalisation avec incohérence pour tester.

---

## 📊 Exemples de Cas d'Usage

### Cas 1 : Saisie Normale
```
Indicateur : GAFSP#1
Période : T1 2026
Valeur : 100
Hommes : 45
Femmes : 55
```
✅ Résultat : Enregistré sans alerte

### Cas 2 : Incohérence Genre
```
Indicateur : GAFSP#1
Période : T1 2026
Valeur : 100
Hommes : 40
Femmes : 50
```
⚠️ Résultat : Alerte "Incohérence" créée

### Cas 3 : Excès
```
Indicateur : GAFSP#1 (Cible: 9885)
Cumul réalisé : 10000
```
⚠️ Résultat : Alerte "Excès" créée

---

## 🎯 Prochaines Étapes

1. ✅ Tester toutes les fonctionnalités
2. ✅ Créer des données réelles
3. ✅ Former les utilisateurs
4. ✅ Collecter les retours
5. 🚀 Passer à la Phase 2

---

## 📞 Support

**Erreur ?** Consultez :
- PHASE1_TERMINEE.md
- NOUVELLES_FONCTIONNALITES.md

**Questions ?** Contactez l'équipe technique.

---

**Phase 1 - Opérationnelle !** 🎉
