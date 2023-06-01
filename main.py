import time
import pygame
import pygame.freetype
import random
from enum import Enum


class Direction(Enum):
    Stop = 0
    Up = 1
    Right = 2
    Down = 3
    Left = 4


# pygame初始化
pygame.init()
# 是否打印log
is_print_log = True
# 颜色
color = {
    'white': [255, 255, 255],
    'gray': [170, 170, 170],
    'dark_gray': [85, 85, 85],
    'black': [0, 0, 0],
    'red': [255, 85, 85],
    'aqua': [85, 255, 255],
    'deep_green': [0, 170, 0],
    'gold': [221, 214, 5],
    'none': [0, 0, 0, 0]
}
#  实际使用的颜色
color['dark_mode'] = color['dark_gray']
color['light_mode'] = color['white']
color['bg'] = color['light_mode']  # 背景色
color['frame'] = color['gold']  # 棋盘边框
color['line'] = color['gray']  # 棋盘网格
color['fruit'] = color['red']  # 水果颜色
color['head'] = color['deep_green']  # 蛇头的颜色
color['tail'] = color['aqua']  # 蛇尾的颜色，实际上做了渐变的效果，这个颜色将会是最末尾的，越往前颜色越深
# 字体
JetBrainsMono_Bold = pygame.freetype.Font('fonts\\JetBrainsMono-Bold.ttf', 24)
# https://www.jetbrains.com/lp/mono/
main_font = JetBrainsMono_Bold
# 窗口标题
pygame.display.set_caption("[GAME] Snake ~\\__/-O~")  # 这条蛇不如不画...
# 窗口大小 (px)
screen_size = screen_width, screen_height = 800, 600
screen = pygame.display.set_mode(screen_size)
# 背景颜色
screen.fill(color['bg'])
# 时钟
clock = pygame.time.Clock()
tick_rate = 4
tick_rate_low = max(tick_rate // 2, 2)
# 游戏网格
#  行列
row = 21
column = 21
#  格尺寸 (px)
tile_size = 25
#  偏移
drift_H = main_font.get_sized_height(1)
drift_W = -8 * tile_size
drift_T = 0
drift_L = 0
#  计算实际边框位置
frame_L = (screen_width - column * tile_size - drift_W) / 2 + drift_L
frame_R = frame_L + column * tile_size
frame_T = (screen_height - row * tile_size + drift_H) / 2 + drift_T
frame_B = frame_T + row * tile_size

# 蛇
snake = {}
# 水果
fruit = []
# 游戏数据
game = {
    'score_max': 0,
    'score': 0
}


# 数据初始化
def init():
    snake['head'] = [column // 2, row // 2]
    snake['tail'] = []
    snake['tail_new'] = snake['head'].copy()
    snake['direction'] = Direction.Stop
    game['score_max'] = max(game['score'], game['score_max'])  # 更新最大分
    game['is_gaming'] = True
    game['is_game_over'] = False
    game['is_fruit_exist'] = False
    game['is_get_fruit'] = False
    game['score'] = 0
    game['is_retry'] = False


# 切换 黑暗/明亮 模式
def change_dark_or_light_mode():
    if color['bg'] == color['light_mode']:
        color['bg'] = color['dark_mode']
    else:
        color['bg'] = color['light_mode']


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


# 渲染
def draw_stage():
    # 游戏框
    #  内框
    #   列
    for i in range(1, column):
        pygame.draw.line(screen, color['line'],
                         (frame_L + tile_size * i, frame_T), (frame_L + tile_size * i, frame_B), 3)
    #   行
    for i in range(1, row):
        pygame.draw.line(screen, color['line'],
                         (frame_L, frame_T + tile_size * i), (frame_R, frame_T + tile_size * i), 3)
    #  外框
    pygame.draw.line(screen, color['frame'], (frame_L, frame_T), (frame_L, frame_B), 3)
    pygame.draw.line(screen, color['frame'], (frame_L, frame_T), (frame_R, frame_T), 3)
    pygame.draw.line(screen, color['frame'], (frame_R, frame_T), (frame_R, frame_B), 3)
    pygame.draw.line(screen, color['frame'], (frame_L, frame_B), (frame_R, frame_B), 3)

    # 文字
    #  操作说明
    main_font.render_to(screen, (5, 5 + 0 * main_font.get_sized_height(16)),
                        "Operations:", color['gray'], color['none'], size=16)
    main_font.render_to(screen, (5, 5 + 1 * main_font.get_sized_height(16)),
                        "↑↓←→ :", color['gray'], color['none'], size=16)
    main_font.render_to(screen, (5, 5 + 2 * main_font.get_sized_height(16)),
                        " Change direction", color['gray'], color['none'], size=16)
    main_font.render_to(screen, (5, 5 + 3 * main_font.get_sized_height(16)), "'Space' :",
                        color['gray'], color['none'], size=16)
    main_font.render_to(screen, (5, 5 + 4 * main_font.get_sized_height(16)), " Stop move",
                        color['gray'], color['none'], size=16)
    main_font.render_to(screen, (5, 5 + 5 * main_font.get_sized_height(16)), "M :",
                        color['gray'], color['none'], size=16)
    main_font.render_to(screen, (5, 5 + 6 * main_font.get_sized_height(16)), " Change Dark/Light mode",
                        color['gray'], color['none'], size=16)
    #  计分板
    main_font.render_to(screen, (frame_L, frame_T - tile_size), "Score:", color['gray'], color['none'])
    main_font.render_to(screen, (frame_L + 8 * tile_size, frame_T - tile_size),
                        "Max Score:", color['gray'], color['none'])


def draw_items():
    #  水果
    pygame.draw.rect(screen, color['fruit'], get_tile_pos_dest(fruit))
    game['is_fruit_paint'] = True
    #  蛇
    #   头
    pygame.draw.rect(screen, color['head'], get_tile_pos_dest(snake['head']))
    #   尾
    temp_color = color['tail'].copy()
    reduce_color = []
    for sub_pixel in color['tail']:
        reduce_color.append(sub_pixel / (1 + len(snake['tail'])))
    for tail in snake['tail']:
        pygame.draw.rect(screen, temp_color, get_tile_pos_dest(tail))
        for sub_pixel in range(3):
            temp_color[sub_pixel] -= reduce_color[sub_pixel]  # 颜色渐变
    #  分数
    main_font.render_to(screen, (frame_L + 4 * tile_size, frame_T - tile_size),
                        "{0}".format(game['score']), color['gray'], color['none'])
    #  最大得分
    main_font.render_to(screen, (frame_L + 14 * tile_size, frame_T - tile_size),
                        "{0}".format(game['score_max']), color['gray'], color['none'])


# 移动蛇
def move_snake():
    # 移动
    if snake['direction'] == Direction.Stop:
        return
    pos = snake['head']
    if snake['direction'] == Direction.Up:
        snake['head'][1] -= 1
    elif snake['direction'] == Direction.Right:
        snake['head'][0] += 1
    elif snake['direction'] == Direction.Down:
        snake['head'][1] += 1
    elif snake['direction'] == Direction.Left:
        snake['head'][0] -= 1
    # 判断是否延长尾巴
    if snake['tail_new']:
        snake['tail'].append(snake['tail_new'])
    if game['is_get_fruit']:
        game['is_get_fruit'] = False
    else:
        del snake['tail'][0]
    # 游戏失败条件
    if (snake['head'][0] < 0 or snake['head'][0] >= column or
            snake['head'][1] < 0 or snake['head'][1] >= row or
            snake['head'] in snake['tail']):
        game['is_game_over'] = True
    # 处理吃水果动作
    if snake['head'] == fruit:
        game['score'] += 1
        game['is_fruit_exist'] = False
        game['is_get_fruit'] = True
    del snake['tail_new']
    snake['tail_new'] = pos.copy()


# 日志
def logger():
    if not is_print_log:
        return
    print('[log] @', time.ctime())
    print('\tTails ... :', snake['tail'])
    print('\tFruit ... :', fruit)
    print('\tHead .... :', snake['head'], snake['direction'])
    print('\tDirection :', snake['direction'])
    print('\tScore ... :', game['score'])


if __name__ == '__main__':
    while True:
        init()
        # 主循环
        while game['is_gaming']:
            # 操作处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game['is_gaming'] = False
                elif event.type == pygame.KEYDOWN:
                    # 移动方向
                    if event.key == pygame.K_UP and snake['direction'] != Direction.Down:
                        snake['direction'] = Direction.Up
                    elif event.key == pygame.K_DOWN and snake['direction'] != Direction.Up:
                        snake['direction'] = Direction.Down
                    elif event.key == pygame.K_LEFT and snake['direction'] != Direction.Right:
                        snake['direction'] = Direction.Left
                    elif event.key == pygame.K_RIGHT and snake['direction'] != Direction.Left:
                        snake['direction'] = Direction.Right
                    elif event.key == pygame.K_SPACE:
                        snake['direction'] = Direction.Stop
                    # 黑暗/明亮 模式
                    elif event.key == pygame.K_m:
                        change_dark_or_light_mode()

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
            draw_items()

            # 游戏结束
            if game['is_game_over']:
                # 显示结算
                main_font.render_to(screen, (10, frame_T),
                                    'Game Over!', color['red'], color['none'], size=100)
                main_font.render_to(screen, (10, frame_T + main_font.get_sized_height(80)),
                                    f'You got {game["score"]} score!', color['red'], color['none'], size=66)
                main_font.render_to(screen, (10, frame_T + 2 * main_font.get_sized_height(70)),
                                    'Press any key to retry.', color['red'], color['none'], size=40)
                game['is_gaming'] = False
            pygame.display.flip()

            logger()

            # 控制帧率
            if snake['direction'] == Direction.Stop:
                clock.tick(tick_rate_low)
            else:
                clock.tick(tick_rate)

        # 游戏结束
        while game['is_game_over']:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game['is_game_over'] = False
                elif event.type == pygame.KEYDOWN:
                    game['is_retry'] = True
                    game['is_game_over'] = False
            clock.tick(tick_rate_low)
        if not game['is_retry']:
            break
    pygame.quit()
