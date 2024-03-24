import socket
import json
import sys

import threading
import time

from src import Strings

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

        # commands
        self.__update_players_command = None

        # start receive in the new thread: --
        threading.Thread(target=self.receive).start()

    def set_update_players_command(self, __command) -> None:
        self.__update_players_command = __command

    def get_players(self) -> list:
        return self.__players

    def disconnect(self) -> None:
        self.__destroy()

        ClientNotifier.disconnection_notify(self.__address, "Client was disconnected")  # notify about disconnection

    def move(self, __to: str) -> None:
        self.__send({
            "request": "move",
            "side": __to
        })

    def rotate(self, __degrees: int) -> None:
        self.__send({
            "request": "rotate",
            "degrees": __degrees
        })

    def __get_response(self) -> list[dict]:
        return Strings.processing_data(self.client.recv(1024))

    def __send(self, data: dict) -> None:
        self.client.send(bytes(json.dumps(data), "utf-8"))

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
                for received in self.__get_response():
                    if received["response"] == "get_players":
                        self.__players = received["players"]

                    if received["response"] == "update_players":
                        self.__players = received["players"]
                        self.__update_players_command()

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
