import RPi.GPIO as GPIO
import time

from HiLens.shumeipai.settings import power_channel

GPIO.setmode(GPIO.BCM)
GPIO.setup(power_channel, GPIO.OUT)


def blink(times):
    GPIO.output(power_channel, GPIO.LOW)
    while times > 0:
        time.sleep(1)
        print(times)
        times -= 1
    GPIO.output(power_channel, GPIO.HIGH)
    GPIO.cleanup()


if __name__ == '__main__':
    blink(5)
