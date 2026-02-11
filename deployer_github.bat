@echo off
echo ========================================
echo   DEPLOIEMENT PROSMAT SUR GITHUB
echo ========================================
echo.

REM Vérifier si Git est installé
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Git n'est pas installe!
    echo Telechargez Git depuis: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo [OK] Git est installe
echo.

REM Vérifier si le dépôt est déjà initialisé
if exist .git (
    echo [INFO] Depot Git deja initialise
) else (
    echo [ETAPE 1] Initialisation du depot Git...
    git init
    echo [OK] Depot initialise
)
echo.

REM Vérifier les fichiers sensibles
echo [ETAPE 2] Verification des fichiers sensibles...
echo.
echo Fichiers qui NE DOIVENT PAS etre sur GitHub:
echo   - .env
echo   - firebase-credentials.json
echo   - prosmat-auth-firebase-adminsdk-*.json
echo   - db.sqlite3
echo.
echo Ces fichiers sont exclus par .gitignore
echo.
pause

REM Ajouter tous les fichiers
echo [ETAPE 3] Ajout des fichiers...
git add .
echo [OK] Fichiers ajoutes
echo.

REM Afficher le statut
echo [ETAPE 4] Statut du depot:
git status
echo.
pause

REM Créer le commit
echo [ETAPE 5] Creation du commit...
git commit -m "Initial commit: ProSMAT Suivi-Evaluation - Authentification Firebase - Gestion des roles - Tableaux de bord - Rapports automatiques"
echo [OK] Commit cree
echo.

REM Demander l'URL du dépôt
echo [ETAPE 6] Configuration du depot distant
echo.
echo Allez sur GitHub et creez un nouveau depot:
echo   1. https://github.com/new
echo   2. Nom: prosmat (ou prosmat-togo)
echo   3. Visibilite: Private (recommande)
echo   4. Ne cochez PAS "Initialize with README"
echo   5. Cliquez sur "Create repository"
echo.
set /p REPO_URL="Entrez l'URL du depot (ex: https://github.com/username/prosmat.git): "

if "%REPO_URL%"=="" (
    echo [ERREUR] URL du depot requise!
    pause
    exit /b 1
)

REM Vérifier si le remote existe déjà
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    git remote add origin %REPO_URL%
    echo [OK] Depot distant ajoute
) else (
    echo [INFO] Depot distant deja configure
    git remote set-url origin %REPO_URL%
    echo [OK] URL du depot mise a jour
)
echo.

REM Renommer la branche en main
echo [ETAPE 7] Configuration de la branche principale...
git branch -M main
echo [OK] Branche renommee en 'main'
echo.

REM Pousser sur GitHub
echo [ETAPE 8] Envoi du code sur GitHub...
echo.
echo IMPORTANT: GitHub va vous demander de vous authentifier
echo   - Username: Votre nom d'utilisateur GitHub
echo   - Password: Utilisez un Personal Access Token (pas votre mot de passe)
echo.
echo Pour creer un token:
echo   1. https://github.com/settings/tokens
echo   2. Generate new token (classic)
echo   3. Cochez 'repo'
echo   4. Copiez le token
echo.
pause

git push -u origin main

if errorlevel 1 (
    echo.
    echo [ERREUR] Echec de l'envoi sur GitHub
    echo.
    echo Solutions possibles:
    echo   1. Verifiez vos identifiants GitHub
    echo   2. Utilisez un Personal Access Token
    echo   3. Verifiez l'URL du depot
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   DEPLOIEMENT REUSSI!
echo ========================================
echo.
echo Votre projet est maintenant sur GitHub!
echo.
echo Verifiez sur: %REPO_URL%
echo.
echo Prochaines etapes:
echo   1. Verifiez que les fichiers sensibles ne sont PAS la
echo   2. Invitez des collaborateurs si necessaire
echo   3. Configurez les parametres du depot
echo.
echo Pour les modifications futures:
echo   git add .
echo   git commit -m "Description des modifications"
echo   git push
echo.
pause
