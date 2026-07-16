from PIL import Image, ImageDraw, ImageFont
import random
import math

ROWS = 4
COLS = 4

CELL_W = 300
CELL_H = 420

OUT = "building_grid.png"


def draw_building(draw, x0, y0, cell_w, cell_h):
    cx = x0 + cell_w // 2

    ground_y = y0 + cell_h - 135

    floors = random.randint(1, 4)
    body_w = random.randint(90, 170)
    floor_h = random.randint(45, 60)
    body_h = floors * floor_h

    body_left = cx - body_w // 2
    body_right = cx + body_w // 2
    body_top = ground_y - body_h

    body_colour = (
        random.randint(170, 230),
        random.randint(150, 220),
        random.randint(120, 200)
    )

    outline_width = random.randint(2, 4)
    wobble = random.randint(0, 8)

    roof_type = random.choice(["flat", "gable", "shed"])

    # slightly wonky body
    body = [
        (body_left + random.randint(-wobble, wobble), body_top),
        (body_right + random.randint(-wobble, wobble), body_top),
        (body_right + random.randint(-wobble, wobble), ground_y),
        (body_left + random.randint(-wobble, wobble), ground_y),
    ]

    draw.polygon(body, fill=body_colour, outline="black")
    draw.line(body + [body[0]], fill="black", width=outline_width)

    # roof
    roof_colour = (
        random.randint(120, 180),
        random.randint(60, 110),
        random.randint(40, 80)
    )

    roof_h = random.randint(25, 55)

    if roof_type == "flat":
        roof = [
            (body_left - 8, body_top),
            (body_right + 8, body_top),
            (body_right + 8, body_top - 12),
            (body_left - 8, body_top - 12),
        ]
    elif roof_type == "gable":
        roof = [
            (body_left - 12, body_top),
            (cx, body_top - roof_h),
            (body_right + 12, body_top),
        ]
    else:  # shed
        roof = [
            (body_left - 10, body_top),
            (body_right + 10, body_top - roof_h),
            (body_right + 10, body_top - roof_h),
            (body_left - 10, body_top),
        ]

    draw.polygon(roof, fill=roof_colour, outline="black")
    draw.line(roof + [roof[0]], fill="black", width=outline_width)

    # door
    door_w = random.randint(24, 36)
    door_h = random.randint(38, 55)
    door_x = cx - door_w // 2

    door_colour = (
        random.randint(90, 150),
        random.randint(50, 100),
        random.randint(30, 70)
    )

    draw.rectangle(
        [door_x, ground_y - door_h, door_x + door_w, ground_y],
        fill=door_colour,
        outline="black",
        width=2
    )

    draw.ellipse(
        [door_x + door_w - 8, ground_y - door_h // 2,
         door_x + door_w - 4, ground_y - door_h // 2 + 4],
        fill="yellow",
        outline="black"
    )

    # windows
    win_cols = random.randint(1, 3)
    win_w = random.randint(18, 28)
    win_h = random.randint(22, 32)

    window_colour = (
        random.randint(120, 190),
        random.randint(180, 230),
        random.randint(210, 255)
    )

    for f in range(floors):
        y = ground_y - (f + 1) * floor_h + 12

        for c in range(win_cols):
            spacing = body_w / (win_cols + 1)
            wx = int(body_left + spacing * (c + 1) - win_w // 2)

            # skip lower middle window if it would collide with door
            if f == 0 and abs(wx + win_w // 2 - cx) < 25:
                continue

            draw.rectangle(
                [wx, y, wx + win_w, y + win_h],
                fill=window_colour,
                outline="black",
                width=2
            )

            # crossbars
            draw.line(
                [(wx + win_w // 2, y), (wx + win_w // 2, y + win_h)],
                fill="black"
            )
            draw.line(
                [(wx, y + win_h // 2), (wx + win_w, y + win_h // 2)],
                fill="black"
            )

    # ground line
    draw.line(
        [(x0 + 35, ground_y), (x0 + cell_w - 35, ground_y)],
        fill="black",
        width=1
    )

    return {
        "floors": floors,
        "bodyW": body_w,
        "floorH": floor_h,
        "roof": roof_type,
        "roofH": roof_h,
        "wins": win_cols,
        "wob": wobble,
        "ow": outline_width,
        "body": body_colour,
        "roofCol": roof_colour,
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

        params = draw_building(draw, x0, y0, CELL_W, CELL_H)

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
