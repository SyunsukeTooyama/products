#numpy pygame をinstallする必要がある
import pygame
import numpy as np
from pygame.locals import *
import sys
import math

class Disc:
    def __init__(self): #black=1, white=2
        self.grid_size = 10 #n*nサイズ指定
        self.directions = ['up', 'down', 'left', 'right', 'left_down', 'left_up', 'right_down', 'right_up']
        self.rects = np.zeros([self.grid_size+1,self.grid_size+1,2]) #マス掛け線
        self.cirs = np.zeros([self.grid_size,self.grid_size]) #置いてあるマス　黒１　白２　置いてないマス０　左上(0,0)
        self.puts = np.zeros([self.grid_size,self.grid_size]) #置けるマス
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)

        self.screen = pygame.display.set_mode((1280,720)) #pygame ウィンドウ生成
        self.clock = pygame.time.Clock() #時間経過
        self.turn = 1 #turn=1で黒のターン
        self.f = 0 #置けなかった時のターンを飛ばすときに使う
        self.put = False #石を置いた時に使う
        self.mark = False #石を置けるマスを表示したときに使う

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
        self.cirs[math.floor(self.grid_size/2)-1][math.floor(self.grid_size/2)-1] = 1
        self.cirs[math.floor(self.grid_size/2)][math.floor(self.grid_size/2)] = 1
        self.cirs[math.floor(self.grid_size/2)-1][math.floor(self.grid_size/2)] = 2       
        self.cirs[math.floor(self.grid_size/2)][math.floor(self.grid_size/2)-1] = 2

    def show_disc (self):
        for i in range(self.grid_size):
            for k in range(self.grid_size):
                if self.cirs[i][k]==1:
                    pygame.draw.circle(self.screen,self.BLACK,[(self.rects[i][k][0]+self.rects[i+1][k][0])/2.,(self.rects[i][k][1]+self.rects[i][k+1][1])/2.],30*8/self.grid_size,0)
                if self.cirs[i][k]==2:
                    pygame.draw.circle(self.screen,self.BLACK,[(self.rects[i][k][0]+self.rects[i+1][k][0])/2.,(self.rects[i][k][1]+self.rects[i][k+1][1])/2.],30*8/self.grid_size,3)
    
    def show_can_put (self):
        #置けるマスの表示
        for i in range(self.grid_size):
            for k in range(self.grid_size):
                if self.puts[i][k]==1:
                    pygame.draw.circle(self.screen,'gray',[(self.rects[i][k][0]+self.rects[i+1][k][0])/2.,(self.rects[i][k][1]+self.rects[i][k+1][1])/2.],30*8/self.grid_size,0)

    def show_window(self):
        self.screen.fill('gray') #背景色
        pygame.draw.rect(self.screen, self.WHITE, [340, 60, 600, 600], 0) #長方形生成
        for i in range(self.grid_size-1):    
            pygame.draw.line(self.screen,self.BLACK,[340+600/self.grid_size*(i+1),60],[340+600/self.grid_size*(i+1),660],2)
            pygame.draw.line(self.screen,self.BLACK,[340,60+600/self.grid_size*(i+1)],[940,60+600/self.grid_size*(i+1)],2)

    def show_turn(self):
        if self.turn==1:
            self.screen.blit(self.b_text,(40,120))
        elif self.turn==2:
            self.screen.blit(self.w_text,(1000,120))

    def show_num_discs(self):
        self.b_num=np.sum(self.cirs==1)
        self.w_num=np.sum(self.cirs==2)
        b_num_text = self.font.render(f"{self.b_num}", True, (0,0,0))
        w_num_text = self.font.render(f"{self.w_num}", True, (0,0,0))
        self.screen.blit(b_num_text,(100,500))
        self.screen.blit(w_num_text,(1100,500))

    def game_end(self):
        if (np.any(self.puts==1) == False) and (self.f==2): #置ける場所がなくなった時のゲーム終了
        
            if self.b_num<self.w_num:
                self.screen.blit(self.w_win,(250,120))
            elif self.b_num>self.w_num:
                self.screen.blit(self.b_win,(250,120))
            else:
                self.screen.blit(self.draw,(250,120))

        elif (np.any(self.puts==1) == False) and (self.f==0): #置けるマスのないときのターン飛ばし
            if self.turn==1:
                self.f+=1
                self.turn=2
                self.mark=False

            elif self.turn==0:
                self.f+=1
                self.turn=1
                self.mark=False

        elif (np.any(self.puts==1) == False) and (np.any(self.cirs==0)==False): #マスがすべて埋まった時のゲーム終了
            if self.b_num<self.w_num:
                self.screen.blit(self.w_win,(250,120))
            elif self.b_num>self.w_num:
                self.screen.blit(self.b_win,(250,120))
            else:
                self.screen.blit(self.draw,(250,120))

    def boundary_condition(self, i: int, k: int):
        boundary_condition = {'up': i-1 >= 0 , 'down': i+1 < self.grid_size, 'left': k-1 >= 0, 'right': k+1 < self.grid_size, 'left_down': i-1>=0 and k+1<self.grid_size, 'left_up': i-1>=0 and k-1>=0, 'right_down': i+1<self.grid_size and k+1<self.grid_size, 'right_up': i+1<self.grid_size and k-1>=0}
        return boundary_condition

    def inner_condition(self, i: int, k: int, m: int):   
        inner_condition = {'up': i-m < 0 , 'down': i+m > self.grid_size-1, 'left': k-m < 0, 'right': k+m > self.grid_size-1, 'left_down': i-m<0 or k+m>self.grid_size-1, 'left_up': i-m<0 or k-m<0, 'right_down': i+m>self.grid_size-1 or k+m>self.grid_size-1, 'right_up': i+m>self.grid_size-1 or k-m<0}
        return inner_condition
    
    def x_condition (self,direction, i: int, m: int):
        x_condi = {'up': i-m, 'down': i+m, 'left': i, 'right': i, 'left_down': i-m, 'left_up': i-m, 'right_down': i+m, 'right_up': i+m}
        return x_condi[direction]

    def y_condition (self,direction, k: int, m: int):
        y_condi = {'up': k, 'down': k, 'left': k-m, 'right': k+m, 'left_down': k+m, 'left_up': k-m, 'right_down': k+m, 'right_up': k-m}
        return y_condi[direction]

    def put_disc (self):
        put=False

        if self.turn == 1:
            op_turn = 2
        else:
            op_turn = 1

        for i in range(self.grid_size): 
            for k in range(self.grid_size):
                if (self.rects[i][k][0]<pygame.mouse.get_pos()[0]<self.rects[i+1][k][0]) and (self.rects[i][k][1]<pygame.mouse.get_pos()[1]<self.rects[i][k+1][1]): #クリックしたマスを取得
                    if self.cirs[i][k]==0: #石が置いていないか確認
                        for direction in self.directions:
                            if self.boundary_condition(i, k)[direction]: #上方向
                                if self.cirs[self.x_condition(direction, i, 1)][self.y_condition(direction, k, 1)]==op_turn:  
                                    for m in range(2,self.grid_size):
                                        if self.inner_condition(i, k, m)[direction]:
                                            break 
                                        if self.cirs[self.x_condition(direction, i, m)][self.y_condition(direction, k, m)]== op_turn:
                                            continue
                                        elif self.cirs[self.x_condition(direction, i, m)][self.y_condition(direction, k, m)]== self.turn:
                                            for n in range(m):
                                                self.cirs[self.x_condition(direction, i, n)][self.y_condition(direction, k, n)]= self.turn 
                                            put=True
                                            self.mark=False
                                            break
                                        else:
                                            break
              
            if put==True: #置いたか確認　置いたときput=True
                self.turn = op_turn
                self.f = 0

    def can_put(self):
        if self.turn == 1:
            op_turn = 2
        else:
            op_turn = 1

        if self.mark==False: #置ける場所を表示していない時　mark=False
            #puts初期化
            for i in range(self.grid_size): 
                for k in range(self.grid_size):
                    self.puts[i][k] = 0
            
            #置ける場所を探す
            self.mark=True 
            for i in range(self.grid_size):
                for k in range(self.grid_size):
                    if self.cirs[i][k]==0:
                        for direction in self.directions:
                            #print(direction)
                            if self.boundary_condition(i,k)[direction]:
                                if self.cirs[self.x_condition(direction, i, 1)][self.y_condition(direction, k, 1)]==op_turn:  
                                    for m in range(2,self.grid_size):
                                        if self.inner_condition(i, k, m)[direction]:
                                            break
                                        if self.cirs[self.x_condition(direction, i, m)][self.y_condition(direction, k, m)]==op_turn:
                                            continue
                                        elif self.cirs[self.x_condition(direction, i, m)][self.y_condition(direction, k, m)]==self.turn:
                                            self.puts[i][k]=1
                                            break       
                                        else:
                                            break 

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
