import random
import socket
import json
import re

import threading

from dataclasses import dataclass

from typing import Tuple, Never
from SwitchGame import Vec2

from notify import ServerNotifier
from src import Math, Strings

HOST, PORT = 'localhost', 5050


@dataclass
class _Player:
    id: int
    address: Tuple[str, int]
    sock: socket.socket
    position: Vec2
    movement: Vec2
    degrees: int


class Server:
    def __init__(self, addr: Tuple[str, int]) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(addr)
        self.server.listen()

        ServerNotifier.start_server()  # notify about the start

        # variables setup: --
        self.__clients: list[socket.socket] = []
        self.__players: list[_Player] = []

    def listen(self) -> Never:
        ServerNotifier.listening_server()

        while True:
            client, address = self.server.accept()
            self.__clients.append(client)

            ServerNotifier.notify_connected(address)  # notify about the connect client

            threading.Thread(target=self.handle_client, args=(client, address)).start()  # start handle client

    def __disconnect_client(self, address: Tuple[str, int], client, player: _Player) -> None:
        ServerNotifier.notify_disconnected(address)
        self.__clients.remove(client)
        self.__players.remove(player)

        self.__send_update_players()

    @staticmethod
    def __send(data: dict, client) -> None:
        client.send(bytes(json.dumps(data), "utf-8"))

    def __sendall(self, data: dict) -> None:
        for cl in self.__clients:
            self.__send(data, cl)

    def __send_update_players(self) -> None:
        self.__sendall({
            "response": "update_players",
            "players": self.__get_players()
        })

    def __get_players(self) -> list[dict]:
        result = []

        for player in self.__players:
            result.append({
                'id': player.id,
                'address': player.address,
                'position': player.position.xy,
                'movement': player.movement.xy,
                'degrees': player.degrees
            })

        return result

    def handle_client(self, client: socket.socket, address: Tuple[str, int]) -> None:
        player = _Player(len(self.__clients), address, client, Vec2(random.randint(0, 300), 100), Vec2(0, 0), 90)
        self.__players.append(player)

        self.__send_update_players()

        while True:
            try:
                recv = client.recv(1024)

                if not recv:  # if client disconnect
                    self.__disconnect_client(address, client, player)
                    break

                # update position
                # player.position.x += player.movement.x
                # player.position.y += player.movement.y

                for data in Strings.processing_data(recv):
                    if data['request'] == 'get_players':  # send all players on the server
                        self.__send({
                            "response": "get_players",
                            "players": self.__get_players()
                        }, client)
                        print(self.__get_players())

                    if data['request'] == 'move':
                        if data["side"] == "forward":
                            player.movement.x = 1

                        elif data["side"] == "backward":
                            ...

                        # else:
                        #     player.movement = Vec2(0, 0)

                    if data['request'] == 'rotate':
                        player.degrees = data['degrees']

            except (ConnectionResetError, OSError, json.decoder.JSONDecodeError):
                self.__disconnect_client(address, client, player)
                break


if __name__ == '__main__':
    server = Server((HOST, PORT))
    server.listen()