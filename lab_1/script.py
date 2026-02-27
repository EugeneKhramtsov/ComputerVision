import graphics
from graphics import *
import math
import random

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 1024

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return color_rgb(r, g, b)

class Triangle:

    def __init__(self, center: Point, radius: float):
        self.center = center
        self.radius = radius

    def _calculate_vertices(self):
        points = []
        initial_offset = math.radians(30)
        angle_step = math.radians(120)

        for i in range(3):
            x = self.center.x + self.radius * math.cos(initial_offset + angle_step * i)
            y = self.center.y + self.radius * math.sin(initial_offset + angle_step * i)
            points.append(Point(x, y))

        return points

    def draw_lines(self, win: GraphWin):
        points = self._calculate_vertices()
        for i in range(3):
            line = Line(points[i], points[(i + 1) % 3])
            line.draw(win)

    def draw_polygon(self, win: GraphWin):
        points = self._calculate_vertices()
        triangle = Polygon(points)
        triangle.setFill(random_color())
        triangle.draw(win)

class Square:

    def __init__(self, center: Point, side_length: float):
        self.center = center
        self.side_length = side_length

    def _calculate_vertices(self):
        half = self.side_length / 2
        return [
            Point(self.center.x - half, self.center.y - half),
            Point(self.center.x - half, self.center.y + half),
            Point(self.center.x + half, self.center.y + half),
            Point(self.center.x + half, self.center.y - half),
        ]

    def draw_lines(self, win: GraphWin):
        points = self._calculate_vertices()
        for i in range(4):
            line = Line(points[i], points[(i + 1) % 4])
            line.draw(win)

    def draw_rectangle(self, win: GraphWin):
        half = self.side_length / 2
        p1 = Point(self.center.x - half, self.center.y - half)
        p2 = Point(self.center.x + half, self.center.y + half)
        rectangle = Rectangle(p1, p2)
        rectangle.setFill(random_color())
        rectangle.draw(win)

class Circle:

    def __init__(self, center: Point, radius: float, sides: int = 100):
        self.center = center
        self.radius = radius
        self.sides = sides

    def _calculate_vertices(self):
        points = []
        for i in range(self.sides):
            angle = 2 * math.pi * i / self.sides
            x = self.center.x + self.radius * math.cos(angle)
            y = self.center.y + self.radius * math.sin(angle)
            points.append(Point(x, y))
        return points

    def draw_lines(self, win: GraphWin):
        points = self._calculate_vertices()
        for i in range(self.sides):
            line = Line(points[i], points[(i + 1) % self.sides])
            line.draw(win)

    def draw_polygon(self, win: GraphWin):
        points = self._calculate_vertices()
        circle_poly = Polygon(points)
        circle_poly.setOutline(color_rgb(163, 247, 181))
        circle_poly.draw(win)

    def has_point(self, x, y):
        d2 = (x - self.center.x) ** 2 + (y - self.center.y) ** 2
        return d2 <= self.radius ** 2

def draw_as_lines():
    global win, triangle_center, square_center, step, i
    win = GraphWin("Triangle(lines), Square(lines)", WINDOW_WIDTH, WINDOW_HEIGHT)

    triangle_center = Point(WINDOW_WIDTH / 2 - 250, WINDOW_HEIGHT / 2)
    square_center = Point(WINDOW_WIDTH / 2 + 350, WINDOW_HEIGHT / 2 - 50)

    step = 100

    for i in range(4, 0, -1):
        Triangle(triangle_center, i * step).draw_lines(win)

    for i in range(5, 0, -1):
        Square(square_center, i * step).draw_lines(win)

    win.getMouse()
    win.close()

draw_as_lines()

def draw_as_polygon():
    global win, triangle_center, square_center, i
    win = GraphWin("Triangle(polygon), Square(rectangle)", WINDOW_WIDTH, WINDOW_HEIGHT)

    triangle_center = Point(WINDOW_WIDTH / 2 - 250, WINDOW_HEIGHT / 2)
    square_center = Point(WINDOW_WIDTH / 2 + 350, WINDOW_HEIGHT / 2 - 50)

    for i in range(4, 0, -1):
        Triangle(triangle_center, i * step).draw_polygon(win)

    for i in range(5, 0, -1):
        Square(square_center, i * step).draw_rectangle(win)

    win.getMouse()
    win.close()

draw_as_polygon()

def draw_circle_as_lines():
    global win, radius, centers, pt
    win = GraphWin("Logo(lines)", WINDOW_WIDTH, WINDOW_HEIGHT)

    radius = 200
    offset = radius - 40

    centers = [
        Point(WINDOW_WIDTH / 2 - offset, WINDOW_HEIGHT / 2),
        Point(WINDOW_WIDTH / 2 + offset, WINDOW_HEIGHT / 2),
        Point(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - offset),
        Point(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + offset),
    ]

    for pt in centers:
        Circle(pt, radius, 100).draw_lines(win)

    win.getMouse()
    win.close()

draw_circle_as_lines()

def draw_circle_as_polygon():
    global win, pt

    win = GraphWin("Logo(polygon)", WINDOW_WIDTH, WINDOW_HEIGHT)

    radius = 100
    offset = radius - 20

    centers = [
        Point(WINDOW_WIDTH / 2 - offset, WINDOW_HEIGHT / 2),
        Point(WINDOW_WIDTH / 2 + offset, WINDOW_HEIGHT / 2),
        Point(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - offset),
        Point(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + offset),
    ]

    circle1 = Circle(centers[0], radius, 100)
    circle2 = Circle(centers[1], radius, 100)
    circle3 = Circle(centers[2], radius, 100)
    circle4 = Circle(centers[3], radius, 100)

    circle1.draw_polygon(win)
    circle2.draw_polygon(win)
    circle3.draw_polygon(win)
    circle4.draw_polygon(win)

    step = 1
    colors = [
        color_rgb(163, 247, 181),
        color_rgb(64, 201, 162),
        color_rgb(229, 249, 224),
        color_rgb(47, 156, 149)
    ]

    for x in range(0, WINDOW_WIDTH, step):
        for y in range(0, WINDOW_HEIGHT, step):
            color_index = 0

            if circle1.has_point(x, y):
                color_index += 1
            if circle2.has_point(x, y):
                color_index += 1
            if circle3.has_point(x, y):
                color_index += 1
            if circle4.has_point(x, y):
                color_index += 1

            if color_index > 0:
                pt = Point(x, y)
                pt.setOutline(colors[color_index - 2])
                pt.draw(win)

    win.getMouse()
    win.close()

WINDOW_WIDTH = int (WINDOW_WIDTH / 2)
WINDOW_HEIGHT = int (WINDOW_HEIGHT / 2)
draw_circle_as_polygon()
