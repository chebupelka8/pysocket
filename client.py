import socket
import json

import threading

from typing import Tuple, Never

HOST, PORT = 'localhost', 5050


class Client:
    def __init__(self, address: Tuple[str, int]) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(address)
        print(f'Connected to {address}.')

        threading.Thread(target=self.receive).start()

    def get_response(self) -> dict:
        return json.loads(self.client.recv(1024).decode('UTF-8'))

    def receive(self) -> Never:
        while True:
            try:
                received = self.get_response()
                print(received)

            except (ConnectionResetError, OSError):
                print("Connection is broken. (Server has broken the connection)")
                self.client.close()
                break


if __name__ == '__main__':
    client = Client((HOST, PORT))
