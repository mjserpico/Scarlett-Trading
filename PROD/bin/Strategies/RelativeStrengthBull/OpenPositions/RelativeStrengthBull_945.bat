@ECHO OFF 
call "C:\LocalEnv\LocalEnv.bat"
set LOGFILE=%Logs%\RelativeStrengthBull%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt


ECHO Starting RelativeStrengthBull %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0\RelativeStrengthBull_945.py"
ECHO Finished with RelativeStrengthBull %date% %time% >> "%LOGFILE%"
timeout /t 1




