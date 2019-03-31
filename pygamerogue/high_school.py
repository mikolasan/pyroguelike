import math


def calc_angle_rad(mouse_pos, object_pos):
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]
    object_x = object_pos[0]
    object_y = object_pos[1]
    angle = 0
    if mouse_x > object_x:
        angle = math.atan((object_y - mouse_y) / (mouse_x - object_x))
    elif mouse_x == object_x:
        angle = (math.pi / 2.) if mouse_y < object_y else (-math.pi / 2.)
    elif mouse_x < object_x:
        angle = math.pi + math.atan((object_y - mouse_y) / (mouse_x - object_x))
    return angle


def calc_angle_deg(mouse_pos, object_pos):
    return math.degrees(calc_angle_rad(mouse_pos, object_pos))
