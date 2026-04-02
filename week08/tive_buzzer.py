
import RPi.GPIO as GPIO
import time


class ActiveBuzzer:
    """Controls an active buzzer connected to the Raspberry Pi."""

    def __init__(self, buzzer_pin=12, frequency=2000):
        self.buzzer_pin = buzzer_pin
        self.frequency = frequency

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.buzzer_pin, self.frequency)
        self.pwm.start(0)

    def set_volume(self, duty_cycle):
        self.pwm.ChangeDutyCycle(duty_cycle)

    def on(self, duty_cycle=50):
        self.pwm.ChangeDutyCycle(duty_cycle)

    def off(self):
        self.pwm.ChangeDutyCycle(0)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()


if __name__ == '__main__':
    try:
        buzzer = ActiveBuzzer()

        while True:
            buzzer.on(50)
            time.sleep(1)

            buzzer.off()
            time.sleep(1)

    except KeyboardInterrupt:
        buzzer.cleanup()