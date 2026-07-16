import random

def make_rocket_genes():
    return {
        "body_w": random.randint(55, 95),
        "body_h": random.randint(150, 230),
        "nose_h": random.randint(45, 85),
        "fin_h": random.randint(55, 90),
        "fin_w": random.randint(25, 50),
        "window_r": random.randint(16, 27),
        "stripe_h": random.randint(12, 24),
        "body_colour": (
            random.randint(170, 245),
            random.randint(170, 245),
            random.randint(170, 245),
        ),
        "accent_colour": (
            random.randint(80, 230),
            random.randint(80, 230),
            random.randint(80, 230),
        ),
    }


def draw_rocket(draw, x, y, scale, genes, flame_scale=1.0):
    """
    Draw a rocket centred at (x, y).

    x, y:
        Position of the bottom of the rocket body.

    scale:
        Size multiplier, such as 0.5, 1.0 or 1.5.

    genes:
        Dictionary containing the rocket's permanent design.
    """

    body_w = int(genes["body_w"] * scale)
    body_h = int(genes["body_h"] * scale)
    nose_h = int(genes["nose_h"] * scale)

    fin_h = int(genes["fin_h"] * scale)
    fin_w = int(genes["fin_w"] * scale)

    window_r = int(genes["window_r"] * scale)
    stripe_h = int(genes["stripe_h"] * scale)

    body_colour = genes["body_colour"]
    accent_colour = genes["accent_colour"]

    outline_w = max(1, int(3 * scale))

    body_left = x - body_w // 2
    body_right = x + body_w // 2
    body_bottom = y
    body_top = y - body_h

    # Main body
    draw.rounded_rectangle(
        [
            body_left,
            body_top,
            body_right,
            body_bottom,
        ],
        radius=max(1, body_w // 4),
        fill=body_colour,
        outline="black",
        width=outline_w,
    )

    # Nose cone
    draw.polygon(
        [
            (x, body_top - nose_h),
            (body_left, body_top + 8),
            (body_right, body_top + 8),
        ],
        fill=accent_colour,
        outline="black",
    )

    left_fin = [
        (body_left + int(8 * scale), body_bottom - fin_h),
        (body_left - fin_w, body_bottom),
        (body_left + int(12 * scale), body_bottom - int(8 * scale)),
    ]

    right_fin = [
        (body_right - int(8 * scale), body_bottom - fin_h),
        (body_right + fin_w, body_bottom),
        (body_right - int(12 * scale), body_bottom - int(8 * scale)),
    ]

    draw.polygon(
        left_fin,
        fill=accent_colour,
        outline="black",
    )

    draw.polygon(
        right_fin,
        fill=accent_colour,
        outline="black",
    )

    window_y = body_top + body_h // 3

    draw.ellipse(
        [
            x - window_r,
            window_y - window_r,
            x + window_r,
            window_y + window_r,
        ],
        fill=(130, 210, 245),
        outline="black",
        width=outline_w,
    )

    # Window reflection
    highlight_r = max(2, window_r // 4)

    draw.ellipse(
        [
            x - window_r // 2,
            window_y - window_r // 2,
            x - window_r // 2 + highlight_r,
            window_y - window_r // 2 + highlight_r,
        ],
        fill="white",
    )

    stripe_y = body_top + int(body_h * 0.62)

    draw.rectangle(
        [
            body_left + outline_w,
            stripe_y,
            body_right - outline_w,
            stripe_y + stripe_h,
        ],
        fill=accent_colour,
        outline="black",
        width=max(1, int(2 * scale)),
    )

    nozzle_w = body_w // 2
    nozzle_h = max(8, int(24 * scale))

    draw.rectangle(
        [
            x - nozzle_w // 2,
            body_bottom - 2,
            x + nozzle_w // 2,
            body_bottom + nozzle_h,
        ],
        fill=(80, 80, 90),
        outline="black",
        width=outline_w,
    )

    flame_w = max(8, int(36 * scale))
    flame_h = max(12, int(60 * scale * flame_scale))

    draw.polygon(
        [
            (x - flame_w // 2, body_bottom + nozzle_h),
            (x, body_bottom + nozzle_h + flame_h),
            (x + flame_w // 2, body_bottom + nozzle_h),
        ],
        fill=(255, 150, 30),
        outline="black",
    )

    draw.polygon(
        [
            (x - flame_w // 5, body_bottom + nozzle_h),
            (x, body_bottom + nozzle_h + flame_h * 2 // 3),
            (x + flame_w // 5, body_bottom + nozzle_h),
        ],
        fill=(255, 245, 100),
    )

