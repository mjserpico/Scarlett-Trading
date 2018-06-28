@ECHO OFF 
SETLOCAL
set LOGFILE=C:\Program Files\SERPICO\autotasks\Logs\DailyRecovery%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt


"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\AUDCADdailyOHLC_recover.py"
ECHO Ran 1st AUDCAD to enable connectivity to Gateway %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\AUDCADdailyOHLC_recover.py"
echo Ran AUDCAD OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\AUDCADdailyOHLC_recover.py"
echo Ran AUDCAD OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\AUDCHFdailyOHLC_recover.py"
ECHO Ran AUDCHF OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\AUDJPYdailyOHLC_recover.py"
ECHO Ran AUDJPY OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\AUDNZDdailyOHLC_recover.py"
ECHO Ran AUDNZD OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\AUDUSDdailyOHLC_recover.py"
ECHO Ran AUDUSD OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\CADCHFdailyOHLC_recover.py"
ECHO Ran CADCHF OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\CADJPYdailyOHLC_recover.py"
ECHO Ran CADJPY OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\CHFJPYdailyOHLC_recover.py"
ECHO Ran CHFJPY OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\EURAUDdailyOHLC_recover.py"
ECHO Ran EURAUD OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\EURCADdailyOHLC_recover.py"
ECHO Ran EURCAD OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\EURCHFdailyOHLC_recover.py"
ECHO Ran EURCHF OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\EURGBPdailyOHLC_recover.py"
ECHO Ran EURGBP OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\EURJPYdailyOHLC_recover.py"
ECHO Ran EURJPY OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\EURUSDdailyOHLC_recover.py"
ECHO Ran EURUSD OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\GBPJPYdailyOHLC_recover.py"
ECHO Ran GBPJPY OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\GBPNZDdailyOHLC_recover.py"
ECHO Ran GBPNZD OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\GBPUSDdailyOHLC_recover.py"
ECHO Ran GBPUSD OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\NZDCADdailyOHLC_recover.py"
ECHO Ran NZDCAD OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\NZDCHFdailyOHLC_recover.py"
ECHO Ran NZDCHF OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\NZDJPYdailyOHLC_recover.py"
ECHO Ran NZDJPY OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\NZDUSDdailyOHLC_recover.py"
ECHO Ran NZDUSD OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\USDCADdailyOHLC_recover.py"
ECHO Ran USDCAD OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\USDCHFdailyOHLC_recover.py"
ECHO Ran USDCHF OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\USDJPYdailyOHLC_recover.py"
ECHO Ran USDJPY OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\USDMXNdailyOHLC_recover.py"
ECHO Ran USDMXN OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\USDNOKdailyOHLC_recover.py"
ECHO Ran USDNOK OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\USDSEKdailyOHLC_recover.py"
ECHO Ran USDSEK OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\USDTRYdailyOHLC_recover.py"
ECHO Ran USDTRY OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1

"C:\Program Files\Anaconda3\envs\Scarlett1\Python.exe" "C:\Program Files\SERPICO\autotasks\PythonScripts\PriceRecovery\USDZARdailyOHLC_recover.py"
ECHO Ran USDZAR OHLC_recover %date% %time% >> "%LOGFILE%"
timeout /t 1


