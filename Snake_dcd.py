#!/usr/bin/python3
"""
Making a python snake game using pygame

We will start with a playingfield of 15 by 15.
every 32 game ticks a foodpoint will appear, which allows the snake to grow.
If the food is not eaten, it goes bad, and after 38 gameticks it vanishes.
The snake will start in the middle, and dies if it runs into itself or the wall.
Or if it starves to death, losing a segment every 42 gameticks.


The snake will be a list, or an array or an dictionary.



TODO:
    - define playfield
        - 16 x 16, tiles will have a 5 px padding and be 20 px large.
        - no wrap around
    - model snake as object
        - get user input to direct the snake.
        - move player
            - get inputs from keyboard
        - detect if entering allowed area
"""
#%% imports
import sys
import pygame
import copy
from random import randint

#%% Defaults
#%%% colours
WHT = (255,255,255)
BLK = (0,0,0)
GRY = (100,100,100)
RED = (255,0,0)
GRN = (0,255,0)
BLU = (0,0,255)
YEL = (255,255,0)
MGN = (255,0,255)
CYA = (0,255,255)

#%% settings
BOARD_X = 20
BOARD_Y = 20
Window_Width = 480
Window_Height = 480
Window_Width = 30 * BOARD_X
Window_Height = 30 * BOARD_Y
Background = WHT
Tictime = 200
Food_spawn = 32
Food_spoil = 8
Starve_tic = 40

#%% control dictionarys
"""direction to add [x,y]"""
compass={"N":[0,-1],
         "E":[1,0],
         "S":[0,1],
         "W":[-1,0]}
ijkl={pygame.K_i:'N',pygame.K_j:'W',pygame.K_k:'S',pygame.K_l:'E'}
wasd={pygame.K_w:'N',pygame.K_a:'W',pygame.K_s:'S',pygame.K_d:'E'}
updown={pygame.K_UP:'N',pygame.K_LEFT:'W',pygame.K_DOWN:'S',pygame.K_RIGHT:'E'}
colour={0:GRY,1:GRN, 2:CYA}
#%% classes
class Player:
    """
    The player is a snake, with a head which moves along all the squares.
    Each game tick, there is a movement.
    """
    def __init__(self,pose = None,dir = None, colour = None, cset = None):
        self.pose=pose
        self.dir = dir
        self.colour=colour
        self.cset=cset
        self.number=len(players)+1
        if colour == None:
            self.colour = RED
        if pose == None:
            pose = [8,8]
        if dir == None:
            self.dir = "N"
        if self.cset == None:
            self.cset = updown
        self.length = 0
        self.body = [[self.length,pose]] #body with just the head
        self.grow = 1  #grow at the first step
        print(f'player {self.number} initialised: {self.body}, GR: {self.grow}, dir: {self.dir}')

    def dokey(self,event):
        if event.key in player.cset:
            print(f'Probeer dit eens: {player.cset[event.key]}')
            print(f'origineel: {player.dir}')
            player.dir = player.cset[event.key]
            print(f'ori nieuw: {player.dir}')

    def move(self):
        #print(f'we move')
        temp = copy.deepcopy(self.body)
        goalx=self.body[0][1][0]+compass[self.dir][0]
        goaly=self.body[0][1][1]+compass[self.dir][1]
        test = -1
        while test == -1 or test >9:#look for a valid direction
            goalx=self.body[0][1][0]+compass[self.dir][0]
            goaly=self.body[0][1][1]+compass[self.dir][1]
            #print(f'testing for: {goalx, goaly}')
            test=check(board,goalx,goaly)
            says = 'OK' if test ==0 else 'NO!'
            #print(f'computer says: {says}')
            'right bottom left top'
            if test ==10:
                self.dir='S'
            if test ==11:
                self.dir='W'
            if test ==12:
                self.dir='N'
            if test ==13:
                self.dir='E'
        #now we could move
        if test == -1:
            self.die()
        if test == 1:
            self.grow = 1
        if test == 2 or board.tick%Starve_tic ==0:
            self.grow = -1
        self.body[0][1][0]+=compass[self.dir][0]
        self.body[0][1][1]+=compass[self.dir][1]
        self.body[0][0]=len(self.body)
        for element in range(len(temp)):
            if element == 0:
                continue
            self.body[element]=temp[element-1]
        if self.grow == 1:
            print(f'Player {self.number} grows')
            self.body.append(temp[-1])
            self.body[-1][0]=self.body[-2][0]+1
            print(f'new segment for player {player.number}: {self.body}')
            self.grow = 0
        if self.grow == -1:
            print(f'player {player.number} shrinks')
            self.body.pop() # remove last segment from the list
            self.grow = 0
        print(f'Player {player.number} has length: {len(self.body)}')
        if len(self.body)==0:
            self.die()
    def die(self):
        print(f'player {self.number} died!')
        quitgame()
    def show(self):
        #print(f'showing this player {self.body}')
        for seg,element in enumerate(self.body):
            #print(f'this segment: {seg} at :{element[1][0]},{element[1][1]}')
            row = element[1][0]
            square = element[1][1]
            #print(f'r,s: {row},{square}')
            part = pygame.Rect(row*30+5,square*30+5,20,20)
            #print(f'that part: {part}{self.colour}')
            pygame.draw.rect(screen,MGN,part)
            if seg == 0:
                head = pygame.Rect(row*30+5,square*30+5,20,20)
                #print(f'if it is a head: {head}{self.colour}')
                pygame.draw.rect(screen,self.colour,head)
            pygame.display.update()

class Board:
    def __init__(self):
        self.tick = 0
        self.xmax = BOARD_X
        self.ymax = BOARD_Y
        tiles=[[] for i in range(BOARD_X)]  # tiles is a list of lists
                                            # Effectively it is just a matrix
                                            # There are probably easier ways
                                            # to implement this
        #print(f'these rows\n{tiles}')
        for row in range(len(tiles)):
            tiles[row]=[square for square in range(BOARD_Y)]
        #print(f'een tegel: {tiles[0][5]}')
        self.tiles= tiles
        #self.gift = tiles #python points to the same thing.. bad idea
        self.gift = copy.deepcopy(self.tiles)

        for row in range(self.xmax):
            for square in range(self.ymax):
                #print(f'this is my position\nrow{row}, square{square},value{self.tiles[row][square]}')
                self.tiles[row][square] = pygame.Rect(row*30+5,square*30+5,20,20)
                self.gift[row][square]=0
    def tile(self,x,y):
        return self.gift[x][y]
    def update(self):
        self.tick+=1
        #print(f'we live at: {self.tick}')
        if self.tick%Food_spawn ==0:
            for i in range(len(players)):
                self.food(randint(0,BOARD_X-1),randint(0,BOARD_Y-1))
            self.poison(randint(0,BOARD_X-1),randint(0,BOARD_Y-1))
    def food(self,x,y):
        self.gift[x][y]=1
    def poison(self,x,y):
        self.gift[x][y]=2
#%%% for the user:
    def show(self):
        #print(f'show board')
        self.update()
        for x,row in enumerate(self.tiles):
            for y,tile in enumerate(row):
                #print(f'this tile {x},{y}: {tile}')
                #print(f'this gift: {self.gift[x][y]}')
                #print(f'this colour: {colour[self.gift[x][y]]}')
                pygame.draw.rect(screen,colour[self.gift[x][y]],tile)
                #pygame.time.delay(1000)
        pygame.display.update()


#%% functions
def check(board,goalx,goaly): #Could be a method, but should work for actors other
                              # than players
    #print(f'looking at {goalx, goaly}')
    if goalx+1 > BOARD_X:
        print(f'You would fall off the right: {goalx}, max={BOARD_X}')
        return 10
    if goaly+1 > BOARD_Y:
        print(f'You would fall off the bottom : {goaly}, max={BOARD_Y}')
        return 11
    if goalx < 0:
        print(f'You would fall off the left {goalx}')
        return 12
    if goaly < 0:
        print(f'You would fall off the top: {goalx}')
        return 13

    if board.gift[goalx][goaly] == 1: #square has food
        board.gift[goalx][goaly] = 0 # food is now eaten
        return 1
    if board.gift[goalx][goaly] == 2: #square has poison
        board.gift[goalx][goaly] = 0 # food is now eaten
        return 2
    # nothing special there:
    return 0

def quitgame():
    print(f'Shutting display')
    pygame.display.quit()
    print(f'Quitting pygame, bye!')
    pygame.quit()
    print(f'Quitting python, bye!')
    sys.exit()

#%% Main
if __name__ == "__main__": # Boilerplate code https://en.wikipedia.org/wiki/Boilerplate_code
                           # in case you want to implement the code
                           # as a module
    print(f'\n{"_-"*20}\n\n\n\n')
#%%% Adminstrative stuff
    pygame.init()
    screen= pygame.display.set_mode((Window_Width,Window_Height))
    screen.fill(Background)
    #screenarea= pygame.Rect(0,0,width,height)
    pygame.font.init()

#%%% more interesting stuff

    board = Board()
    board.food(8,4)
    board.poison(8,2)
    players=[]
    player1 = Player()
    players.append(player1)
    player2 = Player([1,6],'E',cset=wasd)
    players.append(player2)
    #player3 = Player([4,4],'W',cset=ijkl)
    #players.append(player3)

    board.show()
    for player in players:
        player.show()
    run = True
    while run:
        """ This is the game loop """
        pygame.time.delay(Tictime)
        for player in players:
            player.move()
        #board.update()
        board.show() #show the board before the players
        for player in players:
            player.show()

        for event in pygame.event.get():
            #print(f'deze dan: {event}')
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print(f'Escaped!')
                    run = False
                    continue
                for player in players:
                    player.dokey(event)

            if event.type == pygame.QUIT:
                run = False
    """If the loop is done, go back to main menu, or just quit."""
    quitgame()
