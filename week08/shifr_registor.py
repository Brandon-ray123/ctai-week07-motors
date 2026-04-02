
import RPi.GPIO as GPIO
import time


class ShiftRegister:
    """Controls a shift register connected to the Raspberry Pi."""

    def __init__(self, data_pin=22, clock_pin=17, latch_pin=27):
        self.data_pin = data_pin
        self.clock_pin = clock_pin
        self.latch_pin = latch_pin

        self._setup()

    def _setup(self):
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.data_pin, GPIO.OUT)
        GPIO.setup(self.clock_pin, GPIO.OUT)
        GPIO.setup(self.latch_pin, GPIO.OUT)

        GPIO.output(self.data_pin, GPIO.LOW)
        GPIO.output(self.clock_pin, GPIO.LOW)
        GPIO.output(self.latch_pin, GPIO.LOW)

    def storage_pulse(self):
        GPIO.output(self.latch_pin, GPIO.HIGH)
        GPIO.output(self.latch_pin, GPIO.LOW)

    def shift_byte_out(self, value):
        for i in range(8):
            bit = (value >> (7 - i)) & 1

            GPIO.output(self.data_pin, bit)

            GPIO.output(self.clock_pin, GPIO.HIGH)
            GPIO.output(self.clock_pin, GPIO.LOW)

    def shift_out_16bit(self, value):
        high_byte = (value >> 8) & 0xFF
        low_byte = value & 0xFF

        self.shift_byte_out(high_byte)
        self.shift_byte_out(low_byte)

        self.storage_pulse()


class LedBarGraph:
    """Represents a 10-LED bar graph controlled by shift registers."""

    def __init__(self, shift_register):
        self.shift_register = shift_register

    def set_pattern(self, value, fill=False):
        if fill:
            pattern = 0
            for i in range(value):
                pattern |= (1 << i)
        else:
            pattern = value

        self.shift_register.shift_out_16bit(pattern)


if __name__ == '__main__':
    try:
        shift_reg = ShiftRegister()  # DATA_PIN, CLOCK_PIN, LATCH_PIN are set by default, but can still be passed
        led_bar = LedBarGraph(shift_reg)  # create a led bar instance by passing in a shift register instance

        led_bar.set_pattern(0b1100001111)

        while True:
            for i in range(10):
                led_bar.set_pattern(i + 1, True)
                time.sleep(0.25)

    except KeyboardInterrupt:
        GPIO.cleanup()