@echo off
cd /D "%~dp0"
pyinstaller.exe --windowed -F --icon=icon.ico main.py --hidden-import pkg_resources.py2_warn
REM pyinstaller.exe --windowed -F --icon=icon.ico --onefile main.py --hidden-import pkg_resources.py2_warn
color 46
echo EXECUTABLE FILE CREATED!
pause