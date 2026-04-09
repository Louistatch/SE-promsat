@echo off
echo ============================================================
echo TEST DE CONFIGURATION FIREBASE
echo ============================================================
echo.

REM Activer l'environnement virtuel
call venv_prosmat\Scripts\activate.bat

REM Tester la configuration
python tester_firebase.py

echo.
echo ============================================================
echo DEMARRAGE DU SERVEUR
echo ============================================================
echo.
echo Le serveur va demarrer sur http://localhost:8000
echo.
echo URLs disponibles:
echo   - Firebase Login: http://localhost:8000/accounts/login-firebase/
echo   - Dashboard: http://localhost:8000/dashboard/
echo.
echo Appuyez sur CTRL+C pour arreter le serveur
echo.
pause

REM Démarrer le serveur
python manage.py runserver

pause
