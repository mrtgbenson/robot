from gpiozero import Robot
from time import sleep

# CamJam EduKit 3 Pin Configuration
# Left Motor:  10 (Forward), 9 (Backward)
# Right Motor: 8 (Forward), 7 (Backward)
robot = Robot(left=(10, 9), right=(8, 7))

print("-----------------------------------------")
print("DIAGNOSTIC TEST STARTING")
print("-----------------------------------------")

# TEST 1: FORWARD
print("1. Moving FORWARD for 2 seconds...")
robot.forward(1.0) # Full speed
sleep(2)
robot.stop()
sleep(0.5)

# TEST 2: BACKWARD
print("2. Moving BACKWARD for 2 seconds...")
robot.backward(1.0) # Full speed
sleep(2)
robot.stop()
sleep(0.5)

# TEST 3: SPIN LEFT
print("3. Spinning LEFT (Left Backward, Right Forward)...")
robot.left(1.0)
sleep(2)
robot.stop()

print("-----------------------------------------")
print("TEST COMPLETE")
