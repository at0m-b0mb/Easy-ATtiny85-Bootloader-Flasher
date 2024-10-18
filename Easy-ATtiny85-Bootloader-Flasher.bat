@echo off
setlocal enabledelayedexpansion

color 0A

:::
:::              ,----------------,              ,---------,
:::         ,-----------------------,          ,"        ,"|
:::       ,"                      ,"|        ,"        ,"  |
:::      +-----------------------+  |      ,"        ,"    |
:::      |  .-----------------.  |  |     +---------+      |
:::      |  |                 |  |  |     | -==----'|      |
:::      |  |  HackProKP!      |  |  |     |         |      |
:::      |  |  Hack The World |  |  |/----|---=     |      |
:::      |  |  C:\>_          |  |  |   ,/|==== ooo |      ;
:::      |  |                 |  |  |  // |(((( [33]|    ,"
:::      |  -----------------'   |," .;'| |((((     |  ,"
:::      +-----------------------+  ;;  | |         |,"     
:::         /_)______________(_/  //'   | +---------+
:::    ___________________________/___  ,
:::   /  oooooooooooooooo  .o.  oooo /,   \,"-----------
:::  / ==ooooooooooooooo==.o.  ooo= //   ,\--{)B     ,"
::: /_____________________________/'   /___________,"
:::  -----------------------------'
:::  GitHub: https://github.com/at0m-b0mb/Easy-ATtiny85-Bootloader-Flasher/     
:::  HackProKP - Kailash Parshad
:::

rem Print the banner

::
:: [*] Pin Diagram
:: 
::                ATtiny85 / Digispark                Arduino UNO
::                +------------------+
::                |                  |
::                |         5V       |------------- 5V  (Arduino Uno)
::                |                  |
::                |       GND        |------------- GND (Arduino Uno)
::                |                  |
::                |   Pin 0    o-----|------------- Pin 11 (Arduino Uno)
::                |   Pin 1    o-----|------------- Pin 12 (Arduino Uno)
::                |   Pin 2    o-----|------------- Pin 13 (Arduino Uno)
::                |                  |
::                |   Pin 5    o-----|------------- Pin 10 (Arduino Uno)
::                +------------------+
::
::    
:: [*] Connections Table
:: 
::  ___________________________________________
:: | ATtiny85/Digispark Pin  | Arduino Uno Pin |
:: |-------------------------|-----------------|
:: | Pin 0                   | Pin 11          |
:: | Pin 1                   | Pin 12          |
:: | Pin 2                   | Pin 13          |
:: | Pin 5                   | Pin 10          |
:: | 5V                      | 5V              |
:: | GND                     | GND             |
:: |_________________________|_________________|
::
::
:: [*] Connection Instructions
::
:: 1. Power Connections:
::    - Connect 5V on the ATtiny85 to 5V on the Arduino Uno.
::    - Connect GND on the ATtiny85 to GND on the Arduino Uno.
::
:: 2. Data Connections:
::    - Connect Pin 0 on the ATtiny85 to Pin 11 on the Arduino Uno.
::    - Connect Pin 1 on the ATtiny85 to Pin 12 on the Arduino Uno.
::    - Connect Pin 2 on the ATtiny85 to Pin 13 on the Arduino Uno.
::    - Connect Pin 5 on the ATtiny85 to Pin 10 on the Arduino Uno.
::
:: Tips
:: - Make sure all connections are secure to avoid any communication issues.
:: - Verify the power supply to ensure the ATtiny85 is getting the required voltage.
:: 
::

for /f "delims=: tokens=*" %%A in ('findstr /b :: "%~f0"') do @echo(%%A

rem Set the base directory for Arduino
set "ARDUINO_DIR=C:\Users\%USERNAME%\AppData\Local\Arduino15\packages\arduino\tools\avrdude"

rem Find the latest version directory
set "LATEST_VERSION="
for /f "tokens=*" %%i in ('dir /b /ad "%ARDUINO_DIR%"') do (
    set "LATEST_VERSION=%%i"
)

rem Check if the latest version was found
if not defined LATEST_VERSION (
    echo No avrdude version found in %ARDUINO_DIR%.
    exit /b 1
)

rem Construct the path to the avrdude executable and config file
set "AVRDUDE_PATH=%ARDUINO_DIR%\!LATEST_VERSION!\bin\avrdude.exe"
set "AVRDUDE_CONF=%ARDUINO_DIR%\!LATEST_VERSION!\etc\avrdude.conf"

rem Debugging output
echo [+] AVRDUDE Path: "!AVRDUDE_PATH!"
echo [+] AVRDUDE Config: "!AVRDUDE_CONF!"

rem Check if the files exist
if not exist "!AVRDUDE_PATH!" (
    echo avrdude executable not found at !AVRDUDE_PATH!.
    exit /b 1
)

if not exist "!AVRDUDE_CONF!" (
    echo avrdude config file not found at !AVRDUDE_CONF!.
    exit /b 1
)

rem Prompt for COM port
set /p COM_PORT="Please enter the COM port to use (e.g., COM4): "

rem Validate the user input for COM port
if "!COM_PORT!"=="" (
    echo No COM port entered. Exiting...
    exit /b 1
)

rem Run the avrdude command
"!AVRDUDE_PATH!" -C"!AVRDUDE_CONF!" -F -v -pattiny85 -cstk500v1 -P"!COM_PORT!" -b19200 -Uflash:w:"%~dp0\ATtiny85.hex":i -U lfuse:w:0xe1:m -U hfuse:w:0xdd:m -U efuse:w:0xfe:m

rem Check the exit code of the last command
if %errorlevel% neq 0 (
    echo avrdude command failed with error code %errorlevel%.
) else (
    echo avrdude command completed successfully.
)

@pause
