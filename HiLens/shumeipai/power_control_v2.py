import RPi.GPIO as GPIO
import time

from HiLens.shumeipai.settings import power_channel

print("PC ON: PC-ON")
print("Exit: Q and q")

GPIO.setmode(GPIO.BCM)
GPIO.setup(power_channel, GPIO.OUT, initial=GPIO.LOW)
while True:
    user_choice = input("Choice:")
    if user_choice == "1":
        print("on")
        GPIO.output(power_channel, GPIO.HIGH)
        time.sleep(3.0)
    elif user_choice == "2":
        print("off")
        GPIO.output(power_channel, GPIO.LOW)
        time.sleep(3.0)
    elif user_choice == "q" or user_choice == "Q":
        GPIO.cleanup()
GPIO.cleanup()
