@ECHO OFF
call "C:\LocalEnv\LocalEnv.bat"
set LOGFILE=%Logs%\PosSizeMgmt%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt
ECHO Starting PosSizeMgmt %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0\PositionSizeMgmt.py"
ECHO Ending PosSizeMgmt Mgmt %date% %time% >> "%LOGFILE%"
