@ECHO OFF 
call "C:\LocalEnv\LocalEnv.bat"
set LOGFILE=%Logs%\SPYOHLC%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt

ECHO Starting SPY OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0SPYDailyOHLC_withvol.py"
ECHO Ending SPY OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1

