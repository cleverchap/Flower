import RPi.GPIO as GPIO
import time

power_channel = 24


def blink():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(power_channel, GPIO.OUT, initial=GPIO.LOW)
    while True:
        GPIO.output(power_channel, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(power_channel, GPIO.LOW)
        time.sleep(5)


def blink(times):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(power_channel, GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(power_channel, GPIO.HIGH)
    time.sleep(times)
    GPIO.output(power_channel, GPIO.LOW)
    time.sleep(1)
    GPIO.cleanup()


if __name__ == '__main__':
    blink()
