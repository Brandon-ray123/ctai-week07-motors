
import smbus2
import time


def read_temperature(i2c_address=0x68):
    with smbus2.SMBus(1) as bus:
        # Wake up MPU6050
        bus.write_byte_data(i2c_address, 0x6B, 0x01)

        # Read temperature registers
        temp_data = bus.read_i2c_block_data(i2c_address, 0x41, 2)

        # Combine bytes
        temp_raw = (temp_data[0] << 8) | temp_data[1]

        # Convert signed 16-bit
        if temp_raw > 32767:
            temp_raw -= 65536

        # Convert to Celsius
        temperature = (temp_raw / 340.0) + 36.53
        return temperature


if __name__ == "__main__":
    try:
        while True:
            temp = read_temperature()
            print("Temperature:", round(temp, 2), "°C")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Temperature monitoring stopped")
    except OSError:
        print("I2C error: sensor not found or not responding")