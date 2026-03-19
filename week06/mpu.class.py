
import smbus2
import time

# I2C bus
i2c = smbus2.SMBus(1)

# MPU-6050 address
MPU_ADDR = 0x68

# Registers
CONF_PWR = 0x6B
CONF_ACC = 0x1C
CONF_GYR = 0x1B

REG_TEMP = 0x41
REG_ACC = 0x3B
REG_GYR = 0x43


def init_MPU():
    # Wake up MPU-6050
    i2c.write_byte_data(MPU_ADDR, CONF_PWR, 1)
    time.sleep(0.001)

    # Set accelerometer range
    i2c.write_byte_data(MPU_ADDR, CONF_ACC, 0)
    time.sleep(0.001)

    # Set gyroscope range
    i2c.write_byte_data(MPU_ADDR, CONF_GYR, 0)
    time.sleep(0.001)


def to_signed_16bit(high_byte, low_byte):
    value = (high_byte << 8) | low_byte

    if value & 0x8000:
        value = value - 2**16

    return value


def get_temp():
    temp_bytes = i2c.read_i2c_block_data(MPU_ADDR, REG_TEMP, 2)

    raw_temp = to_signed_16bit(temp_bytes[0], temp_bytes[1])

    # Formula from MPU-6050 datasheet
    temp_c = (raw_temp / 340.0) + 36.53

    return temp_c


def get_accel():
    acc_bytes = i2c.read_i2c_block_data(MPU_ADDR, REG_ACC, 6)

    acc_x = to_signed_16bit(acc_bytes[0], acc_bytes[1])
    acc_y = to_signed_16bit(acc_bytes[2], acc_bytes[3])
    acc_z = to_signed_16bit(acc_bytes[4], acc_bytes[5])

    # Divide by 16384 for ±2g range
    acc_x = acc_x / 16384.0
    acc_y = acc_y / 16384.0
    acc_z = acc_z / 16384.0

    return [acc_x, acc_y, acc_z]


def get_gyro():
    gyr_bytes = i2c.read_i2c_block_data(MPU_ADDR, REG_GYR, 6)

    gyr_x = to_signed_16bit(gyr_bytes[0], gyr_bytes[1])
    gyr_y = to_signed_16bit(gyr_bytes[2], gyr_bytes[3])
    gyr_z = to_signed_16bit(gyr_bytes[4], gyr_bytes[5])

    # Divide by 131 for ±250 deg/s range
    gyr_x = gyr_x / 131.0
    gyr_y = gyr_y / 131.0
    gyr_z = gyr_z / 131.0

    return [gyr_x, gyr_y, gyr_z]


# Start sensor
init_MPU()

# Loop forever
while True:
    temp = get_temp()
    accel = get_accel()
    gyro = get_gyro()

    print(f"Temp:  {temp:.2f}°C")
    print(f"Accel: {accel}")
    print(f"Gyro:  {gyro}")
    print("---------------------------")

    time.sleep(1)