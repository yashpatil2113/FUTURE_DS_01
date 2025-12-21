@echo off
setlocal
cd /d "%~dp0"

echo ==================================================
echo   Business Sales Dashboard - Automation Script
echo ==================================================
echo.

echo [1/5] Installing/updating dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing dependencies. Exiting.
    exit /b 1
)

echo.
echo [2/5] Generating sample e-commerce data...
python data_generator.py
if errorlevel 1 (
    echo Error running data_generator.py. Exiting.
    exit /b 1
)

echo.
echo [3/5] Cleaning and enriching dataset...
python data_cleaner.py
if errorlevel 1 (
    echo Error running data_cleaner.py. Exiting.
    exit /b 1
)

echo.
echo [4/5] Running analytical pipeline...
python analysis.py
if errorlevel 1 (
    echo Error running analysis.py. Exiting.
    exit /b 1
)

echo.
echo [5/5] Building dashboard UI...
python generate_dashboard.py
if errorlevel 1 (
    echo Error running generate_dashboard.py. Exiting.
    exit /b 1
)

echo.
echo Pipeline completed successfully!
echo - raw_ecommerce_data.csv
echo - cleaned_ecommerce_data.csv
echo - analysis_output\*.csv
echo - dashboard.html

echo.
echo Opening dashboard...
start "" "dashboard.html"

echo Done.
endlocal

