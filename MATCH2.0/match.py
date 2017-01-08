import pygame
from pygame.locals import *
pygame.init()

import random
import easygui

#SPRITES
class Card(pygame.sprite.Sprite):
    '''A class that is a Sprite object and models playing cards with properties for the images of each side, a flipped property, rect position coordinate, and a ID number property.'''
    
    def __init__(self, num_1, img_1, img_2, flipped, num_2):
        '''Create a Card that is a Sprite with rect coordinate(num_1), front image(img_1), back image(img_2), what side its flipped on(flipped), and its ID number(num_2).'''
        pygame.sprite.Sprite.__init__(self)
        
        self.img_1 = pygame.image.load(img_1).convert()
        self.img_2 = pygame.image.load(img_2).convert()
        
        self.image = self.img_1
        
        self.rect = self.image.get_rect()
        self.rect.topleft = num_1
        
        self.flipped = flipped
        self.num = num_2
        
    def set_flip(self):
        '''C.set_flip()
        Set this card's flip property.'''        
        if self.flipped == True:
            self.flipped = False
        else:
            self.flipped = True
        
    def update(self):
        '''C.update()
        Update this Card so that it is showing its front(False) or back(True) image.'''        
        if self.flipped == True:
            self.image = self.img_2
        else:
            self.image = self.img_1

class Moves(pygame.sprite.Sprite):
    '''A class that is a Sprite object and models a tally that keeps the number of Moves with properties for the number of moves and the rect's top left corner.'''
    
    def __init__(self, score, num):
        '''Create a number of Moves keeper that is a Sprite with rect coordinate(num_1), and the beginning score (score).'''
        pygame.sprite.Sprite.__init__(self) 
        self.score = score
        
        self.my_font = pygame.font.SysFont("impact", 40)
        self.image = self.my_font.render("Number of Moves: {}".format(self.score), True, (0, 0, 0))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = num
    
    def update(self, moves, done, size):
        '''M.update()
        Update the number of Moves.'''         
        self.moves = moves
        self.image = self.my_font.render("Number of Moves: {}".format(self.moves), True, (0, 0, 0)) 
        
        #moves the number of moves sprite to the center at the end of the game
        if done == True:
            self.rect.center = (size[0]//2, size[1]//2)
    
class Square(pygame.sprite.Sprite):
    '''A class that is a Sprite object and models a Square.'''
    
    def __init__(self, speed):
        '''Create a Square that is a Sprite.'''
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((7, 7)).convert()
        self.image.fill((random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256)))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randrange(0, 516), random.randrange(-500, 500))
        
        self.speed = speed
        
    def update(self): 
        '''S.update()
        Update this Square so that it moves vertically downwards.'''         
        self.rect.move_ip(0, self.speed)
        
class Takeback(pygame.sprite.Sprite):
    '''A class that is a Sprite object and models a cheat option where the player can lower their score by one.'''
    
    def __init__(self, pos):
        '''Create a Takeback (check mark) that is a Sprite.'''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("check_mark.jpg").convert()
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos)
              
#GAME DIFFICULTY      
inp = easygui.buttonbox("Choose a Game Size:", "Fruit Match", ["easy", "medium", "hard"])

if inp == "easy":
    #determines the number of pairs in each game
    pairs = 4
    #determines the number in each colomn
    col = 2
    #size of the screen
    size = (516, 295)
    #position of the number of moves keeper
    moves_pos = (20, 248)

elif inp == "medium":
    pairs = 6
    col = 3
    size = (516, 420)
    moves_pos = (20, 369)

else:
    pairs = 8
    col = 4
    size = (516, 545)
    moves_pos = (20, 498)

#CARDS  
imgs = []
number = []

#uploading the cards
for n in range(0, pairs):
    for i in range(0, 2):
        imgs.append("fruit_{}.jpg".format(n+1)) 

screen = pygame.display.set_mode(size)

cards = []
for a in range(col):
    for b in range(4):
        #randomizing the position of the cards
        num = random.randrange(0, (len(imgs)))
        img = imgs[num]
        
        card = Card((124*b + 20, 124*a + 20), "picnic.jpg", img, False, int(img[-5]))
        
        cards.append(card)
        imgs.remove(img)
        #in order to make sure that there are a random assortment of cards, while preserving the pairs
        
card_group = pygame.sprite.Group(cards)

#BACKGROUND
background = pygame.Surface(screen.get_size()).convert()
background.fill((255, 255, 255))
screen.blit(background, (0, 0))        

#SOUNDS
flip = pygame.mixer.Sound("flip.wav")
flip.set_volume(1.0)

match = pygame.mixer.Sound("match_1.wav")
match.set_volume(1.0)

congrats = pygame.mixer.Sound("congrats.wav")
congrats.set_volume(1.0)

#FONT
moves = 0
moves_group = pygame.sprite.Group(Moves(moves, moves_pos))

#SQUARES
squares = []
speed = 5
for n in range(500):
    squares.append(Square(speed))
square_group = pygame.sprite.Group(squares)

#TAKEBACK
takeback = Takeback((450, moves_pos[1]+15))
takeback_group = pygame.sprite.Group(takeback)

#GAME LOOP
clock = pygame.time.Clock()
keepGoing = True

cards_flipped = []
counter_1 = 0
counter_2 = 1
done = False

while keepGoing:
    clock.tick(30)
    
    pygame.display.set_caption("Fruit Match")
    
    #MATCH CONDITIONS
    if counter_1 == 5:
        #to test if the two cards match compare their self.num values
        if cards_flipped[0].num != cards_flipped[1].num:
            #if they don't match flip them over and clear the list
            for n in cards_flipped:
                n.set_flip()
            cards_flipped = [] 
            
        elif cards_flipped[0].num == cards_flipped[1].num:
            #if they match remove the cards
            if len(card_group) != 2:
                #doesn't play the music if it is the last pair, just plays the ending music
                match.play()
            card_group.remove(cards_flipped)
        
        #to keep track of number of moves        
        moves += 1
        cards_flipped = []     
    
    #EVENT HANDLING
    elif counter_1 == 0:            
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                keepGoing = False
                
            elif ev.type == MOUSEBUTTONDOWN:
                x = ev.pos[0]
                y = ev.pos[1]
                
                #if only one card was flipped then flip another
                if len(cards_flipped) < 2:
                    for n in card_group:
                        if n.rect.collidepoint(x, y) == True:
                            #to prevent anything from happening when the user click on the same card
                            if n not in cards_flipped:
                                flip.play()
                                n.set_flip()
                                cards_flipped.append(n)
                            
                            if len(cards_flipped) == 2:
                                counter_1 = 30 
            
            elif ev.type == KEYDOWN:
                #cheat: take back a move
                if ev.key == K_SPACE:
                    if moves != 0:
                        #to restrict the number of takebacks to one
                        if len(takeback_group) == 1:
                            moves -= 1
                            takeback_group.remove(takeback)
    
    #counter to delay the flipping of the cards
    if counter_1 > 0:
        counter_1 -= 1
    
    #counter to delay the game from closing at the end    
    if counter_2 < 0:
        counter_2 += 1
    elif counter_2 == 0:
        keepGoing = False
    
    #detect when there are no cards left and to start the counter              
    if len(card_group) == 0:
        #make sure it doesn't play the sound or start the counter twice
        if done != True:
            counter_2 = -100
            congrats.play()
            takeback_group.remove(takeback)
            done = True
    
    #CLEAR/UPDATE/DRAW SPRITE GROUPS
    #animation only starts if the game is over
    if done == True:
        square_group.clear(screen, background)
        square_group.update()
        square_group.draw(screen) 
        
    card_group.clear(screen, background) 
    moves_group.clear(screen, background) 
    takeback_group.clear(screen, background)

    card_group.update()
    moves_group.update(moves, done, size)
    takeback_group.update()

    card_group.draw(screen) 
    moves_group.draw(screen)
    takeback_group.draw(screen)
    
    pygame.display.flip()      