from PIL import Image, ImageDraw, ImageFont
import random
import math
import random


def draw_car(draw, x, ground_y, scale=1.0):
    cx = x

    body_w = int(random.randint(145, 220) * scale)
    body_h = int(random.randint(45, 70) * scale)

    cabin_w = int(random.randint(65, 120) * scale)
    cabin_h = int(random.randint(35, 60) * scale)

    body_left = cx - body_w // 2
    body_right = cx + body_w // 2
    body_top = ground_y - body_h

    cabin_left = cx - cabin_w // 2
    cabin_right = cx + cabin_w // 2
    cabin_top = body_top - cabin_h

    wheel_r = max(3, int(random.randint(14, 24) * scale))
    wheel_gap = int(random.randint(35, 55) * scale)
    wheel_y = ground_y

    outline_width = max(1, int(random.randint(2, 4) * scale))
    wobble = int(random.randint(0, 5) * scale)

    body_colour = (
        random.randint(120, 240),
        random.randint(90, 220),
        random.randint(70, 220)
    )

    window_colour = (
        random.randint(120, 180),
        random.randint(180, 230),
        random.randint(210, 255)
    )

    roof_type = random.choice(["round", "box", "low"])

    # car body
    body = [
        (
            body_left + random.randint(-wobble, wobble),
            body_top + int(8 * scale)
        ),
        (
            body_right + random.randint(-wobble, wobble),
            body_top + int(10 * scale)
        ),
        (
            body_right - int(10 * scale),
            ground_y - int(8 * scale)
        ),
        (
            body_left + int(10 * scale),
            ground_y - int(8 * scale)
        ),
    ]

    draw.polygon(body, fill=body_colour, outline="black")
    draw.line(
        body + [body[0]],
        fill="black",
        width=outline_width
    )

    # cabin / roof
    if roof_type == "round":
        cabin = [
            (cabin_left, body_top + int(4 * scale)),
            (cabin_left + int(18 * scale), cabin_top),
            (cabin_right - int(18 * scale), cabin_top),
            (cabin_right, body_top + int(4 * scale)),
        ]

    elif roof_type == "box":
        cabin = [
            (cabin_left, body_top + int(4 * scale)),
            (cabin_left + int(5 * scale), cabin_top),
            (cabin_right - int(5 * scale), cabin_top),
            (cabin_right, body_top + int(4 * scale)),
        ]

    else:
        cabin = [
            (cabin_left - int(10 * scale), body_top + int(4 * scale)),
            (cabin_left + int(25 * scale), cabin_top + int(15 * scale)),
            (cabin_right - int(15 * scale), cabin_top + int(12 * scale)),
            (cabin_right + int(10 * scale), body_top + int(4 * scale)),
        ]

    draw.polygon(cabin, fill=body_colour, outline="black")
    draw.line(
        cabin + [cabin[0]],
        fill="black",
        width=outline_width
    )

    # windows
    windscreen = [
        (
            cabin_left + int(8 * scale),
            body_top + int(2 * scale)
        ),
        (
            cx - int(4 * scale),
            cabin_top + int(8 * scale)
        ),
        (
            cx - int(4 * scale),
            body_top + int(2 * scale)
        ),
    ]

    rear_window = [
        (
            cx + int(4 * scale),
            cabin_top + int(8 * scale)
        ),
        (
            cabin_right - int(8 * scale),
            body_top + int(2 * scale)
        ),
        (
            cx + int(4 * scale),
            body_top + int(2 * scale)
        ),
    ]

    draw.polygon(
        windscreen,
        fill=window_colour,
        outline="black"
    )

    draw.polygon(
        rear_window,
        fill=window_colour,
        outline="black"
    )

    # wheels
    wheel1_x = cx - wheel_gap
    wheel2_x = cx + wheel_gap

    for wheel_x in [wheel1_x, wheel2_x]:
        draw.ellipse(
            [
                wheel_x - wheel_r,
                wheel_y - wheel_r,
                wheel_x + wheel_r,
                wheel_y + wheel_r
            ],
            fill=(20, 20, 20),
            outline="black",
            width=max(1, int(2 * scale))
        )

        hub_r = max(1, wheel_r // 2)

        draw.ellipse(
            [
                wheel_x - hub_r,
                wheel_y - hub_r,
                wheel_x + hub_r,
                wheel_y + hub_r
            ],
            fill=(180, 180, 180),
            outline="black",
            width=1
        )

    # lights
    light_size = max(2, int(random.randint(5, 9) * scale))

    draw.ellipse(
        [
            body_left + int(5 * scale),
            body_top + body_h // 2,
            body_left + int(5 * scale) + light_size,
            body_top + body_h // 2 + light_size
        ],
        fill="yellow",
        outline="black"
    )

    draw.ellipse(
        [
            body_right - int(5 * scale) - light_size,
            body_top + body_h // 2,
            body_right - int(5 * scale),
            body_top + body_h // 2 + light_size
        ],
        fill="orange",
        outline="black"
    )

    # door line
    draw.line(
        [
            (cx, body_top + int(8 * scale)),
            (cx, ground_y - int(12 * scale))
        ],
        fill="black",
        width=max(1, int(scale))
    )

    return {
        "bodyW": body_w,
        "bodyH": body_h,
        "cabW": cabin_w,
        "cabH": cabin_h,
        "roof": roof_type,
        "wheelR": wheel_r,
        "gap": wheel_gap,
        "wob": wobble,
        "ow": outline_width,
        "colour": body_colour,
    }
