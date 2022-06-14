#!/usr/bin/env python3

import threading
import socket
import argparse
import os


class Server(threading.Thread):

    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.host = host
        self.port = port

    def run(self):

        # SO_REUSEADDR为1，允许地址复用

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))

        sock.listen(1)
        print('Listening at', sock.getsockname())

        while True:
            # 接收到新的连接
            sc, sockname = sock.accept()
            print('Accepted a new connection from {} to {}'.format(sc.getpeername(), sc.getsockname()))

            # 创建新线程
            server_socket = ServerSocket(sc, sockname, self)

            # 开始运行新线程
            server_socket.start()

            # 添加该新线程到活跃的连接集合中
            self.connections.append(server_socket)
            print('Ready to receive messages from', sc.getpeername())

    def broadcast(self, message, source):
        # 广播消息如何实现
        for connection in self.connections:

            # 将消息发送给除了source的所有连接
            if connection.sockname != source:
                connection.send(message)

    def remove_connection(self, connection):

        self.connections.remove(connection)


class ServerSocket(threading.Thread):
    # sc为已连接的套接字
    def __init__(self, sc, sockname, server):
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.server = server

    def run(self):
        # 监听Client发出的data
        while True:
            message = self.sc.recv(1024).decode('utf-8')
            if message:
                print('{} says {!r}'.format(self.sockname, message))
                self.server.broadcast(message, self.sockname)
            else:
                # message为‘’，说明Client已经关闭了套接字连接，退出了线程，将该连接从活跃用户集合中移除
                # 客户端关闭套接字，退出连接
                print('{} has closed the connection'.format(self.sockname))
                self.sc.close()
                server.remove_connection(self)
                return

    def send(self, message):
        # 为了避免因为buffer快满了而只发送了一部分data，使用sendall
        self.sc.sendall(message.encode('utf-8'))

# 用户输入q，退出程序
def exit(server):
    while True:
        ipt = input('')
        if ipt == 'q':
            print('Closing all connections...')
            for connection in server.connections:
                connection.sc.close()
            print('Shutting down the server...')
            os._exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=4780,
                        help='TCP port (default 4780)')
    args = parser.parse_args()

    # 创建并运行服务器线程
    server = Server(args.host, args.p)
    server.start()

    exit = threading.Thread(target=exit, args=(server,))
    exit.start()
