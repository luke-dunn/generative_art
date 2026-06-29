import os
import math
import random

import pygame
import pymunk
from noise import pnoise2


# ============================================================
# Settings
# ============================================================

WIDTH, HEIGHT = 1080, 1920
FPS = 20
N_FRAMES = 1800
N_BLOBS = 55

OUTPUT_DIR = "frames2"
VIDEO_NAME = "blobs06.mp4"

BG = (210, 230, 240)

MERGE_SPEED = 40
SPLIT_SPIN = 7.5

MIN_START_MASS = 200
MAX_START_MASS = 12000

MIN_START_SPEED = -400
MAX_START_SPEED = 400

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# Genetics / morphology helpers
# ============================================================

def rand_colour():
    return tuple(random.randint(000, 255) for _ in range(3))


def mutate_colour(colour, amount=10):
    return tuple(
        max(0, min(255, c + random.randint(-amount, amount)))
        for c in colour
    )


def blend_colours(a, b):
    return tuple((x + y) // 2 for x, y in zip(a, b))


def make_signature(num_points=100, scale=1.0, amp=12):
    values = []

    for i in range(num_points):
        theta = 2 * math.pi * i / num_points

        n = pnoise2(
            math.cos(theta) * scale + 1000,
            math.sin(theta) * scale + 1000
        )

        values.append(n * amp)

    return values


def mutate_signature(signature, amount=2):
    return [x + random.uniform(-amount, amount) for x in signature]


def blend_signatures(a, b):
    return [(x + y) / 2 for x, y in zip(a, b)]


# ============================================================
# Blob
# ============================================================

class Blob:
    def __init__(self, space, pos=None, mass=None, colour=None, signature=None):
        if mass is None:
            mass = random.uniform(MIN_START_MASS, MAX_START_MASS)

        radius = math.sqrt(mass)
        moment = pymunk.moment_for_circle(mass, 0, radius)

        self.body = pymunk.Body(mass, moment)

        if pos is None:
            pos = (
                random.randint(100, WIDTH - 100),
                random.randint(100, HEIGHT - 100),
            )

        self.body.position = pos
        self.body.velocity = (
            random.uniform(MIN_START_SPEED, MAX_START_SPEED),
            random.uniform(MIN_START_SPEED, MAX_START_SPEED),
        )

        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = random.uniform(0.4, 0.6)
        self.shape.friction = 0.5
        self.shape.collision_type = 1

        if colour is None:
            colour = rand_colour()
        self.colour = colour

        if signature is None:
            signature = make_signature(
                scale=random.uniform(0.9, 1.1),
                amp=random.randint(5, 15)
            )
        self.signature = signature

        space.add(self.body, self.shape)

    def jitter(self, strength=50):
        fx = random.uniform(-strength, strength)
        fy = random.uniform(-strength, strength)
        self.body.apply_force_at_local_point((fx, fy))

    def drift_shape(self, base_amount=0.3):
        spin = abs(self.body.angular_velocity)
        amount = base_amount + min(spin * 0.005, 2.0)
        self.signature = mutate_signature(self.signature, amount)

    def spin_up(self):
        self.body.apply_impulse_at_local_point((0, 10000), (30, 0))

    def draw(self, surface):
        cx, cy = self.body.position
        angle = self.body.angle
        base_radius = self.shape.radius

        points = []
        n = len(self.signature)

        for i in range(n):
            theta = 2 * math.pi * i / n
            r = max(base_radius * 0.3, base_radius + self.signature[i])

            x = r * math.cos(theta)
            y = r * math.sin(theta)

            xr = x * math.cos(angle) - y * math.sin(angle)
            yr = x * math.sin(angle) + y * math.cos(angle)

            points.append((cx + xr, cy + yr))

        pygame.draw.polygon(surface, self.colour, points)

        nucleus_radius = max(5, int(base_radius ** 0.8))
        pygame.draw.circle(
            surface,
            (100, 70, 85),
            (int(cx), int(cy)),
            nucleus_radius
        )


# ============================================================
# World
# ============================================================

class World:
    def __init__(self):
        pygame.init()

        self.screen = pygame.Surface((WIDTH, HEIGHT))

        self.space = pymunk.Space()
        self.space.gravity = (0, 0)

        self.blobs = []

        self.create_walls()
        self.create_blobs(N_BLOBS)
        self.install_collision_handler()

    def create_walls(self):
        walls = [
            pymunk.Segment(self.space.static_body, (0, 0), (WIDTH, 0), 1),
            pymunk.Segment(self.space.static_body, (0, 0), (0, HEIGHT), 1),
            pymunk.Segment(self.space.static_body, (WIDTH, 0), (WIDTH, HEIGHT), 1),
            pymunk.Segment(self.space.static_body, (0, HEIGHT), (WIDTH, HEIGHT), 1),
        ]

        for wall in walls:
            wall.elasticity = 1.0

        self.space.add(*walls)

    def create_blobs(self, n):
        for _ in range(n):
            self.blobs.append(Blob(self.space))

    def remove_blob(self, blob):
        self.space.remove(blob.body, blob.shape)

        if blob in self.blobs:
            self.blobs.remove(blob)

    def split_blob(self, blob):
        child_mass = blob.body.mass / 2
        parent_pos = tuple(blob.body.position)
        parent_vel = tuple(blob.body.velocity)

        for direction in (-1, 1):
            child = Blob(
                self.space,
                pos=parent_pos,
                mass=child_mass,
                colour=mutate_colour(blob.colour),
                signature=mutate_signature(blob.signature, 2)
            )

            offset = 150
            child.body.velocity = (
                parent_vel[0] + direction * random.uniform(offset, offset * 1.2),
                parent_vel[1] + direction * random.uniform(offset, offset * 1.2),
            )

            self.blobs.append(child)

        self.remove_blob(blob)

    def merge_blobs(self, a, b):
        new_mass = (a.body.mass + b.body.mass) * 0.85
        new_pos = (a.body.position + b.body.position) / 2
        new_colour = blend_colours(a.colour, b.colour)
        new_signature = blend_signatures(a.signature, b.signature)

        self.remove_blob(a)
        self.remove_blob(b)

        new_blob = Blob(
            self.space,
            pos=tuple(new_pos),
            mass=new_mass,
            colour=new_colour,
            signature=new_signature
        )

        self.blobs.append(new_blob)

    def install_collision_handler(self):
        handler = self.space.add_collision_handler(1, 1)
        handler.pre_solve = self.on_blob_collision

    def on_blob_collision(self, arbiter, space, data):
        shape_a, shape_b = arbiter.shapes
        body_a = shape_a.body
        body_b = shape_b.body

        rel_vel = (body_a.velocity - body_b.velocity).length

        if rel_vel < MERGE_SPEED:
            blob_a = next((b for b in self.blobs if b.body == body_a), None)
            blob_b = next((b for b in self.blobs if b.body == body_b), None)

            if blob_a and blob_b and blob_a is not blob_b:
                self.merge_blobs(blob_a, blob_b)

            return False

        return True

    def update(self):
        for blob in self.blobs[:]:
            blob.jitter()
            blob.drift_shape()

            if blob in self.blobs and abs(blob.body.angular_velocity) > SPLIT_SPIN:
                self.split_blob(blob)

        if len(self.blobs) == 1:
            self.blobs[0].spin_up()

        self.space.step(1 / FPS)

    def draw(self):
        self.screen.fill(BG)

        for blob in self.blobs:
            blob.draw(self.screen)

    def save_frame(self, frame_number):
        filename = os.path.join(OUTPUT_DIR, f"frame_{frame_number:04d}.png")
        pygame.image.save(self.screen, filename)

    def run(self, n_frames):
        for frame in range(n_frames):
            self.update()
            self.draw()
            self.save_frame(frame)

            if frame % 1000 == 0:
                print(".", end="", flush=True)


# ============================================================
# Export
# ============================================================

def export_video():
    cmd = (
        f'ffmpeg -y -framerate {FPS} '
        f'-i "{OUTPUT_DIR}/frame_%04d.png" '
        f'-c:v libx264 -pix_fmt yuv420p "{VIDEO_NAME}"'
    )
    os.system(cmd)


# ============================================================
# Main
# ============================================================

def main():
    world = World()
    world.run(N_FRAMES)
    export_video()
    pygame.quit()


if __name__ == "__main__":
    main()
