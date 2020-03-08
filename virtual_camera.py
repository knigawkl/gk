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


def render(canvas: tkinter.Canvas):
    canvas.delete(tkinter.ALL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf_path')
    args = parser.parse_args()

    cfg = read_cfg(args.conf_path)
    bg_colour = cfg["bg_colour"]

    window = create_window()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    canvas = tkinter.Canvas(window, width=screen_width, height=screen_height, bg=bg_colour)
    tkinter.mainloop()
