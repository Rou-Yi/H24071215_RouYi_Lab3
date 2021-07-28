import pygame
from enemy import EnemyGroup
import os
from settings import WIN_WIDTH, WIN_HEIGHT, FPS, PATH_1, PATH_2

# initialization
pygame.init()
# load image
BACKGROUND_IMAGE = pygame.image.load(os.path.join("images", "Map.png"))
HP_IMAGE = pygame.image.load(os.path.join("images", "hp.png"))
HP_GRAY_IMAGE = pygame.image.load(os.path.join("images", "hp_gray.png"))
# set the title and icon
pygame.display.set_caption("My TD game")


class Game:
    def __init__(self):
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.bg_image = pygame.transform.scale(BACKGROUND_IMAGE, (WIN_WIDTH, WIN_HEIGHT))
        self.hp_images = [pygame.transform.scale(HP_IMAGE, (40, 40)),
                          pygame.transform.scale(HP_GRAY_IMAGE, (40, 40))]
        self.enemies = EnemyGroup()
        self.base = pygame.Rect(430, 90, 195, 130)
        self.wave_parameter = 1  # set wave parameter for change_path()

    def collide_base(self, enemy):
        """
        Return True if the enemy collide with base.
        :param enemy: object (Enemy())
        :return: Bool
        """
        x, y = self.base.center
        width, height = self.base.w, self.base.h
        if x - width // 2 < enemy.x < x + width // 2 and y - height // 2 < enemy.y < y + height // 2:
            return True
        return False

    def draw(self):
        """
        Draw everything in this method.
        :return: None
        """
        # draw background
        self.win.blit(self.bg_image, (0, 0))
        # draw enemy
        for en in self.enemies.get():
            en.draw(self.win)

    # change_path() function is for BONUS
    def change_path(self):
        """
        初始 self.wave_num 設置為 1
        當 wave_num 無法被 2 整除時, self.path 選擇從左側出發的 PATH_1
        當 wave_num 可以被 2 整除時, self.path 選擇從右側出發的 PATH_2
        """
        self.wave_parameter += 1
        if self.wave_parameter % 2 != 0:
            print("Change to PATH 1")
            return PATH_1
        else:
            print("Change to PATH 2")
            return PATH_2

    def game_run(self):
        # game loop
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(10)
            # event loop
            for event in pygame.event.get():
                # quit the game
                if event.type == pygame.QUIT:
                    run = False
                # generate enemy of the next wave
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n and self.enemies.is_empty():
                        # use self.change_path() to change the path for the new wave
                        self.enemies.generate(3, self.change_path())

            # enemy loop
            self.enemies.campaign()
            for en in self.enemies.get():
                en.move()
                # delete the object when it reach the base
                if self.collide_base(en):
                    self.enemies.retreat(en)

            # draw everything
            self.draw()
            pygame.display.update()
        pygame.quit()


if __name__ == '__main__':
    covid_game = Game()
    covid_game.game_run()