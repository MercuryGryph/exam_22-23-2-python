import pygame
import sys

# 定义几个颜色备用
COLOR_bg = [255, 255, 255]
COLOR_red = [255, 85, 85]

# 初始化
pygame.init()
# 窗口标题
pygame.display.set_caption("[GAME]")
# 窗口大小
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
# 背景颜色
screen.fill(COLOR_bg)
# 基本时钟
clock = pygame.time.Clock()
clock.tick(20)

# 主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        pygame.display.update()

