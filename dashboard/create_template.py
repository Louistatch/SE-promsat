#!/usr/bin/env python3
"""
Script pour créer un template Excel vide pour le Dashboard ProSMAT
"""

import pandas as pd

# Définir les colonnes avec les noms exacts requis
columns = [
    '2.1. Région',
    'prefectures',
    'Commune',
    '2.4. Canton',
    '2.5. Village',
    '3.1. Nom de la coopérative',
    '3.2.1.Effectif total des membres ',  # Espace à la fin
    '3.2.2.Nombre de Jeune (moins de 35 ans)',
    '3.2.3.Nombre de femmes',
    '3.2.4.Nombre de personnes vivant avec un handicap',
    '_6.3. Coordonnées géographiques delaparcelle_latitude',
    '_6.3. Coordonnées géographiques delaparcelle_longitude',
    '3.4. Êtes-vous immatriculé ? ',  # Espace à la fin
    '4.1. Avez-vous organisé la restitution de la formation ? ',  # Espace à la fin
    "4.1.6. Y-a-t-il eu des engagements fermes d'adoption des pratiques agroécologiques par les membres ?",
    "6.1. Avez-vous déjà choisi la parcelle d'apprentissage ?",
    '6.4. Pouvez-vous produire collectivement ou individuellement en cette contre saison (Période de Décembre à Avril) ',  # Espace à la fin
    "5.1. La coopérative a-t-elle reçu du matériel de production d'intrants ?",
    'Nom et prénoms du CRP',
    '1.Date de la visite',
    '3.3.1.Nom du président',
    '3.3.2.Contact du président',
    '6.6. Si oui, quelles sont les cultures que vous voudriez produire en contre-saison ? '
]

# Créer un DataFrame vide avec ces colonnes
df_template = pd.DataFrame(columns=columns)

# Ajouter une ligne d'exemple
exemple = {
    '2.1. Région': 'Kara',
    'prefectures': 'Kozah',
    'Commune': 'Kara',
    '2.4. Canton': 'Kara',
    '2.5. Village': 'Kara-Centre',
    '3.1. Nom de la coopérative': 'Exemple Coopérative',
    '3.2.1.Effectif total des membres ': 50,
    '3.2.2.Nombre de Jeune (moins de 35 ans)': 20,
    '3.2.3.Nombre de femmes': 30,
    '3.2.4.Nombre de personnes vivant avec un handicap': 2,
    '_6.3. Coordonnées géographiques delaparcelle_latitude': 9.5511,
    '_6.3. Coordonnées géographiques delaparcelle_longitude': 1.1864,
    '3.4. Êtes-vous immatriculé ? ': 'Oui',
    '4.1. Avez-vous organisé la restitution de la formation ? ': 'Oui',
    "4.1.6. Y-a-t-il eu des engagements fermes d'adoption des pratiques agroécologiques par les membres ?": 'Oui',
    "6.1. Avez-vous déjà choisi la parcelle d'apprentissage ?": 'Oui',
    '6.4. Pouvez-vous produire collectivement ou individuellement en cette contre saison (Période de Décembre à Avril) ': 'Oui',
    "5.1. La coopérative a-t-elle reçu du matériel de production d'intrants ?": 'Oui',
    'Nom et prénoms du CRP': 'Jean DUPONT',
    '1.Date de la visite': '2025-02-11',
    '3.3.1.Nom du président': 'Marie KOUASSI',
    '3.3.2.Contact du président': '+228 90 00 00 00',
    '6.6. Si oui, quelles sont les cultures que vous voudriez produire en contre-saison ? ': 'Maïs, Tomate, Oignon'
}

df_template = pd.DataFrame([exemple])

# Sauvegarder le template
df_template.to_excel('TEMPLATE_VIDE_ProSMAT.xlsx', index=False)

print("✓ Template créé : TEMPLATE_VIDE_ProSMAT.xlsx")
print(f"  Colonnes : {len(columns)}")
print("  Ligne d'exemple incluse")
print("\nVous pouvez maintenant :")
print("1. Ouvrir le fichier dans Excel")
print("2. Supprimer la ligne d'exemple")
print("3. Ajouter vos propres données")
print("4. Charger le fichier dans le dashboard")
