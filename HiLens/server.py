from socket import gethostbyname, gethostname, socket, AF_INET, SOCK_STREAM
from time import ctime

from HiLens.utils import set_temperature_and_humidity

HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)


def start_listen():
    myname = gethostname()
    myaddr = gethostbyname(myname)
    print(myname + ", " + myaddr)
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(5)
    try:
        while True:
            print('waiting for connection...')
            tcpCliSock, addr = tcpSerSock.accept()
            print('...connnecting from:', addr)

            while True:
                data = tcpCliSock.recv(BUFSIZ)
                if not data:
                    break
                print(data)
                if len(data) < 3:
                    break
                str_data = str(data)[2:-1]
                print(str_data)
                print(str((str(str_data)).split(',')))
                split_data = str_data.split(',')
                if len(data) < 4:
                    break
                set_temperature_and_humidity(split_data[0], split_data[1], split_data[2], split_data[3])

                # tcpCliSock.send('[%s] %s' %(bytes(ctime(),'utf-8'),data))
                tcpCliSock.send(('[%s] %s' % (ctime(), data)).encode())
            tcpCliSock.close()
    finally:
        tcpSerSock.close()


if __name__ == '__main__':
    start_listen()
    start_listen()
