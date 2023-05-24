import pygame
import sys

color_bg = [255, 255, 255]

pygame.init()
pygame.display.set_caption("[2048]")

size = width, height = 800, 600
screen = pygame.display.set_mode(size)
screen.fill(color_bg)

clock = pygame.time.Clock()
clock.tick(20)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        pygame.display.update()
