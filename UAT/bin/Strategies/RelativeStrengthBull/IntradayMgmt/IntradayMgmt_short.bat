@ECHO OFF 
call "C:\LocalEnv\LocalEnv.bat"
set LOGFILE=\IntradayMgmt%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt


ECHO Starting IntradayMgmt %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0\IntradayMgmt_short.py"
ECHO Finished with IntradayMgmt %date% %time% >> "%LOGFILE%"
timeout /t 1
