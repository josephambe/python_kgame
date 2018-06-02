#
# NWEN 241 Programming Assignment 5
# kgame.py Python Source File
#
# Name:
# Student ID:
#
# IMPORTANT: Implement the functions specified in kgame.h here.
# You are free to implement additional functions that are not specified in kgame.h here.
#

import random
import time

# This is the title of the game
KGAME_TITLE = "The K-Game (Python Edition)"

# This is the file name of the saved game state
KGAME_SAVE_FILE = "kgame.sav"

# Number of tiles per side
KGAME_SIDES = 4

# Output buffer size in bytess
KGAME_OUTPUT_BUFLEN = ((18 * 40) + 1)

# Arrow keys
dirs = {'UP': 1, 'DOWN': 2, 'LEFT': 3, 'RIGHT': 4}

# Keys accepted by game
inputs = {'LOAD': 5, 'SAVE': 6, 'EXIT': 7}


def kgame_init(game):
    game['score'] = 0
    game['board'] = [[' ' for row in range(KGAME_SIDES)] for col in range(KGAME_SIDES)]
    kgame_add_random_tile(game)


def kgame_add_random_tile(game):

    # 1.Find empty spaces
    emptyCells = []  # list of dictionaries
    cell = {}  # dictionary
    for row in range(0, KGAME_SIDES):
        for col in range(0, KGAME_SIDES):
            if game['board'][row][col] == ' ':
                cell['row'] = row
                cell['col'] = col
                emptyCells.append(cell)
                cell = {}

    # 2.Choose random empty space
    random.shuffle(emptyCells)

    if not emptyCells:
        return

    # 3. Place 'A' or 'B' at a random empty cell
    game['board'][emptyCells[0]["row"]][emptyCells[0]["col"]] = 'A'
    if random.randint(0, 1) == 1:
        game['board'][emptyCells[0]["row"]][emptyCells[0]["col"]] = 'B'


def kgame_render(game):
    # (task 1)

    output_buffer = 'Score: ' + str(game['score']) + '\n+---+---+---+---+\n|'

    for row in range(0, KGAME_SIDES):
        for col in range(0, KGAME_SIDES):
            output_buffer += ' %c |' % game['board'][row][col]
        output_buffer += '\n+---+---+---+---+\n'
        if row != KGAME_SIDES - 1:
            output_buffer += '|'

    return output_buffer


def kgame_is_won(game):
    # (task 2)

    if kgame_is_move_possible(game) == False:
        return False

    for row in range(0, KGAME_SIDES):
        for col in range(0, KGAME_SIDES):
            if game['board'][row][col] == 'K':
                return True;

    return False


def kgame_is_move_possible(game):
    # FIXME: Implement correctly (task 3)

    # checks to see if there is an empty tile
    for col in range(0, KGAME_SIDES):
        for row in range(0, KGAME_SIDES):
            if game['board'][row][col] == ' ':
                return True;

    for col in range(0, KGAME_SIDES - 1):
        for row in range(0, KGAME_SIDES - 1):
            if game['board'][row][col] == game['board'][row + 1][col] or game['board'][row][col] == game['board'][row][col + 1]:
                return True;

    return False;


def kgame_score(game):
    game['score'] = 0

    for row in range(0, KGAME_SIDES):
        for col in range(0, KGAME_SIDES):
            if game['board'][row][col] != ' ':
                game['score'] += pow(ord(game['board'][row][col]) - 64, 2)


def remove_whiteSpaces(game, row, direction):

    # Find free cell closest to the side in that direction
    if direction == dirs['LEFT']:
        currentLeftFree = 0
        for col in range(0, KGAME_SIDES):
            if game['board'][row][col] != ' ':
                currentLeftFree += 1
            else:
                break

        for col in range(currentLeftFree + 1, KGAME_SIDES):

                if game['board'][row][col] != ' ' and game['board'][row][currentLeftFree] == ' ':
                    game['board'][row][currentLeftFree] = game['board'][row][col]
                    game['board'][row][col] = ' '
                    currentLeftFree += 1

    elif direction == dirs['RIGHT']:
        currentRightFree = KGAME_SIDES-1
        for col in range(KGAME_SIDES-1, -1, -1):
            if game['board'][row][col] != ' ':
                currentRightFree -= 1
            else:
                break

        for col in range(currentRightFree, -1, -1):

            if game['board'][row][col] != ' ' and game['board'][row][currentRightFree] == ' ':
                game['board'][row][currentRightFree] = game['board'][row][col]
                game['board'][row][col] = ' '
                currentRightFree -= 1

    elif direction == dirs['UP']:

        currentRowFree = 0
        for col in range(0, KGAME_SIDES):
            if game['board'][col][row] != ' ':
                currentRowFree += 1
            else:
                break

        for col in range(currentRowFree + 1, KGAME_SIDES):

            if game['board'][col][row] != ' ' and game['board'][currentRowFree][row] == ' ':
                game['board'][currentRowFree][row] = game['board'][col][row]
                game['board'][col][row] = ' '
                currentRowFree += 1

    elif direction == dirs['DOWN']:

        currentDownFree = KGAME_SIDES-1
        for col in range(KGAME_SIDES-1, -1, -1):
            if game['board'][col][row] != ' ':
                currentDownFree -= 1
            else:
                break

        for col in range(currentDownFree, -1, -1):

            if game['board'][col][row] != ' ' and game['board'][currentDownFree][row] == ' ':
                game['board'][currentDownFree][row] = game['board'][col][row]
                game['board'][col][row] = ' '
                currentDownFree -= 1

    return game


def kgame_update(game, direction):
    # FIXME: Implement correctly (task 4)
    changed = True;

    if direction == dirs['LEFT']:
        for row in range(0, KGAME_SIDES):

            game = remove_whiteSpaces(game, row, dirs['LEFT'])

            #Merge same cells in a row
            for col in range(0, KGAME_SIDES - 1):
                if game['board'][row][col] == game['board'][row][col + 1] and game['board'][row][col] != ' ':
                    game['board'][row][col] = chr(ord(game['board'][row][col]) + 1)
                    game['board'][row][col + 1] = ' '
                    changed = True
                    break

            game = remove_whiteSpaces(game, row, dirs['LEFT'])


    if direction == dirs['RIGHT']:

        for row in range(0, KGAME_SIDES):

            game = remove_whiteSpaces(game, row, dirs['RIGHT'])

            #Merge same cells in a row
            for col in range(KGAME_SIDES-1, 0, -1):
                if game['board'][row][col] == game['board'][row][col - 1] and game['board'][row][col] != ' ':
                    game['board'][row][col] = chr(ord(game['board'][row][col]) + 1)
                    game['board'][row][col - 1] = ' '
                    changed = True
                    break

            game = remove_whiteSpaces(game, row, dirs['RIGHT'])


    if direction == dirs['UP']:

        for col in range(0, KGAME_SIDES):

            game = remove_whiteSpaces(game, col, dirs['UP'])

            # Merge same cells in a row
            for row in range(KGAME_SIDES-1, 0, -1):
                if game['board'][row][col] == game['board'][row-1][col] and game['board'][row-1][col] != ' ':
                    game['board'][row-1][col] = chr(ord(game['board'][row-1][col]) + 1)
                    game['board'][row][col] = ' '
                    changed = True
                    break

            game = remove_whiteSpaces(game, col, dirs['UP'])


    if direction == dirs['DOWN']:

        for col in range(0, KGAME_SIDES):

            game = remove_whiteSpaces(game, col, dirs['DOWN'])

            # Merge same cells in a row
            for row in range(0, KGAME_SIDES-1):
                if game['board'][row][col] == game['board'][row+1][col] and game['board'][row+1][col] != ' ':
                    game['board'][row+1][col] = chr(ord(game['board'][row+1][col]) + 1)
                    game['board'][row][col] = ' '
                    changed = True
                    break

            game = remove_whiteSpaces(game, col, dirs['DOWN'])

    kgame_add_random_tile(game)
    kgame_score(game)
    kgame_render(game)
    return changed;


def kgame_save(game):
    # FIXME: Implement correctly (task 5)
    pass


def kgame_load(game):
    # FIXME: Implement correctly (task 6)
    pass
