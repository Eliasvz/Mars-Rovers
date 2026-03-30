import board
import displayio
import terminalio
import time
from i2cdisplaybus import I2CDisplayBus
import adafruit_displayio_ssd1306

#releases current displays if any were initialized before setup
displayio.release_displays()

# Use for I2C
i2c = board.I2C()
display_bus = I2CDisplayBus(i2c, device_address=0x3d) # or 0x3d
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)


for i in range(5):
    print("index:", i)
    time.sleep(1)

