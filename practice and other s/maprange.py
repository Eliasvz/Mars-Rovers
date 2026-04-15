import time
import board
import neopixel
from analogio import AnalogIn
from adafruit_simplemath import map_range

# Setup hardware
pot = AnalogIn(board.A0)
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

while True:
    # Map the 0-65535 pot value to a 0.0-1.0 brightness float
    red_val = map_range(pot.value, 0, 65535, 0, 255)
    blue_val = map_range(pot.value, 0, 65535, 255, 0)

    # Apply the brightness and turn the pixel Blue
    pixel.brightness = red_val
    pixel.fill((int(blue_val), 0, (red_val))) # B, G, R values for colour

    print("Current Brightness:", red_val)
    time.sleep(0.05)
# Write your code here :-)
