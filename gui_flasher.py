#!/usr/bin/env python3
"""
ATtiny85 Bootloader Flasher GUI
Cross-platform GUI application for flashing ATtiny85 bootloader
using Arduino as ISP programmer
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import platform
import os
import sys
import glob

# Constants
DEFAULT_AVRDUDE_CONF = "/etc/avrdude.conf"


class ATtiny85FlasherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ATtiny85 Bootloader Flasher")
        self.root.geometry("800x900")
        self.root.resizable(True, True)
        
        # Detect OS
        self.os_type = platform.system()
        
        # Get script directory
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            self.script_dir = os.path.dirname(sys.executable)
        else:
            # Running as script
            self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.hex_file = os.path.join(self.script_dir, "ATtiny85.hex")
        
        # Create GUI
        self.create_widgets()
        
        # Auto-detect avrdude and ports
        self.detect_avrdude()
        self.refresh_ports()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        row = 0
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="ATtiny85 Bootloader Flasher",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=row, column=0, pady=(0, 10), sticky=tk.W)
        row += 1
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="Flash Digispark bootloader to ATtiny85 using Arduino as ISP",
            font=("Arial", 10)
        )
        subtitle_label.grid(row=row, column=0, pady=(0, 20), sticky=tk.W)
        row += 1
        
        # Pin diagram section
        diagram_frame = ttk.LabelFrame(main_frame, text="Connection Diagram", padding="10")
        diagram_frame.grid(row=row, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        diagram_frame.columnconfigure(0, weight=1)
        row += 1
        
        diagram_text = """
               ATtiny85 / Digispark                Arduino UNO
               +------------------+
               |                  |
               |         5V       |------------- 5V  (Arduino Uno)
               |                  |
               |       GND        |------------- GND (Arduino Uno)
               |                  |
               |   Pin 0    o-----|------------- Pin 11 (Arduino Uno)
               |   Pin 1    o-----|------------- Pin 12 (Arduino Uno)
               |   Pin 2    o-----|------------- Pin 13 (Arduino Uno)
               |                  |
               |   Pin 5    o-----|------------- Pin 10 (Arduino Uno)
               +------------------+
        """
        
        diagram_display = tk.Text(diagram_frame, height=14, width=70, font=("Courier", 9))
        diagram_display.insert("1.0", diagram_text)
        diagram_display.config(state=tk.DISABLED)
        diagram_display.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Connection table
        table_frame = ttk.LabelFrame(main_frame, text="Connection Table", padding="10")
        table_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        row += 1
        
        # Create table header
        headers = ["ATtiny85 Pin", "Arduino Uno Pin"]
        connections = [
            ("Pin 0", "Pin 11"),
            ("Pin 1", "Pin 12"),
            ("Pin 2", "Pin 13"),
            ("Pin 5", "Pin 10"),
            ("5V", "5V"),
            ("GND", "GND")
        ]
        
        for col, header in enumerate(headers):
            label = ttk.Label(table_frame, text=header, font=("Arial", 10, "bold"))
            label.grid(row=0, column=col, padx=10, pady=5, sticky=tk.W)
        
        for row_idx, (attiny_pin, arduino_pin) in enumerate(connections, start=1):
            ttk.Label(table_frame, text=attiny_pin).grid(row=row_idx, column=0, padx=10, pady=2, sticky=tk.W)
            ttk.Label(table_frame, text=arduino_pin).grid(row=row_idx, column=1, padx=10, pady=2, sticky=tk.W)
        
        # Configuration section
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        row += 1
        
        # Serial port selection
        ttk.Label(config_frame, text="Serial Port:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        port_frame = ttk.Frame(config_frame)
        port_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        port_frame.columnconfigure(0, weight=1)
        
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(port_frame, textvariable=self.port_var, width=40)
        self.port_combo.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        refresh_btn = ttk.Button(port_frame, text="Refresh", command=self.refresh_ports, width=10)
        refresh_btn.grid(row=0, column=1)
        
        # Avrdude path
        ttk.Label(config_frame, text="Avrdude:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.avrdude_label = ttk.Label(config_frame, text="Detecting...", foreground="gray")
        self.avrdude_label.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Hex file path
        ttk.Label(config_frame, text="Hex File:").grid(row=2, column=0, sticky=tk.W, pady=5)
        hex_status = "Found" if os.path.exists(self.hex_file) else "Not Found"
        hex_color = "green" if os.path.exists(self.hex_file) else "red"
        self.hex_label = ttk.Label(config_frame, text=f"{hex_status}: {self.hex_file}", foreground=hex_color)
        self.hex_label.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Flash button
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, pady=(0, 10))
        row += 1
        
        self.flash_btn = ttk.Button(
            button_frame,
            text="Flash Bootloader",
            command=self.flash_bootloader,
            width=30
        )
        self.flash_btn.grid(row=0, column=0, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        row += 1
        
        # Output console
        console_frame = ttk.LabelFrame(main_frame, text="Console Output", padding="10")
        console_frame.grid(row=row, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(row, weight=1)
        row += 1
        
        self.console = scrolledtext.ScrolledText(
            console_frame,
            height=15,
            width=80,
            font=("Courier", 9),
            state=tk.DISABLED
        )
        self.console.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.grid(row=row, column=0, sticky=(tk.W, tk.E))
    
    def log(self, message, tag=None):
        """Log message to console"""
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, message + "\n")
        if tag:
            # Configure tag colors
            self.console.tag_config("error", foreground="red")
            self.console.tag_config("success", foreground="green")
            self.console.tag_config("info", foreground="blue")
            
            # Apply tag to last line
            line_start = self.console.index("end-2c linestart")
            line_end = self.console.index("end-1c")
            self.console.tag_add(tag, line_start, line_end)
        
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def get_serial_ports(self):
        """Get list of available serial ports based on OS"""
        ports = []
        
        if self.os_type == "Windows":
            # Windows COM ports
            # Try to use pyserial if available, otherwise list common ports
            try:
                import serial
                for i in range(256):
                    try:
                        port = f"COM{i}"
                        s = serial.Serial(port)
                        s.close()
                        ports.append(port)
                    except (OSError, serial.SerialException):
                        pass
            except ImportError:
                # If serial module not available, just list common ports
                pass
            
            # Fallback: list common ports if none found
            if not ports:
                ports = [f"COM{i}" for i in range(1, 21)]
        
        elif self.os_type == "Darwin":  # macOS
            ports = glob.glob("/dev/cu.usb*") + glob.glob("/dev/cu.wchusbserial*")
            if not ports:
                ports = ["/dev/cu.usbserial", "/dev/cu.usbmodem"]
        
        elif self.os_type == "Linux":
            ports = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")
            if not ports:
                ports = ["/dev/ttyUSB0", "/dev/ttyACM0"]
        
        return sorted(ports) if ports else ["No ports found"]
    
    def refresh_ports(self):
        """Refresh the list of available serial ports"""
        ports = self.get_serial_ports()
        self.port_combo['values'] = ports
        if ports and ports[0] != "No ports found":
            self.port_combo.current(0)
        self.log(f"[*] Found {len(ports)} serial port(s)", "info")
    
    def find_avrdude_windows(self):
        """Find avrdude on Windows"""
        username = os.environ.get('USERNAME', '')
        base_path = f"C:\\Users\\{username}\\AppData\\Local\\Arduino15\\packages\\arduino\\tools\\avrdude"
        
        if os.path.exists(base_path):
            versions = os.listdir(base_path)
            if versions:
                latest = sorted(versions)[-1]
                avrdude_path = os.path.join(base_path, latest, "bin", "avrdude.exe")
                avrdude_conf = os.path.join(base_path, latest, "etc", "avrdude.conf")
                if os.path.exists(avrdude_path) and os.path.exists(avrdude_conf):
                    return avrdude_path, avrdude_conf
        
        return None, None
    
    def find_avrdude_macos(self):
        """Find avrdude on macOS"""
        paths = [
            os.path.expanduser("~/Library/Arduino15/packages/arduino/tools/avrdude"),
            "/Applications/Arduino.app/Contents/Java/hardware/tools/avr/bin",
            "/usr/local/bin",
            "/opt/homebrew/bin"
        ]
        
        for base_path in paths:
            if "Arduino15" in base_path and os.path.exists(base_path):
                versions = os.listdir(base_path)
                if versions:
                    latest = sorted(versions)[-1]
                    avrdude_path = os.path.join(base_path, latest, "bin", "avrdude")
                    avrdude_conf = os.path.join(base_path, latest, "etc", "avrdude.conf")
                    if os.path.exists(avrdude_path) and os.path.exists(avrdude_conf):
                        return avrdude_path, avrdude_conf
            elif os.path.exists(os.path.join(base_path, "avrdude")):
                avrdude_path = os.path.join(base_path, "avrdude")
                avrdude_conf = DEFAULT_AVRDUDE_CONF
                return avrdude_path, avrdude_conf
        
        # Check PATH
        try:
            result = subprocess.run(["which", "avrdude"], capture_output=True, text=True)
            if result.returncode == 0:
                avrdude_path = result.stdout.strip()
                return avrdude_path, DEFAULT_AVRDUDE_CONF
        except (subprocess.SubprocessError, OSError, FileNotFoundError):
            pass
        
        return None, None
    
    def find_avrdude_linux(self):
        """Find avrdude on Linux"""
        paths = [
            os.path.expanduser("~/.arduino15/packages/arduino/tools/avrdude"),
            "/usr/share/arduino/hardware/tools/avr/bin",
            "/usr/bin",
            "/usr/local/bin"
        ]
        
        for base_path in paths:
            if ".arduino15" in base_path and os.path.exists(base_path):
                versions = os.listdir(base_path)
                if versions:
                    latest = sorted(versions)[-1]
                    avrdude_path = os.path.join(base_path, latest, "bin", "avrdude")
                    avrdude_conf = os.path.join(base_path, latest, "etc", "avrdude.conf")
                    if os.path.exists(avrdude_path) and os.path.exists(avrdude_conf):
                        return avrdude_path, avrdude_conf
            elif os.path.exists(os.path.join(base_path, "avrdude")):
                avrdude_path = os.path.join(base_path, "avrdude")
                avrdude_conf = DEFAULT_AVRDUDE_CONF
                return avrdude_path, avrdude_conf
        
        # Check PATH
        try:
            result = subprocess.run(["which", "avrdude"], capture_output=True, text=True)
            if result.returncode == 0:
                avrdude_path = result.stdout.strip()
                return avrdude_path, DEFAULT_AVRDUDE_CONF
        except (subprocess.SubprocessError, OSError, FileNotFoundError):
            pass
        
        return None, None
    
    def detect_avrdude(self):
        """Detect avrdude installation"""
        self.log("[*] Detecting avrdude installation...", "info")
        
        if self.os_type == "Windows":
            self.avrdude_path, self.avrdude_conf = self.find_avrdude_windows()
        elif self.os_type == "Darwin":
            self.avrdude_path, self.avrdude_conf = self.find_avrdude_macos()
        elif self.os_type == "Linux":
            self.avrdude_path, self.avrdude_conf = self.find_avrdude_linux()
        else:
            self.avrdude_path, self.avrdude_conf = None, None
        
        if self.avrdude_path and self.avrdude_conf:
            self.avrdude_label.config(text=f"Found: {self.avrdude_path}", foreground="green")
            self.log(f"[+] Found avrdude: {self.avrdude_path}", "success")
            self.log(f"[+] Config file: {self.avrdude_conf}", "success")
        else:
            self.avrdude_label.config(text="Not found - Please install Arduino IDE", foreground="red")
            self.log("[!] Avrdude not found!", "error")
            self.log("[!] Please install Arduino IDE or avrdude", "error")
    
    def validate_flash(self):
        """Validate that all requirements are met for flashing"""
        errors = []
        
        if not os.path.exists(self.hex_file):
            errors.append(f"Hex file not found: {self.hex_file}")
        
        if not self.avrdude_path or not os.path.exists(self.avrdude_path):
            errors.append("Avrdude not found. Please install Arduino IDE.")
        
        if not self.port_var.get() or self.port_var.get() == "No ports found":
            errors.append("Please select a valid serial port.")
        
        return errors
    
    def flash_bootloader(self):
        """Flash the bootloader in a separate thread"""
        errors = self.validate_flash()
        
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            for error in errors:
                self.log(f"[!] {error}", "error")
            return
        
        # Disable flash button
        self.flash_btn.config(state=tk.DISABLED)
        self.progress.start(10)
        self.status_var.set("Flashing...")
        
        # Run in separate thread to avoid blocking GUI
        thread = threading.Thread(target=self._flash_thread)
        thread.daemon = True
        thread.start()
    
    def _flash_thread(self):
        """Thread function to execute avrdude"""
        try:
            serial_port = self.port_var.get()
            
            self.log("=" * 80)
            self.log("[*] Starting bootloader flash process...", "info")
            self.log(f"[*] Target: ATtiny85")
            self.log(f"[*] Port: {serial_port}")
            self.log(f"[*] Hex file: {self.hex_file}")
            self.log("=" * 80)
            
            # Build avrdude command
            cmd = [
                self.avrdude_path,
                f"-C{self.avrdude_conf}",
                "-F",
                "-v",
                "-pattiny85",
                "-cstk500v1",
                f"-P{serial_port}",
                "-b19200",
                f"-Uflash:w:{self.hex_file}:i",
                "-U", "lfuse:w:0xe1:m",
                "-U", "hfuse:w:0xdd:m",
                "-U", "efuse:w:0xfe:m"
            ]
            
            self.log(f"[*] Executing: {' '.join(cmd)}", "info")
            self.log("")
            
            # Execute command
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Read output line by line
            for line in process.stdout:
                self.log(line.rstrip())
            
            # Wait for completion
            process.wait()
            
            self.log("")
            self.log("=" * 80)
            
            if process.returncode == 0:
                self.log("[+] SUCCESS! Bootloader flashed successfully!", "success")
                self.status_var.set("Flash completed successfully!")
                messagebox.showinfo("Success", "Bootloader flashed successfully!")
            else:
                self.log(f"[!] ERROR: Flashing failed with error code {process.returncode}", "error")
                self.log("[!] Common issues:", "error")
                self.log("    - Wrong serial port selected")
                self.log("    - Arduino not running ArduinoISP sketch")
                self.log("    - Incorrect wiring between Arduino and ATtiny85")
                self.log("    - Insufficient permissions (try running as admin/sudo)")
                self.status_var.set("Flash failed!")
                messagebox.showerror("Error", f"Flashing failed with error code {process.returncode}")
            
            self.log("=" * 80)
            
        except Exception as e:
            self.log(f"[!] Exception occurred: {str(e)}", "error")
            self.status_var.set("Error occurred!")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        finally:
            # Re-enable flash button
            self.root.after(0, self._flash_complete)
    
    def _flash_complete(self):
        """Called after flash completes to update GUI"""
        self.progress.stop()
        self.flash_btn.config(state=tk.NORMAL)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ATtiny85FlasherGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
