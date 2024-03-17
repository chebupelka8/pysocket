import socket
import json

import threading

from typing import Tuple, Never
from notify import ServerNotifier

HOST, PORT = 'localhost', 5050


class Server:
    def __init__(self, addr: Tuple[str, int]) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(addr)
        self.server.listen()

        ServerNotifier.start_server()  # notify about the start

        # variables setup: --
        self.__is_working = True
        self.__clients = []

    def listen(self) -> Never:
        ServerNotifier.listening_server()

        while self.__is_working:
            client, address = self.server.accept()
            self.__clients.append(client)

            ServerNotifier.notify_connected(address)  # notify about the connect client

            threading.Thread(target=self.handle_client, args=(client, address)).start()  # start handle client

    def __disconnect_client(self, address: Tuple[str, int], client) -> None:
        ServerNotifier.notify_disconnected(address)
        self.__clients.remove(client)

    def handle_client(self, client: socket.socket, address: Tuple[str, int]) -> None:
        while True:
            try:
                data = json.loads(client.recv(1024).decode('utf-8'))

                if not data:  # if client disconnect
                    self.__disconnect_client(address, client)
                    break

            except (ConnectionResetError, OSError):
                self.__disconnect_client(address, client)
                break


if __name__ == '__main__':
    server = Server((HOST, PORT))
    server.listen()