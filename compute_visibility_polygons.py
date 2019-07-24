
# Creates shapes for visiLibity input environment.
# And then uses them by calling visilibity wrapper.
# Currently deterministic.
# Edges should not intersect.
# TO DO:
# --

import numpy as np
import pygame
import os
from compute_visibility import *

res = np.array([600, 900])

def create_shapes():
    border = 0.1 * min(res)
    nHoles = 0
        # Random only
    nEdgesPerHole = 30
    rMin = 10.0
    rMax = 25.0
    rDiff = rMax - rMin
    buffer = border + rMax + 10.0

    shapes = []     # TO DO: change to shapes_ of _.shapes

    frame = np.array([[0, 0], [res[0], 0], res, [0, res[1]]]) + \
            np.array([[1, 1], [-1, 1], [-1, -1], [1, -1]]) * border
    shapes.append(frame)

    angles = np.linspace(0.0, -6.28, nEdgesPerHole + 1)
    angles = angles[:-1]  # Ensures nonzero edge lengths.
    radii = rMin + 0.5 * rDiff * (1.0 - np.cos(2.0 * angles))

    hole = np.zeros((nEdgesPerHole, 2))
    hole[:, 0] = radii * np.cos(angles)
    hole[:, 1] = radii * np.sin(angles)
    # remember "dtype=object" if mixing float & int in np.array

    centers = np.random.uniform(buffer, res - buffer, size=(nHoles, 2))
    for c in centers:
        movedHole = hole + c
        shapes.append(movedHole)

    if True:
        xCen1d = np.linspace(buffer, res[0] - buffer, 8)
        yCen1d = np.linspace(buffer, res[1] - buffer, 8)
        for x in xCen1d:
            for y in yCen1d:
                c = np.array([x, y])
                shape = hole + c
                shapes.append(shape)
    return [shapes, np.concatenate(shapes, axis=0)]


[shapes, verts] = create_shapes()


query = res / 2

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 100)
pygame.init()
screen = pygame.display.set_mode(res)


def update_display():
    for shape in shapes:
        pygame.draw.polygon(screen, (50, 50, 50), shape[:, 0:2], 2)
    rad = 5
    pygame.draw.rect(screen, (250, 250, 250), (query[0] - rad, query[1] - rad, 2 * rad, 2 * rad), 1)
    pygame.display.update()


screen.fill((0, 0, 0))
update_display()

def update_files(query_):

    def dump_surroundings_and_guards():
        file = open("./surroundings.txt", mode="w", encoding="utf-8")   # may need sym link to/from visilibity/src
        for shape in shapes:
            s = "/ another shape\n"
            file.write(s)
            for vert in shape:
                file.write(str(vert[0]) + " ")
                file.write(str(vert[1]) + "\n")
        file.close()

        file = open("./guards.txt",
                    mode="w", encoding="ascii")
        file.write(str(query_[0]) + " ")
        file.write(str(query_[1]) + "\n")
        file.close()
    #dump_surroundings_and_guards()
    # see also np.genfromtxt, os.system

    return compute_visibility(shapes, query_)

def user_closes_window():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        else:
            if event.type == pygame.KEYDOWN:
                prev = query.copy()
                name = pygame.key.name(event.key)
                step_size = 10
                if name == "down":
                    query[1] += step_size
                elif name == "up":
                    query[1] -= step_size
                elif name == "left":
                    query[0] -= step_size
                elif name == "right":
                    query[0] += step_size
                # else do nothing.
                if (query != prev).any():
                    colPr = update_files(query)
                    screen.fill((0, 0, 0))
                    #print(colPr)
                    update_display()
                    pygame.draw.polygon(screen, (250, 150, 50), colPr, 2)
                    rCirc = 100
                    pygame.draw.arc(screen, (0, 200, 200), [int(round(query[0])) - rCirc, int(round(query[1])) - rCirc, 2 * rCirc, 2 * rCirc], 0, 6.3, 3)
                    pygame.display.update()
                            # TO DO: mv these three lines into update_display.
            return False


while not user_closes_window():
    pygame.time.wait(1)

