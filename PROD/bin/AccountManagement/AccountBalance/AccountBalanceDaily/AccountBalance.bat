@ECHO OFF 
call "C:\LocalEnv\LocalEnv.bat"
set LOGFILE=%Logs%\AccounttBalance%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt
ECHO Launching Account Balance script %date% %time%
"%Python%Python.exe" "%~dp0AccountBalance.py"
ECHO Finished Account Balance %date% %time%
