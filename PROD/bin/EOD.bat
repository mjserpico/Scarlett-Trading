rem ***********************************************************
rem Scarlett Trading End of Day Processing Script
rem
rem	Performs the Following Processes each night at 5:05PM while TWS is down
rem	from 5PM to 6PM each night.
rem	
rem	1) Sends kick off mail
rem	2) Pulls historical data for instruments for nightly calculations
rem	3) Performs Correlation Matrix Calculation
rem 	4) Pulls and emails Daily PnL statements
rem 	5) Archives trade list and account statements to hard drive
rem 	
rem **********************************************************

@ECHO OFF 
call "C:\LocalEnv\LocalEnv.bat"
set LOGFILE=%Logs%\EOD%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt

ECHO Starting EOD processes %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0EOD\System\Start\EODsendmail.py"
ECHO Sent EOD mail %date% %time% >> "%LOGFILE%"
timeout /t 1

ECHO Launching Account Balance script %date% %time% >> "%LOGFILE%"
"%Python%Python.exe" "%~dp0AccountManagement\AccountBalance\AccountBalanceDaily\AccountBalance.py"
ECHO Finished Account Balance %date% %time% >> "%LOGFILE%"
timeout /t 1

ECHO SPY Index script %date% %time% >> "%LOGFILE%"
"%Python%Python.exe" "%~dp0MarketData\Daily\SPYdailyOHLC_withvol.py"
ECHO Finished SPY Index %date% %time% >> "%LOGFILE%"
timeout /t 1

ECHO EOD Finished --Sending Email %date% %time% >> "%LOGFILE%"
"%Python%Python.exe" "%~dp0EOD\System\EmailSummary\emailSummaryend.py"
ECHO EOD Done %date% %time% >> "%LOGFILE%"
timeout /t 1

ECHO Daily OHLC, ATR, Vol DOW components script %date% %time% >> "%LOGFILE%"
call "%~dp0MarketData\Daily\dailyOHLC_withvol.bat"
ECHO Finished OHLC components %date% %time% >> "%LOGFILE%"
timeout /t 1

ECHO Extended DailyOHLC %date% %time% >> "%LOGFILE%"
call "%~dp0MarketData\Daily\dailyOHLC_withvol_expansion.bat"
ECHO EOD Done %date% %time% >> "%LOGFILE%"
timeout /t 1

ECHO Calculate the Relative Strength of DOW components to SPY and write to HasPositions Table  %date% %time% >> "%LOGFILE%"
"%Python%Python.exe" "%~dp0EOD\Analytics\RelativeStrength\RelativeStrength.py"
ECHO Finished Relative Strength  %date% %time% >> "%LOGFILE%"
timeout /t 1

ECHO Rank Top 5 Relative Strength values for placing trades  %date% %time% >> "%LOGFILE%"
"%Python%Python.exe" "%~dp0EOD\Analytics\RelativeStrength\RelativeStrengthRank.py"
ECHO Finished Relative Strength ranking %date% %time% >> "%LOGFILE%"
timeout /t 1

rem ECHO Calculate Position Size based on ATR and Risk Metrics  %date% %time% >> "%LOGFILE%"
rem call "%~dp0EOD\Analytics\PosSizeMgmt\PositionSizeMgmt.bat"
rem ECHO Finished Position Size %date% %time% >> "%LOGFILE%"
rem timeout /t 1

rem ECHO Calculate the Stop Loss Value for the Stock on the Day based on ATR  %date% %time% >> "%LOGFILE%"
rem call "%~dp0EOD\Analytics\StopLossMgmt\StopLossMgmt.bat"
rem ECHO Finished Stop Loss Values %date% %time% >> "%LOGFILE%"
rem timeout /t 1

ECHO Reset connection flag %date% %time% >> "%LOGFILE%"
"%Python%Python.exe" "%~dp0SystemManagement\MorningConnection\resetConnection.py"
ECHO done with reset %date% %time% >> "%LOGFILE%"
timeout /t 1
