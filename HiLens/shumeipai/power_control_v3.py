import RPi.GPIO as GPIO
import time

# https://blog.csdn.net/jiaojuan9641/article/details/107510342?utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~all~first_rank_v2~rank_v25-2-107510342.nonecase&utm_term=%E6%A0%91%E8%8E%93%E6%B4%BE%E7%BB%A7%E7%94%B5%E5%99%A8%E6%8E%A7%E5%88%B6%E6%B0%B4%E6%B3%B5&spm=1000.2123.3001.4430
from HiLens.shumeipai.sensor import print_result_from_sensor
from HiLens.shumeipai.settings import power_channel, sensor_channel

if __name__ == '__main__':
    inchannel = sensor_channel
    outchannel = power_channel
    sleepTime = 3
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(inchannel, GPIO.IN)
    GPIO.setup(outchannel, GPIO.OUT)
    GPIO.output(outchannel, False)
    # if GPIO.input(inchannel):
    #     GPIO.output(outchannel, True)
    #     time.sleep(sleepTime)
    #     GPIO.output(outchannel, False)
    # GPIO.cleanup()
    while True:
        user_choice = input("Choice:")
        print_result_from_sensor()
        if user_choice == "1":
            GPIO.output(outchannel, True)
            print("set " + str(outchannel) + " to True")
            time.sleep(sleepTime)
            GPIO.output(outchannel, False)
        elif user_choice == "2":
            print("set " + str(outchannel) + " to False")
            GPIO.output(outchannel, False)
            time.sleep(sleepTime)
        elif user_choice == "3":
            break
    GPIO.cleanup()
