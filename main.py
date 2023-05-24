import pygame
import pygame.freetype
import random
import time
from enum import Enum


class Direction(Enum):
    Stop = 0
    Up = 1
    Right = 2
    Down = 3
    Left = 4


# pygame初始化
pygame.init()

# 颜色
#  定义几个颜色备用
color = {
    'white': [255, 255, 255],
    'gray': [170, 170, 170],
    'black': [0, 0, 0],
    'red': [255, 85, 85],
    'aqua': [85, 255, 255],
    'deep_green': [0, 170, 0],
    'gold': [221, 214, 5],
    'none': [0, 0, 0, 0]
}
#  实际使用的颜色
color['bg'] = color['white']
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
clock.tick(5)

# 游戏网格
#  行列
row = 21
column = 21
#  格尺寸
tile_size = 25
# 绘制游戏网格
#  偏移
drift_H = default_font.get_sized_height(1)
drift_W = -8*tile_size
drift_T = 0
drift_L = 0
#  计算实际边框位置
frame_L = (width - column * tile_size - drift_W) / 2 + drift_L
frame_R = frame_L + column * tile_size
frame_T = (height - row * tile_size + drift_H) / 2 + drift_T
frame_B = frame_T + row * tile_size

# 蛇
snake = {
    'head': [column // 2, row // 2],
    'tail': [],
    'tail_new': [column // 2, row // 2]
}
snake_direction = Direction(0)
# 水果
fruit_pos = []


# 生成水果
def set_fruit_pos():
    x = random.randint(0, column - 1)
    y = random.randint(0, row - 1)
    while [x, y] == snake['head'] or [x, y] in snake['tail']:
        x = random.randint(0, column - 1)
        y = random.randint(0, row - 1)
    return [x, y]


# 逻辑网格位置 转换为 屏幕坐标区域
def get_tile_pos_dest(pos):
    x = pos[0]
    y = pos[1]
    px = frame_L + x * tile_size
    py = frame_T + y * tile_size
    return px, py, tile_size, tile_size


def draw_stage():
    # 游戏框
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

    # 文字
    #  操作说明
    default_font.render_to(screen, (5, 5+0*default_font.get_sized_height(16)),
                           "Operations:", color['gray'], color['none'], size=16)
    default_font.render_to(screen, (5, 5+1*default_font.get_sized_height(16)),
                           "↑↓←→ :", color['gray'], color['none'], size=16)
    default_font.render_to(screen, (5, 5+2*default_font.get_sized_height(16)),
                           " Change direction", color['gray'], color['none'], size=16)
    default_font.render_to(screen, (5, 5+3*default_font.get_sized_height(16)), "'Space' :",
                           color['gray'], color['none'], size=16)
    default_font.render_to(screen, (5, 5+4*default_font.get_sized_height(16)), " Stop move",
                           color['gray'], color['none'], size=16)
    #  计分板
    default_font.render_to(screen, (frame_L, frame_T - tile_size), "Score:", color['gray'], color['none'])


# 移动蛇
def move_snake():
    # 移动
    if snake_direction == Direction(0):
        return
    pos = snake['head']
    if snake_direction == Direction(1):
        snake['head'][1] -= 1
    elif snake_direction == Direction(2):
        snake['head'][0] += 1
    elif snake_direction == Direction(3):
        snake['head'][1] += 1
    elif snake_direction == Direction(4):
        snake['head'][0] -= 1
    # 判断是否移动尾巴
    if snake['tail_new']:
        snake['tail'].append(snake['tail_new'])
    if game['is_get_fruit']:
        game['is_get_fruit'] = False
    else:
        del snake['tail'][0]
    # 游戏失败条件
    if (snake['head'][0] < 0 or snake['head'][0] > column or
            snake['head'][1] < 0 or snake['head'][1] > row or
            snake['head'] in snake['tail']):
        game['is_game_over'] = True
    # 处理吃水果动作
    if snake['head'] == fruit:
        game['score'] += 1
        game['is_fruit_exist'] = False
        game['is_get_fruit'] = True
    del snake['tail_new']
    snake['tail_new'] = []
    for i in pos:
        snake['tail_new'].append(i)


if __name__ == '__main__':
    game = {
        'is_gaming': True,
        'is_game_over': False,
        'is_fruit_exist': False,
        'is_get_fruit': False,
        'score': 0
    }
    # 主循环
    while game['is_gaming']:
        # 操作处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game['is_gaming'] = False
            # 移动方向
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != Direction(3):
                    snake_direction = Direction(1)
                elif event.key == pygame.K_DOWN and snake_direction != Direction(1):
                    snake_direction = Direction(3)
                elif event.key == pygame.K_LEFT and snake_direction != Direction(2):
                    snake_direction = Direction(4)
                elif event.key == pygame.K_RIGHT and snake_direction != Direction(4):
                    snake_direction = Direction(2)
                elif event.key == pygame.K_SPACE:
                    snake_direction = Direction(0)

        # 逻辑处理
        #  移动蛇
        move_snake()
        #  生成水果
        if not game['is_fruit_exist']:
            fruit = set_fruit_pos()
            game['is_fruit_exist'] = True
        # 更新画面
        screen.fill(color['bg'])
        draw_stage()
        #  水果
        pygame.draw.rect(screen, color['apple'], get_tile_pos_dest(fruit))
        game['is_fruit_paint'] = True
        #  蛇
        #   头
        pygame.draw.rect(screen, color['head'], get_tile_pos_dest(snake['head']))
        #   尾
        temp_color = []
        reduce_color = []
        for i in color['tail']:
            temp_color.append(i)
            reduce_color.append(i / (1 + len(snake['tail'])))
        for tail in snake['tail']:
            pygame.draw.rect(screen, temp_color, get_tile_pos_dest(tail))
            for i in range(3):
                temp_color[i] -= reduce_color[i]
        #  分数
        default_font.render_to(screen, (frame_L + tile_size * 5, frame_T - tile_size),
                               "{0}".format(game['score']), color['gray'], color['none'])

        # 日志
        print('[log]')
        print('-', snake['tail'])
        print('#', fruit)
        print('@', snake['head'])

        if game['is_game_over']:
            default_font.render_to(screen, (0, frame_T), 'Game Over!', color['red'], color['none'], size=100)
            game['is_gaming'] = False
        pygame.display.flip()
        clock.tick(4)

    while game['is_game_over']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game['is_game_over'] = False
    pygame.quit()
