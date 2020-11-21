import RPi.GPIO as GPIO
import time

power_channel = 24


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
