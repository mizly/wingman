import serial
import time

# Adjust the port to match your Arduino
ser = serial.Serial('COM3', 9600, timeout=1)  # Use '/dev/ttyUSB0' for Linux/macOS
time.sleep(2)  # Allow time for Arduino to reset

faces = {
    "neutral": "/face_0~1.bmp",
    "angry": "/face_0~2.bmp",
    "cry": "/face_0~3.bmp",
    "x_x": "/face_0~4.bmp",
    "owo": "/fa0724~1.bmp",
    "frown": "/faccf4~1.bmp",
    "sob": "/faa19c~1.bmp",
    "smile": "/fa38f5~1.bmp",
    "wink": "/fadb58~1.bmp",
    "surprised": "/fa9d8d~1.bmp",
    "happy": "/fa560f~1.bmp",
    "heart": "/fa13e6~1.bmp"
}

def send_image(filename):
    ser.write((filename + "\n").encode())  # Send image filename to Arduino
    time.sleep(0.5)  # Give time for Arduino to process

# Example usage:
def update_face(name):
    send_image(faces[name])

while True:
    img = input("Enter face name to display (or 'exit' to quit): ")
    if img.lower() == 'exit':
        break
    update_face(img)

ser.close()