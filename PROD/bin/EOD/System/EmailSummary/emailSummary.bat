@ECHO OFF 
REM Runs both my project scripts
SETLOCAL
set LOGFILE=C:\Program Files\SERPICO\autotasks\Logs\EmailSummary%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\emailSummary.py"
ECHO Ran Daily Summary %date% %time%