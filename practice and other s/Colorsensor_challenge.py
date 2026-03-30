import board
import busio
import time
import adafruit_apds9960.apds9960

# Set up I2C connection
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)

# Enable color sensing
sensor.enable_color = True

while True:
    r, g, b, c = sensor.color_data
    if b > r + g:
        print("blue")
        time.sleep(1)
    elif r > g + b:
        print("red")
        time.sleep(1)
    elif g > b + r:
        print("green"x)
        time.sleep(1)
    else:
        print("unknown")
        time.sleep(1)
# Write your code here :-)
