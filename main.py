import pygame
import pygame.freetype
import random
from enum import Enum
from snake import *

# pygame初始化
pygame.init()
# 是否打印log
is_print_log = False
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
color['apple'] = color['red']  # 苹果（水果）的颜色
color['head'] = color['deep_green']  # 蛇头的颜色
color['tail'] = color['aqua']  # 蛇尾的颜色，实际上做了渐变的效果，这个颜色将会是最末尾的，越往前颜色越深
# 字体
JetBrainsMono_Bold = pygame.freetype.Font('fonts\\JetBrainsMono-Bold.ttf', 24)
# https://www.jetbrains.com/lp/mono/
default_font = JetBrainsMono_Bold
# 窗口标题
pygame.display.set_caption("[GAME] Snake ~\\__/-O~")  # 这条蛇不如不画...
# 窗口大小
window_size = width, height = 800, 600
game_screen = pygame.display.set_mode(window_size)
# 背景颜色
game_screen.fill(color['bg'])
# 时钟
clock = pygame.time.Clock()
tick_rate = 5
# 游戏网格
#  行列
game_plane_size = row, column = 21, 21
#  格尺寸
tile_size = 25
#  偏移
drift_H = default_font.get_sized_height(1)
drift_W = -8 * tile_size
drift_T = 0
drift_L = 0
#  计算实际边框位置
frame_L = (width - column * tile_size - drift_W) / 2 + drift_L
frame_R = frame_L + column * tile_size
frame_T = (height - row * tile_size + drift_H) / 2 + drift_T
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
# 操作说明
operations_info = """Operations:
                ↑↓←→ :
                -Change direction.
                'Space' :
                -Stop move.
                M :
                 Change dark/light."""\
    .split('\n')


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


def draw_text():
    # 文字
    #  操作说明
    line_n = 0
    for line in operations_info:
        default_font.render_to(game_screen, (5, 5 + line_n * default_font.get_sized_height(18)), line.lstrip(),
                               color['gray'], color['none'], size=18)
        line_n += 1
    del line_n
    #  计分板
    default_font.render_to(game_screen, (frame_L + 0 * tile_size, frame_T - tile_size), "Score:",
                           color['gray'], color['none'])
    default_font.render_to(game_screen, (frame_L + 8 * tile_size, frame_T - tile_size), "Max Score:",
                           color['gray'], color['none'])


def draw_items():
    #  水果
    pygame.draw.rect(game_screen, color['apple'], get_tile_pos_dest(fruit))
    #  蛇
    #   头
    pygame.draw.rect(game_screen, color['head'], get_tile_pos_dest(snake['head']))
    #   尾
    temp_color = color['tail'].copy()
    reduce_color = []
    for sub_pixel in color['tail']:
        reduce_color.append(sub_pixel / (1 + len(snake['tail'])))
    for tail in snake['tail']:
        pygame.draw.rect(game_screen, temp_color, get_tile_pos_dest(tail))
        for sub_pixel in range(3):
            temp_color[sub_pixel] -= reduce_color[sub_pixel]  # 颜色渐变
    #  分数
    default_font.render_to(game_screen, (frame_L + 4 * tile_size, frame_T - tile_size),
                           f"{game['score']}",
                           color['gray'], color['none'])
    default_font.render_to(game_screen, (frame_L + 14 * tile_size, frame_T - tile_size),
                           f"{game['score_max']}",
                           color['gray'], color['none'])


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


# 切换 黑暗/明亮 模式
def change_dark_or_light_mode():
    if color['bg'] == color['light_mode']:
        color['bg'] = color['dark_mode']
    else:
        color['bg'] = color['light_mode']


def main():
    pass


if __name__ == '__main__':
    snake = Snake(game_plane_size)
    game = SnakeGame(window_size)
    main()
