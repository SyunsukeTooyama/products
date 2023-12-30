import pygame

# make piece class
class Piece:
    def __init__(self):
        pass
    def move_piece():
        pass
    def draw_piece():
        pass

class King(Piece):
    def __init__(self):
        self.name = "King"
        self.value = 100

class Queen(Piece):
    def __init__(self):
        self.name = "Queen"
        self.value = 9

class Rook(Piece):
    def __init__(self):
        self.name = "Rook"
        self.value = 5

class Bishop(Piece):
    def __init__(self):
        self.name = "Bishop"
        self.value = 3

class Knight(Piece):
    def __init__(self):
        self.name = "Knight"
        self.value = 3

class Pawn(Piece):
    def __init__(self):
        self.name = "Pawn"
        self.value = 1 

# make board class
class Board:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280,720))

    def draw_screen():
        pass


board = Board()

# draw window
pygame.init()
running = True 
while running:          
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
    
    board.screen.fill('gray')

pygame.quit()