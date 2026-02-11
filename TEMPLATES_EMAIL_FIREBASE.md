# 📧 Templates d'Emails Firebase pour ProSMAT

## Configuration des Templates d'Emails

### Accès aux Templates

1. Aller sur: https://console.firebase.google.com
2. Sélectionner le projet: **prosmat-auth**
3. Menu latéral → **Authentication**
4. Onglet **Templates** (en haut)

---

## 1. 📧 Vérification d'Email

### Template Français (Recommandé)

**Objet:**
```
Vérifiez votre adresse email - ProSMAT
```

**Corps du message:**
```html
Bonjour %DISPLAY_NAME%,

Bienvenue sur ProSMAT - Système de Suivi du Maraîchage Agroécologique au Togo!

Pour activer votre compte et accéder à la plateforme, veuillez vérifier votre adresse email en cliquant sur le lien ci-dessous:

%LINK%

Ce lien expirera dans 24 heures.

Si vous n'avez pas créé de compte ProSMAT, vous pouvez ignorer cet email en toute sécurité.

Cordialement,
L'équipe ProSMAT

---
ProSMAT - Ministère de l'Agriculture, de l'Élevage et du Développement Rural
République Togolaise
```

### Template Anglais (Alternative)

**Subject:**
```
Verify your email address - ProSMAT
```

**Body:**
```html
Hello %DISPLAY_NAME%,

Welcome to ProSMAT - Agroecological Market Gardening Monitoring System in Togo!

To activate your account and access the platform, please verify your email address by clicking the link below:

%LINK%

This link will expire in 24 hours.

If you didn't create a ProSMAT account, you can safely ignore this email.

Best regards,
The ProSMAT Team

---
ProSMAT - Ministry of Agriculture, Livestock and Rural Development
Togolese Republic
```

---

## 2. 🔑 Réinitialisation de Mot de Passe

### Template Français (Recommandé)

**Objet:**
```
Réinitialisation de votre mot de passe - ProSMAT
```

**Corps du message:**
```html
Bonjour %DISPLAY_NAME%,

Vous avez demandé la réinitialisation de votre mot de passe ProSMAT.

Cliquez sur le lien ci-dessous pour créer un nouveau mot de passe:

%LINK%

Ce lien expirera dans 1 heure.

Si vous n'avez pas demandé cette réinitialisation, veuillez ignorer cet email. Votre mot de passe actuel restera inchangé.

Pour votre sécurité:
- Ne partagez jamais votre mot de passe
- Utilisez un mot de passe fort (minimum 8 caractères)
- Changez votre mot de passe régulièrement

Cordialement,
L'équipe ProSMAT

---
ProSMAT - Ministère de l'Agriculture, de l'Élevage et du Développement Rural
République Togolaise
```

### Template Anglais (Alternative)

**Subject:**
```
Reset your password - ProSMAT
```

**Body:**
```html
Hello %DISPLAY_NAME%,

You requested to reset your ProSMAT password.

Click the link below to create a new password:

%LINK%

This link will expire in 1 hour.

If you didn't request this reset, please ignore this email. Your current password will remain unchanged.

For your security:
- Never share your password
- Use a strong password (minimum 8 characters)
- Change your password regularly

Best regards,
The ProSMAT Team

---
ProSMAT - Ministry of Agriculture, Livestock and Rural Development
Togolese Republic
```

---

## 3. 📧 Changement d'Email

### Template Français (Recommandé)

**Objet:**
```
Vérifiez votre nouvelle adresse email - ProSMAT
```

**Corps du message:**
```html
Bonjour %DISPLAY_NAME%,

Vous avez demandé à changer l'adresse email associée à votre compte ProSMAT.

Pour confirmer cette nouvelle adresse email, cliquez sur le lien ci-dessous:

%LINK%

Ce lien expirera dans 24 heures.

Si vous n'avez pas demandé ce changement, veuillez contacter immédiatement l'administrateur système.

Cordialement,
L'équipe ProSMAT

---
ProSMAT - Ministère de l'Agriculture, de l'Élevage et du Développement Rural
République Togolaise
```

---

## 4. 🎨 Template HTML Personnalisé (Avancé)

### Template avec Design ProSMAT

**Corps du message (HTML):**
```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 600px;
            margin: 20px auto;
            background-color: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 28px;
        }
        .header p {
            margin: 10px 0 0 0;
            font-size: 14px;
            opacity: 0.9;
        }
        .content {
            padding: 40px 30px;
        }
        .content h2 {
            color: #333;
            margin-top: 0;
        }
        .content p {
            color: #666;
            line-height: 1.6;
            margin: 15px 0;
        }
        .button {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 15px 40px;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
            font-weight: bold;
        }
        .button:hover {
            background: #5568d3;
        }
        .footer {
            background-color: #f9f9f9;
            padding: 20px 30px;
            text-align: center;
            color: #999;
            font-size: 12px;
            border-top: 1px solid #eee;
        }
        .warning {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌱 ProSMAT</h1>
            <p>Système de Suivi du Maraîchage Agroécologique</p>
        </div>
        
        <div class="content">
            <h2>Bonjour %DISPLAY_NAME%,</h2>
            
            <p>Bienvenue sur la plateforme ProSMAT!</p>
            
            <p>Pour activer votre compte et accéder à toutes les fonctionnalités de suivi et de monitoring, veuillez vérifier votre adresse email en cliquant sur le bouton ci-dessous:</p>
            
            <center>
                <a href="%LINK%" class="button">Vérifier mon email</a>
            </center>
            
            <p>Ou copiez ce lien dans votre navigateur:</p>
            <p style="word-break: break-all; color: #667eea;">%LINK%</p>
            
            <div class="warning">
                <strong>⚠️ Important:</strong> Ce lien expirera dans 24 heures. Si vous n'avez pas créé de compte ProSMAT, vous pouvez ignorer cet email en toute sécurité.
            </div>
            
            <p>Une fois votre email vérifié, vous pourrez:</p>
            <ul>
                <li>Accéder au dashboard de suivi</li>
                <li>Consulter les indicateurs ProSMAT</li>
                <li>Saisir et suivre les réalisations</li>
                <li>Générer des rapports</li>
            </ul>
        </div>
        
        <div class="footer">
            <p><strong>L'équipe ProSMAT</strong></p>
            <p>Ministère de l'Agriculture, de l'Élevage et du Développement Rural</p>
            <p>République Togolaise</p>
            <p style="margin-top: 15px;">
                Cet email a été envoyé automatiquement, merci de ne pas y répondre.
            </p>
        </div>
    </div>
</body>
</html>
```

---

## 📋 Instructions de Configuration

### Étape 1: Accéder aux Templates

1. Console Firebase: https://console.firebase.google.com
2. Projet: **prosmat-auth**
3. Authentication → **Templates**

### Étape 2: Configurer Chaque Template

#### A. Vérification d'Email

1. Cliquer sur **Email address verification**
2. Personnaliser:
   - **Nom de l'expéditeur**: ProSMAT
   - **Email de l'expéditeur**: noreply@prosmat-auth.firebaseapp.com
   - **Objet**: Copier l'objet ci-dessus
   - **Corps**: Copier le template français
3. Cliquer sur **Save**

#### B. Réinitialisation de Mot de Passe

1. Cliquer sur **Password reset**
2. Personnaliser:
   - **Nom de l'expéditeur**: ProSMAT
   - **Email de l'expéditeur**: noreply@prosmat-auth.firebaseapp.com
   - **Objet**: Copier l'objet ci-dessus
   - **Corps**: Copier le template français
3. Cliquer sur **Save**

#### C. Changement d'Email

1. Cliquer sur **Email address change**
2. Personnaliser:
   - **Nom de l'expéditeur**: ProSMAT
   - **Email de l'expéditeur**: noreply@prosmat-auth.firebaseapp.com
   - **Objet**: Copier l'objet ci-dessus
   - **Corps**: Copier le template français
3. Cliquer sur **Save**

### Étape 3: Configurer le Domaine d'Action (Optionnel)

Pour utiliser votre propre domaine au lieu de `prosmat-auth.firebaseapp.com`:

1. Authentication → **Settings**
2. Section **Authorized domains**
3. Ajouter votre domaine personnalisé
4. Configurer les enregistrements DNS

---

## 🔧 Variables Disponibles

Firebase remplace automatiquement ces variables:

| Variable | Description | Exemple |
|----------|-------------|---------|
| `%DISPLAY_NAME%` | Nom d'affichage de l'utilisateur | "Jean Dupont" |
| `%EMAIL%` | Email de l'utilisateur | "jean@example.com" |
| `%LINK%` | Lien d'action (vérification, reset, etc.) | URL complète |
| `%APP_NAME%` | Nom de l'application | "ProSMAT" |

---

## 🎨 Personnalisation Avancée

### Ajouter un Logo

Pour ajouter le logo ProSMAT dans les emails:

1. Héberger le logo sur un serveur public
2. Ajouter dans le template HTML:

```html
<div class="header">
    <img src="https://votre-domaine.com/logo_prosmat.jpg" 
         alt="ProSMAT" 
         style="max-width: 150px; margin-bottom: 10px;">
    <h1>ProSMAT</h1>
</div>
```

### Personnaliser les Couleurs

Modifier les couleurs dans le CSS:

```css
/* Couleur principale */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Couleur des boutons */
.button {
    background: #667eea;
}

/* Couleur des liens */
color: #667eea;
```

---

## 🧪 Test des Templates

### Tester l'Email de Vérification

```javascript
// Dans la console du navigateur sur la page de connexion
firebase.auth().currentUser.sendEmailVerification()
    .then(() => console.log('Email envoyé!'))
    .catch(error => console.error(error));
```

### Tester la Réinitialisation de Mot de Passe

```javascript
firebase.auth().sendPasswordResetEmail('test@example.com')
    .then(() => console.log('Email envoyé!'))
    .catch(error => console.error(error));
```

---

## 📊 Statistiques des Emails

Firebase fournit des statistiques sur les emails envoyés:

1. Console Firebase → **Authentication**
2. Onglet **Usage**
3. Section **Email verification**

Vous pouvez voir:
- Nombre d'emails envoyés
- Taux de vérification
- Erreurs d'envoi

---

## 🔐 Sécurité

### Bonnes Pratiques

✅ Utiliser HTTPS pour tous les liens
✅ Expiration des liens (24h pour vérification, 1h pour reset)
✅ Ne jamais inclure de mot de passe dans l'email
✅ Ajouter un message de sécurité
✅ Utiliser un email noreply

### Messages de Sécurité Recommandés

```
⚠️ ProSMAT ne vous demandera jamais votre mot de passe par email.

🔒 Pour votre sécurité, ce lien expirera dans [durée].

❌ Si vous n'avez pas demandé cette action, ignorez cet email.
```

---

## 📱 Responsive Design

Les templates HTML sont optimisés pour:
- ✅ Desktop (Outlook, Gmail, etc.)
- ✅ Mobile (iOS Mail, Gmail App, etc.)
- ✅ Webmail (Gmail, Yahoo, Outlook.com, etc.)

---

## 🌍 Support Multilingue

Pour supporter plusieurs langues:

1. Créer des templates pour chaque langue
2. Détecter la langue de l'utilisateur
3. Envoyer l'email dans la langue appropriée

```javascript
// Exemple: Définir la langue avant l'envoi
firebase.auth().languageCode = 'fr'; // Français
// ou
firebase.auth().languageCode = 'en'; // Anglais
```

---

## 📞 Support

Pour toute question sur les templates d'emails:

- Documentation Firebase: https://firebase.google.com/docs/auth/custom-email-handler
- Console Firebase: https://console.firebase.google.com
- Support Firebase: https://firebase.google.com/support

---

**Date**: 11 février 2026  
**Version**: 1.0  
**Projet**: ProSMAT - prosmat-auth
