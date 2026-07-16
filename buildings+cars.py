from PIL import Image, ImageDraw, ImageFont
import random
import math
from carfunction import draw_car
from housefunction import draw_building
ROWS = 4
COLS = 4

CELL_W = 300
CELL_H = 420

OUT = "buildings+cars_grid.png"




def draw_town_tile(draw, x0, y0, cell_w, cell_h):
    # background
    draw.rectangle(
        [x0, y0, x0 + cell_w, y0 + cell_h],
        fill=(190, 220, 255)
    )

    # ground / road
    draw.rectangle(
        [x0, y0 + cell_h - 120, x0 + cell_w, y0 + cell_h],
        fill=(80, 80, 80)
    )

    # reuse existing building
    draw_building(draw, x0, y0, cell_w, cell_h)

    # reuse existing car
    draw_car(draw, x0, y0 + 80, cell_w, cell_h)

img = Image.new("RGB", (1920, 1080), (180, 220, 255))
draw = ImageDraw.Draw(img)

# draw lots of buildings
for _ in range(25):
    x = random.randint(0, 1920 - CELL_W)
    y = random.randint(0, 680 - CELL_H)
    draw_building(draw, x, y, CELL_W, CELL_H)

# draw lots of cars
for _ in range(12):
    x = random.randint(0, 1920 - CELL_W)
    y = random.randint(680, 1080)
    draw_car(draw, x, y, CELL_W, CELL_H)
img.save(OUT)
img.show()
