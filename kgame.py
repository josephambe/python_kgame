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
KGAME_OUTPUT_BUFLEN = ((18*40)+1)

# Arrow keys
dirs = { 'UP': 1, 'DOWN': 2, 'LEFT': 3, 'RIGHT': 4 }

# Keys accepted by game
inputs = { 'LOAD': 5, 'SAVE': 6, 'EXIT': 7}


def kgame_init(game):
    game['score'] = 0
    game['board'] = [[' ' for row in range(KGAME_SIDES)] for col in range(KGAME_SIDES)]
    kgame_add_random_tile(game)


def kgame_add_random_tile(game):
    # find random, but empty tile
    # FIXME: will go to infinite loop if no empty tile
    if kgame_is_move_possible(game) == False:
        return
    
    row = random.randint(0, KGAME_SIDES-1)
    col = random.randint(0, KGAME_SIDES-1)
    
    while game['board'][row][col] != ' ':
        row = random.randint(0, KGAME_SIDES-1)
        col = random.randint(0, KGAME_SIDES-1)


    # place to the random position 'A' or 'B' tile
    game['board'][row][col] = 'A'
    if random.randint(0, 2) == 1:
        game['board'][row][col] = 'B'


def kgame_render(game):
    # (task 1)

    bufferPosition = 0
    output_buffer = 'Score: '+ str(game['score']) + '\n+---+---+---+---+\n|'
    bufferPosition += len(output_buffer)

    for row in range(0, KGAME_SIDES):
     for col in range(0, KGAME_SIDES):
         output_buffer += ' %c |' %game['board'][row][col]
         bufferPosition += len(output_buffer)

     output_buffer += '\n+---+---+---+---+\n'
     bufferPosition += len(output_buffer)
     if row != KGAME_SIDES-1:
         output_buffer += '|'
         bufferPosition += len(output_buffer)


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

    #checks to see if there is an empty tile
    for col in range(0, KGAME_SIDES):
     for row in range(0, KGAME_SIDES):
         if game['board'][row][col] == ' ':
             return True;

    for col in range(0, KGAME_SIDES-1):
     for row in range(0, KGAME_SIDES-1):
         if game['board'][row][col] == game['board'][row+1][col] or game['board'][row][col] == game['board'][row][col+1]:
             return True;


    return False;


def kgame_score(game):
    game['score'] = 0
##    a = "game['board'][row][col]"
##    float(a)
##    
##    for row in range(0, KGAME_SIDES):
##     for col in range(0, KGAME_SIDES):
##         if game['board'][row][col] == ' ':
##            game['score'] += pow(float(int(a))-64,2)




def kgame_update(game, direction):
    
    # FIXME: Implement correctly (task 4)
    changed = False;

    if direction == dirs['LEFT']:
        if kgame_is_move_possible(game) == False:
            kgame_add_random_tile(game)
            return
    
        for row in range(0, KGAME_SIDES):

         currentLeftFree = 0
         for col in range(0, KGAME_SIDES):
             if game['board'][row][col] != ' ':
                 currentLeftFree += 1
             else:
                 break
                
         for col in range(currentLeftFree+1, KGAME_SIDES):
                if game['board'][row][col] != ' ' and game['board'][row][currentLeftFree] == ' ':
                    game['board'][row][currentLeftFree] = game['board'][row][col]
                    game['board'][row][col] = ' '
                    changed = True
                    currentLeftFree += 1
                    
    
##         for col in range(0, KGAME_SIDES-1):
##            for nextCol in range(col+1, KGAME_SIDES):
##                if game['board'][row][col] == game['board'][row][nextCol] and game['board'][row][col] != ' ':
##                   game['board'][row][nextCol] = chr(ord(game['board'][row][nextCol])+1)
##                   game['board'][row][col] = ' '
##                   changed = True
##                   break
##                elif game['board'][row][nextCol] != ' ':
##                   break
                    
    
    
    if direction == dirs['RIGHT']:
    
        for row in range(0, KGAME_SIDES):
         for col in range(0, KGAME_SIDES):
            for nextCol in range(col+1, KGAME_SIDES):
                if game['board'][row][col] != ' ' and game['board'][row][nextCol] == ' ':
                    game['board'][row][nextCol] == game['board'][row][col]
                    game['board'][row][col] == ' '
                    changed = True
                    break
                elif game['board'][row][col] != ' ':
                    break
    
         for col in range(0, KGAME_SIDES-1):
            for nextCol in range(col+1, KGAME_SIDES):
                if game['board'][row][col] == game['board'][row][nextCol] and game['board'][row][col] != ' ':
                   game['board'][row][nextCol] = chr(ord(game['board'][row][nextCol])+1)
                   game['board'][row][col] = ' '
                   changed = True
                   break
                elif game['board'][row][nextCol] != ' ':
                   break
    
    
    if direction == dirs['UP']:
    
        for row in range(0, KGAME_SIDES):
         for col in range(0, KGAME_SIDES):
            for nextRow in range(row+1, KGAME_SIDES):
                if game['board'][row][col] == ' ' and game['board'][nextRow][col] != ' ':
                   game['board'][row][col] = game['board'][nextRow][col]
                   game['board'][nextRow][col] = ' '
                   changed = True
                   break
                elif game['board'][row][col] != ' ':
                   break;
    
        for col in range(0, KGAME_SIDES):
            for nextRow in range(row+1, KGAME_SIDES):
                if game['board'][row][col] == game['board'][nextRow][col] and game['board'][row][col] != ' ':
                   game['board'][row][col] = chr(ord(game['board'][row][col])+1)
                   game['board'][nextRow][col] = ' '
                   changed = True
                   break
                elif game['board'][nextRow][col] != ' ':
                   break
    
    
    if direction == dirs['DOWN']:
        
        for col in range(0, KGAME_SIDES):
         for row in range(KGAME_SIDES-1, 0, -1):
            for nextRow in range(row-1, 0, -1):
                if game['board'][row][col] == ' ' and game['board'][nextRow][col] != ' ':
                   game['board'][row][col] = game['board'][nextRow][col]
                   game['board'][nextRow][col] = ' '
                   changed = True
                   break
                elif game['board'][row][col] != ' ':
                   break;
    
        for row in range(KGAME_SIDES-1, 0, -1):
            for nextRow in range(row-1, 0, -1):
                if game['board'][row][col] == game['board'][nextRow][col] and game['board'][row][col] != ' ':
                   game['board'][row][col] = chr(ord(game['board'][row][col])+1)
                   game['board'][nextRow][col] = ' '
                   changed = True
                   break
                elif game['board'][nextRow][col] != ' ':
                   break

                
    kgame_add_random_tile(game)
    kgame_score(game)
    return changed;


def kgame_save(game):
    # FIXME: Implement correctly (task 5)
    pass


def kgame_load(game):
    # FIXME: Implement correctly (task 6)
    pass




