#!/usr/bin/env python3
import asyncio
import time
from bleak import BleakClient
import statistics

MAC_ADDRESS = "58:2F:40:8D:50:71"
INPUT_UUID = "6675e16c-f36d-4567-bb55-6b51e27a23e6"

class PokeballCalibrator:
    def __init__(self):
        self.client = None
        self.x_values = []
        self.y_values = []
        self.sample_count = 0
        self.max_samples = 500  # Collect 500 samples for calibration
        
    async def connect(self):
        print(f"Connecting to {MAC_ADDRESS}...")
        self.client = BleakClient(MAC_ADDRESS)
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                await self.client.connect()
                print("Connected successfully!")
                break
            except Exception as e:
                print(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2)
                else:
                    raise
        
        await self.client.start_notify(INPUT_UUID, self.notification_handler)
    
    def notification_handler(self, sender, data):
        if len(data) >= 4 and self.sample_count < self.max_samples:
            x = data[2]
            y = data[3]
            
            self.x_values.append(x)
            self.y_values.append(y)
            self.sample_count += 1
            
            if self.sample_count % 50 == 0:
                print(f"Collected {self.sample_count}/{self.max_samples} samples...")
                print(f"  Current reading: X={x}, Y={y}")
    
    async def calibrate(self):
        try:
            await self.connect()
            
            print("\n" + "="*60)
            print("POKEBALL CALIBRATION")
            print("="*60)
            print("IMPORTANT: DO NOT TOUCH THE JOYSTICK!")
            print("Let it rest in its natural center position.")
            print("Collecting data for calibration...")
            print("="*60 + "\n")
            
            # Wait for data collection
            while self.sample_count < self.max_samples:
                await asyncio.sleep(0.1)
            
            # Calculate statistics
            x_median = int(statistics.median(self.x_values))
            y_median = int(statistics.median(self.y_values))
            x_mean = statistics.mean(self.x_values)
            y_mean = statistics.mean(self.y_values)
            x_min = min(self.x_values)
            x_max = max(self.x_values)
            y_min = min(self.y_values)
            y_max = max(self.y_values)
            
            # Calculate drift
            x_drift = x_max - x_min
            y_drift = y_max - y_min
            
            print("\n" + "="*60)
            print("CALIBRATION RESULTS")
            print("="*60)
            print(f"Center X: {x_median} (median), {x_mean:.1f} (mean)")
            print(f"Center Y: {y_median} (median), {y_mean:.1f} (mean)")
            print(f"X range: {x_min} - {x_max} (drift: {x_drift})")
            print(f"Y range: {y_min} - {y_max} (drift: {y_drift})")
            
            # Recommend deadzone based on drift
            recommended_deadzone = max(x_drift, y_drift) + 5
            
            print(f"\nRecommended settings:")
            print(f"  center_x = {x_median}")
            print(f"  center_y = {y_median}")
            print(f"  deadzone = {recommended_deadzone}")
            
            # Save calibration to file
            with open('/home/user/pokeball_calibration.txt', 'w') as f:
                f.write(f"center_x={x_median}\n")
                f.write(f"center_y={y_median}\n")
                f.write(f"deadzone={recommended_deadzone}\n")
                f.write(f"# Calibrated at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# X range: {x_min}-{x_max}, Y range: {y_min}-{y_max}\n")
            
            print("\nCalibration saved to: /home/user/pokeball_calibration.txt")
            print("="*60)
            
        except Exception as e:
            print(f"Calibration failed: {e}")
        finally:
            if self.client and self.client.is_connected:
                await self.client.disconnect()

async def main():
    calibrator = PokeballCalibrator()
    await calibrator.calibrate()

if __name__ == "__main__":
    print("Pokeball Calibration Tool")
    print("-" * 40)
    print("This will find the true center position of your joystick")
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    asyncio.run(main())