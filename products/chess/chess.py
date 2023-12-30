import pygame

screen = pygame.display.set_mode((1280,720))

pygame.init()
running = True 
while running:          
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
    
    screen.fill('gray')
pygame.quit()