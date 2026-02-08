# 🎨 GUIDE D'INTÉGRATION DES LOGOS PROSMAT

## Étape 1: Téléchargement des Logos

### Logo 1: FIDA/IFAD
**Télécharger depuis**: https://seeklogo.com/vector-logo/70024/ifad

1. Visitez le lien ci-dessus
2. Téléchargez le logo en format PNG (transparent)
3. Sauvegardez comme: `static/images/logo_ifad.png`

**Alternative**: https://freebiesupply.com/logos/ifad-logo-2/

### Logo 2: GAFSP
**Télécharger depuis**: https://www.gafspfund.org/

1. Visitez le site officiel GAFSP
2. Cherchez le logo dans le footer ou la page "About"
3. Clic droit > Enregistrer l'image sous
4. Sauvegardez comme: `static/images/logo_gafsp.png`

**Note**: Si le logo n'est pas facilement accessible, contactez GAFSP pour obtenir le logo officiel.

### Logo 3: Armoiries du Togo
**Télécharger depuis**: https://brandeps.com/logo/C/Coat-of-arms-of-Togo-01

1. Visitez le lien ci-dessus
2. Téléchargez en format PNG ou SVG
3. Sauvegardez comme: `static/images/armoiries_togo.png`

**Alternative Wikimedia**: https://incubator.wikimedia.org/wiki/File:Armoiries_du_Togo.svg

### Logo 4: Drapeau du Togo (optionnel)
**Télécharger depuis**: https://iconlogovector.com/vector/togo

1. Visitez le lien ci-dessus
2. Téléchargez en format PNG
3. Sauvegardez comme: `static/images/drapeau_togo.png`

---

## Étape 2: Structure des Dossiers

Créez la structure suivante:

```
prosmat_se/
├── static/
│   ├── images/
│   │   ├── logo_ifad.png
│   │   ├── logo_gafsp.png
│   │   ├── armoiries_togo.png
│   │   ├── drapeau_togo.png (optionnel)
│   │   └── logo_prosmat.png (si vous créez un logo spécifique)
│   └── css/
│       └── style.css
```

---

## Étape 3: Intégration dans les Templates

### 3.1 En-tête Principal (`templates/base.html`)

Ajoutez dans la section `<header>` ou créez une nouvelle section:

```html
{% load static %}

<div class="header-logos">
    <div class="logos-left">
        <img src="{% static 'images/armoiries_togo.png' %}" alt="République du Togo" class="logo-togo">
    </div>
    
    <div class="header-title">
        <h1>ProSMAT</h1>
        <p class="subtitle">Système de Suivi-Évaluation</p>
        <p class="project-full-name">Projet de Soutien à la Promotion du Maraîchage Agroécologique au Togo</p>
    </div>
    
    <div class="logos-right">
        <img src="{% static 'images/logo_gafsp.png' %}" alt="GAFSP" class="logo-partner">
        <img src="{% static 'images/logo_ifad.png' %}" alt="FIDA/IFAD" class="logo-partner">
    </div>
</div>
```

### 3.2 Styles CSS (`static/css/style.css`)

Ajoutez ces styles:

```css
/* En-tête avec logos */
.header-logos {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 40px;
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border-bottom: 3px solid #006233; /* Vert du drapeau togolais */
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.logos-left, .logos-right {
    display: flex;
    align-items: center;
    gap: 20px;
}

.logo-togo {
    height: 80px;
    width: auto;
}

.logo-partner {
    height: 60px;
    width: auto;
    margin: 0 10px;
}

.header-title {
    text-align: center;
    flex: 1;
}

.header-title h1 {
    font-size: 2.5rem;
    color: #006233; /* Vert togolais */
    margin: 0;
    font-weight: bold;
}

.header-title .subtitle {
    font-size: 1.2rem;
    color: #666;
    margin: 5px 0;
}

.header-title .project-full-name {
    font-size: 0.9rem;
    color: #888;
    font-style: italic;
    margin: 5px 0 0 0;
}

/* Responsive */
@media (max-width: 768px) {
    .header-logos {
        flex-direction: column;
        padding: 15px;
    }
    
    .logos-left, .logos-right {
        margin: 10px 0;
    }
    
    .logo-togo, .logo-partner {
        height: 50px;
    }
    
    .header-title h1 {
        font-size: 1.8rem;
    }
    
    .header-title .project-full-name {
        display: none; /* Masquer sur mobile */
    }
}
```

### 3.3 Page de Connexion (`templates/accounts/login.html`)

Ajoutez avant le formulaire:

```html
{% load static %}

<div class="login-header">
    <div class="login-logos">
        <img src="{% static 'images/armoiries_togo.png' %}" alt="République du Togo" class="logo-login">
        <img src="{% static 'images/logo_gafsp.png' %}" alt="GAFSP" class="logo-login">
        <img src="{% static 'images/logo_ifad.png' %}" alt="FIDA/IFAD" class="logo-login">
    </div>
    <h1>ProSMAT</h1>
    <p>Système de Suivi-Évaluation</p>
</div>
```

Styles CSS:

```css
.login-header {
    text-align: center;
    margin-bottom: 30px;
}

.login-logos {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 30px;
    margin-bottom: 20px;
}

.logo-login {
    height: 60px;
    width: auto;
}
```

---

## Étape 4: Intégration dans les Exports PDF

Modifiez `monitoring/views.py` dans la fonction `export_pdf_view`:

```python
from reportlab.platypus import Image as RLImage
from django.conf import settings
import os

# Dans la fonction export_pdf_view, ajoutez:

# Chemins des logos
logo_togo_path = os.path.join(settings.STATIC_ROOT or settings.BASE_DIR / 'static', 'images', 'armoiries_togo.png')
logo_gafsp_path = os.path.join(settings.STATIC_ROOT or settings.BASE_DIR / 'static', 'images', 'logo_gafsp.png')
logo_ifad_path = os.path.join(settings.STATIC_ROOT or settings.BASE_DIR / 'static', 'images', 'logo_ifad.png')

# Créer une table pour l'en-tête avec logos
header_data = []
logos_row = []

# Ajouter les logos s'ils existent
if os.path.exists(logo_togo_path):
    logos_row.append(RLImage(logo_togo_path, width=2*cm, height=2*cm))
else:
    logos_row.append('')

logos_row.append(Paragraph('<b>ProSMAT</b><br/>Système de Suivi-Évaluation', title_style))

if os.path.exists(logo_gafsp_path):
    logos_row.append(RLImage(logo_gafsp_path, width=2*cm, height=1.5*cm))
else:
    logos_row.append('')

if os.path.exists(logo_ifad_path):
    logos_row.append(RLImage(logo_ifad_path, width=2*cm, height=1.5*cm))
else:
    logos_row.append('')

header_data.append(logos_row)

# Créer la table d'en-tête
header_table = Table(header_data, colWidths=[3*cm, 10*cm, 2.5*cm, 2.5*cm])
header_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))

elements.append(header_table)
elements.append(Spacer(1, 1*cm))
```

---

## Étape 5: Configuration Django

Assurez-vous que `config/settings.py` contient:

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Pour la production

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## Étape 6: Collecte des Fichiers Statiques

Pour la production, exécutez:

```bash
python manage.py collectstatic
```

---

## Étape 7: Vérification

1. **Démarrez le serveur**:
   ```bash
   python manage.py runserver
   ```

2. **Vérifiez les pages**:
   - http://localhost:8000/ (page d'accueil)
   - http://localhost:8000/accounts/login/ (page de connexion)
   - http://localhost:8000/executif/ (dashboard exécutif)

3. **Testez les exports**:
   - Export PDF avec logos
   - Export Excel (si logos ajoutés)

---

## Notes Importantes

### Droits d'Utilisation
- ✅ **Armoiries du Togo**: Domaine public (symbole national)
- ✅ **Logo FIDA/IFAD**: Utilisation autorisée pour les projets financés par le FIDA
- ✅ **Logo GAFSP**: Utilisation autorisée pour les projets financés par GAFSP
- ⚠️ **Important**: Vérifiez les guidelines d'utilisation des logos auprès des partenaires

### Qualité des Images
- Utilisez des images haute résolution (minimum 300 DPI pour PDF)
- Format PNG avec transparence recommandé
- Format SVG idéal pour le web (scalable)

### Couleurs Officielles du Togo
- **Vert**: #006233 (vert du drapeau)
- **Jaune**: #FFCE00 (jaune du drapeau)
- **Rouge**: #D21034 (rouge du drapeau)

---

## Commandes Rapides

```bash
# Créer le dossier images
mkdir static\images

# Vérifier que les fichiers statiques sont bien configurés
python manage.py findstatic images/logo_ifad.png

# Collecter les fichiers statiques
python manage.py collectstatic --noinput
```

---

**Prochaines Étapes**:
1. ✅ Télécharger les logos depuis les sources indiquées
2. ✅ Placer les fichiers dans `static/images/`
3. ✅ Modifier les templates selon les exemples ci-dessus
4. ✅ Ajouter les styles CSS
5. ✅ Tester l'affichage
6. ✅ Intégrer dans les exports PDF

---

**Date**: 8 février 2026
**Version**: 1.0
