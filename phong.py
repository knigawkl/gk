import math
import tkinter
import itertools
from numpy import multiply, subtract, dot
from helpers import read_cfg, get_parser

parser = get_parser()
args = parser.parse_args()

cfg = read_cfg(args.conf_path)
WIDTH = cfg["window"]["width"]
HEIGHT = cfg["window"]["height"]

OBSERVER = cfg["coords"]["observer"]
CENTER = cfg["coords"]["center"]
SOURCE = cfg["coords"]["source"]

RADIUS = cfg["radius"]

root = tkinter.Tk()
root.title('Phong')
image = tkinter.PhotoImage(width=WIDTH, height=HEIGHT)
label = tkinter.Label(image=image)
label.pack()


def z_coord(x, y):
    # a = 1 so it can be skipped
    b = -2 * CENTER[2]
    c = CENTER[2] ** 2 + (x - CENTER[0]) ** 2 + (y - CENTER[1]) ** 2 - RADIUS ** 2

    delta = b ** 2 - 4 * c

    if delta == 0:
        return -b / 2
    elif delta > 0:
        z1 = (-b - math.sqrt(delta)) / 2
        z2 = (-b + math.sqrt(delta)) / 2
        return min(z1, z2)


def vector(start_point, end_point):
    return [end_point[0] - start_point[0],
            end_point[1] - start_point[1],
            end_point[2] - start_point[2]]


def norm(vector):
    return math.sqrt(sum(e ** 2 for e in vector))


def versor(vector):
    n = norm(vector)
    return [e / n for e in vector]


def illumination(point):
    IA = cfg["illumination"]["IA"]
    IP = cfg["illumination"]["IP"]
    KA = 0.05
    KD = 0.5
    KS = 0.5
    N = 50

    n = versor(vector(CENTER, point))
    v = versor(vector(point, OBSERVER))
    l = versor(vector(point, SOURCE))
    r = versor(subtract(multiply(multiply(n, 2), multiply(n, l)), l))

    return IA * KA + IP * KD * max(dot(n, l), 0) + KS * max(dot(r, v), 0) ** N


def render():
    for x, y in itertools.product(range(WIDTH), range(HEIGHT)):
        coords = (x, HEIGHT - y)
        z = z_coord(x, y)
        if z:
            intensity = min(int(illumination([x, y, z]) * 255), 255)
            image.put('#{0:02x}{0:02x}{0:02x}'.format(intensity), coords)
        else:
            image.put('black', coords)


render()

tkinter.mainloop()
