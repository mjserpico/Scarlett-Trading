@ECHO OFF 
call "C:\LocalEnv\LocalEnv.bat"
set LOGFILE=%Logs%\AccounttBalanceIntraday%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt

ECHO Launching Account Balance Intraday script %date% %time%
"%Python%Python.exe" "%~dp0AccountBalanceIntraday.py"
ECHO Finished Account Balance Intraday %date% %time%

ECHO Starting Email for Account Balance Intraday %date% %time%
call "%MAIN_DIR%\bin\SystemManagement\Email\emailSummaryintraday\emailSummaryintraday.bat"
ECHO Finished Email for Account Balance Intraday %date% %time%