import time

from graphics import *
import math
import numpy as np
import random

# Варіант 18. Паралелепіпед. З’являється та гасне, з’являється в різних частинах графічного вікна змінюючи колір заливки.

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 1024

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

def translation(dx, dy, dz):
    return np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ])

def scaling(k):
    return np.array([
        [k, 0, 0, 0],
        [0, k, 0, 0],
        [0, 0, k, 0],
        [0, 0, 0, 1]
    ])

def shear(sh_xy=0.0, sh_xz=0.0, sh_yx=0.0, sh_yz=0.0, sh_zx=0.0, sh_zy=0.0):
    return np.array([
        [1, sh_xy, sh_xz, 0],
        [sh_yx, 1, sh_yz, 0],
        [sh_zx, sh_zy, 1, 0],
        [0, 0, 0, 1]
    ])

def rotation_x(angle):
    theta = math.radians(angle)
    return np.array([
        [1, 0, 0, 0],
        [0, math.cos(theta), -math.sin(theta), 0],
        [0, math.sin(theta), math.cos(theta), 0],
        [0, 0, 0, 1]
    ])

def rotation_y(angle):
    theta = math.radians(angle)
    return np.array([
        [math.cos(theta), 0, -math.sin(theta), 0],
        [0, 1, 0, 0],
        [math.sin(theta), 0, math.cos(theta), 0],
        [0, 0, 0, 1]
    ])

def isometric_projection():
    angle_x = math.radians(35.264)
    angle_y = math.radians(45)
    Rx = rotation_x(angle_x)
    Ry = rotation_y(angle_y)
    return Rx @ Ry

def projection_points(points3D):
    proj_matrix = np.array([[1,0,0,0],
                            [0,1,0,0]])
    return proj_matrix @ points3D

def create_parallelepiped(size):
    w, h, d = size
    h_x, h_y, h_z = w / 2, h / 2, d / 2
    vertices = np.array([[-h_x, -h_y, -h_z, 1],
                       [h_x, -h_y, -h_z, 1],
                       [h_x, h_y, -h_z, 1],
                       [-h_x, h_y, -h_z, 1],
                       [-h_x, -h_y, h_z, 1],
                       [h_x, -h_y, h_z, 1],
                       [h_x, h_y, h_z, 1],
                       [-h_x, h_y, h_z, 1]])

    vertices = vertices @ shear(0.25, 0.5, 0.75).T

    return np.array(vertices).T

def draw_parallelepiped(win, matrix, color = "green"):
    faces_idx = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 1, 5, 4],
        [2, 3, 7, 6],
        [1, 2, 6, 5],
        [0, 3, 7, 4]
    ]
    polygons = []
    for face in faces_idx:
        face_points = [Point(matrix[0, i], matrix[1, i]) for i in face]
        facet_polygon = Polygon(face_points)
        facet_polygon.setFill(color)
        facet_polygon.setOutline("black")
        facet_polygon.setWidth(2)
        facet_polygon.draw(win)
        polygons.append(facet_polygon)
    return polygons

def undraw_polygons(polygons):
    for poly in polygons:
        poly.undraw()

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return color_rgb(r, g, b)

win = GraphWin("3D Parallelepiped", WINDOW_WIDTH, WINDOW_HEIGHT)
win.setBackground("white")

color = random_color()
scale_factor = 1
scale_speed = 200
scale_min = 0.0
scale_max = 1.5
figure_size = (100, 200, 300)
figure_x = random.randint(figure_size[0], WINDOW_WIDTH - figure_size[0])
figure_y = random.randint(figure_size[1], WINDOW_HEIGHT - figure_size[1])
theta = math.pi

parallelepiped = create_parallelepiped(figure_size)

running = True
while running:
    if win.checkMouse():
        running = False
        break

    scale_factor = scale_min + (scale_max - scale_min) * (0.5 + 0.5 * math.sin(scale_speed + theta))
    print(scale_factor, theta)

    T = translation(figure_x, figure_y, 0)
    S = scaling(scale_factor)
    P = isometric_projection()

    parallelepiped_3D = P @ (T @ (S @ parallelepiped))
    parallelepiped_2D = projection_points(parallelepiped_3D)

    figure = draw_parallelepiped(win, parallelepiped_2D, color)

    time.sleep(0.1)
    undraw_polygons(figure)
    theta += math.pi * 0.05

    if scale_factor <= 0.005:
        color = random_color()
        figure_x = random.randint(figure_size[0], WINDOW_WIDTH - figure_size[0] - 1)
        figure_y = random.randint(figure_size[1], WINDOW_HEIGHT - figure_size[1] - 1)
