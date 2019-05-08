@ECHO OFF
SETLOCAL
set LOGFILE=C:\Program Files\SERPICO\autotasks\Logs\EOD%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt



ECHO Ran 1st AUDCAD to enable connectivity to Gateway >> "%LOGFILE%"
Echo %LOGFILE%

timeout /t 10


