@echo off
REM Dubbelklik dit bestand om de vluchten-website te starten.
REM De website opent dan automatisch in je browser.
cd /d "%~dp0"
streamlit run vluchten.py
pause
