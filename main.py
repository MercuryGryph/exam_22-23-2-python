import pygame
import pygame.freetype
import random

# 初始化
pygame.init()
# 定义几个颜色备用
color = {
    'white': [255, 255, 255],
    'gray': [170, 170, 170],
    'black': [0, 0, 0],
    'red': [255, 85, 85],
    'green': [85, 255, 85],
    'aqua': [85, 255, 255],
    'deep_green': [0, 170, 0],
    'gold': [221, 214, 5],
    'none': [0, 0, 0, 0]
}
color['bg'] = color['black']
color['frame'] = color['gold']
color['line'] = color['gray']
color['apple'] = color['red']
color['head'] = color['deep_green']
color['tail'] = color['aqua']
# 字体
JBmonoB = pygame.freetype.Font('fonts\\JetBrainsMono-Bold.ttf', 24)
default_font = JBmonoB
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

# 游戏网格
#  行列
row = 20
column = 20
#  格尺寸
tile_size = 25
#  偏移
drift_T = tile_size
drift_L = 0

frame_L = (width - column * tile_size) / 2 + drift_L
frame_R = width - frame_L + drift_L * 2
frame_T = (height - row * tile_size) / 2 + drift_T
frame_B = height - frame_T + drift_T * 2
#  内框
#   列
for i in range(1, column):
    pygame.draw.line(screen, color['line'], (frame_L + tile_size * i, frame_T), (frame_L + tile_size * i, frame_B), 3)
#   行
for i in range(1, row):
    pygame.draw.line(screen, color['line'], (frame_L, frame_T + tile_size * i), (frame_R, frame_T + tile_size * i), 3)
#  外框
pygame.draw.line(screen, color['frame'], (frame_L, frame_T), (frame_L, frame_B), 3)
pygame.draw.line(screen, color['frame'], (frame_L, frame_T), (frame_R, frame_T), 3)
pygame.draw.line(screen, color['frame'], (frame_R, frame_T), (frame_R, frame_B), 3)
pygame.draw.line(screen, color['frame'], (frame_L, frame_B), (frame_R, frame_B), 3)
#  逻辑网格
plant = []
for i in range(0, row):
    plant.append([])
    for j in range(0, column):
        plant[i].append(0)
# 蛇
snake_head = [row//2, column//2]
plant[snake_head[0]][snake_head[1]] = -1
snake_tail = []
# 文字
default_font.render_to(screen, (frame_L, frame_T - tile_size), "Score:", color['gray'], color['none'])


# 逻辑网格位置 转换为 屏幕坐标
def get_tile_pos_dest(pos):
    x = pos[0]
    y = pos[1]
    px = frame_L + x * tile_size
    py = frame_T + y * tile_size
    return px, py


def main():
    # 主循环
    is_gaming = True
    is_fruit_exist = False
    score = 1234567890
    while is_gaming:
        # 操作处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_gaming = False
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
        #  生成水果
        if not is_fruit_exist:
            pass
        #  更新画面
        default_font.render_to(screen, (frame_L + tile_size * 5, frame_T - tile_size),
                               "{0}".format(score), color['gray'], color['none'])
        pygame.display.update()


if __name__ == '__main__':
    main()
    pygame.quit()
