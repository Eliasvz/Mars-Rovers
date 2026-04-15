import time
import board
import digitalio
from elapsed_time import ElapsedTime

led = digitalio.DigitalInOut(board.D0)
led.direction = digitalio.Direction.OUTPUT

heartbeat_timer = ElapsedTime()
day_timer =  ElapsedTime()
led_state = "ON"
day_state = "Day"

def update_led_state():
    global led_state

    if led_state == "ON":
        led.value = True
        if heartbeat_timer.seconds() > 0.5: # The "Transition" event
            led_state = "OFF"
            heartbeat_timer.reset()

    elif led_state == "OFF":
        led.value = False
        if heartbeat_timer.seconds() > 0.5: # The "Transition" event
            led_state = "ON"
            heartbeat_timer.reset()

def upd_day_state():
    global day_state

    if day_state == "Day":
        if day_timer.seconds() > 5:
            day_state = "Night"
            day_timer.reset()
            print("transitioning to Night")

    elif day_state == "Night":
        if day_timer.seconds() > 5: # The "Transition" event
            day_state= "Day"
            day_timer.reset()
            print("transitioning to Day")




heartbeat_timer.reset()
day_timer.reset()
while True:
    update_led_state()
    upd_day_state()
    time.sleep(0.02)
# Write your code here :-)
