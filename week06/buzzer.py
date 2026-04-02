import smbus
import time
import RPi.GPIO as GPIO

# -----------------------
# MPU6050 CLASS
# -----------------------
class MPU6050:
    def __init__(self, address=0x68):
        self.addr = address
        self.bus = smbus.SMBus(1)

    def setup(self):
        # Wake up sensor
        self.bus.write_byte_data(self.addr, 0x6B, 0x01)

        # Accelerometer ±2g
        self.bus.write_byte_data(self.addr, 0x1C, 0x00)

    @staticmethod
    def combine(msb, lsb):
        value = (msb << 8) | lsb
        if value & 0x8000:
            value -= 2**16
        return value

    def read_accel(self):
        data = self.bus.read_i2c_block_data(self.addr, 0x3B, 6)

        x = self.combine(data[0], data[1]) / 16384.0
        y = self.combine(data[2], data[3]) / 16384.0
        z = self.combine(data[4], data[5]) / 16384.0

        return x, y, z


# -----------------------
# BUZZER SETUP
# -----------------------
BUZZER = 12          # GPIO12 (Pin 32)
THRESHOLD = 0.15     

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)

# -----------------------
# MAIN PROGRAM
# -----------------------
mpu = MPU6050()
mpu.setup()

#  CALIBRATION STEP
print("Calibrating... keep sensor still!")
time.sleep(2)

ax0, ay0, az0 = mpu.read_accel()
print(f"Baseline: X={ax0:.2f}, Y={ay0:.2f}, Z={az0:.2f}")

print("System ready. Move the sensor!")

try:
    while True:
        ax, ay, az = mpu.read_accel()

        # Debug output
        print(f"X={ax:.2f}  Y={ay:.2f}  Z={az:.2f}")

        # Movement detection using baseline
        if (abs(ax - ax0) > THRESHOLD or
            abs(ay - ay0) > THRESHOLD or
            abs(az - az0) > THRESHOLD):

            print(" MOVEMENT DETECTED!")
            GPIO.output(BUZZER, GPIO.HIGH)
        else:
            GPIO.output(BUZZER, GPIO.LOW)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopping...")
    GPIO.cleanup()