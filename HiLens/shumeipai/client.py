from socket import *
from time import *

from HiLens.shumeipai.bme280 import get_temp_pressure_humidity_from_sensor
from HiLens.shumeipai.sensor import get_result_from_sensor
from HiLens.shumeipai.settings import sensor_channel

HOST = '192.168.0.102'  # HOME Hilens
# HOST = '192.168.43.236'  # Mate 20 Pro
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)
while True:
    sleep(3)
    # data1 = input('>')
    t1, t2, temperature, pressure, humidity = get_temp_pressure_humidity_from_sensor()
    dry_or_humid = get_result_from_sensor(sensor_channel)
    # data1 = ("Temperature : %f C, Pressure : %f hPa, Humidity : %f RH" % (temperature, pressure, humidity))
    # data = str(data)
    data1 = ("%f,%f,%f,%s" % (temperature, pressure, humidity, dry_or_humid))
    if not data1:
        break
    tcpCliSock.send(data1.encode())
    data1 = tcpCliSock.recv(BUFSIZ)
    if not data1:
        break
    print(data1.decode('utf-8'))
tcpCliSock.close()
