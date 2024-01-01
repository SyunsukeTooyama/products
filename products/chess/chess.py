import pygame
from pygame.locals import *
import numpy as np
import string

# make piece class
class Piece:
    def __init__(self,player,location):
        self.player = player
        self.location = location
        self.name = ""
        self.to_num_dict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        self.to_alp_dict = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
        self.location_number = self.location_to_tuple(self.location)
        self.move_value = [(0,0)]

    def location_to_tuple(self, location):        
        column = self.to_num_dict[location[0]]
        row = int(location[1]) - 1 
        return (column, row)

    def tuple_to_location(self, location_tuple):
        column = self.to_alp_dict[location_tuple[0]]
        row = int(location_tuple[1] + 1)

        return f"{column}{row}"

    def set_piece_img(self,piece_size=75):
        self.piece_img = pygame.image.load(f"pieces/{self.player}_{self.name}.png")
        self.piece_img = pygame.transform.scale(self.piece_img, (piece_size, piece_size))
        if self.player == "black":
            self.piece_img = pygame.transform.rotate(self.piece_img, 180)
        
        return self.piece_img

    def value_to_key(self,value):
        for item in self.to_num_dict.items():
            if item[1] == value:
                return item[0]            

    def draw_piece(self, screen):   
        screen.blit(self.piece_img,(340. + self.location_number[0] * 75, 60. + (7-self.location_number[1]) * 75))

    def initialize_size(self):
        self.piece_img = self.set_piece_img()

    def choose_piece(self, board):
        self.initialize_size()
        selected = 0
        result = 0
        places = []
        board.initialize_board_color()
        for i in range(8): 
            for k in range(8):
                if (board.rects[i][k][0] < pygame.mouse.get_pos()[0] < board.rects[i+1][k][0]) and (board.rects[i][k][1] < pygame.mouse.get_pos()[1] < board.rects[i][k+1][1]):
                    if self.location_number == (i, 7 - k):
                        print(f"{self.name} is selected at {self.tuple_to_location((i, 7-k))}")
                        self.piece_img = self.set_piece_img(piece_size = 90)
                        if selected == 0:
                            result = self
                            places = self.get_can_move(board)
                        selected = 1

        return (selected,result, places)

    def move_piece(self, board, places):
        self.initialize_size()
        board.initialize_board_color()
        for i in range(8): 
            for k in range(8):
                if (board.rects[i][k][0] < pygame.mouse.get_pos()[0] < board.rects[i+1][k][0]) and (board.rects[i][k][1] < pygame.mouse.get_pos()[1] < board.rects[i][k+1][1]):
                    if places:
                        location_tuple = (i,7-k)
                        for place in places:
                            if location_tuple == place:
                                self.location_number = place
                                self.draw_piece(board.screen)
                                print(f"{self.name} moves to {self.tuple_to_location(location_tuple)}")
    
    def get_can_move(self, board):
        old_pos = self.location_number
        places = []
        for val in self.move_value:
            if (8 > (old_pos[0] + val[0])) and (8 > (old_pos[1] + val[1])) and ((old_pos[0] + val[0]) >= 0) and ((old_pos[1] + val[1]) >= 0):
                place = (old_pos[0] + val[0], old_pos[1] + val[1])
                places.append(place)
                place_str = self.tuple_to_location(place)
                print(f"{self.name} can move to {place_str}")
        board.color_part(places)
        return places

class King(Piece):
    def __init__(self,player,location):
        super().__init__(player,location)
        self.name = "king"
        self.value = 100
        self.piece_img = self.set_piece_img()
        self.move_value = [(i,j) for i in range(-1,2) for j in range(-1,2)]
        self.move_value.remove((0,0))

class Queen(Piece):
    def __init__(self,player,location):
        super().__init__(player,location)
        self.name = "queen"
        self.value = 9
        self.piece_img = self.set_piece_img()
        self.move_value = [(i,i) for i in range(-8,8)] + [(i,-i) for i in range(-8,8)] + [(i,0) for i in range(-8,8)] + [(0,i) for i in range(-8,8)]
        self.move_value = [val for val in self.move_value if val != (0,0)]

class Rook(Piece):
    def __init__(self,player,location):
        super().__init__(player,location)
        self.name = "rook"
        self.value = 5
        self.piece_img = self.set_piece_img()
        self.move_value = list(range(1,8)) + list(range(-1,-8,-1)) + list(range(8, 64, 8)) + list(range(-8, -64, -8))
        self.move_value = [(i,0) for i in range(-8,8)] + [(0,i) for i in range(-8,8)]
        self.move_value = [val for val in self.move_value if val != (0,0)]

class Bishop(Piece):
    def __init__(self,player,location):
        super().__init__(player,location)
        self.name = "bishop"
        self.value = 3
        self.piece_img = self.set_piece_img()
        self.move_value = list(range(9, 72, 9)) + list(range(-9, -72, -9)) + list(range(7, 56, 7)) + list(range(-7, -56, -7))
        self.move_value = [(i,i) for i in range(-8,8)] + [(i,-i) for i in range(-8,8)]
        self.move_value = [val for val in self.move_value if val != (0,0)]

class Knight(Piece):
    def __init__(self,player,location):
        super().__init__(player,location)
        self.name = "knight"
        self.value = 3
        self.piece_img = self.set_piece_img()
        self.move_value = [(-1,-2),(-2,-1),(2,-1),(-2,1),(-1,2),(1,-2),(1,2),(2,1)]
        self.move_value = [val for val in self.move_value if val != (0,0)]

class Pawn(Piece):
    def __init__(self,player,location):
        super().__init__(player,location)
        self.name = "pawn"
        self.value = 1 
        self.piece_img = self.set_piece_img()
        self.move_value = [7, 8, 9, 16]
        if self.player == "black":
            self.move_value = [(0,-1)]
        else:
            self.move_value = [(0,1)]

# make board class
class Board:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280,720))
        self.rects = np.zeros([9,9,2])
        self.coloring_tuples = []
        for i in range(9):
            for k in range(9):
                self.rects[i][k][0] = 340. + i * 75.
                self.rects[i][k][1] = 60. + k * 75.
    
    def draw_screen(self):
        # background color
        self.screen.fill('gray') 

        # set board
        pygame.draw.rect(self.screen, 'black', [340-1, 60-1, 600+2, 600+2], 1) # set board
        
        # coloring board
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(self.screen, "white", (340 + 75 * i,60 + 75 * j, 75, 75)) 
                else:
                    pygame.draw.rect(self.screen, "brown", (340 + 75 * i,60 + 75 * j, 75, 75)) 
        
        if len(self.coloring_tuples) > 0:
            for coloring_tuple in self.coloring_tuples:
                pygame.draw.rect(self.screen, Color(0,100,200,1), (341 + 75 * coloring_tuple[0], 61 + 75 * coloring_tuple[1], 73, 73))
    
    def color_part(self, location_tuples):
        for location_tuple in location_tuples:
            self.coloring_tuples.append((location_tuple[0],(7 - location_tuple[1])))

    def initialize_board_color(self):
        self.coloring_tuples = []

class Game:
    def __init__(self, turn = 0):
        self.turn = turn
        self.pieces = []

    def initialize_game(self):
        alps = list(string.ascii_lowercase)[0:8]
        for color in ["black","white"]:
            king = []
            queen = []
            rook = []
            bishop = []
            knight = []
            pawn = []

            if color == "black":
                color_sign = +1
            else:
                color_sign = -1

            # pawn
            for alp in alps[0:8]:
                pawn.append(Pawn(color,(f"{alp}{4.5 + 2.5*color_sign}")))

            # knight bishop rook
            for column_num in [-1,+1]:
                knight.append(Knight(color,(f"{alps[int(3.5 + 1.5*column_num)]}{4.5 + 3.5*color_sign}")))
                bishop.append(Bishop(color,(f"{alps[int(3.5 + 2.5*column_num)]}{4.5 + 3.5*color_sign}")))
                rook.append(Rook(color,(f"{alps[int(3.5 + 3.5*column_num)]}{4.5 + 3.5*color_sign}")))

            # queen
            queen.append(Queen(color,(f"d{4.5 + 3.5*color_sign}")))
            
            # king
            king.append(King(color,(f"e{4.5 + 3.5*color_sign}")))

            pieces_dict = {
                "king":king,
                "queen":queen,
                "rook":rook,
                "bishop":bishop,
                "knight":knight,
                "pawn":pawn
            }

            self.pieces.append(pieces_dict)

        return self.pieces
    
    def end_game(self):
        for i in [0,1]:
            if self.pieces[i]["king"]:
                pass
            elif i==0:
                print("white win")
            else:
                print("black win")

    def draw_game(self):
        pass

def main():
    board = Board()
    game = Game()
    pieces = game.initialize_game()
    chosen = 0

    # draw window
    pygame.init()
    running = True 
    while running:      
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False
        
            if chosen == 0:
                if event.type == pygame.MOUSEBUTTONDOWN:    
                    for piece in pieces:
                        if chosen: break
                        for vals in piece.values():
                            if chosen: break
                            for val in vals:
                                chosen, selected_piece, places = val.choose_piece(board)
                                if chosen: break
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    selected_piece.move_piece(board, places)
                    chosen = False

        board.draw_screen()  

        for piece in pieces:
            for vals in piece.values():
                for val in vals: 
                    val.draw_piece(board.screen)
        
        pygame.display.update()
        game.end_game()
    pygame.quit()

if __name__ == "__main__":
    main()