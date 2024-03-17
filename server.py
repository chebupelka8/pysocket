import socket
import json

import threading
import random

from dataclasses import dataclass

from typing import Tuple, Never

from notify import ServerNotifier

HOST, PORT = 'localhost', 5050


@dataclass
class _Player:
    id: int
    address: Tuple[str, int]
    sock: socket.socket
    position: Tuple[int, int]


class Server:
    def __init__(self, addr: Tuple[str, int]) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(addr)
        self.server.listen()

        ServerNotifier.start_server()  # notify about the start

        # variables setup: --
        self.__is_working = True
        self.__clients: list[socket.socket] = []
        self.__players: list[_Player] = []

    def listen(self) -> Never:
        ServerNotifier.listening_server()

        while self.__is_working:
            client, address = self.server.accept()
            self.__clients.append(client)

            ServerNotifier.notify_connected(address)  # notify about the connect client

            threading.Thread(target=self.handle_client, args=(client, address)).start()  # start handle client

    def __disconnect_client(self, address: Tuple[str, int], client, player: _Player) -> None:
        ServerNotifier.notify_disconnected(address)
        self.__clients.remove(client)
        self.__players.remove(player)

    @staticmethod
    def __send(data: dict, client) -> None:
        client.sendall(bytes(json.dumps(data), "utf-8"))

    def __get_players(self) -> list[dict]:
        result = []

        for player in self.__players:
            result.append({
                'id': player.id,
                'address': player.address,
                'position': player.position
            })

        return result

    def handle_client(self, client: socket.socket, address: Tuple[str, int]) -> None:
        player = _Player(len(self.__clients), address, client, (random.randint(0, 300), 100))
        self.__players.append(player)

        while True:
            try:
                data = json.loads(client.recv(1024).decode('utf-8'))

                if not data:  # if client disconnect
                    self.__disconnect_client(address, client, player)
                    break

                if data['request'] == 'get_players':
                    self.__send({
                        "response": "get_players",
                        "players": self.__get_players()
                    }, client)

            except (ConnectionResetError, OSError, json.decoder.JSONDecodeError):
                self.__disconnect_client(address, client, player)
                break


if __name__ == '__main__':
    server = Server((HOST, PORT))
    server.listen()