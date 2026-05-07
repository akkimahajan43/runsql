@echo off
cd /d %~dp0

call venv\Scripts\activate

streamlit run learn_streamlit.py

pause