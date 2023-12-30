import pygame
from pygame.locals import *
import numpy as np

# make piece class
class Piece:
    def __init__(self,player,location):
        self.player = player
        self.location = location
        self.name = ""
        self.location_number = self.location_tuple()
        print(self.location_number)

    def location_tuple(self):
        column_dict = {"a": 0, "b": 1, "c": 2, "d":3, "e": 4, "f": 5, "g": 6, "h": 7}
        column = column_dict[self.location[0]]
        row = int(self.location[1]) - 1 
        return (column, row)

    def set_piece_img(self):
        self.piece_img = pygame.image.load(f"pieces/{self.player}_{self.name}.png")
        return self.piece_img

    def move_piece(self):
        pass

    def draw_piece(self,screen):      
        screen.blit(self.piece_img,(20,50))

class King(Piece):
    def __init__(self,player,location):
        super().__init__(player,location)
        self.name = "king"
        self.value = 100
        self.piece_img = self.set_piece_img()

class Queen(Piece):
    def __init__(self,player,location):
        super().__init__(player,location)
        self.name = "queen"
        self.value = 9
        self.piece_img = self.set_piece_img()

class Rook(Piece):
    def __init__(self,player,location):
        super().__init__(player,location)
        self.name = "rook"
        self.value = 5
        self.piece_img = self.set_piece_img()

class Bishop(Piece):
    def __init__(self,player,location):
        super().__init__(player,location)
        self.name = "bishop"
        self.value = 3
        self.piece_img = self.set_piece_img()

class Knight(Piece):
    def __init__(self,player,location):
        super().__init__(player,location)
        self.name = "knight"
        self.value = 3
        self.piece_img = self.set_piece_img()

class Pawn(Piece):
    def __init__(self,player,location):
        super().__init__(player,location)
        self.name = "pawn"
        self.value = 1 
        self.piece_img = self.set_piece_img()

# make board class
class Board:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280,720))
        self.rects = np.zeros([9,9,2])
        for i in range(9):
            for k in range(9):
                self.rects[i][k][0] = 340.+i*75.
                self.rects[i][k][1] = 60.+k*75.
    
    def draw_screen(self):
        self.screen.fill('gray') #background color
        pygame.draw.rect(self.screen, 'white', [340, 60, 600, 600], 0) #set stage
        for i in range(7):    
            pygame.draw.line(self.screen,'black',[340+75*(i+1),60],[340+75*(i+1),660],2)
            pygame.draw.line(self.screen,'black',[340,60+75*(i+1)],[940,60+75*(i+1)],2)

def main():
    board = Board()
    pawn = Pawn("black",("b1"))
    print(pawn.player)

    # draw window
    pygame.init()
    running = True 
    while running:          
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False
        
        board.draw_screen()
        pawn.draw_piece(board.screen)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()