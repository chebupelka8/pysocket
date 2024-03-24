from SwitchGame import (
    StaticSprite, Image, ImageEditor,
    Vec2
)

import pygame.key
from pygame.locals import *

from typing import Optional

from .utils import Math


class Player(StaticSprite):

    def __init__(self, __position: Vec2, __angle: int, client, addr: tuple[str, int]) -> None:
        super().__init__(__position, ImageEditor.rotate(Image("SwitchGame/assets/icon.png"), __angle))

        self.__client = client
        self.address = addr
        self.__rotate_angle = 0
        self.rotated_image: Optional[Image] = None

    def get_client(self):
        return self.__client

    @property
    def angle(self) -> int:
        return self.__rotate_angle

    @angle.setter
    def angle(self, value: int) -> None:
        self.__rotate_angle = value

    def rotation(self) -> None:
        self.rotated_image = ImageEditor.rotate(self.image, self.__rotate_angle)

        keypress = pygame.key.get_pressed()

        if keypress[K_a]:
            self.__rotate_angle += 2
            self.__client.rotate(self.__rotate_angle)

        if keypress[K_d]:
            self.__rotate_angle -= 2
            self.__client.rotate(self.__rotate_angle)

        self.__rotate_angle = self.__rotate_angle % 360

    def moving(self) -> None:
        keypress = pygame.key.get_pressed()

        if keypress[K_w]:
            self.movement = Math.get_vector_from_angle(self.__rotate_angle, 3)
            self.__client.move(self.movement)

        else:
            self.movement = Vec2(0, 0)
            self.__client.move(self.movement)