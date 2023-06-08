import pygame
from enum import Enum

from main import get_tile_pos_dest


class Direction(Enum):
    Stop = 0
    Up = 1
    Right = 2
    Down = 3
    Left = 4


class SnakeGame:
    def __init__(self, screen_size, font, plane_size, tile_size):
        self.score = 0
        self.score_max = 0
        self.fruit_pos = []

        self.screen = pygame.display.set_mode(screen_size)
        self.width = screen_size[0]
        self.height = screen_size[1]

        self.plane_size = plane_size
        self.row = plane_size[0]
        self.col = plane_size[1]
        #  格尺寸
        self.tile_size = tile_size
        #  偏移
        self.drift_H = font.get_sized_height(1)
        self.drift_W = -8 * self.tile_size
        self.drift_T = 0
        self.drift_L = 0
        #  计算实际边框位置
        self.frame_L = (self.width - self.col * self.tile_size - self.drift_W) / 2 + self.drift_L
        self.frame_R = self.frame_L + self.col * self.tile_size
        self.frame_T = (self.height - self.row * self.tile_size + self.drift_H) / 2 + self.drift_T
        self.frame_B = self.frame_T + self.row * self.tile_size

    def update_score_max(self):
        self.score_max = max(self.score, self.score_max)

    # 逻辑网格位置 转换为 屏幕坐标区域
    def get_tile_pos_dest(self, pos):
        x = pos[0]
        y = pos[1]
        px = self.frame_L + x * self.tile_size
        py = self.frame_T + y * self.tile_size
        return px, py, self.tile_size, self.tile_size

    def render(self, color_fruit, color_line, color_frame):
        pygame.draw.rect(self.screen, color_fruit, self.get_tile_pos_dest(self.fruit_pos))
        # 游戏框
        #  内框
        #   列
        for i in range(1, self.col):
            pygame.draw.line(self.screen, color_line,
                             (self.frame_L + self.tile_size * i, self.frame_T),
                             (self.frame_L + self.tile_size * i, self.frame_B),
                             3)
        #   行
        for i in range(1, self.row):
            pygame.draw.line(self.screen, color_line,
                             (self.frame_L, self.frame_T + self.tile_size * i),
                             (self.frame_R, self.frame_T + self.tile_size * i),
                             3)
        #  外框
        pygame.draw.line(self.screen, color_frame, (self.frame_L, self.frame_T), (self.frame_L, self.frame_B), 3)
        pygame.draw.line(self.screen, color_frame, (self.frame_L, self.frame_T), (self.frame_R, self.frame_T), 3)
        pygame.draw.line(self.screen, color_frame, (self.frame_R, self.frame_T), (self.frame_R, self.frame_B), 3)
        pygame.draw.line(self.screen, color_frame, (self.frame_L, self.frame_B), (self.frame_R, self.frame_B), 3)


class Snake:
    def __init__(self, game_info: SnakeGame):
        self.game = game_info
        self.pos = [self.game.plane_size[0] // 2, self.game.plane_size[1] // 2]
        self.direction = Direction.Stop
        self.tail = []
        self.tail_new = self.pos.copy()
        self.is_get_fruit = False

    def render(self, color_head, color_tail_base):
        # 头
        pygame.draw.rect(self.game.screen, color_head, self.game.get_tile_pos_dest(self.pos))
        # 尾
        color_tail = color_tail_base.copy()
        reduce_color = []
        for sub_pixel in color_tail:
            reduce_color.append(sub_pixel / (1 + len(self.tail)))
        for tail in self.tail:
            pygame.draw.rect(self.game.screen, color_tail, get_tile_pos_dest(tail))
            for sub_pixel in range(len(color_tail)):
                color_tail[sub_pixel] -= reduce_color[sub_pixel]  # 颜色渐变

    def move(self):
        # 移动
        if self.direction == Direction.Stop:
            return
        pos = self.pos.copy()
        if self.direction == Direction.Up:
            self.pos[1] -= 1
        elif self.direction == Direction.Right:
            self.pos[0] += 1
        elif self.direction == Direction.Down:
            self.pos[1] += 1
        elif self.direction == Direction.Left:
            self.pos[0] -= 1
        # 判断是否延长尾巴
        if self.tail_new:
            self.tail.append(self.tail_new.copy())
        if self.is_get_fruit:
            self.is_get_fruit = False
        else:
            del self.tail[0]
