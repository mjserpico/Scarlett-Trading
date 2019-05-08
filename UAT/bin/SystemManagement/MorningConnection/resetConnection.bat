@ECHO OFF 
call "C:\LocalEnv\LocalEnv.bat"
set LOGFILE=%Logs%\resetConnection%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt
ECHO Launching reset Connection script %date% %time%
"%Python%Python.exe" "%~dp0resetConnection.py"
ECHO Finished reset Connection %date% %time%

