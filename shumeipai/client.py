from socket import *
from time import *

from shumeipai.bme280 import get_temp_pressure_humidity_from_sensor
from shumeipai.power_control import blink
from shumeipai.soil_sensor import get_result_from_sensor
from shumeipai.settings import sensor_channel, ADDR, BUFSIZ

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

while True:
    sleep(3)
    t1, t2, temperature, pressure, humidity = get_temp_pressure_humidity_from_sensor()
    dry_or_humid = get_result_from_sensor(sensor_channel)
    # data1 = ("Temperature : %f C, Pressure : %f hPa, Humidity : %f RH" % (temperature, pressure, humidity))
    data1 = ("%.2f,%.2f,%.2f,%s" % (temperature, pressure, humidity, dry_or_humid))
    if not data1:
        break
    tcpCliSock.send(data1.encode())
    data1 = tcpCliSock.recv(BUFSIZ)
    if not data1:
        break
    command = data1.decode('utf-8')
    print(command)
    if command.startswith("Watering"):
        time = command[8:]
        print(time)
        blink(int(float(time)))
tcpCliSock.close()
