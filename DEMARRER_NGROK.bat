@echo off
chcp 65001 >nul
echo ╔══════════════════════════════════════════════════════════════╗
echo ║          🚀 PROSMAT - DEMARRAGE AVEC NGROK                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Vérifier si ngrok existe
if not exist "ngrok.exe" (
    echo ❌ ERREUR: ngrok.exe non trouvé dans ce dossier
    echo.
    echo Téléchargez ngrok depuis: https://ngrok.com/download
    echo Placez ngrok.exe dans le dossier du projet
    echo.
    pause
    exit /b 1
)

REM Activer l'environnement virtuel
echo [1/4] Activation de l'environnement virtuel...
call venv_prosmat\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Erreur lors de l'activation de l'environnement virtuel
    pause
    exit /b 1
)
echo ✅ Environnement virtuel activé
echo.

REM Vérifier la base de données
echo [2/4] Vérification de la base de données...
python manage.py check --deploy >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Avertissement: Problèmes détectés (non bloquant)
) else (
    echo ✅ Base de données OK
)
echo.

REM Démarrer le serveur Django
echo [3/4] Démarrage du serveur Django sur le port 8000...
start "Django Server" cmd /k "venv_prosmat\Scripts\activate.bat && python manage.py runserver 8000"
timeout /t 5 /nobreak >nul
echo ✅ Serveur Django démarré
echo.

REM Démarrer ngrok
echo [4/4] Démarrage de ngrok...
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    📡 TUNNEL NGROK                           ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Une fois ngrok démarré:
echo.
echo 1️⃣  COPIER L'URL HTTPS (ex: https://abc123.ngrok-free.app)
echo.
echo 2️⃣  AJOUTER DANS FIREBASE CONSOLE:
echo    - Aller sur: https://console.firebase.google.com
echo    - Projet: prosmat-auth
echo    - Authentication → Settings → Authorized domains
echo    - Ajouter votre URL ngrok
echo.
echo 3️⃣  AJOUTER DANS config/settings.py:
echo    - ALLOWED_HOSTS = ['*']  (déjà configuré)
echo    - CSRF_TRUSTED_ORIGINS = ['https://votre-url.ngrok-free.app']
echo.
echo 4️⃣  ACCEDER A L'APPLICATION:
echo    - Ouvrir l'URL ngrok dans votre navigateur
echo    - Cliquer sur "Visit Site" si demandé
echo.
echo ⚠️  IMPORTANT: Ne pas fermer cette fenêtre!
echo.
echo 🛑 Pour arrêter: Appuyez sur CTRL+C puis fermez les fenêtres
echo.
echo ════════════════════════════════════════════════════════════════
echo.

REM Lancer ngrok
ngrok http 8000

REM Nettoyage quand ngrok est fermé
echo.
echo ════════════════════════════════════════════════════════════════
echo Arrêt en cours...
echo ════════════════════════════════════════════════════════════════
echo.

REM Arrêter le serveur Django
taskkill /F /FI "WINDOWTITLE eq Django Server*" >nul 2>&1
timeout /t 2 /nobreak >nul

echo ✅ Application arrêtée
echo.
pause
