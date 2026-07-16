from PIL import Image, ImageDraw
import random

from housefunction import draw_building
from carfunction import draw_car
from treefunction import draw_tree


W = 1400
H = 900
OUT = "townscape.png"

random.seed()

img = Image.new("RGB", (W, H), (225, 240, 255))
draw = ImageDraw.Draw(img)


def draw_row(y, count, scale_min, scale_max):
    for _ in range(count):
        x = random.randint(100, W - 100)
        scale = random.uniform(scale_min, scale_max)

        draw_building(
            draw,
            x,
            y + random.randint(-20, 20),
            scale
        )


def draw_row_of_cars(y, count, scale_min, scale_max):
    for _ in range(count):
        x = random.randint(50, W - 50)
        scale = random.uniform(scale_min, scale_max)

        draw_car(
            draw,
            x,
            y + random.randint(-8, 8),
            scale
        )


def draw_row_of_trees(y, count, scale_min, scale_max):
    for _ in range(count):
        scale = random.uniform(scale_min, scale_max)

        cell_w = int(220 * scale)
        cell_h = int(330 * scale)

        x = random.randint(-cell_w // 2, W - cell_w // 2)

        # draw_tree expects the top-left corner of a cell
        x0 = x
        y0 = y - cell_h

        draw_tree(
            draw,
            x0,
            y0,
            cell_w,
            cell_h
        )


# distant hills
draw.polygon(
    [
        (0, 360),
        (200, 260),
        (420, 350),
        (650, 240),
        (900, 350),
        (1120, 270),
        (W, 360),
        (W, H),
        (0, H)
    ],
    fill=(190, 210, 200)
)

# ground bands
draw.rectangle([0, 390, W, H], fill=(205, 220, 190))
draw.rectangle([0, 620, W, H], fill=(190, 205, 175))
draw.rectangle([0, 760, W, H], fill=(175, 185, 160))


# Draw far to near

# distant neighbourhood
draw_row_of_trees(360, 10, 0.30, 0.45)
draw_row(410, 38, 0.35, 0.50)

# middle neighbourhood
draw_row_of_trees(550, 9, 0.45, 0.65)
draw_row(590, 34, 0.55, 0.75)

# near neighbourhood
draw_row_of_trees(705, 8, 0.65, 0.90)
draw_row(760, 30, 0.85, 1.15)

# a few trees visible in front of buildings
draw_row_of_trees(770, 3, 0.75, 1.05)

# foreground traffic
draw_row_of_cars(825, 9, 0.75, 1.05)


img.save(OUT)
img.show()
