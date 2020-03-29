import math
import numpy
from typing import List
import tkinter

from helpers import read_cfg, get_parser


priority = lambda p: math.sqrt(sum([e**2 for e in numpy.mean(numpy.array(p), axis=0)]))
project = lambda point, dist, h, w: (w / 2 + (dist * point[0] / point[2]), h / 2 - (dist * point[1] / point[2]))


def render(canvas: tkinter.Canvas, polygons: List[List[int]], outline: str, dist: int, height: int, width: int):
    canvas.delete(tkinter.ALL)
    polygons = sorted(polygons, key=priority, reverse=True)
    for polygon in polygons:
        points = []
        for point in polygon:
            points.append(project(point, dist, height, width))
        canvas.create_line(points[0], points[1], fill=outline)
        canvas.create_line(points[1], points[2], fill=outline)
        canvas.create_line(points[2], points[3], fill=outline)
        canvas.create_line(points[3], points[0], fill=outline)
    canvas.pack()


if __name__ == "__main__":
    args = get_parser().parse_args()
    cfg = read_cfg(args.conf_path)
    bg_colour = cfg["bg_colour"]
    outline_colour = cfg["outline_colour"]
    distance = cfg["distance"]
    polygons = cfg["polygons"]
    width = cfg["screen"]["width"]
    height = cfg["screen"]["height"]

    window = tkinter.Tk().title("Virtual Camera")
    canvas = tkinter.Canvas(window, width=width, height=height, bg=bg_colour)

    render(canvas, polygons, outline_colour, distance, height, width)

    tkinter.mainloop()
