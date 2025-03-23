import pygame
import serial
import time
import math

# Initialize Pygame and joystick module
pygame.init()
pygame.joystick.init()

# Open the serial connection
ser = serial.Serial('/dev/ttyACM1', baudrate=9600, timeout=1)

# Ensure a joystick is connected
if pygame.joystick.get_count() == 0:
    print("No controller detected. Please connect an Xbox controller.")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print("Xbox controller detected. Sending VFL, VFR, BFL, BFR data...")

def calculate_and_send(angle, speed):
    """Calculate VFL, VFR, BFL, BFR and send them via serial"""
    
    # Convert angle to radians for trigonometric functions
    theta_rad = math.radians(angle)
    
    # Calculate motor speeds
    VFL = speed * (math.cos(theta_rad) + math.sin(theta_rad))
    VFR = speed * (-math.cos(theta_rad) + math.sin(theta_rad))
    #BFL = speed * (-math.cos(theta_rad) + math.sin(theta_rad))
    #BFR = speed * (math.cos(theta_rad) + math.sin(theta_rad))

    # Format the output as "VFL,VFR,BFL,BFR"
    message = f"{int(VFL)},{int(VFR)},\n"
    ser.write(message.encode())  # Send to serial

    # Read response from serial device
    response = ser.readline().decode().strip()

    # Print sent data and received response
    print(f"Sent: {message.strip()} | Received: {response}")

try:
    while True:
        pygame.event.pump()  # Process events

        # Read joystick values
        x = joystick.get_axis(0)  # Left joystick X (-1 to 1)
        y = -joystick.get_axis(1)  # Invert Y because Pygame's Y is negative up

        # Calculate angle (-180 to 180 degrees)
        angle = math.degrees(math.atan2(y, x))

        # Calculate speed (0-255)
        magnitude = math.sqrt(x**2 + y**2)  # Joystick distance from center (0-1)
        speed = int(magnitude * 255)  # Scale to 0-255

        # Call the function to compute motor speeds and send them
        calculate_and_send(angle, speed)

        time.sleep(0.1)  # Adjust loop speed

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    ser.close()
    pygame.quit()
