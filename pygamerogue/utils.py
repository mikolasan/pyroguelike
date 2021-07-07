def shift_rect(rect, direction, distance):
    if direction == 'left':
        rect.left -= distance
    elif direction == 'right':
        rect.left += distance
    elif direction == 'up':
        rect.top -= distance
    elif direction == 'down':
        rect.top += distance
    return rect
