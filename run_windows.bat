@echo off
title VS AI Studio V1 Free
cd /d "%~dp0"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
pause
