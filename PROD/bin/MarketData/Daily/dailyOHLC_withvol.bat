@ECHO OFF 
call "C:\LocalEnv\LocalEnv.bat"
set LOGFILE=%Logs%\DAILYOHLC%date:~-4,4%%date:~-7,2%%date:~-10,2%.txt

ECHO Open API connection %date% %time% >> "%LOGFILE%"
rem call "%Python%Python.exe" "%~dp0CONNECTdailyOHLC_withvol.py"
rem ECHO Ending SPY OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1


ECHO Starting AAPL OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0AAPLdailyOHLC_withvol.py"
ECHO Ending AAPL OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting ABT OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0ABTdailyOHLC_withvol.py"
ECHO Ending ABT OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting ACN OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0ACNdailyOHLC_withvol.py"
ECHO Ending ACN OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting AGN OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0AGNdailyOHLC_withvol.py"
ECHO Ending AGN OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting AIG OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0AIGdailyOHLC_withvol.py"
ECHO Ending AIG OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting AMGN OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0AMGNdailyOHLC_withvol.py"
ECHO Ending AMGN OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting AXP OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0AXPdailyOHLC_withvol.py"
ECHO Ending AXP OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting BA OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0BAdailyOHLC_withvol.py"
ECHO Ending BA OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting BAC OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0BACdailyOHLC_withvol.py"
ECHO Ending BAC OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting BIIB OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0BIIBdailyOHLC_withvol.py"
ECHO Ending BIIB OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting BK OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0BKdailyOHLC_withvol.py"
ECHO Ending BK OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting BLK OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0BLKdailyOHLC_withvol.py"
ECHO Ending BLK OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting BMY OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0BMYdailyOHLC_withvol.py"
ECHO Ending BMY OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting C OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0CdailyOHLC_withvol.py"
ECHO Ending BMY C %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting CAT OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0CATdailyOHLC_withvol.py"
ECHO Ending BMY CAT %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting CELG OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0CELGdailyOHLC_withvol.py"
ECHO Ending CELG OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting CHTR OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0CHTRdailyOHLC_withvol.py"
ECHO Ending CHTR OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting CL OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0CLdailyOHLC_withvol.py"
ECHO Ending CL OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting CMCSA OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0CMCSAdailyOHLC_withvol.py"
ECHO Ending CMCSA OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting COST OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0COSTdailyOHLC_withvol.py"
ECHO Ending COST OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting CVS OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0CVSdailyOHLC_withvol.py"
ECHO Ending CVS OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting CVX OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0CVXdailyOHLC_withvol.py"
ECHO Ending CVX OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting DHR OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0DHRdailyOHLC_withvol.py"
ECHO Ending DHR OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting DIS OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0DISdailyOHLC_withvol.py"
ECHO Ending DIS OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting DUK OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0DUKdailyOHLC_withvol.py"
ECHO Ending DUK OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting DWDP OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0DWDPdailyOHLC_withvol.py"
ECHO Ending DWDP OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting EMR OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0EMRdailyOHLC_withvol.py"
ECHO Ending EMR OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting EXC OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0EXCdailyOHLC_withvol.py"
ECHO Ending EXC OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting F OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0FdailyOHLC_withvol.py"
ECHO Ending F OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting FB OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0FBdailyOHLC_withvol.py"
ECHO Ending FB OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting FDX OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0FDXdailyOHLC_withvol.py"
ECHO Ending FDX OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting FOX OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0FOXdailyOHLC_withvol.py"
ECHO Ending FOX OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting FOXA OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0FOXAdailyOHLC_withvol.py"
ECHO Ending FOXA OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting GD OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0GDdailyOHLC_withvol.py"
ECHO Ending GD OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting GE OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0GEdailyOHLC_withvol.py"
ECHO Ending GE OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting GILD OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0GILDdailyOHLC_withvol.py"
ECHO Ending GILD OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting GM OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0GMdailyOHLC_withvol.py"
ECHO Ending GM OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting GS OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0GSdailyOHLC_withvol.py"
ECHO Ending GS OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting HAL OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0HALdailyOHLC_withvol.py"
ECHO Ending HAL OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting HD OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0HDdailyOHLC_withvol.py"
ECHO Ending HD OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting HON OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0HONdailyOHLC_withvol.py"
ECHO Ending HON OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting IBM OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0IBMdailyOHLC_withvol.py"
ECHO Ending IBM OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting INTC OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0INTCdailyOHLC_withvol.py"
ECHO Ending INTC OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting JNJ OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0JNJdailyOHLC_withvol.py"
ECHO Ending JNJ OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting JPM OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0JPMdailyOHLC_withvol.py"
ECHO Ending JPM OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting KHC OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0KHCdailyOHLC_withvol.py"
ECHO Ending KHC OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting KMI OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0KMIdailyOHLC_withvol.py"
ECHO Ending KMI OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting KO OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0KOdailyOHLC_withvol.py"
ECHO Ending KO OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting LLY OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0LLYdailyOHLC_withvol.py"
ECHO Ending LLY OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting LMT OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0LMTdailyOHLC_withvol.py"
ECHO Ending LMT OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting LOW OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0LOWdailyOHLC_withvol.py"
ECHO Ending LOW OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting MA OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0MAdailyOHLC_withvol.py"
ECHO Ending MA OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting MCD OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0MCDdailyOHLC_withvol.py"
ECHO Ending MCD OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting MDLZ OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0MDLZdailyOHLC_withvol.py"
ECHO Ending MDLZ OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting MDT OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0MDTdailyOHLC_withvol.py"
ECHO Ending MDT OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting MET OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0METdailyOHLC_withvol.py"
ECHO Ending MET OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting MMM OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0MMMdailyOHLC_withvol.py"
ECHO Ending MMM OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting MO OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0MOdailyOHLC_withvol.py"
ECHO Ending MO OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting MRK OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0MRKdailyOHLC_withvol.py"
ECHO Ending MRK OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting MS OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0MSdailyOHLC_withvol.py"
ECHO Ending MS OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting MSFT OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0MSFTdailyOHLC_withvol.py"
ECHO Ending MSFT OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting NEE OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0NEEdailyOHLC_withvol.py"
ECHO Ending NEE OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting NFLX OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0NFLXdailyOHLC_withvol.py"
ECHO Ending NFLX OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting NKE OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0NKEdailyOHLC_withvol.py"
ECHO Ending NKE OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting NVDA OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0NVDAdailyOHLC_withvol.py"
ECHO Ending NVDA OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting ORCL OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0ORCLdailyOHLC_withvol.py"
ECHO Ending ORCL OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting OXY OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0OXYdailyOHLC_withvol.py"
ECHO Ending OXY OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting PEP OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0PEPdailyOHLC_withvol.py"
ECHO Ending PEP OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting PFE OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0PFEdailyOHLC_withvol.py"
ECHO Ending PFE OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting PG OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0PGdailyOHLC_withvol.py"
ECHO Ending PG OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting PM OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0PMdailyOHLC_withvol.py"
ECHO Ending PM OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting PYPL OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0PYPLdailyOHLC_withvol.py"
ECHO Ending PYPL OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting QCOM OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0QCOMdailyOHLC_withvol.py"
ECHO Ending QCOM OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting RTN OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0RTNdailyOHLC_withvol.py"
ECHO Ending RTN OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting SBUX OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0SBUXdailyOHLC_withvol.py"
ECHO Ending SBUX OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting SLB OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0SLBdailyOHLC_withvol.py"
ECHO Ending SLB OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting SO OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0SOdailyOHLC_withvol.py"
ECHO Ending SO OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting SPG OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0SPGdailyOHLC_withvol.py"
ECHO Ending SPG OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting T OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0TdailyOHLC_withvol.py"
ECHO Ending T OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting TGT OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0TGTdailyOHLC_withvol.py"
ECHO Ending TGT OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting TRV OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0TRVdailyOHLC_withvol.py"
ECHO Ending TRV OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting TXN OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0TXNdailyOHLC_withvol.py"
ECHO Ending TXN OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting UNH OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0UNHdailyOHLC_withvol.py"
ECHO Ending UNH OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting UNP OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0UNPdailyOHLC_withvol.py"
ECHO Ending UNP OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting UPS OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0UPSdailyOHLC_withvol.py"
ECHO Ending UPS OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting USB OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0USBdailyOHLC_withvol.py"
ECHO Ending USB OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting UTX OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0UTXdailyOHLC_withvol.py"
ECHO Ending UTX OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting V OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0VdailyOHLC_withvol.py"
ECHO Ending V OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting WBA OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0WBAdailyOHLC_withvol.py"
ECHO Ending WBA OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting WFC OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0WFCdailyOHLC_withvol.py"
ECHO Ending WFC OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting WMT OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0WMTdailyOHLC_withvol.py"
ECHO Ending WMT OHLC %date% %time% >> "%LOGFILE%"
timeout /t 1
ECHO Starting XOM OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0XOMdailyOHLC_withvol.py"
ECHO Ending XOM OHLC %date% %time% >> "%LOGFILE%"
ECHO Starting TZA OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0TZAdailyOHLC_withvol.py"
ECHO Ending TZA OHLC %date% %time% >> "%LOGFILE%"
ECHO Starting SSO OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0SSOdailyOHLC_withvol.py"
ECHO Ending SSO OHLC %date% %time% >> "%LOGFILE%"
ECHO Starting SPXS OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0SPXSdailyOHLC_withvol.py"
ECHO Ending SPXS OHLC %date% %time% >> "%LOGFILE%"
ECHO Starting SOXS OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0SOXSdailyOHLC_withvol.py"
ECHO Ending SOXS OHLC %date% %time% >> "%LOGFILE%"
ECHO Starting LABD OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0LABDdailyOHLC_withvol.py"
ECHO Ending LABD OHLC %date% %time% >> "%LOGFILE%"
ECHO Starting FAZ OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0FAZdailyOHLC_withvol.py"
ECHO Ending FAZ OHLC %date% %time% >> "%LOGFILE%"
ECHO Starting DUST OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0DUSTdailyOHLC_withvol.py"
ECHO Ending DUST OHLC %date% %time% >> "%LOGFILE%"
ECHO Starting DRIP OHLC %date% %time% >> "%LOGFILE%"
call "%Python%Python.exe" "%~dp0DRIPdailyOHLC_withvol.py"
ECHO Ending DRIP OHLC %date% %time% >> "%LOGFILE%"
ECHO END %date% %time% >> "%LOGFILE%"
ECHO !!!!! %date% %time% >> "%LOGFILE%"