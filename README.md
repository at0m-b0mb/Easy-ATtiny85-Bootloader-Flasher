# Easy ATtiny85 Bootloader Flasher

A cross-platform tool for flashing the ATtiny85 microcontroller (Digispark) bootloader using an Arduino as an ISP programmer. This project provides three different interfaces to suit your needs: Windows batch script, Unix shell script, and a graphical user interface (GUI).

## Features

- **Cross-Platform Support**: Works on Windows, macOS, and Linux
- **Multiple Interfaces**: Choose between command-line or GUI
- **Auto-Detection**: Automatically finds avrdude and serial ports
- **User-Friendly**: Interactive prompts for port selection
- **Custom ASCII Art Banner**: Engaging welcome message in CLI versions
- **Clear Instructions**: Detailed connection diagrams and tables for wiring
- **AVRDUDE Integration**: Utilizes `avrdude` for programming the ATtiny85

## Requirements

### Hardware
- Arduino Uno (or compatible board)
- ATtiny85 microcontroller / Digispark board
- Jumper wires for connections

### Software
- Arduino IDE installed (for `avrdude` tools), or
- `avrdude` installed separately via package manager

### Platform-Specific
- **Windows**: No additional requirements
- **macOS**: No additional requirements
- **Linux**: No additional requirements
- **GUI**: Python 3.x with tkinter (usually pre-installed)

## Connections

### Pin Diagram

![ATtiny85 and Arduino Connections](Image/PinDiagram.jpg)

### Connections Table

| ATtiny85/Digispark Pin | Arduino Uno Pin |
|------------------------|------------------|
| Pin 0                  | Pin 11           |
| Pin 1                  | Pin 12           |
| Pin 2                  | Pin 13           |
| Pin 5                  | Pin 10           |
| 5V                     | 5V               |
| GND                    | GND              |

## Important: Prepare Your Arduino

Before flashing the ATtiny85, you **must** upload the **ArduinoISP** sketch to your Arduino Uno:

1. Open Arduino IDE
2. Go to **File → Examples → 11.ArduinoISP → ArduinoISP**
3. Upload the sketch to your Arduino Uno
4. Wait for upload to complete
5. Now you can proceed with flashing the ATtiny85

## Usage

### Step 1: Connect the Hardware

Connect the ATtiny85 to the Arduino as per the connections table above. Make sure all connections are secure.

### Step 2: Choose Your Interface

Choose the interface that works best for your operating system:

#### Option A: Windows (Batch Script)

1. Clone or download this repository
2. Open Command Prompt
3. Navigate to the repository directory
4. Run the batch script:
   ```cmd
   Easy-ATtiny85-Bootloader-Flasher.bat
   ```
5. Enter the COM port when prompted (e.g., `COM4`)
6. Wait for the flashing process to complete

#### Option B: macOS / Linux (Shell Script)

1. Clone or download this repository
2. Open Terminal
3. Navigate to the repository directory
4. Make the script executable (first time only):
   ```bash
   chmod +x flash_bootloader.sh
   ```
5. Run the shell script:
   ```bash
   ./flash_bootloader.sh
   ```
6. Enter the serial port when prompted (e.g., `/dev/ttyUSB0` for Linux or `/dev/cu.usbserial` for macOS)
7. If you get a permission error, try running with sudo:
   ```bash
   sudo ./flash_bootloader.sh
   ```
8. Wait for the flashing process to complete

#### Option C: GUI (All Platforms)

The GUI version provides a graphical interface with visual connection diagrams and automatic port detection.

**Requirements**: Python 3.x with tkinter (usually pre-installed on most systems)

1. Clone or download this repository
2. Make the script executable (Unix systems only, first time):
   ```bash
   chmod +x gui_flasher.py
   ```
3. Run the GUI:
   
   **On Windows:**
   ```cmd
   python gui_flasher.py
   ```
   
   **On macOS/Linux:**
   ```bash
   python3 gui_flasher.py
   ```
   Or simply:
   ```bash
   ./gui_flasher.py
   ```

4. The GUI will automatically detect:
   - Available serial ports
   - Avrdude installation path
   - The hex file location

5. Select your serial port from the dropdown
6. Click "Flash Bootloader" button
7. Monitor the progress in the console output window

### Step 3: Verify Success

After flashing completes successfully, you should see:
- **CLI**: "SUCCESS! Bootloader flashed successfully."
- **GUI**: Success message dialog and green status in console

Your ATtiny85 is now ready to use with the Digispark bootloader!

## Troubleshooting

### Common Issues

**1. "avrdude not found" or "Avrdude not detected"**
- Install Arduino IDE from https://www.arduino.cc/en/software
- Or install avrdude directly:
  - **macOS**: `brew install avrdude`
  - **Linux**: `sudo apt-get install avrdude` (Debian/Ubuntu) or `sudo yum install avrdude` (RedHat/Fedora)
  - **Windows**: Install Arduino IDE (avrdude is included)

**2. "Serial port not found" or Connection errors**
- Verify your Arduino is connected via USB
- Check that you've uploaded the ArduinoISP sketch to the Arduino
- Try different USB ports or cables
- On Linux, you may need to add your user to the `dialout` group:
  ```bash
  sudo usermod -a -G dialout $USER
  ```
  Then log out and log back in.

**3. "Permission denied" errors (Linux/macOS)**
- Run the script with sudo:
  ```bash
  sudo ./flash_bootloader.sh
  ```
  Or for GUI:
  ```bash
  sudo python3 gui_flasher.py
  ```

**4. Verification errors during flashing**
- Double-check all wiring connections
- Ensure the ATtiny85 is properly seated if using a breadboard
- Try lowering the baud rate (edit the script to change `-b19200` to `-b9600`)
- Check that your Arduino's 5V supply is stable

**5. Python tkinter not found (GUI only)**
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **macOS**: tkinter is included with Python from python.org
- **Windows**: tkinter is included with Python

## What Gets Flashed

The flasher programs:
- **Bootloader**: The Digispark bootloader (`ATtiny85.hex`)
- **Fuse bits**:
  - Low fuse: `0xe1` (16.5 MHz PLL clock)
  - High fuse: `0xdd` (Enable reset pin)
  - Extended fuse: `0xfe` (Self-programming enabled)

These settings configure the ATtiny85 to work as a Digispark-compatible USB development board.

## Files in This Repository

- `Easy-ATtiny85-Bootloader-Flasher.bat` - Windows batch script
- `flash_bootloader.sh` - macOS/Linux shell script
- `gui_flasher.py` - Cross-platform Python GUI application
- `ATtiny85.hex` - Digispark bootloader firmware
- `Digistump.Drivers.zip` - Windows drivers for Digispark (if needed)
- `Image/PinDiagram.jpg` - Visual connection diagram
- `README.md` - This file
- `.gitignore` - Git ignore file for Python artifacts

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- **Original Author**: HackProKP (Kailash Parshad)
- **GitHub**: https://github.com/at0m-b0mb/Easy-ATtiny85-Bootloader-Flasher
- **Bootloader**: Digistump Digispark bootloader

## Disclaimer

This tool is provided as-is. Always double-check your connections before flashing. The authors are not responsible for any damage to your hardware.

## Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Verify your hardware connections match the diagram
3. Ensure ArduinoISP is uploaded to your Arduino
4. Open an issue on GitHub with details about your setup and error messages

Happy Hacking! 🚀
