import RPi.GPIO as GPIO
import time

from HiLens.shumeipai.settings import power_channel

print("PC ON: PC-ON")
print("Exit: Q and q")

while True:
    user_choice = input("Choice:")
    if user_choice == "1":
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(power_channel, GPIO.OUT)
        GPIO.output(power_channel, GPIO.LOW)
        print("3")
        time.sleep(1.0)
        print("2")
        time.sleep(1.0)
        print("1")
        time.sleep(1.0)
        GPIO.cleanup()
    elif user_choice == "q" or user_choice == "Q":
        GPIO.cleanup()
