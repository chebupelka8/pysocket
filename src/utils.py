import math
from SwitchGame import Vec2


class Math:

    @staticmethod
    def get_vector_from_angle(__angle: int, __speed: int) -> Vec2:
        return Vec2(
            math.cos(math.radians(__angle)) * __speed,
            -math.sin(math.radians(__angle)) * __speed
        )