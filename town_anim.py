from PIL import Image, ImageDraw
from pathlib import Path
import random

from housefunction import draw_building
from carfunction import draw_car
from treefunction import draw_tree


W = 1400
H = 900

FRAMES_DIR = Path("town_frames")
FRAMES_DIR.mkdir(exist_ok=True)

# Remove frames left from an earlier render
for old_frame in FRAMES_DIR.glob("frame_*.png"):
    old_frame.unlink()

random.seed()

img = Image.new("RGB", (W, H), (225, 240, 255))
draw = ImageDraw.Draw(img)

frame_number = 0


def save_frame():
    global frame_number

    filename = FRAMES_DIR / f"frame_{frame_number:04d}.png"
    img.save(filename)

    print(f"Saved {filename}")
    frame_number += 1


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

        save_frame()


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

        save_frame()


def draw_row_of_trees(y, count, scale_min, scale_max):
    for _ in range(count):
        scale = random.uniform(scale_min, scale_max)

        cell_w = int(180 * scale)
        cell_h = int(300 * scale)

        x0 = random.randint(
            -cell_w // 2,
            W - cell_w // 2
        )

        y0 = y - cell_h

        draw_tree(
            draw,
            x0,
            y0,
            cell_w,
            cell_h
        )

        save_frame()


# --------------------------------------------------
# Permanent background
# --------------------------------------------------

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

draw.rectangle(
    [0, 390, W, H],
    fill=(205, 220, 190)
)

draw.rectangle(
    [0, 620, W, H],
    fill=(190, 205, 175)
)

draw.rectangle(
    [0, 760, W, H],
    fill=(175, 185, 160)
)


# Save the empty landscape as frame zero
save_frame()


# --------------------------------------------------
# Add objects from far to near
# --------------------------------------------------

# Distant neighbourhood
draw_row_of_trees(360, 8, 0.30, 0.45)
draw_row(410, 38, 0.35, 0.50)

# Middle neighbourhood
draw_row_of_trees(550, 7, 0.45, 0.65)
draw_row(590, 34, 0.55, 0.75)

# Near neighbourhood
draw_row_of_trees(705, 6, 0.65, 0.90)
draw_row(760, 30, 0.85, 1.15)

# Trees in front of buildings
draw_row_of_trees(770, 3, 0.75, 1.05)

# Foreground traffic
draw_row_of_cars(825, 9, 0.75, 1.05)


# Save the completed town separately
img.save("townscape_final.png")

print()
print(f"Finished: {frame_number} frames")
