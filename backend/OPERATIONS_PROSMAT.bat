@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   OPÉRATIONS PROSMAT
echo ========================================
echo.
echo Choisissez une opération:
echo.
echo 1. Vérifier les données importées
echo 2. Importer/Réimporter les données Excel
echo 3. Démarrer le serveur
echo 4. Créer un superutilisateur
echo 5. Ouvrir le shell Django
echo 6. Sauvegarder la base de données
echo 7. Collecter les fichiers statiques
echo 8. Quitter
echo.
set /p choix="Votre choix (1-8): "

if "%choix%"=="1" goto verifier
if "%choix%"=="2" goto importer
if "%choix%"=="3" goto serveur
if "%choix%"=="4" goto superuser
if "%choix%"=="5" goto shell
if "%choix%"=="6" goto backup
if "%choix%"=="7" goto static
if "%choix%"=="8" goto fin

echo Choix invalide!
pause
goto fin

:verifier
echo.
echo === VÉRIFICATION DES DONNÉES ===
echo.
call venv_prosmat\Scripts\activate.bat
python verifier_donnees.py
pause
goto fin

:importer
echo.
echo === IMPORTATION DES DONNÉES ===
echo.
echo ATTENTION: Cette opération va mettre à jour les indicateurs.
echo Les indicateurs existants seront mis à jour (pas de doublons).
echo.
set /p confirm="Continuer? (O/N): "
if /i not "%confirm%"=="O" goto fin
call venv_prosmat\Scripts\activate.bat
python import_prosmat_complet.py
echo.
echo Importation terminée!
pause
goto fin

:serveur
echo.
echo === DÉMARRAGE DU SERVEUR ===
echo.
echo Le serveur va démarrer sur http://localhost:8000
echo Appuyez sur CTRL+C pour arrêter le serveur
echo.
call venv_prosmat\Scripts\activate.bat
python manage.py runserver
goto fin

:superuser
echo.
echo === CRÉATION D'UN SUPERUTILISATEUR ===
echo.
call venv_prosmat\Scripts\activate.bat
python manage.py createsuperuser
pause
goto fin

:shell
echo.
echo === SHELL DJANGO ===
echo.
echo Tapez 'exit()' pour quitter le shell
echo.
call venv_prosmat\Scripts\activate.bat
python manage.py shell
goto fin

:backup
echo.
echo === SAUVEGARDE DE LA BASE DE DONNÉES ===
echo.
call venv_prosmat\Scripts\activate.bat
set filename=backup_prosmat_%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%.json
set filename=%filename: =0%
python manage.py dumpdata > %filename%
echo.
echo Sauvegarde créée: %filename%
pause
goto fin

:static
echo.
echo === COLLECTE DES FICHIERS STATIQUES ===
echo.
call venv_prosmat\Scripts\activate.bat
python manage.py collectstatic --noinput
echo.
echo Fichiers statiques collectés!
pause
goto fin

:fin
echo.
echo Au revoir!
echo.
