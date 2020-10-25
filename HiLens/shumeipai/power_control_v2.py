import RPi.GPIO as GPIO
import time

channel = 24  # 管脚40，参阅树莓派引脚图，物理引脚40对应的BCM编码为21
print("PC ON: PC-ON")
print("Exit: Q and q")

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT, initial=GPIO.LOW)
while True:
    user_choice = input("Choice:")
    if user_choice == "1":
        print("on")
        GPIO.output(channel, GPIO.HIGH)
        time.sleep(3.0)
    elif user_choice == "2":
        print("off")
        GPIO.output(channel, GPIO.LOW)
        time.sleep(3.0)
    elif user_choice == "q" or user_choice == "Q":
        GPIO.cleanup()
GPIO.cleanup()