from typing import List
import argparse
import bios
import tkinter


def read_cfg(cfg_path: str) -> dict:
    config = bios.read(cfg_path)
    return config


def create_window() -> tkinter.Tk:
    window = tkinter.Tk()
    window.title("Virtual Camera")
    return window


def render(canvas: tkinter.Canvas, polygons: List[List[int]], outline_colour: str, distance: int,
           screen_height: int, screen_width: int):
    canvas.delete(tkinter.ALL)
    for polygon in polygons:
        for point in polygon:

            point_2d = project(point, distance, screen_height, screen_width)
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

    window = create_window()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    canvas = tkinter.Canvas(window, width=screen_width, height=screen_height, bg=bg_colour)

    render(canvas, polygons, outline_colour, distance, screen_height, screen_width)

    tkinter.mainloop()
