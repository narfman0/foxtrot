def lerp(origin, destination, progress):
    """ Linear interpolation between origin and destination.
    :param tuple origin: 2-tuple of x, y coordinates for origin
    :param tuple destination: 2-tuple of x, y coordinates for destination
    :param float progress: ratio of completion between origin and destination, [0-1]
    e.g. 25% of the way through the trip from origin to destination would be .25
    """
    origin_x, origin_y = origin
    destination_x, destination_y = destination
    x = origin_x + int(progress * float(destination_x - origin_x))
    y = origin_y + int(progress * float(destination_y - origin_y))
    return x, y


def smoothstep(x):
    if x <= 0:
        return 0
    elif x >= 1:
        return 1
    return 3 * x ** 2 - 2 * x ** 3
