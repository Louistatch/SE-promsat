# 🤝 Guide de Contribution

Merci de votre intérêt pour contribuer au projet ProSMAT!

## 📋 Table des Matières

- [Code de Conduite](#code-de-conduite)
- [Comment Contribuer](#comment-contribuer)
- [Standards de Code](#standards-de-code)
- [Processus de Pull Request](#processus-de-pull-request)
- [Conventions de Commit](#conventions-de-commit)

## 📜 Code de Conduite

Ce projet est destiné à un usage professionnel dans le cadre du Projet ProSMAT. Tous les contributeurs doivent:

- Respecter la confidentialité des données
- Maintenir un environnement professionnel
- Suivre les standards de sécurité
- Documenter leur code

## 🚀 Comment Contribuer

### Signaler un Bug

1. Vérifiez que le bug n'a pas déjà été signalé
2. Créez une Issue avec:
   - Description claire du problème
   - Étapes pour reproduire
   - Comportement attendu vs actuel
   - Captures d'écran si applicable
   - Environnement (OS, Python version, etc.)

### Proposer une Fonctionnalité

1. Créez une Issue décrivant:
   - Le besoin/problème à résoudre
   - La solution proposée
   - Les alternatives considérées
   - Impact sur le système existant

### Soumettre des Modifications

1. **Fork** le dépôt
2. **Créez une branche** pour votre fonctionnalité:
   ```bash
   git checkout -b feature/ma-fonctionnalite
   ```
3. **Faites vos modifications**
4. **Testez** votre code
5. **Commitez** avec un message descriptif
6. **Poussez** vers votre fork
7. **Créez une Pull Request**

## 💻 Standards de Code

### Python/Django

- Suivre PEP 8
- Utiliser des noms de variables descriptifs
- Commenter le code complexe
- Écrire des docstrings pour les fonctions

```python
def calculer_performance(indicateur, periode):
    """
    Calcule le taux de performance d'un indicateur pour une période.
    
    Args:
        indicateur (Indicateur): L'indicateur à évaluer
        periode (Periode): La période concernée
        
    Returns:
        float: Le taux de performance en pourcentage
    """
    # Votre code ici
    pass
```

### HTML/Templates

- Indentation: 2 espaces
- Utiliser les templates Django correctement
- Commenter les sections complexes
- Respecter l'accessibilité (ARIA labels)

### JavaScript

- Utiliser ES6+
- Commenter les fonctions
- Éviter les variables globales
- Utiliser const/let au lieu de var

### CSS

- Utiliser Bootstrap en priorité
- Classes descriptives
- Éviter les !important
- Commenter les sections

## 🔄 Processus de Pull Request

1. **Mise à jour**: Assurez-vous que votre branche est à jour avec main
   ```bash
   git pull origin main
   ```

2. **Tests**: Vérifiez que tout fonctionne
   ```bash
   python manage.py check
   python manage.py test
   ```

3. **Documentation**: Mettez à jour la documentation si nécessaire

4. **Pull Request**: Créez une PR avec:
   - Titre clair et descriptif
   - Description détaillée des changements
   - Référence aux Issues liées
   - Captures d'écran si applicable

5. **Review**: Attendez la revue de code
   - Répondez aux commentaires
   - Faites les modifications demandées
   - Demandez des clarifications si nécessaire

## 📝 Conventions de Commit

Utilisez des messages de commit clairs et descriptifs:

### Format

```
type(scope): description courte

Description détaillée (optionnelle)

Références aux issues (optionnelles)
```

### Types

- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage, style (pas de changement de code)
- `refactor`: Refactoring du code
- `test`: Ajout ou modification de tests
- `chore`: Tâches de maintenance

### Exemples

```bash
# Nouvelle fonctionnalité
git commit -m "feat(rapports): ajout de la génération automatique de rapports"

# Correction de bug
git commit -m "fix(auth): correction de l'erreur de connexion Firebase"

# Documentation
git commit -m "docs(readme): mise à jour du guide d'installation"

# Refactoring
git commit -m "refactor(views): simplification de la logique de filtrage"

# Style
git commit -m "style(templates): amélioration du design de la page d'accueil"
```

## 🧪 Tests

Avant de soumettre une PR:

```bash
# Vérifier la configuration
python manage.py check

# Lancer les tests
python manage.py test

# Vérifier le style (si flake8 est installé)
flake8 .

# Vérifier les migrations
python manage.py makemigrations --check --dry-run
```

## 📚 Documentation

Mettez à jour la documentation pour:

- Nouvelles fonctionnalités
- Changements d'API
- Nouvelles configurations
- Modifications de comportement

Fichiers à mettre à jour:
- `README.md` - Vue d'ensemble
- Guides spécifiques dans le dossier racine
- Docstrings dans le code
- Commentaires dans les templates

## 🔒 Sécurité

### Règles Importantes

1. **Ne jamais commiter**:
   - Clés API ou secrets
   - Fichiers de credentials
   - Données sensibles
   - Mots de passe

2. **Utiliser**:
   - Variables d'environnement (.env)
   - .gitignore pour exclure les fichiers sensibles
   - Validation des entrées utilisateur
   - Protection CSRF

3. **Signaler**:
   - Les vulnérabilités de sécurité en privé
   - Les problèmes de confidentialité
   - Les failles potentielles

## 📞 Questions?

Si vous avez des questions:

1. Consultez la documentation existante
2. Cherchez dans les Issues fermées
3. Créez une nouvelle Issue avec le tag `question`
4. Contactez l'équipe ProSMAT

## 🙏 Remerciements

Merci de contribuer au succès du Projet ProSMAT!

Votre travail aide à améliorer la sécurité alimentaire au Togo. 🇹🇬

---

**ProSMAT - Projet de Sécurité Alimentaire et Nutritionnelle**
*Financé par GAFSP & FIDA - République du Togo*
