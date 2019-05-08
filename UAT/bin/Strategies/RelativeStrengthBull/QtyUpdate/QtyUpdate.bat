@ECHO OFF 
call "C:\LocalEnv\LocalEnv.bat"
set LOGFILE=%Logs%\QtyUpdate%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt


ECHO Starting QtyUpdate %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0\QtyUpdate.py"
ECHO Finished with QtyUpdate %date% %time% >> "%LOGFILE%"
timeout /t 1




