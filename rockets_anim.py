# I've tested with this
from rocketfunction import make_rocket_genes, draw_rocket
from PIL import Image, ImageDraw, ImageFont
import random
import math

img = Image.new(
    "RGB",
    (1080,1920),
    (105, 120, 245)
)

def draw_moon_surface(draw, width, height, horizon_y, craters):

    draw.rectangle(
        [0, horizon_y, width, height],
        fill=(150, 150, 150)
    )

    for crater in craters:
        x = crater["x"]
        y = crater["y"]
        r = crater["r"]

        draw.ellipse(
            [
                x - r,
                y - r // 2,
                x + r,
                y + r // 2
            ],
            fill=(110, 110, 110)
        )

        draw.arc(
            [
                x - r,
                y - r // 2,
                x + r,
                y + r // 2
            ],
            start=200,
            end=340,
            fill=(190, 190, 190),
            width=2
        )



def make_craters(width, horizon_y, height, count=80):
    craters = []

    for _ in range(count):
        r = random.randint(10, 80)

        craters.append({
            "x": random.randint(-r, width + r),
            "y": random.randint(horizon_y + r // 2, height),
            "r": r,
        })

    return craters

craters = make_craters(
    width=1080,
    horizon_y=1650,
    height=1920,
    count=70
)


def make_stars(width, horizon_y, count=300):
    stars = []

    for _ in range(count):
        stars.append({
            "x": random.randint(0, width),
            "y": random.randint(0, horizon_y - 20),
            "r": random.randint(1, 3),
        })

    return stars

def draw_stars(draw, stars):
    for star in stars:
        x = star["x"]
        y = star["y"]
        r = star["r"]

        draw.ellipse(
            [
                x-r,
                y-r,
                x+r,
                y+r
            ],
            fill="white"
        )
stars=make_stars(1080,1650,180)

draw = ImageDraw.Draw(img)
fleet = [make_rocket_genes() for _ in range(6)]

rockets = []

for genes in fleet:
    rockets.append({
        "genes": genes,
        "x": random.randint(100, 980),
        "y": random.randint(-800, -100),
        "speed": random.uniform(2, 6),
        "landed": False,
    })

background = Image.open("a.png").convert("RGB")

for frame_number in range(1000):

##    img = Image.new(
##        "RGB",
##        (1080, 1920),
##        (105, 100, 245)
##    )
    img = background.copy()
    draw = ImageDraw.Draw(img)

    LANDING_Y = 1630


##    draw_stars(draw, stars)
##    
##    draw_moon_surface(
##        draw,
##        1080,
##        1920,
##        1650,
##        craters
##    )

    for rocket in rockets:

        if not rocket["landed"]:
            rocket["y"] += rocket["speed"]

            if rocket["y"] >= LANDING_Y:
                rocket["y"] = LANDING_Y
                rocket["landed"] = True

        flame_scale = (
            random.uniform(0.85, 1.15)
            if not rocket["landed"]
            else 0.0
        )

        draw_rocket(
            draw,
            rocket["x"],
            int(rocket["y"]),
            1.0,
            rocket["genes"],
            flame_scale
        )


    img.save(f"frames/frame_{frame_number:04d}.png")

