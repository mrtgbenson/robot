# CamJam EduKit 3 - Robotics
# Wii controller remote control script (Python 3 Modernized)

from gpiozero import Robot, LED
from evdev import InputDevice, list_devices, ecodes, categorize
import time
import sys

# ===========================================================================
# CONFIGURATION
# ===========================================================================

# Motor Pins (BCM numbering from original script)
# Motor A: Fwd=10, Back=9
# Motor B: Fwd=8, Back=7
robot = Robot(left=(10, 9), right=(8, 7))

# LED Pin
status_led = LED(25)

# ===========================================================================
# HELPER FUNCTIONS
# ===========================================================================

def get_wii_remote():
    """Finds the Wii Remote among connected input devices."""
    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        # Check for standard Wii Remote names
        if "Nintendo" in device.name:
            return device
    return None

# ===========================================================================
# MAIN LOGIC
# ===========================================================================

print("---------------------------------------")
print("Searching for Wii Remote...")
print("Ensure you have paired it via Bluetooth first!")
print("---------------------------------------")

status_led.on()
wii_device = None

# Attempt to find the device
try:
    wii_device = get_wii_remote()
    if wii_device is None:
        print("No Wii Remote found. Please check bluetooth connection.")
        status_led.off()
        sys.exit()
except Exception as e:
    print(f"Error finding device: {e}")
    sys.exit()

print(f"Connected to: {wii_device.name}")
print("Press D-Pad to drive.")
print("Press PLUS (+) to quit.")
status_led.off()

# Define button codes (Standard Linux mappings for Wii Remote)
# These may vary slightly depending on OS version, but these are standard.
BTN_LEFT = ecodes.KEY_LEFT
BTN_RIGHT = ecodes.KEY_RIGHT
BTN_UP = ecodes.KEY_UP
BTN_DOWN = ecodes.KEY_DOWN
BTN_PLUS = ecodes.KEY_NEXT # Often maps to 'Next' or similar
BTN_MINUS = ecodes.KEY_PREVIOUS

try:
    # This loop reads events directly from the Linux kernel
    for event in wii_device.read_loop():
        
        # We only care about key presses (type 1)
        if event.type == ecodes.EV_KEY:
            
            # event.value 1 is pressed, 0 is released, 2 is held
            if event.value == 1: # Button Pressed
                status_led.on()
                if event.code == BTN_UP:
                    print("Forward")
                    robot.forward()
                elif event.code == BTN_DOWN:
                    print("Backward")
                    robot.backward()
                elif event.code == BTN_LEFT:
                    print("Left")
                    robot.left()
                elif event.code == BTN_RIGHT:
                    print("Right")
                    robot.right()
                elif event.code == BTN_PLUS:
                    print("Quitting...")
                    robot.stop()
                    status_led.off()
                    sys.exit()

            elif event.value == 0: # Button Released
                status_led.off()
                # Stop motors when any D-Pad button is released
                if event.code in [BTN_UP, BTN_DOWN, BTN_LEFT, BTN_RIGHT]:
                    robot.stop()

except KeyboardInterrupt:
    print("\nStopping...")
    robot.stop()
    status_led.off()
except OSError:
    print("\nWii Remote disconnected.")
    robot.stop()
