@ECHO OFF 
call "C:\LocalEnv\LocalEnv.bat"
set LOGFILE=%Logs%\ALLDailyOHLC%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt

ECHO Starting All Daily OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0ALL_OHLC_withvol.py"
ECHO Ending All Daily OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1

