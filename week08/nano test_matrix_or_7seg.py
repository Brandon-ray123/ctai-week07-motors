
import RPi.GPIO as GPIO
import time

DATA = 22
CLOCK = 17
LATCH = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA, GPIO.OUT)
GPIO.setup(CLOCK, GPIO.OUT)
GPIO.setup(LATCH, GPIO.OUT)

def pulse(pin):
    GPIO.output(pin, 1)
    time.sleep(0.001)
    GPIO.output(pin, 0)

try:
    while True:
        # send 16 ones
        for i in range(16):
            GPIO.output(DATA, 1)
            pulse(CLOCK)

        pulse(LATCH)
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()