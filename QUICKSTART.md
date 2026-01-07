# Quick Start Guide

This guide will help you quickly get started with flashing the ATtiny85 bootloader.

## Prerequisites Checklist

- [ ] Arduino Uno (or compatible) board
- [ ] ATtiny85 microcontroller or Digispark board
- [ ] USB cable for Arduino
- [ ] Jumper wires (at least 6)
- [ ] Arduino IDE installed (or avrdude installed separately)

## Step-by-Step Instructions

### 1. Prepare Your Arduino

**IMPORTANT**: Before anything else, upload the ArduinoISP sketch to your Arduino:

1. Open Arduino IDE
2. Connect your Arduino Uno via USB
3. Select your Arduino board and port in Arduino IDE
4. Go to: **File → Examples → 11.ArduinoISP → ArduinoISP**
5. Click **Upload** and wait for completion
6. You should see "Done uploading" message

### 2. Wire the ATtiny85 to Arduino

Make these 6 connections:

| ATtiny85 Pin | Arduino Uno Pin |
|--------------|-----------------|
| Pin 0        | Pin 11          |
| Pin 1        | Pin 12          |
| Pin 2        | Pin 13          |
| Pin 5        | Pin 10          |
| 5V           | 5V              |
| GND          | GND             |

**Tip**: Double-check each connection. A single wrong wire will cause flashing to fail!

### 3. Choose Your Flashing Method

Pick the method that suits your system:

#### Windows Users
```cmd
Easy-ATtiny85-Bootloader-Flasher.bat
```
Then enter your COM port (e.g., `COM4`)

#### Mac/Linux Users
```bash
chmod +x flash_bootloader.sh
./flash_bootloader.sh
```
Then enter your serial port (e.g., `/dev/ttyUSB0` or `/dev/cu.usbserial`)

#### GUI Method (All Platforms)
```bash
python3 gui_flasher.py
```
- Select port from dropdown
- Click "Flash Bootloader"
- Watch the progress!

### 4. Success!

If everything worked, you'll see:
- ✓ "Bootloader flashed successfully"
- Your ATtiny85 now has the Digispark bootloader

## Common Problems & Solutions

| Problem | Solution |
|---------|----------|
| "avrdude not found" | Install Arduino IDE or avrdude |
| "Port not found" | Check USB connection, try different port |
| "Verification error" | Check all 6 wire connections |
| "Permission denied" (Linux/Mac) | Run with `sudo` |
| ArduinoISP not responding | Re-upload ArduinoISP sketch to Arduino |

## What Next?

After successful flashing:
1. Disconnect the ATtiny85 from Arduino
2. You can now use it as a Digispark USB development board
3. Program it using Arduino IDE with Digispark board support
4. The bootloader runs for ~5 seconds on power-up, then runs your program

## Need Help?

- Check the full README.md for detailed troubleshooting
- Verify your wiring matches the diagram in README.md
- Make sure ArduinoISP is uploaded to Arduino
- Open a GitHub issue with your error message

Happy hacking! 🚀
