@echo off
title 2xOneFakeDbGenerator - Lancement Administrateur

echo.
echo Demande des droits administrateur...
echo.

:: Chemin complet vers PowerShell (corrige l'erreur "non reconnu")
"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -Command "Start-Process python.exe -ArgumentList '-u \"%~dp0\main.pyw\"' -Verb RunAs -Wait"

echo.
echo Programme terminé. Tu peux fermer cette fenêtre.
pause
