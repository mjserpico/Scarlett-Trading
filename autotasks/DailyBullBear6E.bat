@ECHO OFF 
SETLOCAL
set LOGFILE=C:\Program Files\SERPICO\autotasks\Logs\EOD%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt

Echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\DailyBullBear\6EdailyBullBear.py"
ECHO Ran 6E DailyBullBear Script >> "%LOGFILE%"
timeout /t 2

