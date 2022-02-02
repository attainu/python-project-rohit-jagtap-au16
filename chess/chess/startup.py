import pygame , sys

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('GAME MENU')
screen = pygame.display.set_mode((380,751),0,32)
font = pygame.font.SysFont(None,20)
from chess.game.main_01 import main

def draw_text(text,font,color,surface,x,y):
    textobj = font.render(text,1,color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj,textrect)

click = False

def main_menu():
    while True:
        screen.fill((53, 81, 92))
        draw_text('MENU', font, (255, 255, 255), screen,50,50)

        mx,my = pygame.mouse.get_pos()

        button_1 = screen.blit(font.render('NEW GAME', True, (255,255,255)), (50, 100))
        button_2 = screen.blit(font.render('END GAME', True, (255,255,255)), (50, 150))
        pygame.display.update()
        if button_1.collidepoint((mx,my)):
            if click:
                main()

        if button_2.collidepoint((mx,my)):
            if click:
                pygame.quit()
                sys.exit()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)

main_menu()