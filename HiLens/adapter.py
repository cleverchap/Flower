from gpiozero import LED
from time import sleep
from sense_hat import SenseHat
import RPi.GPIO as GPIO

led = LED(25)
sense = SenseHat()
sense.show_message("Hello world!")

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)