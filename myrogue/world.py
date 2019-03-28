world = """
----------
|........|
|.?......|
|...@....|
|.....$..|
|.!......|
----------
"""

def get_world():
    a = []
    for line in world.splitlines():
        chars = list(line)
        a.append(chars)
    return a
