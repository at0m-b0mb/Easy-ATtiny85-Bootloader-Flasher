#!/bin/bash

# Color codes for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print banner
cat << "EOF"

             ,----------------,              ,---------,
        ,-----------------------,          ,"        ,"|
      ,"                      ,"|        ,"        ,"  |
     +-----------------------+  |      ,"        ,"    |
     |  .-----------------.  |  |     +---------+      |
     |  |                 |  |  |     | -==----'|      |
     |  |  HackProKP!      |  |  |     |         |      |
     |  |  Hack The World |  |  |/----|---=     |      |
     |  |  $>_             |  |  |   ,/|==== ooo |      ;
     |  |                 |  |  |  // |(((( [33]|    ,"
     |  -----------------'   |," .;'| |((((     |  ,"
     +-----------------------+  ;;  | |         |,"     
        /_)______________(_/  //'   | +---------+
   ___________________________/___  ,
  /  oooooooooooooooo  .o.  oooo /,   \,"-----------
 / ==ooooooooooooooo==.o.  ooo= //   ,\--{)B     ,"
/_____________________________/'   /___________,"
 -----------------------------'
 GitHub: https://github.com/at0m-b0mb/Easy-ATtiny85-Bootloader-Flasher/
 HackProKP - Kailash Parshad

EOF

echo ""
echo "================================================================================"
echo " [*] Pin Diagram"
echo "================================================================================"
echo ""
echo "               ATtiny85 / Digispark                Arduino UNO"
echo "               +------------------+"
echo "               |                  |"
echo "               |         5V       |------------- 5V  (Arduino Uno)"
echo "               |                  |"
echo "               |       GND        |------------- GND (Arduino Uno)"
echo "               |                  |"
echo "               |   Pin 0    o-----|------------- Pin 11 (Arduino Uno)"
echo "               |   Pin 1    o-----|------------- Pin 12 (Arduino Uno)"
echo "               |   Pin 2    o-----|------------- Pin 13 (Arduino Uno)"
echo "               |                  |"
echo "               |   Pin 5    o-----|------------- Pin 10 (Arduino Uno)"
echo "               +------------------+"
echo ""
echo "================================================================================"
echo " [*] Connections Table"
echo "================================================================================"
echo ""
echo " ___________________________________________"
echo "| ATtiny85/Digispark Pin  | Arduino Uno Pin |"
echo "|-------------------------|-----------------|"
echo "| Pin 0                   | Pin 11          |"
echo "| Pin 1                   | Pin 12          |"
echo "| Pin 2                   | Pin 13          |"
echo "| Pin 5                   | Pin 10          |"
echo "| 5V                      | 5V              |"
echo "| GND                     | GND             |"
echo "|_________________________|_________________|"
echo ""
echo "================================================================================"
echo " [*] Connection Instructions"
echo "================================================================================"
echo ""
echo " 1. Power Connections:"
echo "    - Connect 5V on the ATtiny85 to 5V on the Arduino Uno."
echo "    - Connect GND on the ATtiny85 to GND on the Arduino Uno."
echo ""
echo " 2. Data Connections:"
echo "    - Connect Pin 0 on the ATtiny85 to Pin 11 on the Arduino Uno."
echo "    - Connect Pin 1 on the ATtiny85 to Pin 12 on the Arduino Uno."
echo "    - Connect Pin 2 on the ATtiny85 to Pin 13 on the Arduino Uno."
echo "    - Connect Pin 5 on the ATtiny85 to Pin 10 on the Arduino Uno."
echo ""
echo " Tips:"
echo " - Make sure all connections are secure to avoid any communication issues."
echo " - Verify the power supply to ensure the ATtiny85 is getting the required voltage."
echo ""
echo "================================================================================"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HEX_FILE="$SCRIPT_DIR/ATtiny85.hex"

# Check if hex file exists
if [ ! -f "$HEX_FILE" ]; then
    echo -e "${RED}[!] Error: ATtiny85.hex not found in $SCRIPT_DIR${NC}"
    exit 1
fi

# Function to find avrdude on macOS
find_avrdude_macos() {
    # Check common macOS Arduino installation paths
    local PATHS=(
        "$HOME/Library/Arduino15/packages/arduino/tools/avrdude"
        "/Applications/Arduino.app/Contents/Java/hardware/tools/avr/bin"
        "/usr/local/bin"
        "/opt/homebrew/bin"
    )
    
    for BASE_PATH in "${PATHS[@]}"; do
        if [ -d "$BASE_PATH" ]; then
            # If it's the Arduino15 path, find the latest version
            if [[ "$BASE_PATH" == *"Arduino15"* ]]; then
                local LATEST_VERSION=$(ls -1 "$BASE_PATH" 2>/dev/null | sort -V | tail -n 1)
                if [ -n "$LATEST_VERSION" ]; then
                    local AVRDUDE_BIN="$BASE_PATH/$LATEST_VERSION/bin/avrdude"
                    local AVRDUDE_CONF="$BASE_PATH/$LATEST_VERSION/etc/avrdude.conf"
                    if [ -f "$AVRDUDE_BIN" ] && [ -f "$AVRDUDE_CONF" ]; then
                        echo "$AVRDUDE_BIN|$AVRDUDE_CONF"
                        return 0
                    fi
                fi
            else
                # Check if avrdude exists in this directory
                local AVRDUDE_BIN="$BASE_PATH/avrdude"
                if [ -f "$AVRDUDE_BIN" ]; then
                    # Try to find avrdude.conf
                    local AVRDUDE_CONF="${BASE_PATH/bin/etc}/avrdude.conf"
                    if [ ! -f "$AVRDUDE_CONF" ]; then
                        AVRDUDE_CONF="/etc/avrdude.conf"
                    fi
                    echo "$AVRDUDE_BIN|$AVRDUDE_CONF"
                    return 0
                fi
            fi
        fi
    done
    
    # Check if avrdude is in PATH
    if command -v avrdude &> /dev/null; then
        local AVRDUDE_BIN=$(which avrdude)
        local AVRDUDE_CONF="/etc/avrdude.conf"
        echo "$AVRDUDE_BIN|$AVRDUDE_CONF"
        return 0
    fi
    
    return 1
}

# Function to find avrdude on Linux
find_avrdude_linux() {
    # Check common Linux Arduino installation paths
    local PATHS=(
        "$HOME/.arduino15/packages/arduino/tools/avrdude"
        "/usr/share/arduino/hardware/tools/avr/bin"
        "/usr/bin"
        "/usr/local/bin"
    )
    
    for BASE_PATH in "${PATHS[@]}"; do
        if [ -d "$BASE_PATH" ]; then
            # If it's the .arduino15 path, find the latest version
            if [[ "$BASE_PATH" == *".arduino15"* ]]; then
                local LATEST_VERSION=$(ls -1 "$BASE_PATH" 2>/dev/null | sort -V | tail -n 1)
                if [ -n "$LATEST_VERSION" ]; then
                    local AVRDUDE_BIN="$BASE_PATH/$LATEST_VERSION/bin/avrdude"
                    local AVRDUDE_CONF="$BASE_PATH/$LATEST_VERSION/etc/avrdude.conf"
                    if [ -f "$AVRDUDE_BIN" ] && [ -f "$AVRDUDE_CONF" ]; then
                        echo "$AVRDUDE_BIN|$AVRDUDE_CONF"
                        return 0
                    fi
                fi
            else
                # Check if avrdude exists in this directory
                local AVRDUDE_BIN="$BASE_PATH/avrdude"
                if [ -f "$AVRDUDE_BIN" ]; then
                    # Try to find avrdude.conf
                    local AVRDUDE_CONF="${BASE_PATH/bin/etc}/avrdude.conf"
                    if [ ! -f "$AVRDUDE_CONF" ]; then
                        AVRDUDE_CONF="/etc/avrdude.conf"
                    fi
                    echo "$AVRDUDE_BIN|$AVRDUDE_CONF"
                    return 0
                fi
            fi
        fi
    done
    
    # Check if avrdude is in PATH
    if command -v avrdude &> /dev/null; then
        local AVRDUDE_BIN=$(which avrdude)
        local AVRDUDE_CONF="/etc/avrdude.conf"
        echo "$AVRDUDE_BIN|$AVRDUDE_CONF"
        return 0
    fi
    
    return 1
}

# Detect OS and find avrdude
echo -e "${YELLOW}[*] Detecting operating system...${NC}"
OS_TYPE=$(uname -s)

if [ "$OS_TYPE" = "Darwin" ]; then
    echo -e "${GREEN}[+] macOS detected${NC}"
    AVRDUDE_INFO=$(find_avrdude_macos)
elif [ "$OS_TYPE" = "Linux" ]; then
    echo -e "${GREEN}[+] Linux detected${NC}"
    AVRDUDE_INFO=$(find_avrdude_linux)
else
    echo -e "${RED}[!] Unsupported operating system: $OS_TYPE${NC}"
    echo -e "${RED}    This script supports macOS and Linux only.${NC}"
    exit 1
fi

# Parse avrdude information
if [ -z "$AVRDUDE_INFO" ]; then
    echo -e "${RED}[!] Error: avrdude not found!${NC}"
    echo ""
    echo "Please install Arduino IDE or avrdude:"
    echo ""
    if [ "$OS_TYPE" = "Darwin" ]; then
        echo "  macOS:"
        echo "    - Install Arduino IDE from https://www.arduino.cc/en/software"
        echo "    - Or install via Homebrew: brew install avrdude"
    else
        echo "  Linux:"
        echo "    - Install Arduino IDE from https://www.arduino.cc/en/software"
        echo "    - Or install via package manager: sudo apt-get install avrdude"
    fi
    echo ""
    exit 1
fi

AVRDUDE_PATH=$(echo "$AVRDUDE_INFO" | cut -d'|' -f1)
AVRDUDE_CONF=$(echo "$AVRDUDE_INFO" | cut -d'|' -f2)

echo -e "${GREEN}[+] AVRDUDE Path: $AVRDUDE_PATH${NC}"
echo -e "${GREEN}[+] AVRDUDE Config: $AVRDUDE_CONF${NC}"
echo ""

# List available serial ports
echo -e "${YELLOW}[*] Searching for serial ports...${NC}"
if [ "$OS_TYPE" = "Darwin" ]; then
    echo -e "${GREEN}[+] Available serial ports:${NC}"
    ls -1 /dev/cu.* 2>/dev/null | grep -E "(usb|serial)" || echo "  No USB serial ports found"
    echo ""
    echo "Common macOS ports: /dev/cu.usbserial-*, /dev/cu.usbmodem*"
elif [ "$OS_TYPE" = "Linux" ]; then
    echo -e "${GREEN}[+] Available serial ports:${NC}"
    ls -1 /dev/tty[UA]* 2>/dev/null || echo "  No USB/ACM serial ports found"
    echo ""
    echo "Common Linux ports: /dev/ttyUSB0, /dev/ttyACM0"
fi
echo ""

# Prompt for serial port
read -p "Please enter the serial port to use (e.g., /dev/ttyUSB0 or /dev/cu.usbserial): " SERIAL_PORT

# Validate user input
if [ -z "$SERIAL_PORT" ]; then
    echo -e "${RED}[!] No serial port entered. Exiting...${NC}"
    exit 1
fi

# Check if port exists
if [ ! -e "$SERIAL_PORT" ]; then
    echo -e "${YELLOW}[!] Warning: Serial port $SERIAL_PORT does not exist.${NC}"
    read -p "Do you want to continue anyway? (y/n): " CONTINUE
    if [ "$CONTINUE" != "y" ] && [ "$CONTINUE" != "Y" ]; then
        echo "Exiting..."
        exit 1
    fi
fi

echo ""
echo -e "${YELLOW}[*] Starting to flash ATtiny85 bootloader...${NC}"
echo ""

# Run avrdude command
"$AVRDUDE_PATH" -C"$AVRDUDE_CONF" -F -v -pattiny85 -cstk500v1 -P"$SERIAL_PORT" -b19200 \
    -Uflash:w:"$HEX_FILE":i \
    -U lfuse:w:0xe1:m \
    -U hfuse:w:0xdd:m \
    -U efuse:w:0xfe:m

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}[+] SUCCESS! Bootloader flashed successfully.${NC}"
    echo ""
else
    echo ""
    echo -e "${RED}[!] ERROR: Flashing failed with error code $?${NC}"
    echo ""
    echo "Common issues:"
    echo "  - Wrong serial port selected"
    echo "  - Arduino not connected or not running ArduinoISP sketch"
    echo "  - Incorrect wiring between Arduino and ATtiny85"
    echo "  - Insufficient permissions (try: sudo $0)"
    echo ""
    exit 1
fi
