import RPi.GPIO as GPIO
import time

from shumeipai.settings import sensor_channel

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_channel, GPIO.IN)


def print_result_from_sensor(_channel):
    if GPIO.input(_channel) == GPIO.LOW:
        print("土壤检测结果：潮湿")
    else:
        print("土壤检测结果：干燥")


def get_result_from_sensor(_channel):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(_channel, GPIO.IN)
    if GPIO.input(_channel) == GPIO.LOW:
        return "Humid"
    else:
        return "Dry"


if __name__ == '__main__':
    while True:
        print_result_from_sensor(sensor_channel)
        time.sleep(1)
