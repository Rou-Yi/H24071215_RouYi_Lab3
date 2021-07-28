import pygame
import math
import os
from settings import RED, GREEN, PATH_1

pygame.init()
ENEMY_IMAGE = pygame.image.load(os.path.join("images", "enemy.png"))


class Enemy:
    def __init__(self, path):
        self.width = 40
        self.height = 50
        self.image = pygame.transform.scale(ENEMY_IMAGE, (self.width, self.height))
        self.health = 5
        self.max_health = 10
        self.path = path
        self.path_index = 0
        self.move_count = 0
        self.stride = 4
        self.x, self.y = self.path[0]

    def draw(self, win):
        # draw enemy
        win.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        # draw enemy health bar
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        """
        Draw health bar on an enemy
        :param win: window
        :return: None
        """
        rect_x = self.x - self.width // 2
        rect_y = self.y - self.height // 2 - 5
        # Red health bar
        pygame.draw.rect(win, RED, [rect_x, rect_y, self.width, 5])
        # Green health bar
        health_bar_width = self.width / self.max_health * self.health
        pygame.draw.rect(win, GREEN, [rect_x, rect_y, health_bar_width, 5])

    def move(self):
        """
        Enemy move toward path points every frame
        :return: None
        """
        if self.path_index < len(self.path):
            ax, ay = self.path[self.path_index]    # original position
            bx, by = self.path[self.path_index+1]  # next position
            distance = math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)
            max_count = int(distance / self.stride)  # total footsteps

            while self.move_count < max_count:
                unit_vector_x = (bx - ax) / distance
                unit_vector_y = (by - ay) / distance
                delta_x = unit_vector_x * self.stride
                delta_y = unit_vector_y * self.stride

                # update the coordinate and the counter
                self.x += delta_x
                self.y += delta_y
                self.move_count += 1

            self.move_count = 0  # set 0 for the next point move
            self.path_index += 1  # update the self.path_index


class EnemyGroup:
    def __init__(self):
        self.gen_count = 0
        self.gen_period = 120   # (unit: frame)
        self.reserved_members = [Enemy(PATH_1) for i in range(3)]  # 初始三隻敵人給定 PATH_1
        self.expedition = []

    def campaign(self):
        """
        Send an enemy to go on an expedition once 120 frame
        :return: None
        """
        # 當 self.reserved_members 還有未送出的敵人時，計算每到 120 幀(?) 送一隻出去 self.expedition
        if len(self.reserved_members) > 0:
            if self.gen_count > self.gen_period:
                self.expedition.append(self.reserved_members.pop())
                self.gen_count = 0
            else:
                # 幀數計算 : 數字越大敵人間隔越小
                self.gen_count += 25

    def generate(self, num, path_):
        """
        Generate the (3) enemies in this wave
        :param num: enemy number
        :return: None
        """
        for i in range(num):
            self.reserved_members.append(Enemy(path_))

    def get(self):
        """
        Get the enemy list
        """
        return self.expedition

    def is_empty(self):
        """
        Return whether the enemy is empty (so that we can move on to next wave)
        """
        return False if self.reserved_members else True

    def retreat(self, enemy):
        """
        Remove the enemy from the expedition
        :param enemy: class Enemy()
        :return: None
        """
        self.expedition.remove(enemy)
