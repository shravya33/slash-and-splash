# collision.py

import math


def point_to_segment_distance(point, segment_start, segment_end):
    """
    Shortest distance from point to line segment.
    """
    px, py = point
    x1, y1 = segment_start
    x2, y2 = segment_end

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)

    t = (
        ((px - x1) * dx) + ((py - y1) * dy)
    ) / (dx * dx + dy * dy)

    t = max(0, min(1, t))

    closest_x = x1 + t * dx
    closest_y = y1 + t * dy

    return math.hypot(
        px - closest_x,
        py - closest_y
    )


def swipe_hits_fruit(swipe_line, fruit, margin=12):
    """
    Check line-circle collision.
    """
    if swipe_line is None:
        return False

    start, end = swipe_line

    center = (fruit.x, fruit.y)

    distance = point_to_segment_distance(
        center,
        start,
        end
    )

    return distance <= (fruit.radius + margin)