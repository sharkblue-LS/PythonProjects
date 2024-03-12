import json
import sys

parameter = sys.argv


# print(parameter, type(parameter))


def add_numbers(a, b):
    # res = a + b
    res = {"sum": a + b}
    print(res)
    return res


if __name__ == '__main__':
    add_numbers(int(parameter[1]), int(parameter[2]))
