@echo off
echo ========================================
echo ProSMAT - Systeme de Suivi & Evaluation
echo ========================================
echo.

echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

echo.
echo Verification des migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo Initialisation des donnees...
python manage.py init_prosmat

echo.
echo ========================================
echo Demarrage du serveur...
echo ========================================
echo.
echo Acces a l'application:
echo - Application: http://localhost:8000
echo - Admin: http://localhost:8000/admin
echo.
echo Comptes par defaut:
echo - Admin: admin / admin123
echo - Coordonnateur: coordonnateur / prosmat2026
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur
echo ========================================
echo.

python manage.py runserver
