# CamJam EduKit 3 - Robotics
# Wii controller remote control script (Debugged Version)

from gpiozero import Robot, LED
from evdev import InputDevice, list_devices, ecodes
import time
import sys
import os

# ===========================================================================
# CONFIGURATION
# ===========================================================================

# Motor Pins
robot = Robot(left=(10, 9), right=(8, 7))

# LED Pin
status_led = LED(25)

# ===========================================================================
# HELPER FUNCTIONS
# ===========================================================================

def get_wii_remote():
    """Finds the Wii Remote and prints debug info."""
    print("Scanning for devices...")
    
    # Get list of device paths
    try:
        device_paths = list_devices()
    except OSError:
        print("ERROR: Unable to access device list.")
        print("TRY RUNNING WITH SUDO: sudo python3 your_script.py")
        sys.exit()

    if not device_paths:
        print("No devices found at all. (Are you running with sudo?)")
        return None

    # Check every device
    for path in device_paths:
        try:
            device = InputDevice(path)
            print(f"  Found: {device.name} at {path}")
            
            # CHECK FOR YOUR SPECIFIC NAME HERE
            if "RVL-CNT-01" in device.name:
                return device
        except:
            pass
            
    return None

# ===========================================================================
# MAIN LOGIC
# ===========================================================================

print("---------------------------------------")
print("Starting Wii Remote Search...")
print("---------------------------------------")

status_led.on()

# 1. Connect to the Remote
wii_device = get_wii_remote()

if wii_device is None:
    print("\nFAILURE: Wii Remote not found in the list above.")
    print("1. Ensure it is paired via Bluetooth.")
    print("2. Press any button on the remote to wake it up.")
    status_led.off()
    sys.exit()

print(f"\nSUCCESS: Connected to {wii_device.name}")
print("Press D-Pad to drive.")
print("Press PLUS (+) to quit.")
status_led.off()

# 2. Grab the device (prevents other apps from reading it)
try:
    wii_device.grab()
except Exception:
    print("Warning: Could not grab device (another app might be using it).")

# 3. Main Loop
try:
    for event in wii_device.read_loop():
        if event.type == ecodes.EV_KEY:
            
            # event.value: 1=Pressed, 0=Released
            if event.value == 1: 
                status_led.on()
                if event.code == ecodes.KEY_LEFT:
                    print("Left")
                    robot.left()
                elif event.code == ecodes.KEY_RIGHT:
                    print("Right")
                    robot.right()
                elif event.code == ecodes.KEY_UP:
                    print("Forward")
                    robot.forward()
                elif event.code == ecodes.KEY_DOWN:
                    print("Backward")
                    robot.backward()
                elif event.code == ecodes.KEY_NEXT or event.code == 407: # 407 is sometimes NEXT
                    print("Quitting...")
                    robot.stop()
                    status_led.off()
                    sys.exit()

            elif event.value == 0: # Button Released
                status_led.off()
                # Stop if it was a driving key
                if event.code in [ecodes.KEY_LEFT, ecodes.KEY_RIGHT, ecodes.KEY_UP, ecodes.KEY_DOWN]:
                    robot.stop()

except KeyboardInterrupt:
    print("\nStopping...")
except OSError:
    print("\nDevice disconnected unexpectedly.")
finally:
    robot.stop()
    status_led.off()
