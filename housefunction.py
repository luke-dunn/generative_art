from PIL import Image, ImageDraw
import random
def draw_building(draw, x, ground_y, scale=1.0):
    floors = random.randint(1, 4)

    body_w = int(scale * random.randint(80, 150))
    floor_h = int(scale * random.randint(40, 55))
    body_h = floors * floor_h

    body_left = x - body_w // 2
    body_right = x + body_w // 2
    body_top = ground_y - body_h

    body_colour = (
        random.randint(170, 235),
        random.randint(150, 220),
        random.randint(120, 200)
    )

    roof_colour = (
        random.randint(120, 180),
        random.randint(50, 100),
        random.randint(30, 70)
    )

    outline_w = max(1, int(scale * 3))
    wobble = int(scale * random.randint(0, 8))

    body = [
        (body_left + random.randint(-wobble, wobble), body_top),
        (body_right + random.randint(-wobble, wobble), body_top),
        (body_right + random.randint(-wobble, wobble), ground_y),
        (body_left + random.randint(-wobble, wobble), ground_y),
    ]

    draw.polygon(body, fill=body_colour, outline="black")
    draw.line(body + [body[0]], fill="black", width=outline_w)

    roof_type = random.choice(["flat", "gable", "gable"])

    roof_h = int(scale * random.randint(25, 55))

    if roof_type == "flat":
        roof = [
            (body_left - 8, body_top),
            (body_right + 8, body_top),
            (body_right + 8, body_top - int(scale * 12)),
            (body_left - 8, body_top - int(scale * 12)),
        ]

    elif roof_type == "gable":
        roof = [
            (body_left - int(scale * 12), body_top),
            (x, body_top - roof_h),
            (body_right + int(scale * 12), body_top),
        ]

    draw.polygon(roof, fill=roof_colour, outline="black")
    draw.line(roof + [roof[0]], fill="black", width=outline_w)

    # door
    door_w = int(scale * random.randint(22, 34))
    door_h = int(scale * random.randint(35, 50))
    door_x = x - door_w // 2

    draw.rectangle(
        [door_x, ground_y - door_h, door_x + door_w, ground_y],
        fill=(110, 70, 40),
        outline="black",
        width=max(1, int(scale * 2))
    )

    # windows
    win_cols = random.randint(1, 3)
    win_w = int(scale * random.randint(16, 24))
    win_h = int(scale * random.randint(18, 28))

    for f in range(floors):
        y = ground_y - (f + 1) * floor_h + int(scale * 10)

        for c in range(win_cols):
            spacing = body_w / (win_cols + 1)
            wx = int(body_left + spacing * (c + 1) - win_w // 2)

            if f == 0 and abs(wx + win_w // 2 - x) < door_w:
                continue

            draw.rectangle(
                [wx, y, wx + win_w, y + win_h],
                fill=(150, 210, 235),
                outline="black",
                width=max(1, int(scale * 2))
            )

            draw.line(
                [(wx + win_w // 2, y), (wx + win_w // 2, y + win_h)],
                fill="black"
            )
            draw.line(
                [(wx, y + win_h // 2), (wx + win_w, y + win_h // 2)],
                fill="black"
            )
