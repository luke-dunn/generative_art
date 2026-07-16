from PIL import Image, ImageDraw
import random
import math
W = 1400
H = 900

img = Image.new("RGB", (W, H), (225, 240, 255))
draw = ImageDraw.Draw(img)


def draw_tree(draw, x0, y0, cell_w, cell_h):
    """Draw one randomly generated tree inside a rectangular cell."""

    cx = x0 + cell_w // 2
    ground_y = y0 + cell_h - 30

    # Random overall dimensions
    tree_h = random.randint(
        int(cell_h * 0.55),
        int(cell_h * 0.85)
    )

    trunk_h = int(tree_h * random.uniform(0.45, 0.65))
    trunk_w = random.randint(18, 35)

    trunk_top = ground_y - trunk_h

    # Trunk
    trunk_colour = (
        random.randint(90, 135),
        random.randint(55, 90),
        random.randint(25, 55)
    )

    draw.rounded_rectangle(
        [
            cx - trunk_w // 2,
            trunk_top,
            cx + trunk_w // 2,
            ground_y
        ],
        radius=trunk_w // 3,
        fill=trunk_colour,
        outline="black",
        width=2
    )

    # Branches
    for _ in range(random.randint(4, 8)):
        branch_y = random.randint(trunk_top, trunk_top + trunk_h // 2)
        angle = random.uniform(-2.8, -0.35)
        length = random.randint(35, 75)

        end_x = cx + math.cos(angle) * length
        end_y = branch_y + math.sin(angle) * length

        draw.line(
            [(cx, branch_y), (end_x, end_y)],
            fill=trunk_colour,
            width=random.randint(5, 10)
        )

    # Leaf canopy
    canopy_cx = cx + random.randint(-15, 15)
    canopy_cy = trunk_top - random.randint(10, 30)

    leaf_colour = (
        random.randint(40, 100),
        random.randint(120, 190),
        random.randint(40, 100)
    )

    for _ in range(random.randint(18, 30)):
        radius = random.randint(22, 45)

        px = canopy_cx + random.randint(-75, 75)
        py = canopy_cy + random.randint(-60, 55)

        colour = (
            max(0, min(255, leaf_colour[0] + random.randint(-15, 15))),
            max(0, min(255, leaf_colour[1] + random.randint(-15, 15))),
            max(0, min(255, leaf_colour[2] + random.randint(-15, 15)))
        )

        draw.ellipse(
            [px - radius, py - radius, px + radius, py + radius],
            fill=colour,
            outline="black",
            width=2
        )


draw_tree(draw, 100, 100, 300, 420)
img.show()
