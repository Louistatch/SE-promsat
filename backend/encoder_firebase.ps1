# Script PowerShell pour encoder les credentials Firebase en base64

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ENCODAGE FIREBASE CREDENTIALS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si le fichier existe
$fichier = "firebase-credentials.json"

if (-not (Test-Path $fichier)) {
    Write-Host "[ERREUR] Fichier $fichier non trouvé!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Assurez-vous que le fichier firebase-credentials.json" -ForegroundColor Yellow
    Write-Host "est dans le même dossier que ce script." -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

Write-Host "[OK] Fichier trouvé: $fichier" -ForegroundColor Green
Write-Host ""

# Lire le contenu
Write-Host "Lecture du fichier..." -ForegroundColor Yellow
$content = Get-Content -Path $fichier -Raw

# Encoder en base64
Write-Host "Encodage en base64..." -ForegroundColor Yellow
$bytes = [System.Text.Encoding]::UTF8.GetBytes($content)
$base64 = [Convert]::ToBase64String($bytes)

# Copier dans le presse-papiers
Write-Host "Copie dans le presse-papiers..." -ForegroundColor Yellow
$base64 | Set-Clipboard

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ENCODAGE REUSSI!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Le contenu encodé a été copié dans votre presse-papiers!" -ForegroundColor Green
Write-Host ""
Write-Host "PROCHAINES ETAPES:" -ForegroundColor Cyan
Write-Host "1. Allez sur Render Dashboard" -ForegroundColor White
Write-Host "2. Créez ou éditez votre Web Service" -ForegroundColor White
Write-Host "3. Dans Environment Variables, ajoutez:" -ForegroundColor White
Write-Host "   - Key: FIREBASE_CREDENTIALS_BASE64" -ForegroundColor Yellow
Write-Host "   - Value: Collez (Ctrl+V) le contenu copié" -ForegroundColor Yellow
Write-Host ""
Write-Host "Longueur du base64: $($base64.Length) caractères" -ForegroundColor Gray
Write-Host ""

# Sauvegarder aussi dans un fichier (optionnel)
$outputFile = "firebase-credentials-base64.txt"
$base64 | Out-File -FilePath $outputFile -Encoding UTF8
Write-Host "Sauvegardé aussi dans: $outputFile" -ForegroundColor Gray
Write-Host ""

pause
