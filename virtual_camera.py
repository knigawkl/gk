import math
import numpy
from typing import List
import tkinter
import functools

from helpers import read_cfg, get_parser

priority = lambda p: math.sqrt(sum([e ** 2 for e in numpy.mean(numpy.array(p), axis=0)]))
project = lambda point, dist, h, w: (w / 2 + (dist * point[0] / point[2]), h / 2 - (dist * point[1] / point[2]))
translate = lambda point, vector: list(numpy.sum([point, vector], axis=0))


def render(canvas: tkinter.Canvas, polygons: List[List[int]], outline: str, dist: int, height: int, width: int):
    canvas.delete(tkinter.ALL)
    polygons = sorted(polygons, key=priority, reverse=True)
    for polygon in polygons:
        points = []
        for point in polygon:
            points.append(project(point, dist, height, width))
        for i in range(len(points) - 1):
            canvas.create_line(points[i], points[i + 1], fill=outline)
        canvas.create_line(points[0], points[len(points) - 1], fill=outline)
    canvas.pack()


def zoom(key: str):
    global distance
    step = zoom_step if key == "r" else -zoom_step
    distance += step


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
    polygons = list(map(lambda p: list(map(functools.partial(translate, vector=vec), p)), polygons))



def action(event):
    actions = {"r": zoom, "t": zoom,
               "a": trans, "d": trans, "c": trans, "x": trans, "w": trans, "s": trans}
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
    step = cfg["step"]
    width = cfg["screen"]["width"]
    height = cfg["screen"]["height"]

    window = tkinter.Tk()
    window.title("Virtual Camera")
    window.bind("<Key>", action)
    canvas = tkinter.Canvas(window, width=width, height=height, bg=background)
    render(canvas, polygons, outline, distance, height, width)
    tkinter.mainloop()
