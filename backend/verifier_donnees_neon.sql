-- Script SQL pour vérifier les données dans Neon
-- Copiez-collez ces requêtes dans Neon Console SQL Editor

-- 1. COMPTER LES DONNÉES
SELECT 
  'Composantes' as table_name, 
  COUNT(*) as total 
FROM monitoring_composante
UNION ALL
SELECT 'Sous-composantes', COUNT(*) FROM monitoring_souscomposante
UNION ALL
SELECT 'Indicateurs', COUNT(*) FROM monitoring_indicateur
UNION ALL
SELECT 'Périodes', COUNT(*) FROM monitoring_periode
UNION ALL
SELECT 'Utilisateurs', COUNT(*) FROM accounts_user
UNION ALL
SELECT 'Réalisations', COUNT(*) FROM monitoring_realisation
UNION ALL
SELECT 'Activités', COUNT(*) FROM monitoring_activite
UNION ALL
SELECT 'Rapports', COUNT(*) FROM monitoring_rapport
UNION ALL
SELECT 'Alertes Qualité', COUNT(*) FROM monitoring_alertequalite;

-- 2. VOIR LES COMPOSANTES
SELECT 
  id,
  nom,
  ordre,
  LEFT(description, 50) as description_courte
FROM monitoring_composante
ORDER BY ordre;

-- 3. VOIR LES INDICATEURS AVEC VALEURS
SELECT 
  code,
  LEFT(libelle, 60) as libelle_court,
  valeur_reference as base,
  cible_finale as cible,
  unite_mesure as unite
FROM monitoring_indicateur
WHERE cible_finale > 0
ORDER BY code
LIMIT 20;

-- 4. STATISTIQUES PAR COMPOSANTE
SELECT 
  c.nom as composante,
  COUNT(DISTINCT sc.id) as nb_sous_composantes,
  COUNT(DISTINCT i.id) as nb_indicateurs,
  SUM(i.cible_finale) as total_cibles
FROM monitoring_composante c
LEFT JOIN monitoring_souscomposante sc ON sc.composante_id = c.id
LEFT JOIN monitoring_indicateur i ON i.sous_composante_id = sc.id
GROUP BY c.id, c.nom, c.ordre
ORDER BY c.ordre;

-- 5. INDICATEURS SANS SOUS-COMPOSANTE
SELECT 
  code,
  LEFT(libelle, 60) as libelle_court,
  cible_finale
FROM monitoring_indicateur
WHERE sous_composante_id IS NULL
ORDER BY code
LIMIT 10;

-- 6. INDICATEURS AVEC VALEUR DE BASE = 0
SELECT 
  COUNT(*) as nb_indicateurs_base_zero
FROM monitoring_indicateur
WHERE valeur_reference = 0;

-- 7. INDICATEURS AVEC CIBLE > 0
SELECT 
  COUNT(*) as nb_indicateurs_avec_cible
FROM monitoring_indicateur
WHERE cible_finale > 0;

-- 8. TOP 10 CIBLES LES PLUS ÉLEVÉES
SELECT 
  code,
  LEFT(libelle, 50) as libelle_court,
  cible_finale,
  unite_mesure
FROM monitoring_indicateur
WHERE cible_finale > 0
ORDER BY cible_finale DESC
LIMIT 10;

-- 9. VÉRIFIER LES UTILISATEURS ADMIN
SELECT 
  email,
  username,
  role,
  is_staff,
  is_superuser,
  is_active
FROM accounts_user
ORDER BY email;

-- 10. VÉRIFIER LES PÉRIODES
SELECT 
  annee,
  trimestre,
  date_debut,
  date_fin,
  cloture
FROM monitoring_periode
ORDER BY annee DESC, trimestre DESC;

-- 11. INDICATEURS GAFSP
SELECT 
  code,
  LEFT(libelle, 60) as libelle_court,
  valeur_reference,
  cible_finale,
  unite_mesure
FROM monitoring_indicateur
WHERE code LIKE 'GAFSP%'
ORDER BY code;

-- 12. RÉSUMÉ COMPLET
SELECT 
  'Total Composantes' as metric, 
  COUNT(*)::text as value 
FROM monitoring_composante
UNION ALL
SELECT 'Total Indicateurs', COUNT(*)::text FROM monitoring_indicateur
UNION ALL
SELECT 'Indicateurs avec Cible > 0', COUNT(*)::text 
FROM monitoring_indicateur WHERE cible_finale > 0
UNION ALL
SELECT 'Indicateurs Base = 0', COUNT(*)::text 
FROM monitoring_indicateur WHERE valeur_reference = 0
UNION ALL
SELECT 'Somme Toutes Cibles', SUM(cible_finale)::text 
FROM monitoring_indicateur WHERE cible_finale > 0;
