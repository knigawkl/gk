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
        for i in range(len(points)-1):
            print(i, i+1)
            canvas.create_line(points[i], points[i+1], fill=outline)
        canvas.create_line(points[0], points[len(points)-1], fill=outline)
    canvas.pack()


if __name__ == "__main__":
    args = get_parser().parse_args()
    cfg = read_cfg(args.conf_path)
    background = cfg["bg_colour"]
    outline = cfg["outline_colour"]
    distance = cfg["distance"]
    polygons = cfg["polygons"]
    width = cfg["screen"]["width"]
    height = cfg["screen"]["height"]

    window = tkinter.Tk().title("Virtual Camera")
    canvas = tkinter.Canvas(window, width=width, height=height, bg=background)

    render(canvas, polygons, outline, distance, height, width)

    tkinter.mainloop()
