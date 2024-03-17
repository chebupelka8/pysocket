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
        self.client.connect(address)

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
        self.__is_connected = False
        self.client.close()

        ClientNotifier.disconnection_notify(self.__address, "Client was disconnected")
        sys.exit()

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
                self.client.close()
                break

            except OSError:
                ClientNotifier.disconnection_notify(self.__address, "Client was disconnected")
                self.client.close()
                break


    def __repr__(self) -> str:
        return f'Client(address={self.__address})'
