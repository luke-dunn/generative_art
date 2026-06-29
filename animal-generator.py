from PIL import Image, ImageDraw
import random
import os

# ============================================
# settings
# ============================================
CELL = 10
GRID_W = 216
GRID_H = 384
N_FRAMES = 1800
GROWTH_PROB = 0.85          # base growth rate
MAX_NEW_PER_FRAME = 20
DEATH_AGE = 60
OUTDIR = "frames"

os.makedirs(OUTDIR, exist_ok=True)

# 4-neighbourhood
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


# ============================================
# seed animal
# ============================================
def make_seed():
    """
    Start with a small pentomino-like animal near the centre.
    Each cell stores its age.
    """
    cx, cy = GRID_W // 2, GRID_H // 2
    return {
        (cx, cy): 0,
        (cx + 1, cy): 0,
        (cx - 1, cy): 0,
        (cx, cy - 1): 0,
        (cx, cy + 1): 0,
    }


# ============================================
# geometry helpers
# ============================================
def in_bounds(x, y):
    return 0 <= x < GRID_W and 0 <= y < GRID_H


def get_frontier(cells):
    """
    Return all empty cells adjacent to the current animal.
    """
    frontier = set()

    for x, y in cells:
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny) and (nx, ny) not in cells:
                frontier.add((nx, ny))

    return frontier


def count_neighbours(pos, cells):
    """
    Count occupied 4-neighbours around a given position.
    """
    x, y = pos
    n = 0
    for dx, dy in DIRS:
        nx, ny = x + dx, y + dy
        if (nx, ny) in cells:
            n += 1
    return n


# ============================================
# colour by age
# ============================================
def age_to_colour(age, death_age=DEATH_AGE):
    """
    Newborn cells flash red for one frame.
    Then they fade from dark to light grayscale.
    Dead cells are absent, so the background remains white.
    """
    if age == 0:
        return (255, 0, 0)  # newborn flash

    # clamp just in case
    if age < 0:
        age = 0
    if age > death_age - 1:
        age = death_age - 1

    # older = lighter
    v = int(255 * age / max(1, death_age - 1))
    return (v, v, v)


# ============================================
# simulation step
# ============================================
def step(cells, p=GROWTH_PROB, max_new=MAX_NEW_PER_FRAME, death_age=DEATH_AGE):
    """
    One generation:
    1. age all existing cells
    2. remove cells that reach death_age
    3. add new cells on the frontier with probability inversely
       proportional to the number of occupied neighbours
    """
    aged_cells = {}

    # age existing cells; remove old ones
    for pos, age in cells.items():
        new_age = age + 1
        if new_age < death_age:
            aged_cells[pos] = new_age

    # grow from current frontier
    frontier = list(get_frontier(aged_cells))
    random.shuffle(frontier)

    added = 0
    for pos in frontier:
        if added >= max_new:
            break

        neighbour_count = count_neighbours(pos, aged_cells)
        growth_prob = p / (neighbour_count + 1)

        if random.random() < growth_prob:
            aged_cells[pos] = 0
            added += 1

    return aged_cells


# ============================================
# drawing
# ============================================
def draw_cells(cells, frame_no):
    img = Image.new("RGB", (GRID_W * CELL, GRID_H * CELL), "white")
    draw = ImageDraw.Draw(img)

    for (x, y), age in cells.items():
        x0 = x * CELL
        y0 = y * CELL
        x1 = x0 + CELL - 1
        y1 = y0 + CELL - 1

        colour = age_to_colour(age)
        draw.rectangle([x0, y0, x1, y1], fill=colour)

    img.save(f"{OUTDIR}/frame_{frame_no:04d}.png")


# ============================================
# main
# ============================================
def main():
    cells = make_seed()

    for frame_no in range(N_FRAMES):
        draw_cells(cells, frame_no)
        cells = step(cells)


if __name__ == "__main__":
    main()
