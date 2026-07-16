from PIL import Image, ImageDraw, ImageFont
import random
import math

ROWS = 4
COLS = 4

CELL_W = 300
CELL_H = 420

OUT = "leaf_grid.png"


def draw_leaf(draw, x0, y0, cell_w, cell_h):
    cx = x0 + cell_w // 2

    top = (cx, y0 + 30)
    bottom = (cx, y0 + cell_h - 120)

    npoints = random.randint(6, 10)
    max_width = random.randint(70, 135)
    wobble = random.randint(5, 35)
    outline_width = random.randint(2, 5)
    curve = random.randint(-35, 35)
    fill = (
        random.randint(185, 220),
        random.randint(230, 255),
        random.randint(185, 220)
    )

    midrib_colour = (
        random.randint(40, 80),
        random.randint(120, 170),
        random.randint(40, 80)
    )


    vein_count = random.randint(6, 14)
    vein_angle = random.randint(25, 55)
    vein_colour = (
        random.randint(80, 130),
        random.randint(150, 210),
        random.randint(80, 130)
    )


    left = [top]

    for i in range(1, npoints):
        t = i / npoints
        y = top[1] + t * (bottom[1] - top[1])

        # curved centre line: zero at top/bottom, strongest in middle
        curve_offset = int(curve * math.sin(math.pi * t))

        centre_x = cx + curve_offset

        bulge = math.sin(math.pi * t)
        width = int(max_width * bulge)

        x = centre_x - width + random.randint(-wobble, wobble)
        left.append((x, int(y)))

    left.append(bottom)


    right = []

    for x, y in reversed(left):
        t = (y - top[1]) / (bottom[1] - top[1])
        curve_offset = int(curve * math.sin(math.pi * t))
        centre_x = cx + curve_offset
        right.append((2 * centre_x - x, y))

    leaf = left + right

    # make a mask for the leaf body
    mask = Image.new("L", draw.im.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.polygon(leaf, fill=255)

    # slightly lighter/darker fill colours
    fill_top = (
        min(fill[0] + 20, 255),
        min(fill[1] + 10, 255),
        min(fill[2] + 20, 255)
    )

    fill_bottom = (
        max(fill[0] - 20, 0),
        max(fill[1] - 15, 0),
        max(fill[2] - 20, 0)
    )

    # create full-image gradient
    gradient = Image.new("RGB", draw.im.size, "white")
    grad_draw = ImageDraw.Draw(gradient)

    for y in range(y0, y0 + cell_h):
        t = (y - y0) / cell_h

        r = int(fill_top[0] * (1 - t) + fill_bottom[0] * t)
        g = int(fill_top[1] * (1 - t) + fill_bottom[1] * t)
        b = int(fill_top[2] * (1 - t) + fill_bottom[2] * t)

        grad_draw.line(
            [(x0, y), (x0 + cell_w, y)],
            fill=(r, g, b)
        )

    # paste gradient only inside leaf
    draw.bitmap((0, 0), mask, fill=None)
    draw._image.paste(gradient, (0, 0), mask)



    # secondary veins
    for i in range(1, vein_count + 1):
        t = i / (vein_count + 1)

        y = top[1] + t * (bottom[1] - top[1])
        curve_offset = int(curve * math.sin(math.pi * t))
        centre_x = cx + curve_offset

        bulge = math.sin(math.pi * t)
        leaf_half_width = int(max_width * bulge * 0.75)

        # veins point slightly upward
        dy = -int(leaf_half_width * math.tan(math.radians(vein_angle)) * 0.35)

        left_end = (
            centre_x - leaf_half_width,
            int(y + dy)
        )

        right_end = (
            centre_x + leaf_half_width,
            int(y + dy)
        )

        start = (centre_x, int(y))

        draw.line([start, left_end], fill=vein_colour, width=1)
        draw.line([start, right_end], fill=vein_colour, width=1)

    outline_colours = []

    for p1, p2 in zip(leaf, leaf[1:] + [leaf[0]]):
        edge = (
            random.randint(20, 50),
            random.randint(90, 150),
            random.randint(20, 50)
        )
        outline_colours.append(edge)
        draw.line([p1, p2], fill=edge, width=outline_width)

    midrib = []

    for i in range(30):
        t = i / 29
        y = top[1] + t * (bottom[1] - top[1])
        curve_offset = int(curve * math.sin(math.pi * t))
        x = cx + curve_offset
        midrib.append((x, int(y)))

    draw.line(midrib, fill=midrib_colour, width=2)
    return {
        "veins": vein_count,
        "vAng": vein_angle,
        "vCol": vein_colour,
        "pts": npoints,
        "maxW": max_width,
        "wob": wobble,
        "ow": outline_width,
        "fill": fill,
        "midrib": midrib_colour,
        "curve": curve,
    }


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

        params = draw_leaf(draw, x0, y0, CELL_W, CELL_H)

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
