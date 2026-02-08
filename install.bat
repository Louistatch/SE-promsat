@echo off
echo ========================================
echo ProSMAT - Installation
echo ========================================
echo.

echo Verification de Python...
python --version
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou n'est pas dans le PATH
    echo Telechargez Python depuis: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo Creation de l'environnement virtuel...
python -m venv venv_new

echo.
echo Activation de l'environnement virtuel...
call venv_new\Scripts\activate.bat

echo.
echo Installation des dependances...
pip install -r requirements.txt

echo.
echo Creation de la base de donnees...
python manage.py makemigrations
python manage.py migrate

echo.
echo Initialisation des donnees...
python manage.py init_prosmat

echo.
echo ========================================
echo Installation terminee avec succes!
echo ========================================
echo.
echo Pour demarrer le serveur:
echo 1. Activez l'environnement: venv_new\Scripts\activate
echo 2. Lancez le serveur: python manage.py runserver
echo.
echo Ou utilisez simplement: start_new.bat
echo.
pause
