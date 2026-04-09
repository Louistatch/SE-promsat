# Format du Fichier Excel pour le Dashboard

## Structure Requise

Le fichier Excel doit contenir les colonnes suivantes (les noms exacts sont importants) :

### Colonnes Géographiques
- `2.1. Région` - Nom de la région (Centre, Kara, Maritime, Plateaux, Savanes)
- `prefectures` - Nom de la préfecture
- `Commune` - Nom de la commune
- `2.4. Canton` - Nom du canton (optionnel)
- `2.5. Village` - Nom du village

### Informations Coopérative
- `3.1. Nom de la coopérative` - Nom de la coopérative
- `3.2.1.Effectif total des membres ` - Nombre total de membres (avec espace à la fin)
- `3.2.2.Nombre de Jeune (moins de 35 ans)` - Nombre de jeunes
- `3.2.3.Nombre de femmes` - Nombre de femmes
- `3.2.4.Nombre de personnes vivant avec un handicap` - Nombre de personnes handicapées

### Coordonnées GPS
- `_6.3. Coordonnées géographiques delaparcelle_latitude` - Latitude (entre 5 et 12)
- `_6.3. Coordonnées géographiques delaparcelle_longitude` - Longitude (entre -1 et 2)

### Statuts et Indicateurs
- `3.4. Êtes-vous immatriculé ? ` - Oui/Non (avec espace à la fin)
- `4.1. Avez-vous organisé la restitution de la formation ? ` - Oui/Non (avec espace à la fin)
- `4.1.6. Y-a-t-il eu des engagements fermes d'adoption des pratiques agroécologiques par les membres ?` - Oui/Non
- `6.1. Avez-vous déjà choisi la parcelle d'apprentissage ?` - Oui/Non
- `6.4. Pouvez-vous produire collectivement ou individuellement en cette contre saison (Période de Décembre à Avril) ` - Oui/Non (avec espace à la fin)
- `5.1. La coopérative a-t-elle reçu du matériel de production d'intrants ?` - Oui/Non

### Informations Supplémentaires
- `Nom et prénoms du CRP` - Nom de l'agent CRP
- `1.Date de la visite` - Date de la visite
- `3.3.1.Nom du président` - Nom du président
- `3.3.2.Contact du président` - Contact du président
- `6.6. Si oui, quelles sont les cultures que vous voudriez produire en contre-saison ? ` - Liste des cultures (séparées par des virgules)

## Notes Importantes

1. **Espaces dans les noms de colonnes** : Certaines colonnes ont des espaces à la fin de leur nom. C'est important pour la compatibilité.

2. **Valeurs acceptées** :
   - Pour les questions Oui/Non : "Oui", "Non", ou vide
   - Pour les effectifs : Nombres entiers positifs
   - Pour les coordonnées GPS : Nombres décimaux

3. **Coordonnées GPS** :
   - Latitude : entre 5 et 12 (pour le Togo)
   - Longitude : entre -1 et 2 (pour le Togo)
   - Les coopératives sans coordonnées valides seront exclues des cartes

4. **Régions** :
   - Les noms doivent correspondre aux régions du Togo
   - "Centrale" sera automatiquement converti en "Centre"

## Exemple de Données

| 2.1. Région | prefectures | Commune | 2.5. Village | 3.1. Nom de la coopérative | 3.2.1.Effectif total des membres  | latitude | longitude |
|-------------|-------------|---------|--------------|----------------------------|-----------------------------------|----------|-----------|
| Kara        | Kozah       | Kara    | Kara-Centre  | Coopérative Test           | 50                                | 9.5511   | 1.1864    |
| Plateaux    | Kloto       | Kpalimé | Agomé        | Union des Producteurs      | 75                                | 6.9000   | 0.6333    |

## Validation

Le dashboard effectue automatiquement :
- Nettoyage des coordonnées GPS invalides
- Conversion des types de données
- Normalisation des noms de régions
- Remplissage des valeurs manquantes

## Téléchargement du Template

Utilisez le fichier `MISSION_DE_SUIVI_cleaned.xlsx` comme template de référence.

## Support

Pour toute question sur le format du fichier, consultez :
- GUIDE_DEMARRAGE_RAPIDE.md
- README_COMPLET.md
- Ou contactez le développeur : TATCHIDA Louis
