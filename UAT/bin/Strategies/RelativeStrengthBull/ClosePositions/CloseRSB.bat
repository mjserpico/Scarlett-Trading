@ECHO OFF 
call "C:\LocalEnv\LocalEnv.bat"
set LOGFILE=%Logs%\CloseRSB%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt


ECHO Starting CloseRSB %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0\CloseRSB.py"
ECHO Finished CloseRSB %date% %time% >> "%LOGFILE%"
timeout /t 1
