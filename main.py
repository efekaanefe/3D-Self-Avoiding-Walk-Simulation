import pygame
import random
import os, sys
import numpy as np

WIDTH = 1000
HEIGHT = 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Self-Avoiding Walk")
ORIGIN_X = WIDTH // 2
ORIGIN_Y = HEIGHT // 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Self_Avoiding_Walk:
    def __init__(self):
        self.coordinates = [(0, 0, 0)]

        self.directions = {  # origin is at the top-left of the screen
            "up": [0, -1, 0],
            "down": [0, 1, 0],
            "left": [-1, 0, 0],
            "right": [1, 0, 0],
            "out": [0, 0, 1],  # from the screen
            "in": [0, 0, -1],  # into the screen
        }

        self.opposite_directions = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left",
            "in": "out",
            "out": "in",
        }

        self.selected_direction_count = {
            "up": 0,
            "down": 0,
            "left": 0,
            "right": 0,
            "out": 0,
            "in": 0,
        }
        self.last_direction = None
        self.angle = 45

        self.followig_last_step = True

    def add_new_coordinate(self, direction="left"):

        if self.last_direction != None:
            self.selected_direction_count[self.last_direction] += 1
            # print(self.selected_direction_count)
        self.last_direction = direction
        last_coordinate = np.array(self.coordinates[-1])
        to_append = list(last_coordinate + np.array(self.directions[direction]))
        if to_append not in self.coordinates:
            self.coordinates.append(to_append)
            return True
        else:
            # print("Chose another direction", random.randint(0, 100))
            return False

    def project(self):
        theta = self.angle
        # projection matrix without perspective
        PROJECTION = np.array([[1, 0, 0], [0, 1, 0]])

        # rotation matrixes
        ROT_MATRIX_X = np.array(
            [
                [1, 0, 0],
                [0, np.cos(theta), -np.sin(theta)],
                [0, np.sin(theta), np.cos(theta)],
            ]
        )

        ROT_MATRIX_Y = np.array(
            [
                [np.cos(theta), 0, np.sin(theta)],
                [0, 1, 0],
                [-np.sin(theta), 0, np.cos(theta)],
            ]
        )

        ROT_MATRIX_Z = np.array(
            [
                [np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1],
            ]
        )

        projected = []
        for coordinate in self.coordinates:
            coordinate = coordinate
            rotated = np.dot(ROT_MATRIX_X, coordinate)
            # rotated = np.dot(ROT_MATRIX_Z, rotated)
            rotated = np.dot(ROT_MATRIX_Y, rotated)

            DISTANCE = 3
            z = 1 / (DISTANCE - rotated[2])
            # PROJECTION adjusted to give perspective
            projected2d = np.dot(PROJECTION, rotated)
            projected2d *= 15
            projected.append(projected2d)

        return projected

    def draw(self):
        global ORIGIN_X, ORIGIN_Y
        projected = self.project()
        length = len(projected)

        # to see the last step in the screen
        if self.followig_last_step:
            x_last = projected[-1][0] + ORIGIN_X
            y_last = projected[-1][1] + ORIGIN_Y
            # print(x_last, y_last)

            frame = 30
            if not (frame < x_last < WIDTH - frame):
                delta = (
                    (WIDTH // 2 - frame) if x_last < frame else -(WIDTH // 2 - frame)
                )
                ORIGIN_X += delta
            if not (frame < y_last < HEIGHT - frame):
                delta = (
                    (HEIGHT // 2 - frame) if y_last < frame else -(HEIGHT // 2 - frame)
                )
                ORIGIN_Y += delta

        for i in range(length):
            coordinate = projected[i]
            # print("x: ", coordinate[0] + ORIGIN_X, "y: ", coordinate[1] + ORIGIN_Y)
            radius = 1 if i != length - 1 else 3
            color = WHITE if i != length - 1 else GREEN
            pygame.draw.circle(
                WIN,
                color,
                (ORIGIN_X + coordinate[0], ORIGIN_Y + coordinate[1]),
                radius,
            )

            if i != length - 1 and length > 2:
                coordinate_next = projected[i + 1]
                x1 = coordinate[0] + ORIGIN_X
                y1 = coordinate[1] + ORIGIN_Y
                x2 = coordinate_next[0] + ORIGIN_X
                y2 = coordinate_next[1] + ORIGIN_Y

                pygame.draw.line(WIN, RED, (x1, y1), (x2, y2), 1)


def main():
    walker = Self_Avoiding_Walk()
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(75)
        WIN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
                sys.exit()

        directions = list(walker.directions.keys())
        if walker.last_direction:
            directions.remove(walker.opposite_directions[walker.last_direction])

        for _ in range(len(walker.coordinates)):
            random_direction = random.choice(directions)
            add_condition = walker.add_new_coordinate(random_direction)
            if add_condition:
                break
            else:
                walker.coordinates.pop()  # backtracking

        walker.angle += 0.002
        walker.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
