@ECHO OFF 
SETLOCAL
set LOGFILE=C:\Program Files\SERPICO\autotasks\Logs\prepBBConnection%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt


"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\E7dailyOHLC.py"
ECHO Ran 1st AUDCAD to enable connectivity to Gateway %date% %time%>> "%LOGFILE%"
timeout /t 2

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\E7dailyOHLC.py"
ECHO Ran 2nd AUDCAD to enable connectivity to Gateway %date% %time%>> "%LOGFILE%"
timeout /t 2


"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\E7dailyOHLC.py"
ECHO Ran 3st AUDCAD to enable connectivity to Gateway %date% %time%>> "%LOGFILE%"
timeout /t 2


