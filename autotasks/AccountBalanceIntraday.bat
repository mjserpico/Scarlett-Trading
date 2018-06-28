@ECHO OFF 
REM Runs both my project scripts
@ECHO OFF 
SETLOCAL
set LOGFILE=C:\Users\Michael\Desktop\autotasks\Logs\AcctBalance%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt


"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\acctbalintraday.py"
ECHO Finished Account Balance %date% %time%

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\emailSummaryintraday.py"
ECHO Finished Account Balance %date% %time%
