from socket import *
from time import *

from HiLens.shumeipai.bme280 import main0

HOST = '192.168.43.236'  # or 'localhost'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)
while True:
    sleep(1)
    # data1 = input('>')
    t1, t2, temperature, pressure, humidity = main0()
    data1 = ("Temperature : %d C, Pressure : %d hPa, Humidity : %d RH" % (temperature, pressure, humidity))
    # data = str(data)
    if not data1:
        break
    tcpCliSock.send(data1.encode())
    data1 = tcpCliSock.recv(BUFSIZ)
    if not data1:
        break
    print(data1.decode('utf-8'))
tcpCliSock.close()
