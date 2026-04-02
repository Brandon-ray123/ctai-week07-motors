#Ctrl + C
#python3

#import RPi.GPIO as GPIO
#GPIO.cleanup()
#exit()









import RPi.GPIO as GPIO
import time

# GPIO pins
DATA_PIN = 22    # DS
CLOCK_PIN = 17   # SHCP
LATCH_PIN = 27   # STCP


def setup():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(DATA_PIN, GPIO.OUT)
    GPIO.setup(CLOCK_PIN, GPIO.OUT)
    GPIO.setup(LATCH_PIN, GPIO.OUT)

    GPIO.output(DATA_PIN, GPIO.LOW)
    GPIO.output(CLOCK_PIN, GPIO.LOW)
    GPIO.output(LATCH_PIN, GPIO.LOW)


def write_one_bit(bit):
    GPIO.output(CLOCK_PIN, GPIO.LOW)
    GPIO.output(DATA_PIN, GPIO.HIGH if bit else GPIO.LOW)
    time.sleep(0.01)

    GPIO.output(CLOCK_PIN, GPIO.HIGH)
    time.sleep(0.01)

    GPIO.output(CLOCK_PIN, GPIO.LOW)
    time.sleep(0.01)


def copy_to_storage_register():
    GPIO.output(LATCH_PIN, GPIO.LOW)
    time.sleep(0.01)

    GPIO.output(LATCH_PIN, GPIO.HIGH)
    time.sleep(0.01)

    GPIO.output(LATCH_PIN, GPIO.LOW)
    time.sleep(0.01)


def reset_storage_register():
    for i in range(16):
        write_one_bit(False)
    copy_to_storage_register()


try:
    setup()

    reset_storage_register()

    for i in range(4):#you can change the number here it was initially 16
        write_one_bit(True)

    copy_to_storage_register()

    print("LED bar should light now")
    time.sleep(10)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()