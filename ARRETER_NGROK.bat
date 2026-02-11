@echo off
chcp 65001 >nul
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              🛑 ARRETER TOUTES LES SESSIONS NGROK            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo [1/2] Arrêt de tous les processus ngrok...
taskkill /F /IM ngrok.exe /T >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Aucun processus ngrok trouvé
) else (
    echo ✅ Processus ngrok arrêtés
)
echo.

echo [2/2] Arrêt du serveur Django...
taskkill /F /IM python.exe /T >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Aucun processus Python trouvé
) else (
    echo ✅ Serveur Django arrêté
)
echo.

timeout /t 2 /nobreak >nul

echo ════════════════════════════════════════════════════════════════
echo ✅ Toutes les sessions sont arrêtées!
echo ════════════════════════════════════════════════════════════════
echo.
echo Vous pouvez maintenant relancer DEMARRER_NGROK.bat
echo.
pause
