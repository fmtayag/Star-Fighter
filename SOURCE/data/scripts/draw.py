import pygame

def draw_hp(surf, x, y, hp, color, img):
    # This is a rusty code but it works!
    if hp < 0:
        hp = 0
    rect_height = img.get_height()*0.5
    rectangle = pygame.Rect(x+24, y+8,  hp * 23, rect_height)
    pygame.draw.rect(surf, color, rectangle)
    surf.blit(img, (x, y))