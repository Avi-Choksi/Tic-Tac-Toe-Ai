import pygame as pg,sys
from pygame.locals import *
import pygame.gfxdraw
import time
import ai
import asyncio


#initialize global variables
XO = 'x'
winner = None
draw = False
width = 400
height = 400
white = (255, 255, 255)
line_color = (255, 255, 255)
#TicTacToe 3x3 board
TTT = [[None]*3,[None]*3,[None]*3]


#initializing pygame window
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height),0,32)
pg.display.set_caption("Tic Tac Toe")

#loading the images
x_img = pg.image.load('data/image/X1.png')
o_img = pg.image.load('data/image/O1.png')
square = pg.image.load('data/image/square.png')
line = pg.image.load('data/image/Line.png')
line1 = pg.image.load('data/image/Line1.png')
bg = pg.image.load('data/image/EndBox.png')

#resizing images
x_img = pg.transform.scale(x_img, (70,70))
o_img = pg.transform.scale(o_img, (70,70))
square = pg.transform.scale(square, (130,130))
line = pg.transform.scale(line, (10,400))
line1 = pg.transform.scale(line1, (400,10))
bg = pg.transform.scale(bg, (200,100))

def game_opening():
    screen.fill(white)
    
    # Drawing vertical lines
    screen.blit(square,(0,0))
    screen.blit(square,(width/3,0))
    screen.blit(square,(width-130,0))
    screen.blit(square,(0,height/3))
    screen.blit(square,(width/3,height/3))
    screen.blit(square,(width-130,height/3))
    screen.blit(square,(0,height-130))
    screen.blit(square,(width/3,height-130))
    screen.blit(square,(width-130,height-130))
    pg.draw.line(screen,line_color,(width/3,0),(width/3, height),7)
    pg.draw.line(screen,line_color,(width/3*2,0),(width/3*2, height),7)
    # Drawing horizontal lines
    pg.draw.line(screen,line_color,(0,height/3),(width, height/3),7)
    pg.draw.line(screen,line_color,(0,height/3*2),(width, height/3*2),7)

    
    screen.blit(line,(width/3 - 5,0))
    screen.blit(line,(width - 130 - 10,0))
    screen.blit(line1,(0,height/3 - 5))
    screen.blit(line1,(0,height - 130 - 10))
    

def draw_status():
    global draw

    if winner is not None:
        screen.blit(bg, (width/3 - 32,height/3 + 15))
        result = "Player"
        if winner.upper() == 'O':
            result = "AI"
        message = result + " wins!"
        font = pg.font.Font(None, 45)
        text = font.render(message, 1, (255, 255, 255))
        screen.blit(bg, (0, height))
        text_rect = text.get_rect(center=(width/2, height/3 + 65))
        screen.blit(text, text_rect)
        pg.display.update()
    if draw:
        screen.blit(bg, (width/3 - 32,height/3 + 15))
        message = 'Draw!'
        font = pg.font.Font(None, 45)
        text = font.render(message, 1, (255, 255, 255))
        screen.blit(bg, (0, height))
        text_rect = text.get_rect(center=(width/2, height/3 + 65))
        screen.blit(text, text_rect)
        pg.display.update()

def check_win():
    global TTT, winner,draw

    # check for winning rows
    for row in range (0,3):
        if ((TTT [row][0] == TTT[row][1] == TTT[row][2]) and(TTT [row][0] is not None)):
            # this row won
            winner = TTT[row][0]
            pg.draw.line(screen, (250,0,0), (0, (row + 1)*height/3 -height/6),\
                            (width, (row + 1)*height/3 - height/6 ), 4)
            break

    # check for winning columns
    for col in range (0, 3):
        if (TTT[0][col] == TTT[1][col] == TTT[2][col]) and (TTT[0][col] is not None):
            # this column won
            winner = TTT[0][col]
            #draw winning line
            pg.draw.line (screen, (250,0,0),((col + 1)* width/3 - width/6, 0),\
                        ((col + 1)* width/3 - width/6, height), 4)
            break

    # check for diagonal winners
    if (TTT[0][0] == TTT[1][1] == TTT[2][2]) and (TTT[0][0] is not None):
        # game won diagonally left to right
        winner = TTT[0][0]
        pg.draw.line (screen, (250,70,70), (50, 50), (350, 350), 4)
    

    if (TTT[0][2] == TTT[1][1] == TTT[2][0]) and (TTT[0][2] is not None):
        # game won diagonally right to left
        winner = TTT[0][2]
        pg.draw.line (screen, (250,70,70), (350, 50), (50, 350), 4)
    
    if(all([all(row) for row in TTT]) and winner is None ):
        draw = True
    draw_status()


def drawXO(row,col):
    global TTT,XO
    if row==1:
        posx = 32
    if row==2:
        posx = width/3 + 32
    if row==3:
        posx = width - 130 + 32

    if col==1:
        posy = 30
    if col==2:
        posy = height/3 + 30
    if col==3:
        posy = height - 130 + 30
    TTT[row-1][col-1] = XO
    if(XO == 'x'):
        screen.blit(x_img,(posy,posx))
        XO= 'o'
    else:
        screen.blit(o_img,(posy,posx))
        XO= 'x'
    pg.display.update()

    

def userClick():
    #get coordinates of mouse click
    x,y = pg.mouse.get_pos()

    #get column of mouse click (1-3)
    if(x<width/3):
        col = 1
    elif (x<width/3*2):
        col = 2
    elif(x<width):
        col = 3
    else:
        col = None
        
    #get row of mouse click (1-3)
    if(y<height/3):
        row = 1
    elif (y<height/3*2):
        row = 2
    elif(y<height):
        row = 3
    else:
        row = None
    #print(row,col)
    

    if(row and col and TTT[row-1][col-1] is None):
        global XO
        
        #draw the x or o on screen
        drawXO(row,col)
        check_win()
        
        

def reset_game():
    global TTT, winner,XO, draw
    time.sleep(3)
    XO = 'x'
    draw = False
    game_opening()
    winner=None
    TTT = [[None]*3,[None]*3,[None]*3]
    
async def main():   
    global XO
    game_opening()

    # run the game loop forever
    while(True):
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and XO == 'x':
                userClick()
                if(winner or draw):
                    pg.display.update()
                    await asyncio.sleep(0)
                    pygame.event.clear()
                    reset_game()
                    pg.display.update()
                    await asyncio.sleep(0)
                    pygame.event.clear()
                    continue
                pg.display.update()
                await asyncio.sleep(0)
                pygame.event.clear()
            elif XO == 'o':
                state = ""
                j = 0
                for row in TTT:
                    for i in range(3):
                        if i != 0:
                            state += " "
                        if row[i] == None:
                            state += "0"
                        elif row[i] == 'x':
                            state += "1"
                        else:
                            state += "2"
                    if j != 2: 
                        state += ","
                    j += 1

                row, column = ai.getMove(state)
                drawXO(row + 1, column + 1)
                check_win()
                if(winner or draw):
                    pg.display.update()
                    await asyncio.sleep(0)
                    pygame.event.clear()
                    reset_game()
                    pg.display.update()
                    await asyncio.sleep(0)
                    pygame.event.clear()
                    continue
                pg.display.update()
                await asyncio.sleep(0)
                pygame.event.clear()
                
        pg.display.update()
        await asyncio.sleep(0)
        CLOCK.tick(fps)

asyncio.run(main())