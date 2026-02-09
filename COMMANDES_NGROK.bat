@echo off
echo ========================================
echo   ProSMAT - Configuration ngrok
echo ========================================
echo.
echo Etape 1: Obtenez votre authtoken
echo   1. Allez sur: https://ngrok.com
echo   2. Connectez-vous
echo   3. Copiez votre authtoken
echo.
echo Etape 2: Collez votre authtoken ci-dessous
echo.
set /p TOKEN="Entrez votre authtoken ngrok: "
echo.
echo Configuration de l'authtoken...
.\ngrok.exe config add-authtoken %TOKEN%
echo.
echo ========================================
echo   Configuration terminee!
echo ========================================
echo.
echo Voulez-vous demarrer ProSMAT maintenant? (O/N)
set /p CHOICE="Votre choix: "
if /i "%CHOICE%"=="O" (
    echo.
    echo Demarrage de ProSMAT...
    start start_ngrok.bat
) else (
    echo.
    echo Pour demarrer plus tard, double-cliquez sur: start_ngrok.bat
)
echo.
pause
