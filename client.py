import socket
import json
import sys

import threading

from typing import Tuple, Never
from notify import ClientNotifier

HOST, PORT = 'localhost', 5050


class Client:
    def __init__(self, address: Tuple[str, int]) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client.connect(address)

        except ConnectionRefusedError:  # if server is not running
            ClientNotifier.disconnection_notify(address, "Server is not running")
            self.client.close()
            sys.exit()

        ClientNotifier.connection_notify(address)  # notify about the connection

        # variable setup: --
        self.__address = address
        self.__is_connected = True
        self.__players = []

        # start receive in the new thread: --
        threading.Thread(target=self.receive).start()

    def get_response(self) -> dict:
        return json.loads(self.client.recv(1024).decode('UTF-8'))

    def __send(self, data: dict) -> None:
        self.client.sendall(bytes(json.dumps(data), "utf-8"))

    def disconnect(self) -> None:
        self.__destroy()

        ClientNotifier.disconnection_notify(self.__address, "Client was disconnected")  # notify about disconnection

    def __destroy(self) -> None:
        self.__is_connected = False
        self.client.close()

    def receive(self) -> Never:
        while self.__is_connected:
            try:
                # send request to get players
                self.__send({
                    "request": "get_players"
                })

                # get response
                received = self.get_response()

                if received["response"] == "get_players":
                    self.__players = received["players"]

                print(self.__players)

            except ConnectionResetError:
                ClientNotifier.disconnection_notify(self.__address, "Server has broken the connection")
                self.__destroy()
                break

            except OSError:
                self.__destroy()
                break

        sys.exit()

    def __repr__(self) -> str:
        return f'Client(address={self.__address})'
