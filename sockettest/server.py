from socket import *
from time import ctime


HOST = '10.12.128.69'
PORT = 21568
BUFSIZ = 1024
ADDR = (HOST, PORT)


if __name__ == '__main__':
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(5)

    while True:
        print('waiting for connection...')
        tcpCliSock, addr = tcpSerSock.accept()
        print('...connnecting from:', addr)

        while True:
            try:
                data = tcpCliSock.recv(BUFSIZ)
                print(data)
            except ConnectionResetError as e:
                tcpCliSock.close()
                print(e)
                print(addr,"已经主动关闭了连接")
                tcpCliSock, addr = tcpSerSock.accept()
                print('...connnecting from:', addr)
                continue
            if not data:
                print("当前用户已退出了会话")
                tcpCliSock.close()
                tcpCliSock, addr = tcpSerSock.accept()
                print("新用户建立了一个连接，客户端信息：",addr)
                continue

                break
            tcpCliSock.send(('%s' % (data)).encode())
        tcpCliSock.close()
