@ECHO OFF 
call "C:\LocalEnv\LocalEnv.bat"
set LOGFILE=%Logs%\MorningConnection%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt
ECHO Launching Morning Connection script %date% %time%
"%Python%Python.exe" "%~dp0MorningConnection.py"
ECHO Finished Morning Connection %date% %time%
"%Python%Python.exe" "%~dp0emailConnection.py"
ECHO Emailed Connection status %date% %time%
