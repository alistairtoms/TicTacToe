import pygame
import math


def drawGrid(screen, width, height):

    white = (255, 255, 255)

    pygame.draw.line(screen, white, ((width/3), 0), ((width/3), height), LINE_THICKNESS)
    pygame.draw.line(screen, white, ((2*width/3), 0), ((2*width/3), height), LINE_THICKNESS)

    pygame.draw.line(screen, white, (0, (height/3)), (width, (height/3)), LINE_THICKNESS)
    pygame.draw.line(screen, white, (0, (2*height/3)), (width, (2*height/3)), LINE_THICKNESS)
    return

def drawBoard(screen):

    for x in range(3):
        for y in range(3):
            if grid[y][x] == ai:
                drawX(screen, y, x)
            elif grid[y][x] == human:
                drawO(screen, x, y)

def drawX(screen, xIndex, yIndex):

    white = (255, 255, 255)
    x = yIndex+1
    y = xIndex+1

    pygame.draw.line(screen, white, ((x-1)*(width/3)+BUFFER, ((y-1)*(height/3)+BUFFER)),
        ((x*(width/3)-BUFFER), (y*(height/3)-BUFFER)), LINE_THICKNESS)
    pygame.draw.line(screen, white, ((x-1)*(width/3)+BUFFER, ((y)*(height/3)-BUFFER)),
        ((x*(width/3)-BUFFER), ((y-1)*(height/3)+BUFFER)), LINE_THICKNESS)
    return

def drawO(screen, xIndex, yIndex):

    white = (255, 255, 255)
    x = xIndex+1
    y = yIndex+1

    centre = (math.floor(x*(width/3)-(width/6)), math.floor(y*(width/3)-(width/6)))
    radius = (width/6)-BUFFER
    pygame.draw.circle(screen, white, centre, math.floor(radius), LINE_THICKNESS)

    return

def getIndex():

    position = pygame.mouse.get_pos()
    xIndex = math.floor(position[0]/(width/3))
    yIndex = math.floor(position[1]/(width/3))
    index = (xIndex, yIndex)

    return index

def checkWinner(character):

    #check horizontal

    for y in range(3):
        characterSum = 0
        for x in range(3):
            if grid[x][y] == 0:
                break
            if grid[x][y] == character:
                characterSum += 1
        if characterSum == 3:
            return True

    #check vertical
    for x in range(3):
        characterSum = 0
        for y in range(3):
            if grid[x][y] == 0:
                break
            if grid[x][y] == character:
                characterSum += 1
        if characterSum == 3:
            return True

    #check diagonal 1
    characterSum = 0
    for x in range(3):
        if grid[x][x] == 0:
            break
        if grid[x][x] == character:
            characterSum += 1
    if characterSum == 3:
        return True

    #check diagonal 2
    characterSum = 0
    y = 2
    for x in range(3):
        if grid[x][y] == 0:
            break
        if grid[x][y] == character:
            characterSum += 1
        y -= 1
    if characterSum == 3:
        return True

    return False

def checkDraw():

    if checkWinner(ai) or checkWinner(human):
        return False
    return True

def isMovesLeft():

    for x in range(3):
        for y in range(3):
            if grid[x][y] == 0:
                return True
    return False

def nextMove():

    for y in range(3):
        for x in range(3):
            if grid[x][y] == 0:
                index = (y, x)
                return index

def bestMove():

    bestScore = -math.inf

    for x in range(3):
        for y in range(3):
            #if spot is available
            if grid[x][y] == 0:
                grid[x][y] = ai
                score = minimax(False)
                grid[x][y] = 0

                if (score > bestScore):
                    bestScore = score
                    move = (x, y)

    return move


def minimax(isMaximising):

    if not isMovesLeft():
        if checkDraw():
            return 0
    if checkWinner(ai):
        return 1
    if checkWinner(human):
        return -1

    if isMaximising:
        bestScore = -math.inf
        for x in range(3):
            for y in range(3):
                #check if available
                if grid[x][y] == 0:
                    grid[x][y] = ai
                    score = minimax(False)
                    grid[x][y] = 0
                    if (score > bestScore):
                        bestScore = score
        return bestScore
    else:
        bestScore = math.inf
        for x in range(3):
            for y in range(3):
                #check if available
                if grid[x][y] == 0:
                    grid[x][y] = human
                    score = minimax(True)
                    grid[x][y] = 0
                    if (score < bestScore):
                        bestScore = score
        return bestScore


# constants
size = width, height = 600, 600
LINE_THICKNESS = 5
BUFFER = 30
black = (0, 0, 0)
human = 'O'
ai = 'X'

pygame.init()

# draw grid
screen = pygame.display.set_mode(size)
screen.fill(black)
drawGrid(screen, width, height)

#initialise
player = True
run = True
grid = [[0,0,0],
        [0,0,0],
        [0,0,0]]


while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if player:
        if pygame.mouse.get_pressed()[0]:

            index = getIndex()
            x = index[0]
            y = index[1]

            if (grid[y][x] == 0):
                grid[y][x] = human
                drawBoard(screen)

                if checkWinner(human):
                    print("Player Wins")
                player = False

    if not isMovesLeft():
        if checkDraw():
            print("Draw")

    elif not player:

        index = bestMove()
        x = index[0]
        y = index[1]

        grid[x][y] = ai
        drawBoard(screen)

        if checkWinner(ai):
            print("Computer Wins")
        player = True

    pygame.display.flip()
