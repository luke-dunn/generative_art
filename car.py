from PIL import Image, ImageDraw, ImageFont
import random
import math
from carfunction import draw_car
ROWS = 4
COLS = 4

CELL_W = 300
CELL_H = 420

OUT = "car_grid.png"




img = Image.new(
    "RGB",
    (COLS * CELL_W, ROWS * CELL_H),
    "white"
)

draw = ImageDraw.Draw(img)
font = ImageFont.load_default()

for row in range(ROWS):
    for col in range(COLS):
        x0 = col * CELL_W
        y0 = row * CELL_H

        params = draw_car(draw, x0, y0, CELL_W, CELL_H)

        lines = [f"{k}: {v}" for k, v in params.items()]
        text = "\n".join(lines)

        draw.multiline_text(
            (x0 + 8, y0 + CELL_H - 125),
            text,
            fill="black",
            font=font,
            spacing=2
        )

        draw.rectangle(
            [x0, y0, x0 + CELL_W - 1, y0 + CELL_H - 1],
            outline="black",
            width=1
        )

img.save(OUT)
img.show()
