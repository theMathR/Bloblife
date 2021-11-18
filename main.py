from math import floor
import pygame
import random
from pygame.locals import *
from constants import *

pygame.init()

window = pygame.display.set_mode((TILE_NUMBER_X * TILE_SIZE, TILE_NUMBER_Y * TILE_SIZE))
pygame.display.set_caption(TITLE)

tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
mini_tile = pygame.Surface((TILE_SIZE * DUCKS, TILE_SIZE * DUCKS))

turn = PLAYER1

selected_tile = UNSELECTED

number_mode = False

blob_movements = {}

font = pygame.font.Font(None, FONT_SIZE)


def create_arrow(direction, movement):
    intensity = floor(movement * 127 / MAX_VALUE + 127)

    if direction in ("left", "right"):
        arrow = pygame.Surface((TILE_SIZE * 2, TILE_SIZE))

        pygame.draw.line(arrow, (intensity, 0, 0), (TILE_SIZE / 2, TILE_SIZE / 2), (TILE_SIZE * 1.5, TILE_SIZE / 2),
                         ARROW_WIDTH)
        if direction == "left":
            pygame.draw.lines(arrow, (intensity, 0, 0), False, ((TILE_SIZE * 3 / 4, TILE_SIZE / 4),
                                                                (TILE_SIZE / 2, TILE_SIZE / 2),
                                                                (TILE_SIZE * 3 / 4, TILE_SIZE * 3 / 4)), ARROW_WIDTH)
        else:
            pygame.draw.lines(arrow, (intensity, 0, 0), False, ((TILE_SIZE * 1.25, TILE_SIZE / 4),
                                                                (TILE_SIZE * 1.5, TILE_SIZE / 2),
                                                                (TILE_SIZE * 1.25, TILE_SIZE * 3 / 4)), ARROW_WIDTH)
    else:
        arrow = pygame.Surface((TILE_SIZE, TILE_SIZE * 2))

        pygame.draw.line(arrow, (intensity, 0, 0), (TILE_SIZE / 2, TILE_SIZE / 2), (TILE_SIZE / 2, TILE_SIZE * 1.5),
                         ARROW_WIDTH)
        if direction == "up":
            pygame.draw.lines(arrow, (intensity, 0, 0), False, ((TILE_SIZE / 4, TILE_SIZE * 3 / 4),
                                                                (TILE_SIZE / 2, TILE_SIZE / 2),
                                                                (TILE_SIZE * 3 / 4, TILE_SIZE * 3 / 4)), ARROW_WIDTH)
        else:
            pygame.draw.lines(arrow, (intensity, 0, 0), False, ((TILE_SIZE / 4, TILE_SIZE * 1.25),
                                                                (TILE_SIZE / 2, TILE_SIZE * 1.5),
                                                                (TILE_SIZE * 3 / 4, TILE_SIZE * 1.25)), ARROW_WIDTH)
    arrow.set_colorkey((0, 0, 0))
    return arrow


def update_blobs():
    global blob_movements

    for from_ in blob_movements.keys():
        grid[from_[0]][from_[1]][1] -= MOVEMENT_COST
        if grid[from_[0]][from_[1]][1] > 0:
            for to in blob_movements[from_].keys():
                grid[from_[0]][from_[1]][1] -= blob_movements[from_][to]
                if grid[from_[0]][from_[1]][1] == 0:
                    grid[from_[0]][from_[1]][0] = GROUND
                grid[to[0]][to[1]][1] += blob_movements[from_][to]
                grid[to[0]][to[1]][0] = turn
        else:
            grid[from_[0]][from_[1]][0] = GROUND

    blob_movements = {}


def update_bacterias_mushrooms():
    for x in range(TILE_NUMBER_X):
        for y in range(TILE_NUMBER_Y):
            if grid[x][y][0] == BACTERIA:
                grid[x][y][1] += BACTERIA_GROWTH

            elif grid[x][y][0] == MUSHROOMS:
                grid[x][y][1] += MUSHROOMS_GROWTH

    for x in range(TILE_NUMBER_X):
        for y in range(TILE_NUMBER_Y):
            if grid[x][y][0] == BACTERIA and grid[x][y][1] > BACTERIA_REPRODUCTION_THRESHOLD:
                for spawn in (
                        (x - 1, y),
                        (x + 1, y),
                        (x, y - 1),
                        (x, y + 1)
                ):
                    if 0 <= spawn[0] <= TILE_NUMBER_X - 1 and 0 <= spawn[1] <= TILE_NUMBER_Y - 1:
                        if grid[spawn[0]][spawn[1]][0] == GROUND:
                            grid[spawn[0]][spawn[1]][0] = BACTERIA
                            grid[spawn[0]][spawn[1]][1] = BACTERIA_SPAWN_VALUE

            if grid[x][y][0] == MUSHROOMS and grid[x][y][1] > MUSHROOMS_REPRODUCTION_THRESHOLD and not grid[x][y][2]:
                for spawn in (
                        (random.randint(0, TILE_NUMBER_X - 1), random.randint(0, TILE_NUMBER_Y - 1))
                        for _ in range(MUSHROOMS_SPORE_NUMBER)
                ):
                    if grid[spawn[0]][spawn[1]][0] == GROUND:
                        grid[spawn[0]][spawn[1]][0] = MUSHROOMS
                        grid[spawn[0]][spawn[1]][1] = MUSHROOMS_SPAWN_VALUE
                        grid[spawn[0]][spawn[1]].append(False)
                grid[x][y][2] = True


def update_screen():
    for x in range(TILE_NUMBER_X):
        for y in range(TILE_NUMBER_Y):
            color = GROUND_COLOR

            if grid[x][y][1] > MAX_VALUE:
                grid[x][y][1] = MAX_VALUE

            intensity = floor(grid[x][y][1] * 127 / MAX_VALUE + 127)

            if grid[x][y][0] == PLAYER1:
                color = (intensity, intensity, 0)
            elif grid[x][y][0] == PLAYER2:
                color = (intensity, floor(intensity / 2), 0)
            elif grid[x][y][0] == BACTERIA:
                color = (0, intensity, 0)
            elif grid[x][y][0] == MUSHROOMS:
                color = (0, 0, intensity)

            if selected_tile == (x, y):
                tile.fill(SELECTED_TILE_COLOR)
                mini_tile.fill(color)
                tile.blit(mini_tile, ((TILE_SIZE - DUCKS * TILE_SIZE) / 2, (TILE_SIZE - DUCKS * TILE_SIZE) / 2))

            elif selected_tile in (
                    (x + 1, y),
                    (x - 1, y),
                    (x, y + 1),
                    (x, y - 1)
            ):
                tile.fill(DESTINATION_TILE_COLOR)
                mini_tile.fill(color)
                tile.blit(mini_tile, ((TILE_SIZE - DUCKS * TILE_SIZE) / 2, (TILE_SIZE - DUCKS * TILE_SIZE) / 2))

            else:
                tile.fill(color)

            window.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))

    for from_ in blob_movements.keys():
        for to in blob_movements[from_].keys():
            movement = (from_, to)

            arrow = 0
            if movement[0][0] > movement[1][0]:
                arrow = create_arrow("left", blob_movements[from_][to])
            elif movement[0][0] < movement[1][0]:
                arrow = create_arrow("right", blob_movements[from_][to])
            elif movement[0][1] > movement[1][1]:
                arrow = create_arrow("up", blob_movements[from_][to])
            elif movement[0][1] < movement[1][1]:
                arrow = create_arrow("down", blob_movements[from_][to])

            window.blit(arrow, (min(movement[0][0], movement[1][0]) * TILE_SIZE,
                                min(movement[0][1], movement[1][1]) * TILE_SIZE))

    if number_mode:
        for x in range(TILE_NUMBER_X):
            for y in range(TILE_NUMBER_Y):
                number = str(grid[x][y][1])
                if number == "0":
                    continue

                text = font.render(number, False, FONT_COLOR)

                window.blit(text, (x * TILE_SIZE, y * TILE_SIZE))

    pygame.display.update()


def move_blob(from_, to):
    if to in blob_movements.keys():
        if from_ in blob_movements[to].keys():
            blob_movements[to][from_] -= 1
            if blob_movements[to][from_] == 0:
                del blob_movements[to][from_]
            return

    if from_ in blob_movements.keys():
        total_movement = MOVEMENT_COST
        for destination in blob_movements[from_].keys():
            total_movement += blob_movements[from_][destination]

        if total_movement < grid[from_[0]][from_[1]][1]:
            if to in blob_movements[from_].keys():
                blob_movements[from_][to] += 1
            else:
                blob_movements[from_][to] = 1
        else:
            if to in blob_movements[from_].keys():
                del blob_movements[from_][to]
    else:
        blob_movements[from_] = {to: 1}


def check_game_won():
    player1_value = 0
    player2_value = 0
    still_food = False

    for x in range(TILE_NUMBER_X):
        for y in range(TILE_NUMBER_Y):
            if grid[x][y][0] == PLAYER1:
                player1_value += grid[x][y][1]
            elif grid[x][y][0] == PLAYER2:
                player2_value += grid[x][y][1]
            else:
                still_food = still_food or grid[x][y][0] in (BACTERIA, MUSHROOMS)

    if not still_food:
        pygame.quit()
        if player1_value > player2_value:
            print("Player 1 won!")
        elif player2_value > player1_value:
            print("Player 2 won!")
        else:
            print("No one won!")
        input()
        quit()

    if player1_value == 0:
        pygame.quit()
        print("Player 2 won!")
        input()
        quit()

    if player2_value == 0:
        pygame.quit()
        print("Player 1 won!")
        input()
        quit()


update_screen()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()

        elif event.type == MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                clicked_tile = (
                    floor(pygame.mouse.get_pos()[0] / TILE_SIZE), floor(pygame.mouse.get_pos()[1] / TILE_SIZE))

                if clicked_tile in (
                        (selected_tile[0] + 1, selected_tile[1]),
                        (selected_tile[0] - 1, selected_tile[1]),
                        (selected_tile[0], selected_tile[1] + 1),
                        (selected_tile[0], selected_tile[1] - 1)
                ):
                    move_blob(selected_tile, clicked_tile)

                elif grid[clicked_tile[0]][clicked_tile[1]][0] == turn:
                    selected_tile = clicked_tile

                else:
                    selected_tile = UNSELECTED

                update_screen()

        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                selected_tile = UNSELECTED

                update_blobs()
                update_bacterias_mushrooms()
                check_game_won()
                update_screen()

                turn += 1
                if turn == 3:
                    turn = 1

            elif event.key == K_SPACE:
                number_mode = not number_mode
                update_screen()
