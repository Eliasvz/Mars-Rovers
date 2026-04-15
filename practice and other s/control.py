import time
from elapsed_time import ElapsedTime

feeder_timer = ElapsedTime()

while True:
    ch5 = rc.read_channel(5)

    # If the switch is flipped, reset the timer to 0
    if ch5 == 1:
        feeder_timer.reset()
        print("Timer reset!")

    # Perform an action only if the timer is under 2 seconds
    if feeder_timer.seconds() < 2:
        print("Feeder active...")
    else:
        print("Feeder idle.")

    time.sleep(0.02)
