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