from SwitchGame import *

from client import Client
from src import Player, Math


class Main(WindowLoop):
    def __init__(self) -> None:
        super().__init__(Vec2(1000, 600), 165)

        self.client = Client(('localhost', 5050))
        self.client.set_update_players_command(self.__generate_players)

        self.__players: list[StaticSprite] = []

    def update_events(self, __event) -> None:
        if __event.type == QUIT:
            self.client.disconnect()
            super().destroy()

        else:
            super().update_events(__event)

    def __generate_players(self) -> None:
        self.__players.clear()

        for i in self.client.get_players():
            self.__players.append(
                Player(Vec2(*i["position"]), i["degrees"], self.client)
            )

    def main(self) -> None:
        # self.__generate_players()

        while True:  # mainloop
            for player, data in zip(self.__players, self.client.get_players()):
                player.movement = Vec2(*data["movement"])
                player.angle = data["degrees"]
                player.rotation()
                player.moving()
                player.draw(self.display, player.rotated_image, alignment_flag=AlignmentFlag.CENTER)

                # print(player.get_client() == self.client)
                #     player.moving()

            # keypress = pygame.key.get_pressed()
            #
            # if keypress[K_w]:
            #     self.movement = Math.get_vector_from_angle(0, 3)
            #     self.client.move(self.movement)
            #
            # else:
            #     self.movement = Vec2(0, 0)
            #     self.client.move(self.movement)

            self.update_display()


if __name__ == "__main__":
    Main().main()