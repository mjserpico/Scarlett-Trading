@ECHO OFF
call "C:\LocalEnv\LocalEnv.bat"
set LOGFILE=%Logs%\ReportPosting%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt
ECHO Starting Daily Report Posting %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0\DailyReportPosting.py"
ECHO Ending Report Posting Daily %date% %time% >> "%LOGFILE%"
