@ECHO OFF 
call "C:\LocalEnv\LocalEnv.bat"
set LOGFILE=%Logs%\MorningPositions%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt
ECHO Launching Morning Positions script %date% %time%
"%Python%Python.exe" "%~dp0MorningPositions.py"
ECHO Finished Morning Positions %date% %time%
"%Python%Python.exe" "%~dp0emailConnection.py"
ECHO Emailed Positions status %date% %time%
