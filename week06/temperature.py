
import smbus2
import time

def read_temperature(i2c_address=0x68):
    """
    Read temperature from MPU6050 sensor with optimal settings:
    - Wakes up from sleep mode (SLEEP=0)
    - Sets clock source to PLL with X-axis gyro reference (CLKSEL=001)
    - Ensures temperature sensor is enabled (TEMP_DIS=0)
    Returns temperature in degrees Celsius
    """
    bus = smbus2.SMBus(1)
    
    # Configure PWR_MGMT_1 register (0x6B):
    # - Clear SLEEP bit (bit6 = 0) to wake up device
    # - Clear TEMP_DIS bit (bit3 = 0) to enable temp sensor
    # - Set CLKSEL to PLL with X-axis gyro reference (bits2:0 = 001)
    # - All other bits remain 0 (DEVICE_RESET=0, CYCLE=0)
    bus.write_byte_data(i2c_address, 0x68, 0x01)  # Binary 00000001
    
    # Read both temperature registers (0x41 and 0x42) in one operation
    temp_data = bus.read_i2c_block_data(i2c_address, 0x41, 2)
    
    # Combine bytes (MSB first, big-endian)
    temp_raw = (temp_data[0] << 8) | temp_data[1]
    
    # Convert from two's complement (16-bit signed value)
    if temp_raw > 32767:  # Check sign bit (bit 15)
        temp_raw -= 65536  # 2^16 adjustment for negative numbers
    
    # Apply datasheet conversion formula
    temperature = (temp_raw / 340.0) + 36.53
    return temperature

# Example usage
if __name__ == "__main__":
    try:
        while True:
            temp = read_temperature()
            print(f"Temperature: {temp:.2f} °C")
            time.sleep(1)  # Read every second
    except KeyboardInterrupt:
        print("Temperature monitoring stopped")
