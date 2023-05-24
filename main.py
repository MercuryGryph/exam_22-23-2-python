import pygame
import pygame.freetype
import sys

# 初始化
pygame.init()
# 定义几个颜色备用
color = {
    'white': [255, 255, 255],
    'gray': [170, 170, 170],
    'black': [0, 0, 0],
    'red': [255, 85, 85],
    'gold': [221, 214, 5],
    'none': [0, 0, 0, 0]
}
color['bg'] = color['black']
color['frame'] = color['gold']
# 字体
JBmonoExB = pygame.freetype.Font('fonts\\JetBrainsMono-ExtraBold.ttf', 24)

# 窗口标题
pygame.display.set_caption("[GAME]")
# 窗口大小
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
# 背景颜色
screen.fill(color['bg'])
# 基本时钟
clock = pygame.time.Clock()
clock.tick(20)


# 暂停界面
def pause_menu():
    menu_title = pygame.Vector2(359, 55)
    pygame.draw.rect(screen, color['white'], (350, 50, 100, 30))
    JBmonoExB.render_to(screen, menu_title,
                        text='PAUSED',
                        fgcolor=color['red'],
                        bgcolor=color['none'],
                        size=24)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.K_ESCAPE:
                return
        pygame.display.flip()


def main():
    pause_menu()
    # 主循环
    while True:
        # 操作处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.K_ESCAPE:
                pause_menu()
            # 行动
            if event.type == pygame.K_UP:
                pass
            if event.type == pygame.K_DOWN:
                pass
            if event.type == pygame.K_LEFT:
                pass
            if event.type == pygame.K_RIGHT:
                pass

        # 逻辑处理
        pygame.display.flip()


if __name__ == '__main__':
    main()
    pygame.quit()
