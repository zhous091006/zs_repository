import math
from typing import List


class LibFunction:
    """-------------------------------------- Basic Function ---------------------------------------------"""

    @staticmethod
    def degrees_to_radians(degrees):
        return degrees * (math.pi / 180)

    @staticmethod
    def radians_to_degrees(radians):
        return radians * (180 / math.pi)


lib_func_t = LibFunction
