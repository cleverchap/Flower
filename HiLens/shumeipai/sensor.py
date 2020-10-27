import RPi.GPIO as GPIO
import time

<<<<<<< Updated upstream
from HiLens.shumeipai.settings import sensor_channel

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_channel, GPIO.IN)
=======
channel = 18  # 管脚40，参阅树莓派引脚图，物理引脚40对应的BCM编码为21

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

>>>>>>> Stashed changes


def print_result_from_sensor(_channel):
    if GPIO.input(_channel) == GPIO.LOW:
        print("土壤检测结果：潮湿")
    else:
        print("土壤检测结果：干燥")


if __name__ == '__main__':
    while True:
        print_result_from_sensor(sensor_channel)
        time.sleep(1)
