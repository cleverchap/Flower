import RPi.GPIO as GPIO
import time

channel = 24  # 管脚40，参阅树莓派引脚图，物理引脚40对应的BCM编码为21
print("PC ON: PC-ON")
print("Exit: Q and q")

while True:
    user_choice = input("Choice:")
    if user_choice == "1":
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.OUT)
        GPIO.output(channel, GPIO.LOW)
        print("3")
        time.sleep(1.0)
        print("2")
        time.sleep(1.0)
        print("1")
        time.sleep(1.0)
        GPIO.cleanup()
    elif user_choice == "q" or user_choice == "Q":
        GPIO.cleanup()