import RPi.GPIO as GPIO
import time

from HiLens.shumeipai.settings import power_channel


def blink(times):
    # 设置channel=8的接口的编号方式是输出，默认是低电平
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(power_channel, GPIO.OUT, initial=GPIO.LOW)
    # GPIO.output(power_channel, GPIO.LOW)
    while times > 0:
        GPIO.output(power_channel, GPIO.HIGH)
        time.sleep(1)
        print(times)
        times -= 1
    GPIO.output(power_channel, GPIO.LOW)
    GPIO.cleanup()
    time.sleep(2)


if __name__ == '__main__':
    blink(5)
