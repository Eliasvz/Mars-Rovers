import time
import board
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

UNIT = 0.3
loop_count = 0

while loop_count<3:
    led.value = True
    time.sleep(UNIT)
    led.value = False
    time.sleep(UNIT)
    loop_count += 1
    print(loop_count)

if loop_count == 3:
    time.sleep(UNIT*3)




