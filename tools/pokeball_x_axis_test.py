#!/usr/bin/env python3
"""
Pokeball X-Axis Isolation Test
Captures data in specific phases to identify X-axis byte location
"""

import asyncio
from bleak import BleakClient
import json
import time

MAC_ADDRESS = "58:2F:40:8D:50:71"
INPUT_UUID = "6675e16c-f36d-4567-bb55-6b51e27a23e6"

class XAxisTest:
    def __init__(self):
        self.data_log = {
            "center": [],
            "left_only": [],
            "center_after_left": [],
            "right_only": [],
            "center_after_right": [],
            "metadata": {
                "start_time": time.time(),
                "description": "X-axis isolation test"
            }
        }
        self.phase = "center"
        self.count = 0
        
    async def connect(self):
        print("Connecting...")
        client = BleakClient(MAC_ADDRESS)
        await client.connect()
        print("Connected!")
        return client
    
    def handler(self, sender, data):
        self.count += 1
        
        # Save every packet during collection phases
        entry = {
            "packet_num": self.count,
            "timestamp": time.time() - self.data_log["metadata"]["start_time"],
            "bytes": list(data[:10]),  # First 10 bytes only
            "phase": self.phase
        }
        
        if self.phase in self.data_log:
            self.data_log[self.phase].append(entry)
        
        # Show progress
        if self.count % 30 == 0:
            if len(data) >= 5:
                print(f"  [{self.phase}] b[1]={data[1]:3d} b[2]={data[2]:3d} b[3]={data[3]:3d} b[4]={data[4]:3d}")
    
    async def run(self):
        client = await self.connect()
        
        print("\n" + "="*60)
        print("X-AXIS ISOLATION TEST")
        print("="*60)
        print("Follow these instructions EXACTLY:")
        print()
        print("1. CENTER: Keep joystick centered (3 sec)")
        print("2. LEFT: Push stick FULLY LEFT only, no up/down (3 sec)")
        print("3. CENTER: Release back to center (2 sec)")
        print("4. RIGHT: Push stick FULLY RIGHT only, no up/down (3 sec)")
        print("5. CENTER: Release back to center (2 sec)")
        print()
        print("Try to keep vertical position constant!")
        print("="*60 + "\n")
        
        await client.start_notify(INPUT_UUID, self.handler)
        
        try:
            # Phase 1: Center baseline
            print("Phase 1: CENTER - Don't touch")
            self.phase = "center"
            await asyncio.sleep(3)
            
            # Phase 2: Left only
            print("\nPhase 2: Push FULLY LEFT now (no up/down)!")
            self.phase = "left_only"
            await asyncio.sleep(3)
            
            # Phase 3: Return to center
            print("\nPhase 3: Release to CENTER")
            self.phase = "center_after_left"
            await asyncio.sleep(2)
            
            # Phase 4: Right only
            print("\nPhase 4: Push FULLY RIGHT now (no up/down)!")
            self.phase = "right_only"
            await asyncio.sleep(3)
            
            # Phase 5: Return to center
            print("\nPhase 5: Release to CENTER")
            self.phase = "center_after_right"
            await asyncio.sleep(2)
            
        except KeyboardInterrupt:
            print("\nInterrupted")
        
        await client.disconnect()
        
        # Save data
        filename = f"pokeball_x_axis_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(self.data_log, f, indent=2)
        
        # Quick analysis
        print(f"\n✅ Data saved to: {filename}")
        print("\nQuick Analysis:")
        print("-" * 40)
        
        # Compare averages
        if len(self.data_log["center"]) > 0 and len(self.data_log["left_only"]) > 0:
            for byte_idx in range(2, 5):  # Check bytes 2, 3, 4
                center_vals = [p["bytes"][byte_idx] for p in self.data_log["center"][:20]]
                left_vals = [p["bytes"][byte_idx] for p in self.data_log["left_only"][:20]]
                right_vals = [p["bytes"][byte_idx] for p in self.data_log["right_only"][:20] if len(self.data_log["right_only"]) > 0]
                
                center_avg = sum(center_vals) / len(center_vals)
                left_avg = sum(left_vals) / len(left_vals)
                right_avg = sum(right_vals) / len(right_vals) if right_vals else 0
                
                print(f"Byte[{byte_idx}]:")
                print(f"  Center: {center_avg:.1f} (range {min(center_vals)}-{max(center_vals)})")
                print(f"  Left:   {left_avg:.1f} (range {min(left_vals)}-{max(left_vals)})")
                if right_vals:
                    print(f"  Right:  {right_avg:.1f} (range {min(right_vals)}-{max(right_vals)})")
                
                # Check if this byte could be X-axis
                left_change = abs(left_avg - center_avg)
                right_change = abs(right_avg - center_avg) if right_vals else 0
                
                if left_change > 20 or right_change > 20:
                    print(f"  ⭐ Possible X-axis! Changes: L={left_change:.1f}, R={right_change:.1f}")
                print()

if __name__ == "__main__":
    print("Pokeball X-Axis Isolation Test")
    print("Reset Pokeball with pin, press button for pairing")
    print("Starting in 3 seconds...")
    time.sleep(3)
    asyncio.run(XAxisTest().run())