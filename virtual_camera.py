import math
import numpy
from typing import List
import argparse
import tkinter

from helpers import read_cfg


priority = lambda p: math.sqrt(sum([e**2 for e in numpy.mean(numpy.array(p), axis=0)]))


def render(canvas: tkinter.Canvas, polygons: List[List[int]], outline_colour: str, distance: int,
           screen_height: int, screen_width: int):
    canvas.delete(tkinter.ALL)
    polygons = sorted(polygons, key=priority, reverse=True)
    for polygon in polygons:
        points = []
        for point in polygon:
            point_2d = project(point, distance, screen_height, screen_width)
            points.append(point_2d)
        canvas.create_line(points[0], points[1], fill=outline_colour)
        canvas.create_line(points[1], points[2], fill=outline_colour)
        canvas.create_line(points[2], points[3], fill=outline_colour)
        canvas.create_line(points[3], points[0], fill=outline_colour)
    canvas.pack()


def project(point: List[int], distance: int, height: int, width: int):
    return (width / 2 + (distance * point[0] / point[2]),
            height / 2 - (distance * point[1] / point[2]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf_path')
    args = parser.parse_args()

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
