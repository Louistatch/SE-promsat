@echo off
echo ========================================
echo   REPARATION AUTOMATIQUE PROSMAT
echo ========================================
echo.

echo [ETAPE 1] Arret des processus Python et ngrok...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM ngrok.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo [ETAPE 2] Installation des dependances...
cd /d %~dp0
call .\venv_prosmat\Scripts\activate.bat
python -m pip install --upgrade pip --quiet
python -m pip install Django==5.1.4 --force-reinstall --no-cache-dir --quiet
python -m pip install whitenoise==6.6.0 --quiet
python -m pip install djangorestframework==3.14.0 --quiet
python -m pip install django-cors-headers==4.3.1 --quiet
python -m pip install django-filter==23.5 --quiet
python -m pip install django-crispy-forms --quiet
python -m pip install crispy-bootstrap5==2024.10 --quiet
python -m pip install Pillow==11.0.0 --quiet
python -m pip install openpyxl==3.1.5 --quiet
python -m pip install reportlab==4.0.7 --quiet
python -m pip install xlsxwriter==3.1.9 --quiet
python -m pip install python-decouple==3.8 --quiet
python -m pip install dj-database-url==2.1.0 --quiet

echo.
echo [ETAPE 3] Verification...
python -c "import django; print('Django version:', django.get_version())"

echo.
echo [ETAPE 4] Test de l'application...
python manage.py check

echo.
echo ========================================
echo   REPARATION TERMINEE!
echo ========================================
echo.
echo Vous pouvez maintenant lancer: start_ngrok.bat
echo.
pause
