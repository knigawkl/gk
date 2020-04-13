from math import sqrt, cos, sin, pi
import numpy
from typing import List
import tkinter
from functools import partial
from helpers import read_cfg, get_parser

priority = lambda p: sqrt(sum([e ** 2 for e in numpy.mean(numpy.array(p), axis=0)]))
project = lambda point, dist, h, w: (w / 2 + (dist * point[0] / point[2]), h / 2 - (dist * point[1] / point[2]))
translate = lambda point, vector: list(numpy.sum([point, vector], axis=0))
rotate = lambda point, matrix: list(numpy.matmul(matrix, point + [1])[:-1])


def render(canvas: tkinter.Canvas, polygons: List[List[int]], outline: str, dist: int, height: int, width: int):
    canvas.delete(tkinter.ALL)
    polygons = sorted(polygons, key=priority, reverse=True)
    for polygon in polygons:
        points = []
        for point in polygon:
            points.append(project(point, dist, height, width))
        canvas.create_polygon(points, fill=background, outline=outline)
    canvas.pack()


def zoom(key: str):
    global distance
    distance = distance + zoom_step if key == "r" else distance - zoom_step


def trans(key: str):
    global polygons
    if key == "a":
        vec = [step, 0, 0]
    elif key == "d":
        vec = [-step, 0, 0]
    elif key == "c":
        vec = [0, -step, 0]
    elif key == "x":
        vec = [0, step, 0]
    elif key == "w":
        vec = [0, 0, -step]
    elif key == "s":
        vec = [0, 0, step]
    polygons = list(map(lambda p: list(map(partial(translate, vector=vec), p)), polygons))


def rot(key):
    global polygons
    angle = -rotation_step if key in ("8", "7", "4") else rotation_step
    if key in ("8", "2"):
        matrix = [[1, 0, 0, 0], [0, cos(angle), -sin(angle), 0], [0, sin(angle), cos(angle), 0], [0, 0, 0, 1]]
    elif key in ("7", "9"):
        matrix = [[cos(angle), 0, sin(angle), 0], [0, 1, 0, 0], [-sin(angle), 0, cos(angle), 0], [0, 0, 0, 1]]
    elif key in ("4", "6"):
        matrix = [[cos(angle), -sin(angle), 0, 0], [sin(angle), cos(angle), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    polygons = list(map(lambda p: list(map(partial(rotate, matrix=matrix), p)), polygons))


def action(event):
    actions = dict.fromkeys(["r", "t"], zoom)
    actions.update(dict.fromkeys(["a", "d", "c", "x", "w", "s"], trans))
    actions.update(dict.fromkeys(["8", "2", "7", "9", "4", "6"], rot))
    actions[event.char](event.char)
    render(canvas, polygons, outline, distance, height, width)


if __name__ == "__main__":
    args = get_parser().parse_args()
    cfg = read_cfg(args.conf_path)
    background = cfg["bg_colour"]
    outline = cfg["outline_colour"]
    distance = cfg["distance"]
    polygons = cfg["polygons"]
    zoom_step = cfg["zoom_step"]
    rotation_step = pi / cfg["rotation_step"]
    step = cfg["step"]
    width = cfg["screen"]["width"]
    height = cfg["screen"]["height"]

    window = tkinter.Tk()
    window.title("Virtual Camera")
    window.bind("<Key>", action)
    canvas = tkinter.Canvas(window, width=width, height=height, bg=background)
    render(canvas, polygons, outline, distance, height, width)
    tkinter.mainloop()
