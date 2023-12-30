import pygame
from pygame.locals import *

# make piece class
class Piece:
    def __init__(self,player):
        self.player = player
        self.name = ""
        
    def set_piece_img(self):
        self.piece_img = pygame.image.load(f"pieces/{self.player}_{self.name}.png")
        return self.piece_img

    def move_piece(self):
        pass

    def draw_piece(self,screen):      
        screen.blit(self.piece_img,(20,50))

class King(Piece):
    def __init__(self,player):
        super().__init__(player)
        self.name = "king"
        self.value = 100
        self.piece_img = self.set_piece_img()

class Queen(Piece):
    def __init__(self,player):
        super().__init__(player)
        self.name = "queen"
        self.value = 9
        self.piece_img = self.set_piece_img()

class Rook(Piece):
    def __init__(self,player):
        super().__init__(player)
        self.name = "rook"
        self.value = 5
        self.piece_img = self.set_piece_img()

class Bishop(Piece):
    def __init__(self,player):
        super().__init__(player)
        self.name = "bishop"
        self.value = 3
        self.piece_img = self.set_piece_img()

class Knight(Piece):
    def __init__(self,player):
        super().__init__(player)
        self.name = "knight"
        self.value = 3
        self.piece_img = self.set_piece_img()

class Pawn(Piece):
    def __init__(self,player):
        super().__init__(player)
        self.name = "pawn"
        self.value = 1 
        self.piece_img = self.set_piece_img()

# make board class
class Board:
    def __init__(self):
        pass
    def draw_screen():
        pass

def main():
    board = Board()
    pawn = Pawn("black")
    print(pawn.player)
    screen = pygame.display.set_mode((1280,720))
    # draw window
    pygame.init()
    running = True 
    while running:          
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False
        
        screen.fill('white')
        pawn.draw_piece(screen)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()