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


def blink2(times):
    print("start blink:" + str(times))
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(power_channel, GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(power_channel, GPIO.HIGH)
    time.sleep(times)
    GPIO.output(power_channel, GPIO.LOW)
    time.sleep(1)
    GPIO.cleanup()
    print("end blink:" + str(times))


def blink(times):
    print("start blink:" + str(times))
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(power_channel, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.output(power_channel, GPIO.LOW)
    time.sleep(times)
    GPIO.output(power_channel, GPIO.HIGH)
    time.sleep(1)
    GPIO.cleanup()
    print("end blink:" + str(times))


if __name__ == '__main__':
    blink()
