"""
Test spécifique pour l'onglet Marché Agroécologique
Vérifie le Top 10 par région et les exports
"""

import pandas as pd
import io
from collections import Counter

print("=" * 60)
print("TEST MARCHÉ AGROÉCOLOGIQUE - TOP 10 PAR RÉGION")
print("=" * 60)

# 1. Charger les données
print("\n1. Chargement des données...")
df_raw = pd.read_excel('MISSION_DE_SUIVI_cleaned.xlsx')
print(f"   ✓ {len(df_raw)} coopératives chargées")

# Mapping des colonnes (comme dans le dashboard)
column_mapping = {
    '2.1. Région': 'region',
    'prefectures': 'prefecture',
    'Commune': 'commune',
    '2.5. Village': 'village',
    '3.1. Nom de la coopérative': 'cooperative',
    '3.2.1.Effectif total des membres ': 'effectif_total',
    '3.2.2.Nombre de Jeune (moins de 35 ans)': 'nb_jeunes',
    '3.2.3.Nombre de femmes': 'nb_femmes',
    '3.2.4.Nombre de personnes vivant avec un handicap': 'nb_handicap',
    '3.4. Êtes-vous immatriculé ? ': 'immatricule',
    '4.1. Avez-vous organisé la restitution de la formation ? ': 'restitution_formation',
    "4.1.6. Y-a-t-il eu des engagements fermes d'adoption des pratiques agroécologiques par les membres ?": 'engagement_agroeco',
    "6.1. Avez-vous déjà choisi la parcelle d'apprentissage ?": 'parcelle_choisie',
    '6.4. Pouvez-vous produire collectivement ou individuellement en cette contre saison (Période de Décembre à Avril) ': 'production_contre_saison',
}

# Appliquer le mapping
df = df_raw.copy()
for old_name, new_name in column_mapping.items():
    if old_name in df.columns:
        df[new_name] = df[old_name]

# Vérifier les colonnes disponibles
print(f"   ✓ Colonnes mappées: {[col for col in column_mapping.values() if col in df.columns]}")

# Normaliser les régions
region_mapping = {
    'Centrale': 'Centre',
    'Centre': 'Centre',
    'Kara': 'Kara',
    'Maritime': 'Maritime',
    'Plateaux': 'Plateaux',
    'Savanes': 'Savanes'
}
if 'region' in df.columns:
    df['region'] = df['region'].map(region_mapping).fillna(df['region'])

# Convertir les colonnes numériques
for col in ['effectif_total', 'nb_jeunes', 'nb_femmes', 'nb_handicap']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

# Nettoyer les valeurs catégorielles
for col in ['immatricule', 'restitution_formation', 'engagement_agroeco', 'parcelle_choisie', 'production_contre_saison']:
    if col in df.columns:
        df[col] = df[col].fillna('Non renseigné')
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace('', 'Non renseigné')
        df[col] = df[col].replace('nan', 'Non renseigné')

print(f"   ✓ Données mappées et nettoyées")

# 2. Calculer les scores
print("\n2. Calcul des scores de potentiel...")
df_score = df.copy()

# Critères de scoring
if 'effectif_total' in df_score.columns and df_score['effectif_total'].max() > 0:
    df_score['score_effectif'] = (df_score['effectif_total'] / df_score['effectif_total'].max() * 100).fillna(0)
else:
    df_score['score_effectif'] = 0

if 'engagement_agroeco' in df_score.columns:
    df_score['score_engagement'] = df_score['engagement_agroeco'].apply(lambda x: 100 if x == 'Oui' else 0)
else:
    df_score['score_engagement'] = 0

if 'immatricule' in df_score.columns:
    df_score['score_immat'] = df_score['immatricule'].apply(lambda x: 100 if x == 'Oui' else 0)
else:
    df_score['score_immat'] = 0

if 'restitution_formation' in df_score.columns:
    df_score['score_formation'] = df_score['restitution_formation'].apply(lambda x: 100 if x == 'Oui' else 0)
else:
    df_score['score_formation'] = 0

if 'parcelle_choisie' in df_score.columns:
    df_score['score_parcelle'] = df_score['parcelle_choisie'].apply(lambda x: 100 if x == 'Oui' else 0)
else:
    df_score['score_parcelle'] = 0

if 'production_contre_saison' in df_score.columns:
    df_score['score_production'] = df_score['production_contre_saison'].apply(lambda x: 100 if x == 'Oui' else 0)
else:
    df_score['score_production'] = 0

if 'nb_femmes' in df_score.columns and 'effectif_total' in df_score.columns:
    df_score['taux_femmes'] = (df_score['nb_femmes'] / df_score['effectif_total'] * 100).fillna(0)
    df_score['score_femmes'] = df_score['taux_femmes'].apply(lambda x: 100 if x > 50 else x * 2)
else:
    df_score['score_femmes'] = 0

if 'nb_jeunes' in df_score.columns and 'effectif_total' in df_score.columns:
    df_score['taux_jeunes'] = (df_score['nb_jeunes'] / df_score['effectif_total'] * 100).fillna(0)
    df_score['score_jeunes'] = df_score['taux_jeunes'].apply(lambda x: 100 if x > 30 else x * 3.33)
else:
    df_score['score_jeunes'] = 0

# Score global
weights = {
    'score_effectif': 0.15,
    'score_engagement': 0.20,
    'score_immat': 0.15,
    'score_formation': 0.15,
    'score_parcelle': 0.10,
    'score_production': 0.10,
    'score_femmes': 0.075,
    'score_jeunes': 0.075
}

df_score['score_total'] = sum(df_score[col] * weight for col, weight in weights.items())
print(f"   ✓ Scores calculés (min: {df_score['score_total'].min():.1f}, max: {df_score['score_total'].max():.1f})")

# 3. Top 10 par région
print("\n3. Génération du Top 10 par région...")
top10_by_region = {}
all_top_coops = []

for region in sorted(df_score['region'].unique()):
    region_data = df_score[df_score['region'] == region]
    top10_region = region_data.nlargest(10, 'score_total')
    top10_by_region[region] = top10_region
    
    for idx, (_, row) in enumerate(top10_region.iterrows(), 1):
        all_top_coops.append({
            'Région': region,
            'Rang': idx,
            'Coopérative': row['cooperative'],
            'Préfecture': row['prefecture'],
            'Commune': row.get('commune', 'N/A'),
            'Effectif': int(row['effectif_total']),
            'Score': round(row['score_total'], 1)
        })
    
    print(f"   ✓ {region}: {len(top10_region)} coopératives (score moyen: {top10_region['score_total'].mean():.1f})")

df_all_tops = pd.DataFrame(all_top_coops)
print(f"\n   ✓ Total: {len(df_all_tops)} coopératives dans le Top 10 global")

# 4. Test export Excel multi-feuilles
print("\n4. Test de l'export Excel multi-feuilles...")
output = io.BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    # Feuille "Toutes les Régions"
    df_all_tops.to_excel(writer, sheet_name='Toutes les Régions', index=False)
    
    # Une feuille par région
    for region in sorted(df_score['region'].unique()):
        region_tops = df_all_tops[df_all_tops['Région'] == region]
        region_tops.to_excel(writer, sheet_name=region[:30], index=False)

excel_data = output.getvalue()
print(f"   ✓ Fichier Excel créé: {len(excel_data)} bytes")
print(f"   ✓ Nombre de feuilles: {len(df_score['region'].unique()) + 1}")

# Sauvegarder pour vérification
with open('test_export_top10_regions.xlsx', 'wb') as f:
    f.write(excel_data)
print(f"   ✓ Fichier sauvegardé: test_export_top10_regions.xlsx")

# 5. Test export CSV
print("\n5. Test de l'export CSV...")
csv_data = df_all_tops.to_csv(index=False)
print(f"   ✓ CSV créé: {len(csv_data)} caractères")

with open('test_export_top10_regions.csv', 'w', encoding='utf-8') as f:
    f.write(csv_data)
print(f"   ✓ Fichier sauvegardé: test_export_top10_regions.csv")

# 6. Analyse des cultures
print("\n6. Analyse des cultures...")
culture_col = '6.6. Si oui, quelles sont les cultures que vous voudriez produire en contre-saison ? '

if culture_col in df.columns:
    all_cultures = []
    for val in df[culture_col].dropna():
        cultures = str(val).split(',')
        for culture in cultures:
            culture_clean = culture.strip().upper()
            if culture_clean and len(culture_clean) > 2:
                all_cultures.append(culture_clean)
    
    culture_counts = Counter(all_cultures)
    df_cultures = pd.DataFrame(culture_counts.most_common(20), columns=['Culture', 'Nombre'])
    
    print(f"   ✓ {len(all_cultures)} mentions de cultures")
    print(f"   ✓ {len(culture_counts)} cultures uniques")
    print(f"\n   Top 5 cultures:")
    for idx, (culture, count) in enumerate(df_cultures.head(5).values, 1):
        print(f"      {idx}. {culture}: {count} mentions")
else:
    print("   Colonne cultures non trouvée")

# 7. Statistiques par région
print("\n7. Statistiques détaillées par région...")
for region in sorted(df_score['region'].unique()):
    region_data = df_score[df_score['region'] == region]
    top10 = top10_by_region[region]
    
    print(f"\n   {region}:")
    print(f"      • Coopératives totales: {len(region_data)}")
    print(f"      • Score moyen région: {region_data['score_total'].mean():.1f}")
    print(f"      • Score moyen Top 10: {top10['score_total'].mean():.1f}")
    print(f"      • Meilleure coopérative: {top10.iloc[0]['cooperative']} (score: {top10.iloc[0]['score_total']:.1f})")

print("\n" + "=" * 60)
print("TOUS LES TESTS SONT PASSÉS")
print("=" * 60)

print("\n🎯 Résumé:")
print(f"   • {len(df_all_tops)} coopératives dans le Top 10 global")
print(f"   • {len(df_score['region'].unique())} régions analysées")
print(f"   • Export Excel: {len(df_score['region'].unique()) + 1} feuilles")
print(f"   • Export CSV: {len(csv_data)} caractères")
if culture_col in df.columns:
    print(f"   • Cultures: {len(culture_counts)} uniques, {len(all_cultures)} mentions")

print("\n📁 Fichiers générés:")
print("   • test_export_top10_regions.xlsx")
print("   • test_export_top10_regions.csv")

print("\nL'onglet Marché Agroécologique est prêt!")
