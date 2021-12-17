from typing import List, Tuple
from math import atan2
from math import pi

class Point:
    def __init__(self, coordinates: Tuple[int, int]):
        self.X = coordinates[0]
        self.Y = coordinates[1]

def __sort_angle(points, minimum_point: Point):
    def key(point: Point):
        p_atan = atan2(point.Y - minimum_point.Y, point.X - minimum_point.X)
        return (p_atan)

    return sorted(points, key = key)

def __ccw(a: Point, b :Point, c :Point):
    return ((b.X - a.X) * (c.Y - a.Y) - (b.Y - a.Y) * (c.X - a.X))

def graham_scan(points: List[Point]):
    minimum_point = points[0]
    p_idx = 0

    for idx, _ in enumerate(points):
        if idx + 1 >= len(points):
            break

        next_point = points[idx+1]
        if minimum_point.Y == next_point.Y:
            if minimum_point.X > next_point.X:
                minimum_point = next_point
                p_idx = idx + 1
        elif minimum_point.Y > next_point.Y:
                minimum_point = next_point
                p_idx = idx + 1

    points[0], points[p_idx] = points[p_idx], points[0]

    # Ordena el vector de puntos por ángulo tomando como origen las
    # coordenadas "X" y "Y" del punto mínimo calculado con anterioridad
    points = __sort_angle(points, points[0]) # O(n log n)

    stack = [points[0], points[1]]
    stack_tmp = [points[0], points[1]]
    stack_steps = []
    for point in points[2:]:
        p = stack.pop()
        while len(stack) > 0 and __ccw(stack[-1], p, point) <= 0:
            p = stack.pop()

        stack.append(p)
        stack.append(point)

        stack_tmp.append(p)
        stack_tmp.append(point)

        stack_steps.append(stack + stack_tmp)
        stack_tmp = []

    return stack, stack_steps, len(stack_steps) + 1