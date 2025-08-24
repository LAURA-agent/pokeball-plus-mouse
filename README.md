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


## Development Journey

This project was an impromptu experiment that was started while searching for a PS4 controller that would work as a bluetooth mouse for the GPi Case 2 (a Raspberry Pi Gameboy).  While digging through through a drawer in my entertainment center i found the old pokeball that my son used to play Pokemon Let's Go (Nintendo Switch 2018).  After a serious of attempts to connect it I realized that it was going to be much more complex than I initially thought.  After a couple of attempts to have Claude Code find the answer itself, i searched and found a few Reddit posts and GitHub repositories of others who had attempted to reverse engineer Nintendo devices.  It was apparent that I was not the only one who was having trouble getting the x-axis to map properly.  There were many attempts to decode the raw bytes, but many involved complex calculations that didn't make sense.  After about 8 hours of different debuggers and tests, I took all of the data I had collected and asked Gemini to investigate and then provide a better debugger.  I took Gemini's response and gave it to Claude Code, and it took the idea for a visual dashboard and improved it to the point that i had something that would provide visual feedback for the different nibbles.  After about 5 minutes of staring at the dashboard while moving the joystick around I noticed that the low nibble of byte[3] was static at 0111 when the joystick was in the nuetral position, and was 0010 or 0011 when pressed left, and when pressed right it was 1100 (or other numbers that were all above 1000). It was at that point that i realized that when it came to x-axis position that the last bit in the nibble was not providing anything meaningful and was the source of all of calculation problems.  To me, this was a perfect example of multi-modal human-ai collaboration to solve a problem.  I worked with Claude to come up with a plan and work towards accomplishing it, then when I got stuck, I used Gemini to be an objective 3rd party to review and provide suggestions, then I had Claude reign the over engineered solution into something a little more human friendly.  It only took 5 minutes of playing around with the dashboard to find the pattern in the low nibble of byte[3]. 

## Contributing

Contributions are welcome!  While i have the basics down, the actual mouse movement and accuracy can definitely be improved, but I'm wanting to work on other bugs with my Gameboy for now.  Please feel free to submit pull requests or open issues for bugs and feature requests if you have suggestions.

## Acknowledgments

- Claude
- Reddit user u/Unity3D for initial Pokeball Plus reverse engineering work
- GitHub user dekuNukem Nintendo Switch Reverse Engineering project for protocol insights

## License

This project is provided as-is for educational and personal use. Nintendo, Pokeball Plus, and Pokemon are trademarks of Nintendo/Game Freak/The Pokemon Company.

## Disclaimer

This is an unofficial project and is not affiliated with Nintendo, Game Freak, or The Pokemon Company. Use at your own risk.

---

**Tested on:** Raspberry Pi CM4 with GPi Case 2 running Raspberry Pi OS (64-bit)

**Status:** Fully functional with both X and Y axis control! 🎉
