@ECHO OFF
call "C:\LocalEnv\LocalEnv.bat"
set LOGFILE=%Logs%\StopLossMgmt%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt
ECHO Starting StopLossMgmt %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0\StopLossMgmt.py"
ECHO Ending StopLoss Mgmt %date% %time% >> "%LOGFILE%"
