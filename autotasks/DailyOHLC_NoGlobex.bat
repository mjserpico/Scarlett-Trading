@ECHO OFF 
SETLOCAL
set LOGFILE=C:\Program Files\SERPICO\autotasks\Logs\DailyOHLC%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt


"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\LEdailyOHLC.py"
ECHO Ran LE OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1



"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\HEdailyOHLC.py"
ECHO Ran LE OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
