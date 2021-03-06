import math


def productivity(affinity_count):
    """ Return number representing productivity given the affinity count
    e.g. if you have nothing, we still automatically produce, but if there
    is someone, it will produce more efficiently.
    """
    if affinity_count == 0:
        return 0.3
    return 0.419874 * math.log(11.2406 * affinity_count)


def distance(origin, destination):
    """ Calculate distance between origin and destination
    :param tuple origin: 2-tuple x, y coordinates
    :param tuple destination: 2-tuple x, y coordinates
    """
    ox, oy = origin
    dx, dy = destination
    return math.sqrt((ox - dx) ** 2 + (oy - dy) ** 2)


def distance_cost(distance):
    """ Create a cost according to distance traveled. Should be roughly
    logarithmic; using wolfram alpha log fit regression analysis:
    log fit {10, 8},{100,10},{1000, 15},{5000, 20}
    """
    return int(1.92577 * math.log(3.65906 * distance))


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


def travel_cost(origin, destination):
    return distance_cost(distance(origin, destination))
