@ECHO OFF 
SETLOCAL
set LOGFILE=C:\Program Files\SERPICO\autotasks\Logs\DailyPosMgmt%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\DailyBullBearPosMgmt\ESPosMgmt.py"
echo ES Pos Mgmt %date% %time% >> "%LOGFILE%"
timeout /t 1




