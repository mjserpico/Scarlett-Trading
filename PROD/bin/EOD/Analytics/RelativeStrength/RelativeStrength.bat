@ECHO OFF
call "C:\LocalEnv\LocalEnv.bat"
set LOGFILE=%Logs%\RelativeStrength%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt
ECHO Starting Daily Relative Strength Ranking %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0\RelativeStrength.py"
ECHO Ending Relative Strength Ranking %date% %time% >> "%LOGFILE%"
