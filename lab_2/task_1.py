import time

from graphics import *
import math
import numpy as np

# Варіант 18. Ромб. Переміщення – (обертання+масштабування). Обертання циклічне, траєкторію скрити.

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 1024

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

def translation(dx, dy):
    return np.array([
        [1, 0, dx],
        [0, 1, dy],
        [0, 0, 1]
    ])

def scaling(k):
    return np.array([
        [k, 0, 0],
        [0, k, 0],
        [0, 0, 1]
    ])

def rotation(angle):
    theta = math.radians(angle)
    return np.array([
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta), math.cos(theta), 0],
        [0, 0, 1]
    ])

def create_diamond(radius: float):
    points = []
    for i in range(4):
        angle = 2 * math.pi * i / 4
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points.append([x, y, 1])
    return np.array(points).T

def draw_diamond(win, matrix, color = "black"):
    points = []
    for i in range(matrix.shape[1]):
        points.append(Point(matrix[0, i], matrix[1, i]))
    diamond = Polygon(points)
    diamond.setOutline(color)
    diamond.setWidth(2)
    diamond.draw(win)
    return diamond

def draw_trajectory_points(win, points, color: Color):
    for i in range(len(points) - 1, 0, -1):
        points[i].undraw()
        points[i].setOutline(color_rgb(color.r, color.g, color.b))
        points[i].draw(win)
        if color.r >= 255 and color.g >= 255 and color.b >= 255:
            points.pop(i)
        color.r = min(color.r + 5, 255)
        color.b = min(color.b + 5, 255)
        color.g = min(color.g + 5, 255)

win = GraphWin("2D Diamond", WINDOW_WIDTH, WINDOW_HEIGHT)
win.setBackground("white")

scale_direction = 1
scale_step = 1.15
rotation_step = math.radians(1)
max_size = 250
diamond_size = 100
diamond_x = WINDOW_WIDTH / 2
diamond_y = WINDOW_HEIGHT / 2
trajectory_radius = 200
trajectory_angle = 1
diamond = create_diamond(diamond_size)
trajectory_points = []

running = True
while running:
    if win.checkMouse():
        running = False
        break

    diamond_x = WINDOW_WIDTH / 2 + trajectory_radius * math.cos(trajectory_angle)
    diamond_y = WINDOW_HEIGHT / 2 + trajectory_radius * math.sin(trajectory_angle)
    trajectory_angle += 0.02

    if scale_step > 2.5 or scale_step < 0.1:
        scale_direction *= -1
    scale_step += scale_direction * 0.01
    rotation_step += 1.15

    T = translation(diamond_x, diamond_y)
    S = scaling(scale_step)
    R = rotation(rotation_step)
    M = T @ R @ S
    diamond_matrix = M @ diamond

    figure = draw_diamond(win, diamond_matrix, "black")
    next_point = Point(diamond_x, diamond_y)
    trajectory_points.append(next_point)
    draw_trajectory_points(win, trajectory_points, Color(255, 0, 0))

    time.sleep(0.01)
    figure.undraw()