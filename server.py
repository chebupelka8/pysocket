import random
import socket
import json
import re
import colorama

import threading

from dataclasses import dataclass

from typing import Tuple, Never, Optional
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
    movement: Vec2 = Vec2(0, 0)
    degrees: int = 0
    speed: int = 3


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

        self.__send_update_players(client)

    @staticmethod
    def __send(data: dict, client) -> None:
        client.send(bytes(json.dumps(data), "utf-8"))

    def __sendall(self, data: dict) -> None:
        for cl in self.__clients:
            self.__send(data, cl)

    def __send_update_players(self, __requesting: socket.socket) -> None:
        self.__sendall({
            "response": "update_players",
            "players": self.__get_players(__requesting)
        })

    def __get_players(self, __requesting: socket.socket) -> list[dict]:
        result = []

        for player in self.__players:
            if player.sock != __requesting:
                result.append({
                    'id': player.id,
                    'address': player.address,
                    'position': player.position.xy,
                    'movement': player.movement.xy,
                    'degrees': player.degrees
                })

        # print(f"From {__requesting}:", colorama.Fore.LIGHTBLUE_EX, result, colorama.Style.RESET_ALL)

        return result

    def handle_client(self, client: socket.socket, address: Tuple[str, int]) -> None:
        player = _Player(len(self.__clients), address, client, Vec2(random.randint(0, 300), 100))
        self.__players.append(player)

        self.__send_update_players(client)

        while True:
            try:
                recv = client.recv(1024)

                if not recv:  # if client disconnect
                    self.__disconnect_client(address, client, player)
                    break

                # update position
                # player.position.x += player.movement.x // 4
                # player.position.y += player.movement.y // 4

                for data in Strings.processing_data(recv):
                    if data['request'] == 'get_players':  # send all players on the server
                        self.__send({
                            "response": "get_players",
                            "players": self.__get_players(client)
                        }, client)

                    elif data['request'] == 'move':
                        # player.movement = Vec2(*data['movement'])
                        player.position.x += 1

                    elif data['request'] == 'rotate':
                        player.degrees = data['degrees']

            except (ConnectionResetError, OSError, json.decoder.JSONDecodeError):
                self.__disconnect_client(address, client, player)
                break


if __name__ == '__main__':
    server = Server((HOST, PORT))
    server.listen()