
import RPi.GPIO as GPIO
import time

DATA = 22
CLOCK = 17
LATCH = 27


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DATA, GPIO.OUT)
    GPIO.setup(CLOCK, GPIO.OUT)
    GPIO.setup(LATCH, GPIO.OUT)


def write_one_bit(bit):
    GPIO.output(DATA, bit)
    GPIO.output(CLOCK, 1)
    GPIO.output(CLOCK, 0)


def set_storage():
    GPIO.output(LATCH, 1)
    GPIO.output(LATCH, 0)


def write_one_byte_simple(bits):
    for bit in bits:
        write_one_bit(bit)


try:
    setup()

    while True:

        # Pattern 1
        write_one_byte_simple([1,1,1,1,0,0,0,0])
        set_storage()
        time.sleep(1)

        # Pattern 2
        write_one_byte_simple([0,0,0,0,1,1,1,1])
        set_storage()
        time.sleep(1)

        # Pattern 3
        write_one_byte_simple([1,0,1,0,1,0,1,0])
        set_storage()
        time.sleep(1)

        # Pattern 4
        write_one_byte_simple([0,1,0,1,0,1,0,1])
        set_storage()
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()