import math
import re
import json

from SwitchGame import Vec2


class Math:

    @staticmethod
    def get_vector_from_angle(__angle: int, __speed: int) -> Vec2:
        return Vec2(
            math.cos(math.radians(__angle)) * __speed,
            -math.sin(math.radians(__angle)) * __speed
        )


class Strings:

    @staticmethod
    def processing_data(__data: bytes) -> list[dict]:
        requests = []
        split_data: list[str] = re.split(r'}(?={)', __data.decode('utf-8'))

        for req in split_data:
            if req[-1] != "}": req = req + "}"
            requests.append(json.loads(req))

        return requests