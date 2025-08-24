# Pokeball Plus Mouse Controller 🎮

Transform your Nintendo Pokeball Plus into a functional Bluetooth mouse! This project provides a Python driver that enables the Pokeball Plus controller to work as a mouse input device on Linux systems.

## Features

- ✨ **Full mouse control** using the Pokeball's analog stick
- 🎯 **Left and right click** support via physical buttons
- 🔄 **Auto-calibration** for accurate center positioning
- 📡 **Bluetooth Low Energy** connection
- 🐧 **Linux compatible** (tested on Raspberry Pi OS)

## How It Works

This driver decodes the Bluetooth Low Energy data packets from the Pokeball Plus:
- **X-axis**: Digital control (left/center/right) from low nibble bit patterns in byte[3]
- **Y-axis**: Analog control with variable speed from byte[4]
- **Buttons**: Top button for left click, stick press for right click

### The Discovery

The X-axis encoding was discovered through careful analysis of the BLE data. The Pokeball Plus uses a clever bit pattern in the low nibble of byte[3]:
- `001X` (binary) = LEFT
- `01XX` (binary) = CENTER  
- `1XXX` (binary) = RIGHT

This digital encoding provides three discrete horizontal positions, while the Y-axis provides smooth analog vertical movement.

## Requirements

- Python 3.7+
- Linux system with Bluetooth support
- Required Python packages:
  ```bash
  pip install bleak
  sudo apt install python3-evdev
  ```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/pokeball-plus-mouse.git
   cd pokeball-plus-mouse
   ```

2. Install dependencies:
   ```bash
   pip install bleak
   sudo apt install python3-evdev
   ```

3. Make the script executable:
   ```bash
   chmod +x pokeball_mouse_working.py
   ```

## Usage

1. **Find your Pokeball's MAC address**:
   ```bash
   # Reset Pokeball with pin, press top button for pairing mode
   sudo bluetoothctl scan on
   # Look for "Pokemon PBP" - note the MAC address (XX:XX:XX:XX:XX:XX)
   # Press Ctrl+C to stop scanning
   ```

2. **Update the MAC address in the script**:
   - Open `pokeball_mouse_working.py` in a text editor
   - Find line 24: `MAC_ADDRESS = "58:2F:40:8D:50:71"`
   - Replace with your Pokeball's MAC address
   - Save the file

3. **Run the mouse driver**:
   ```bash
   # Reset Pokeball again before running
   sudo python3 pokeball_mouse_working.py
   ```

3. **Controls**:
   - Move the analog stick to control the mouse cursor
   - Top button (B) = Left click
   - Stick press (A) = Right click

## Configuration

You can adjust the mouse sensitivity by editing these values in `pokeball_mouse_working.py`:

```python
self.x_speed = 20           # Horizontal movement speed (digital)
self.y_sensitivity = 0.4    # Vertical movement sensitivity (analog)
self.y_deadzone = 15        # Deadzone for analog stick
```

## Technical Details

### BLE Data Packet Structure

| Byte | Content | Type |
|------|---------|------|
| 0 | Packet counter | Counter |
| 1 | Button state | Digital (00=none, 01=B, 02=A, 03=both) |
| 2 | Unused | - |
| 3 | X-axis in low nibble | Digital (bit pattern) |
| 4 | Y-axis | Analog (range ~32-192) |
| 5-16 | Gyro/Accel data | Not implemented |

### Connection Details

- **MAC Address**: Device-specific (find with `bluetoothctl scan on`)
- **BLE Service UUID**: Device-specific
- **Characteristic UUID**: `6675e16c-f36d-4567-bb55-6b51e27a23e6`

## Troubleshooting

**Connection Issues:**
- Ensure Bluetooth is enabled: `sudo systemctl start bluetooth`
- Reset the Pokeball Plus using the hardware reset button
- Run the script with sudo for device access permissions

**Mouse Not Moving:**
- Check that python3-evdev is installed
- Verify the Pokeball is connected (LED should be solid)
- Try recalibrating by restarting the script

**Drift or Erratic Movement:**
- The device auto-calibrates on startup - keep the stick centered for 2 seconds
- Adjust the deadzone value if needed

## Scripts Included

### Main Driver
- **`pokeball_mouse_working.py`** - Fully functional mouse driver with both X and Y axis control

### Development & Analysis Tools
- **`pokeball_dashboard.py`** - Real-time data visualization dashboard showing live byte values and interpretations
- **`pokeball_calibrate.py`** - Calibration utility for finding joystick center position
- **`pokeball_x_axis_test.py`** - Specialized test for isolating X-axis movement data
- **`pokeball_analyzer.py`** - Data capture tool that records packets in movement phases
- **`pokeball_live_debug.py`** - Live debugging viewer for real-time byte monitoring
- **`pokeball_quick_test.py`** - Simple connection test to verify Pokeball is responding

### Legacy/Development Versions
- **`pokeball_mouse.py`** - Initial mouse driver attempt (has drift issues)
- **`pokeball_mouse_v2.py`** - Vertical-only implementation before X-axis solution
- **`pokeball_mouse_final.py`** - Previous "production" version with X-axis disabled
- **`pokeball_controller.py`** through **`pokeball_controller_v4.py`** - Early development iterations
- **`pokeball_simple.py`** - Basic connection and data reading script
- **`pokeball_debug.py`** - Debug utilities
- **`pokeball_auto.py`** - Auto-reconnection attempts
- **`pokeball_scanner.py`** - Bluetooth device scanner
- **`pokeball_mouse_test.py`** - Early testing script
- **`test_pokeball.py`** - Unit tests for Pokeball connection

### Data Files
- **`pokeball_data_*.json`** - Captured movement data from analyzer
- **`pokeball_x_axis_*.json`** - Isolated X-axis test data captures
- **`pokeball_calibration.txt`** - Saved calibration values

## Development Journey

This project involved extensive reverse engineering of the Pokeball Plus BLE protocol. Initial attempts using documented Nintendo Switch controller protocols failed, leading to the discovery that the Pokeball Plus uses a unique encoding scheme. The breakthrough came from visualizing the raw data in real-time and identifying the bit patterns in the low nibble of byte[3].

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Acknowledgments

- Claude
- Reddit user u/Unity3D community for initial Pokeball Plus reverse engineering work
- GitHub user dekuNukem Nintendo Switch Reverse Engineering project for protocol insights

## License

This project is provided as-is for educational and personal use. Nintendo, Pokeball Plus, and Pokemon are trademarks of Nintendo/Game Freak/The Pokemon Company.

## Disclaimer

This is an unofficial project and is not affiliated with Nintendo, Game Freak, or The Pokemon Company. Use at your own risk.

---

**Tested on:** Raspberry Pi CM4 with GPi Case 2 running Raspberry Pi OS (64-bit)

**Status:** Fully functional with both X and Y axis control! 🎉
