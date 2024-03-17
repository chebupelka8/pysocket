import socket
import json

import threading

from typing import Tuple, Never

HOST, PORT = 'localhost', 5050


class Server:
    def __init__(self, addr: Tuple[str, int]) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(addr)
        self.server.listen()

        # variables setup: --
        self.__is_working = True
        self.__clients = []

    def listen(self) -> Never:
        while self.__is_working:
            client, address = self.server.accept()
            self.__clients.append(client)

            print(f'Client {address} connected.')

            threading.Thread(target=self.handle_client, args=(client, address)).start()  # start handle client

    def handle_client(self, client: socket.socket, address: Tuple[str, int]) -> None:
        while True:
            try:
                data = json.loads(client.recv(1024).decode('utf-8'))

                if not data:  # if client disconnect
                    print(f'Client {address} disconnected.')
                    self.__clients.remove(client)
                    break

            except (ConnectionResetError, OSError):
                print(f'Client {address} disconnected.')
                self.__clients.remove(client)
                break


if __name__ == '__main__':
    server = Server((HOST, PORT))
    server.listen()