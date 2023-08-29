#numpy pygame をinstallする必要がある
import pygame
import numpy as np
from pygame.locals import *
import sys
import math

class Disc:
    def __init__(self): #black=1, white=2
        self.grid_size = 8 #n*nサイズ指定

        self.rects = np.zeros([self.grid_size+1,self.grid_size+1,2]) #マス掛け線
        
        self.bit=2**63
        self.black_bit = (self.bit>>3*8+3)|(self.bit>>4*8+4)
        self.white_bit = (self.bit>>4*8+3)|(self.bit>>3*8+4) 
        
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)

        self.screen = pygame.display.set_mode((1280,720)) #pygame ウィンドウ生成
        self.clock = pygame.time.Clock() #時間経過
        self.turn = True #turn=Trueで黒のターン
        self.f = 0 #置けなかった時のターンを飛ばすときに使う
        self.put = False
        self.can_reverse = 0b0
        self.temp=0b0
        self.can_reverse = 0b0


        self.horizontal_mask = 0b0111111001111110011111100111111001111110011111100111111001111110
        self.vertical_mask = 0b0000000011111111111111111111111111111111111111111111111100000000
        self.allside_mask = 0b0000000001111110011111100111111001111110011111100111111000000000

        self.masks = {'left': self.horizontal_mask , 
                    'right': self.horizontal_mask, 
                    'up': self.vertical_mask , 
                    'down': self.vertical_mask,
                    'left_up': self.allside_mask,
                    'left_down': self.allside_mask,
                    'right_up': self.allside_mask,
                    'right_down': self.allside_mask,
                    }

        
        self.directions=['left','right','up','down','left_up','left_down','right_up','right_down']
        self.colors=[self.black_bit, self.white_bit]


        #フォント関連
        pygame.font.init() 
        self.font = pygame.font.SysFont("symap", 100)
        self.win_font = pygame.font.SysFont("symap", 200)
        self.b_text = self.font.render("BLACK", True, (0,0,0), (255,255,255))
        self.w_text = self.font.render("WHITE", True, (255,255,255), (0,0,0))
        self.b_win = self.win_font.render("BLACK WIN", True, (0,0,0), (255,255,255))
        self.w_win = self.win_font.render("WHITE WIN", True, (255,255,255), (0,0,0))
        self.draw = self.win_font.render("DRAW", True, (255,0,0), (0,0,0))
        
        #マス作成
        for i in range(self.grid_size+1):
            for k in range(self.grid_size+1):
                self.rects[i][k][0] = 340.+i*600/self.grid_size
                self.rects[i][k][1] = 60.+k*600/self.grid_size

        #最初の4つ 黒1　白2

    def show_disc (self):
        for k in range(self.grid_size):
            for i in range(self.grid_size):
                n = i+8*k
                if "{:0>64}".format(str(bin(self.black_bit))[2:])[n] == '1':
                    pygame.draw.circle(self.screen,self.BLACK,[(self.rects[i][k][0]+self.rects[i+1][k][0])/2.,(self.rects[i][k][1]+self.rects[i][k+1][1])/2.],30*8/self.grid_size,0)
                if "{:0>64}".format(str(bin(self.white_bit))[2:])[n] == '1':
                    pygame.draw.circle(self.screen,self.BLACK,[(self.rects[i][k][0]+self.rects[i+1][k][0])/2.,(self.rects[i][k][1]+self.rects[i][k+1][1])/2.],30*8/self.grid_size,3)
    
    def show_can_put (self):
        #置けるマスの表示

        for k in range(self.grid_size):
            for i in range(self.grid_size):
                n = i+8*k
                if "{:0>64}".format(str(bin(self.can))[2:])[n] == '1':
                    pygame.draw.circle(self.screen,'gray',[(self.rects[i][k][0]+self.rects[i+1][k][0])/2.,(self.rects[i][k][1]+self.rects[i][k+1][1])/2.],30*8/self.grid_size,0)

    def show_window(self):
        self.screen.fill('gray') #背景色
        pygame.draw.rect(self.screen, self.WHITE, [340, 60, 600, 600], 0) #長方形生成
        for i in range(self.grid_size-1):    
            pygame.draw.line(self.screen,self.BLACK,[340+600/self.grid_size*(i+1),60],[340+600/self.grid_size*(i+1),660],2)
            pygame.draw.line(self.screen,self.BLACK,[340,60+600/self.grid_size*(i+1)],[940,60+600/self.grid_size*(i+1)],2)

    def show_turn(self):
        if self.turn:
            self.screen.blit(self.b_text,(40,120))
        else:
            self.screen.blit(self.w_text,(1000,120))

    def show_num_discs(self):
        self.b_num=str(bin(self.black_bit)).count('1')
        self.w_num=str(bin(self.white_bit)).count('1')
        #print('black')
        #print(self.b_num)
        b_num_text = self.font.render(f"{self.b_num}", True, (0,0,0))
        w_num_text = self.font.render(f"{self.w_num}", True, (0,0,0))
        self.screen.blit(b_num_text,(100,500))
        self.screen.blit(w_num_text,(1100,500))

    def game_end(self):
        if (self.can == 0) and (self.f==1): #置ける場所がなくなった時のゲーム終了
            if self.b_num<self.w_num:
                self.screen.blit(self.w_win,(250,120))
            elif self.b_num>self.w_num:
                self.screen.blit(self.b_win,(250,120))
            else:
                self.screen.blit(self.draw,(250,120))

        elif (self.can == 0) and (self.f==0): #置けるマスのないときのターン飛ばし
            self.f += 1
            self.turn = not self.turn

        elif (self.black_bit + self.white_bit) == 2**64-1: #マスがすべて埋まった時のゲーム終了
            if self.b_num<self.w_num:
                self.screen.blit(self.w_win,(250,120))
            elif self.b_num>self.w_num:
                self.screen.blit(self.b_win,(250,120))
            else:
                self.screen.blit(self.draw,(250,120))

    def shifts(self,direction,temp):
            shifts_direction = {'left': temp<<1 , 
                'right': temp>>1, 
                'up': temp<<8, 
                'down': temp>>8,
                'left_up': temp<<9,
                'left_down': temp>>7,
                'right_up': temp<<7,
                'right_down': temp>>9,
                }
            return shifts_direction[direction]

    def put_disc (self):
        '''print_line="{:0>64}".format(str(bin(black_bit))[2:])
        print('black')
        for n in range(8):
            print(print_line[8*n:8+8*n])
        print('----------------')

        print_line="{:0>64}".format(str(bin(white_bit))[2:])
        print('white')
        for n in range(8):
            print(print_line[8*n:8+8*n])
        print('----------------')'''
        if self.turn:
            color = self.black_bit
            other_color = self.white_bit
        else:
            color = self.white_bit
            other_color = self.black_bit

        was_put = False
        for i in range(self.grid_size): 
            for k in range(self.grid_size):
                if (self.rects[i][k][0]<pygame.mouse.get_pos()[0]<self.rects[i+1][k][0]) and (self.rects[i][k][1]<pygame.mouse.get_pos()[1]<self.rects[i][k+1][1]):
                    put=self.bit>>k*8+i
                    if self.can & put:
                        for direction in self.directions: 
                            reverse = 0b0
                            temp = self.shifts(direction,put) & self.masks[direction]
                            reversed = 0b0
                            was_reverse = False   
                            for i in range(6):
                                if temp & other_color:
                                    reverse = reverse | (other_color & temp)
                                    '''print_line="{:0>64}".format(str(bin(reverse))[2:])
                                    for n in range(8):
                                        print(print_line[8*n:8+8*n])
                                    print('----------------')''' 
                                    temp = self.shifts(direction,temp)
                                    was_reverse = True  
                                else:
                                    break 

                            if (color & temp) and was_reverse :
                                reversed = self.can_reverse & reverse 
                                color = color | reversed | put
                                other_color = other_color & ~reversed
                                if self.turn:
                                    self.black_bit = color
                                    self.white_bit = other_color
                                else:
                                    self.white_bit = color
                                    self.black_bit = other_color

                                was_put = True

        if was_put:
            self.turn = not self.turn
            self.f = 0

            

    def can_put(self):
        if self.turn:
            color = self.black_bit
            other_color = self.white_bit
        else:
            color = self.white_bit
            other_color = self.black_bit

        self.can=0b0
        empty_board = ~ (color | other_color)

        for direction in self.directions:
            masked_board = other_color & self.masks[direction]
            temp = self.shifts(direction,color) & masked_board
            for i in range(6):
                temp = (self.shifts(direction,temp) & masked_board)  | temp
            self.can_reverse = self.can_reverse|temp    
            can_temp = self.shifts(direction,temp) & empty_board
            #print(bin(can))
            self.can = self.can | can_temp

        '''print_line="{:0>64}".format(str(bin(self.can))[2:])
        print('can')
        for n in range(8):
            print(print_line[8*n:8+8*n])
        print('----------------')'''

pygame.init() #pygame初期化

DISC = Disc()

running = True #起動中
while running: #無限ループ   falseで切る  ループなしでも良さそう          
    for event in pygame.event.get(): #
        if event.type==pygame.QUIT: #ウィンドウを閉じる
            running=False

        if event.type==pygame.MOUSEBUTTONDOWN: #クリックで石を置く                
            DISC.put_disc()
    
    #置ける場所を表示する部分
    DISC.can_put() 
    
    '''
    for i in range(self.grid_size):
        for k in range(self.grid_size):
            cirs[i][k]=1
    '''

    #掛け線の表示
    DISC.show_window()
    
    #石の表示
    DISC.show_disc()

    #ターンを示す文字列表示
    DISC.show_turn()

    #石の数の表示
    DISC.show_num_discs()
    
    #ゲーム終了表示
    DISC.game_end()

    DISC.show_can_put()
    
    
    #print(cirs) 
    pygame.display.update() #ディスプレイ表示
    DISC.clock.tick(20) #ループ間隔

pygame.quit() #ゲーム終了






