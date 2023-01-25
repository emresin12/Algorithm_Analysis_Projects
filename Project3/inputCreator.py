from random import randint
import math


def create_input(case, input_type, size):
    if case == "average":
        if input_type == 1:
            return [randint(1, 10 * size) for _ in range(size)]
        elif input_type == 2:
            return [randint(1, math.floor(0.75 * size)) for _ in range(size)]
        elif input_type == 3:
            return [randint(1, math.floor(0.25 * size)) for _ in range(size)]
        elif input_type == 4:
            return [1 for _ in range(size)]
    elif case == "worst":
        if input_type == 1:
            arr = [randint(1, 10 * size) for _ in range(size)]
            arr.sort()
            return arr
        elif input_type == 2:
            arr = [randint(1, math.floor(0.75 * size)) for _ in range(size)]
            arr.sort()
            return arr
        elif input_type == 3:
            arr = [randint(1, math.floor(0.25 * size)) for _ in range(size)]
            arr.sort()
            return arr
        elif input_type == 4:
            return [1 for _ in range(size)]
