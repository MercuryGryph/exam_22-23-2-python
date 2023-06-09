# 提醒：查看从本地复制的代码前，先从Git更新
from snake import *
import pygame.freetype
import random

# pygame初始化
pygame.init()
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
color['bg'] = color['light_mode']       # 背景色
color['font'] = color['gray']           # 字体颜色
color['frame'] = color['gold']          # 棋盘边框
color['line'] = color['gray']           # 棋盘网格
color['fruit'] = color['red']           # 苹果（水果）的颜色
color['head'] = color['deep_green']     # 蛇头的颜色
color['tail'] = color['aqua']           # 蛇尾的颜色，实际上做了渐变的效果，这个颜色将会是最末尾的，越往前颜色越深
# 字体
#  https://www.jetbrains.com/lp/mono/
JetBrainsMono_Bold = pygame.freetype.Font('fonts\\JetBrainsMono-Bold.ttf', 24)
default_font = JetBrainsMono_Bold
# 窗口标题
pygame.display.set_caption("[GAME] Snake ~\\__/-O~")  # 这条蛇不如不画...
# 窗口大小
window_size = width, height = 800, 600
# 时钟
clock = pygame.time.Clock()
tick_rate = 5
# 游戏网格
#  行列
game_plane_size = row, column = 21, 21
#  格尺寸
tile_size = 25


# 生成水果
def gen_fruit_pos():
    x = random.randint(0, game.col - 1)
    y = random.randint(0, game.row - 1)
    while [x, y] == snake.pos or [x, y] in snake.tail:  # 如果生成的位置非法，就重新生成
        x = random.randint(0, game.col - 1)
        y = random.randint(0, game.row - 1)
    return [x, y]


# 操作说明
operations_info = """Operations:

                ↑↓←→ :
                - Change direction.

                'Space' :
                - Stop move.

                M :
                - Change dark/light."""\
    .split('\n')


# 渲染操作说明
def render_text():
    line_n = 0
    for line in operations_info:
        default_font.render_to(game.screen, (5, 5 + line_n * default_font.get_sized_height(18)), line.lstrip(),
                               color['gray'], color['none'], size=18)
        line_n += 1
    del line_n


# 判断蛇头位置是否合法
def is_out_of_bounds():
    if (not 0 <= snake.pos[0] < game.row
            or not 0 <= snake.pos[1] < game.col
            or snake.pos in snake.tail):
        return True
    else:
        return False


# 处理吃水果
def handle_is_get_fruit():
    if snake.pos == game.fruit_pos:
        snake.is_get_fruit = True
        game.score += 1
        game.fruit_pos = gen_fruit_pos()
        return True
    else:
        return False


# 切换 黑暗/明亮 模式
def change_dark_or_light_mode():
    if color['bg'] == color['light_mode']:
        color['bg'] = color['dark_mode']
    else:
        color['bg'] = color['light_mode']


def __main__():
    while True:
        is_game_over = False
        game.fruit_pos = gen_fruit_pos()
        # ---主循环---
        while not is_game_over:
            # 操作处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.KEYDOWN:
                    # 方向控制
                    if event.key == pygame.K_UP:
                        if snake.direction not in Direction_Y:   # 防止原地调头直接掉头
                            snake.direction = Direction.Up
                            break

                    elif event.key == pygame.K_DOWN:
                        if snake.direction not in Direction_Y:
                            snake.direction = Direction.Down
                            break

                    elif event.key == pygame.K_LEFT:
                        if snake.direction not in Direction_X:
                            snake.direction = Direction.Left
                            break

                    elif event.key == pygame.K_RIGHT:
                        if snake.direction not in Direction_X:
                            snake.direction = Direction.Right
                            break

                    elif event.key == pygame.K_SPACE:
                        snake.direction = Direction.Stop

                    # 切换背景
                    elif event.key == pygame.K_m:
                        change_dark_or_light_mode()

            # 逻辑处理
            snake.move()
            if is_out_of_bounds():
                is_game_over = True
            handle_is_get_fruit()

            # 渲染
            game.screen.fill(color['bg'])
            render_text()
            game.render(color['fruit'], color['line'], color['frame'], color['font'])
            snake.render(color['head'], color['tail'])
            pygame.display.update()

            # 控制帧率
            clock.tick(tick_rate)

        # ---主循环结束---

        # 显示结算
        default_font.render_to(game.screen, (10, game.frame_T),
                               'Game Over!', color['red'], color['none'], size=100)
        default_font.render_to(game.screen, (10, game.frame_T + default_font.get_sized_height(80)),
                               f'You got {game.score} score!', color['red'], color['none'], size=66)
        default_font.render_to(game.screen, (10, game.frame_T + 2 * default_font.get_sized_height(70)),
                               'Press any key to retry.', color['red'], color['none'], size=40)
        pygame.display.flip()
        # 等待退出或重开
        is_retry = False
        while not is_retry:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        change_dark_or_light_mode()

                    else:
                        is_retry = True

            clock.tick(tick_rate)

        # 重置数据
        game.update_score_max()
        game.restart()
        snake.restart()


if __name__ == '__main__':
    while True:
        game = SnakeGame(window_size, default_font, game_plane_size, tile_size)
        snake = Snake(game)
        __main__()
