from SwitchGame import *

from client import Client


class Main(WindowLoop):
    def __init__(self) -> None:
        super().__init__(Vec2(1000, 600), 165)

        self.client = Client(('localhost', 5050))

    def update_events(self, __event) -> None:
        if __event.type == QUIT:
            self.client.disconnect()
            super().destroy()

        else:
            super().update_events(__event)

    def main(self) -> None:
        while True:  # mainloop
            for i in self.client.get_players():
                player = StaticSprite(Vec2(*i["position"]), Image("SwitchGame/assets/icon.png"))
                player.draw(self.display)

            self.update_display()


if __name__ == "__main__":
    Main().main()