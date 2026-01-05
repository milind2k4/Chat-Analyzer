@echo off
setlocal enabledelayedexpansion

REM --- 1. Set Encoding Fix ---
set PYTHONUTF8=1

REM --- 2. Find the Database File ---
set "DB_FILE="
REM Loops through files in current folder to find the first .crypt15 file
for %%f in (*.crypt15) do (
    set "DB_FILE=%%f"
)

if "%DB_FILE%"=="" (
    echo [ERROR] No file ending in .crypt15 found in this folder.
    pause
    exit /b
)

REM --- 3. Find and Read the Key File ---
if not exist "key.key" (
    echo [ERROR] File 'key.key' not found in this folder.
    echo Please create a text file named 'key.key' and paste your key string inside it.
    pause
    exit /b
)

REM Read the content of key.key into the variable KEY_VAL
set /p KEY_VAL=<key.key

REM --- 4. Run the Command ---
echo.
echo Found Database: !DB_FILE!
echo Found Key: !KEY_VAL!
echo.
echo Starting Export...
echo.

wtsexporter -a -k !KEY_VAL! -b "!DB_FILE!" -j --per-chat --avoid-encoding-json --no-html --pretty-print-json

echo.
echo Export Complete!
pause