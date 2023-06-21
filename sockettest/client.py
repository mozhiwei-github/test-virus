from socket import *

HOST = '10.12.128.69'  # or 'localhost'
PORT = 21568
ADDR = (HOST, PORT)
BUFSIZ = 1024

if __name__ == '__main__':
    while True:
        print("find server to connect...")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.settimeout(20)
        try:
            tcpCliSock.connect(ADDR)
        except ConnectionRefusedError as e :
            print("server refused")
            continue
        print("connect success")
        while True:
            try:
                data = input('>>>')
                if not data:
                    break
                tcpCliSock.send(data.encode())
                recvdata = tcpCliSock.recv(BUFSIZ)
                if not recvdata:
                    break
                print(recvdata.decode('utf-8'))
            except ConnectionResetError as e:
                print("server is not existed")
                break

