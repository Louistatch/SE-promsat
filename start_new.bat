@echo off
echo ========================================
echo ProSMAT - Demarrage
echo ========================================
echo.

echo Activation de l'environnement virtuel...
call venv_new\Scripts\activate.bat

echo.
echo Verification des migrations...
python manage.py migrate

echo.
echo ========================================
echo Demarrage du serveur...
echo ========================================
echo.
echo Acces a l'application:
echo - Application: http://localhost:8000
echo - Admin: http://localhost:8000/admin
echo.
echo Comptes:
echo - Admin: admin / admin123
echo - Coordonnateur: coordonnateur / prosmat2026
echo - Regions: charge_[region] / prosmat2026
echo.
echo Appuyez sur Ctrl+C pour arreter
echo ========================================
echo.

python manage.py runserver
