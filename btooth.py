# CamJam EduKit 3 - Robotics
# Standard Wireless Controller Script (Tank Steering)

from gpiozero import Robot, LED
from evdev import InputDevice, list_devices, ecodes
import time
import sys

# ===========================================================================
# CONFIGURATION
# ===========================================================================

# Motor Pins (Same as before)
# Motor A (Left):  10, 9
# Motor B (Right): 8, 7
robot = Robot(left=(8, 7), right=(10, 9))

# Status LED
status_led = LED(25)

# Controller Deadzone (Ignores small drifts in the stick)
DEADZONE = 0.15 

# ===========================================================================
# HELPER: Find the Controller
# ===========================================================================
def get_gamepad():
    """Finds the first available gamepad/joystick."""
    print("Scanning for controllers...")
    devices = [InputDevice(path) for path in list_devices()]
    
    for device in devices:
        # We look for devices with 'Gamepad', 'Joystick', or 'Controller' in the name
        # Most USB Wireless dongles show up as "Generic USB Joystick" or similar.
        print(f"  Found: {device.name}")
        if any(x in device.name.lower() for x in ['gamepad', 'joystick', 'controller', 'xbox', 'playstation', 'shanwan', 'android']):
            return device
    return None

# ===========================================================================
# HELPER: Map Stick Value to Motor Speed
# ===========================================================================
# ===========================================================================
# HELPER: Map Stick Value to Motor Speed
# ===========================================================================
def map_stick_to_motor(value, min_val=0, max_val=255):
    # 1. Handle Generic 8-bit Controllers (0 to 255)
    if max_val <= 255:
        center = 128
        radius = 127
        normalized = (value - center) / radius
        normalized = -normalized 
        
    # 2. Handle Xbox/PS Controllers (-32768 to 32767)
    else:
        normalized = value / 32767
        normalized = -normalized

    # 3. SAFETY CLAMP (The Fix!)
    # Force value to stay between -1 and 1 no matter what
    if normalized > 1.0:
        normalized = 1.0
    elif normalized < -1.0:
        normalized = -1.0

    # 4. Apply Deadzone
    if abs(normalized) < DEADZONE:
        return 0.0
    
    return normalized

# ===========================================================================
# MAIN LOGIC
# ===========================================================================

print("---------------------------------------")
print("Wireless Controller Robot")
print("---------------------------------------")

gamepad = get_gamepad()

if gamepad is None:
    print("No Gamepad found!")
    print("1. Plug in your USB Wireless Dongle.")
    print("2. Make sure the controller batteries are fresh.")
    print("3. Run this script with 'sudo'.")
    sys.exit()

print(f"Connected to: {gamepad.name}")
print("Controls: Left Stick = Left Motor | Right Stick = Right Motor")
status_led.blink(on_time=0.2, off_time=0.2, n=3) # Blink to confirm

# Variables to store current stick positions
speed_left = 0.0
speed_right = 0.0

# Standard Axis Codes (These work for 90% of controllers)
# ABS_Y (01) is usually Left Stick Y
# ABS_RZ (05) or ABS_RY (04) is usually Right Stick Y
# We will print the codes found so you can debug.

try:
    for event in gamepad.read_loop():
        
        # Look for Analog Stick Events
        if event.type == ecodes.EV_ABS:
            print(f"Axis Moved! Code: {event.code} | Value: {event.value}")
            
            # Left Stick Y-Axis (Usually Code 1)
            if event.code == 1: 
                speed_left = map_stick_to_motor(event.value, gamepad.absinfo(1).min, gamepad.absinfo(1).max)
                robot.left_motor.value = speed_left
                
            # Right Stick Y-Axis (Usually Code 5 or 4)
            elif event.code == 5 or event.code == 4: 
                speed_right = map_stick_to_motor(event.value, gamepad.absinfo(event.code).min, gamepad.absinfo(event.code).max)
                robot.right_motor.value = speed_right

        # Quit Button (Usually 'Select' or 'Mode' or Button 8/9)
        elif event.type == ecodes.EV_KEY:
            if event.value == 1 and event.code in [ecodes.KEY_MODE, 314, 316]: # Common "Select" codes
                print("Quitting...")
                break

except OSError:
    print("Controller Disconnected.")
except KeyboardInterrupt:
    print("\nStopping...")

finally:
    robot.stop()
    status_led.off()
