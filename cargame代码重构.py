import pygame, sys, time, random

# pygame 初始化
pygame.init()
pygame.display.set_caption('逆行飙车')


# 常量类
class Constant:
    # 自定义事件
    OUT_OF_SIDE = pygame.USEREVENT + 1  # 碰到边界
    SPEED_UP = pygame.USEREVENT + 2  # 速度加快

    # 初始分数
    SCORE = 0

    # 帧数
    FPS = 30


# 屏幕
size = width, height = (351, 600)
screen = pygame.display.set_mode(size)  # 屏幕surface
screen_rect = screen.get_rect()  # 屏幕rect

# 背景图片
street_img = pygame.image.load('images/AnimatedStreet.png')  # 背景surface
street_rect = street_img.get_rect()  # 背景rect

# 字体和音乐
font_big = pygame.font.Font('fonts/Hellocute.ttf', 60)
font_small = pygame.font.Font('fonts/文道甜甜圈.ttf', 20)
font_game_over = font_big.render('Game Over !', True, (255, 0, 0))
font_game_over_rect = font_game_over.get_rect()
font_game_over_rect.center = screen_rect.center
font_score = font_small.render(f'SCORE: {Constant.SCORE}', True, (255, 255, 255))
font_score_rect = font_score.get_rect()
font_score_rect.x = 10
font_score_rect.y = 10

# 定时添加自定义事件
pygame.time.set_timer(Constant.SPEED_UP, 5000)  #

clock = pygame.time.Clock()


# 敌人类
class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()  # 调用父类方法初始化对象
        self.img = pygame.image.load('images/Enemy.png')
        self.surf = pygame.Surface((40, 48))
        self.rect = self.surf.get_rect(left=screen.get_width() / 2 - 22, top=0)
        self.speed = 5

    def move(self):
        global font_score
        self.rect.move_ip(0, self.speed)
        if self.rect.top > screen_rect.height:
            Constant.SCORE += 1
            font_score = font_small.render(f'SCORE: {Constant.SCORE}', True, (255, 255, 255))
            self.rect.top = 0
            self.rect.left = random.randint(60, 250)


# 玩家类
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()  # 调用父类方法初始化对象
        self.img = pygame.image.load('images/Player.png')
        self.rect = self.img.get_rect()
        self.rect.midbottom = screen_rect.midbottom
        self.speed = 5

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_UP] and self.rect.top >= 0:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[pygame.K_DOWN] and self.rect.bottom <= screen.get_height():
            self.rect.move_ip(0, self.speed)
        if pressed_keys[pygame.K_LEFT] and self.rect.left >= 33:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[pygame.K_RIGHT] and self.rect.right <= screen.get_width() - 34:
            self.rect.move_ip(self.speed, 0)
        # 超出边界
        if self.rect.left <= 50 or self.rect.right >= screen.get_width() - 52:
            pygame.event.post(pygame.event.Event(Constant.OUT_OF_SIDE))


# 游戏类
class Game:
    # 游戏初始化
    def __init__(self):
        self.player = Player()
        self.enemy = Enemy()
        # 定义敌人精灵组
        self.enemies = pygame.sprite.Group()
        self.enemies.add(self.enemy)

        # 定义所有精灵组
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.enemy)

    # 游戏运行/循环
    def run(self):

        # 播放背景音乐
        pygame.mixer.Sound("wave/background.mp3").play(-1)

        while 1:

            screen.blit(street_img, street_rect)
            screen.blit(font_score, font_score_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # 自定义事件触发
                if event.type == Constant.OUT_OF_SIDE:
                    print('超出边界了')
                if event.type == Constant.SPEED_UP:  # 敌人 加速 事件
                    # print('speed up')
                    self.enemy.speed += 1

            for sprite in self.all_sprites:
                screen.blit(sprite.img, sprite.rect)
                sprite.move()

            # 发生碰撞4种情况：

            # 1、敌人和玩家都存在
            # if pygame.sprite.spritecollide(player, enemies, False):
            #     print('撞车了')

            # 2、敌人消失
            # if pygame.sprite.spritecollide(player, enemies, True):
            #     print('撞车了')

            # 3、玩家和敌人都消失
            # if pygame.sprite.spritecollide(player, enemies, True):
            #     player.kill()   # 单独控制某个精灵消失
            #     print('撞车了')

            # 4、玩家消失
            if pygame.sprite.spritecollideany(self.player, self.enemies):
                # 延迟2秒 刷新退出

                # 播放碰撞声音
                pygame.mixer.Sound('wave/crash.mp3').play()
                # 玩家从所有精灵组移除
                self.player.kill()

                # 显示游戏结束任务
                screen.blit(font_game_over, font_game_over_rect)
                # 更新显示字体
                pygame.display.update()

                time.sleep(3)
                pygame.quit()
                sys.exit()

            pygame.display.flip()

            clock.tick(Constant.FPS)

if __name__ == '__main__':
    Game().run()
# 这个代码较为完整
