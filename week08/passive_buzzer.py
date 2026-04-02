
import RPi.GPIO as GPIO
import time


class PassiveBuzzer:
    """Controls a passive buzzer connected to the Raspberry Pi."""

    def __init__(self, buzzer_pin=12, frequency=440):
        self.buzzer_pin = buzzer_pin
        self.frequency = frequency

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.buzzer_pin, self.frequency)
        self.pwm.start(0)

    def play_tone(self, frequency, duty_cycle=50):
        self.pwm.ChangeFrequency(frequency)
        self.pwm.ChangeDutyCycle(duty_cycle)

    def stop(self):
        self.pwm.ChangeDutyCycle(0)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()


if __name__ == '__main__':
    try:
        buzzer = PassiveBuzzer()

        while True:
            buzzer.play_tone(262)   # C
            time.sleep(0.5)

            buzzer.play_tone(330)   # E
            time.sleep(0.5)

            buzzer.play_tone(392)   # G
            time.sleep(0.5)

            buzzer.stop()
            time.sleep(0.5)

    except KeyboardInterrupt:
        buzzer.cleanup()