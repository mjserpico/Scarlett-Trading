@ECHO OFF
call "C:\LocalEnv\LocalEnv.bat"
set LOGFILE=%Logs%\RSBDataFrame%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt
ECHO Starting RSBDataFrame %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0\RSBDataFrame.py"
ECHO Ending RSBDataFrame %date% %time% >> "%LOGFILE%"
