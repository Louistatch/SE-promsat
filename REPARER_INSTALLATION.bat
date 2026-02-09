@echo off
echo ========================================
echo   REPARATION DE L'INSTALLATION PROSMAT
echo ========================================
echo.

echo [ETAPE 1] Fermeture des processus Django et ngrok...
echo.
echo IMPORTANT: Fermez manuellement toutes les fenetres Django et ngrok!
echo Appuyez sur une touche quand c'est fait...
pause >nul

echo.
echo [ETAPE 2] Installation des dependances...
echo.
cd /d %~dp0
call .\venv_prosmat\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt --force-reinstall --no-cache-dir

echo.
echo [ETAPE 3] Verification de l'installation...
echo.
python -m pip list | findstr /i "django whitenoise"

echo.
echo [ETAPE 4] Test de Django...
echo.
python manage.py check

echo.
echo ========================================
echo   REPARATION TERMINEE!
echo ========================================
echo.
echo Vous pouvez maintenant lancer: start_ngrok.bat
echo.
pause
