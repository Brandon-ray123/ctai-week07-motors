
import smbus2
import RPi.GPIO as GPIO
import time

# -------------------------
# 1. DEFINE CONSTANTS
# -------------------------

# I2C
MPU_ADDR = 0x68

# MPU6050 registers
CONF_PWR = 0x6B
CONF_ACC = 0x1C
REG_ACC = 0x3B

# Buzzer pin
BUZZER_PIN = 12

# Sensitivity
SENSITIVITY = 0.20
# smaller = more sensitive
# bigger = less sensitive


# -------------------------
# 2. CREATE OBJECTS
# -------------------------

i2c = smbus2.SMBus(1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)


# -------------------------
# 3. INIT MPU
# -------------------------

def init_MPU():
    # wake up sensor
    i2c.write_byte_data(MPU_ADDR, CONF_PWR, 1)
    time.sleep(0.001)

    # accelerometer range = ±2g
    i2c.write_byte_data(MPU_ADDR, CONF_ACC, 0)
    time.sleep(0.001)


# -------------------------
# 4. CONVERT 2 BYTES
# -------------------------

def to_signed_16bit(high_byte, low_byte):
    value = (high_byte << 8) | low_byte

    if value & 0x8000:
        value = value - 2**16

    return value


# -------------------------
# 5. GET ACCELEROMETER
# -------------------------

def get_accel():
    acc_bytes = i2c.read_i2c_block_data(MPU_ADDR, REG_ACC, 6)

    acc_x = to_signed_16bit(acc_bytes[0], acc_bytes[1])
    acc_y = to_signed_16bit(acc_bytes[2], acc_bytes[3])
    acc_z = to_signed_16bit(acc_bytes[4], acc_bytes[5])

    # convert to g
    acc_x = acc_x / 16384.0
    acc_y = acc_y / 16384.0
    acc_z = acc_z / 16384.0

    return [acc_x, acc_y, acc_z]


# -------------------------
# 6. CHECK MOVEMENT
# -------------------------

def detect_movement(old_acc, new_acc):
    dx = abs(new_acc[0] - old_acc[0])
    dy = abs(new_acc[1] - old_acc[1])
    dz = abs(new_acc[2] - old_acc[2])

    if dx > SENSITIVITY or dy > SENSITIVITY or dz > SENSITIVITY:
        return True
    else:
        return False


# -------------------------
# 7. BUZZER FUNCTIONS
# -------------------------

def buzzer_on():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)


def buzzer_off():
    GPIO.output(BUZZER_PIN, GPIO.LOW)


# -------------------------
# 8. MAIN PROGRAM
# -------------------------

init_MPU()

old_acc = get_accel()

try:
    while True:
        new_acc = get_accel()

        print("Old:", old_acc)
        print("New:", new_acc)

        if detect_movement(old_acc, new_acc):
            print("Movement detected!")
            buzzer_on()
            time.sleep(0.3)
            buzzer_off()
        else:
            print("No important movement")

        print("----------------------")

        old_acc = new_acc
        time.sleep(0.2)

except KeyboardInterrupt:
    print("Program stopped")

finally:
    buzzer_off()
    GPIO.cleanup()