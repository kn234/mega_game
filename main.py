import pygame
import random
import sys
global status


score_list = list()
f = open('scores.txt', 'r')
for i in f:
    score_list.append(i)
score_list[0] = int(score_list[0])
WIDTH = 920
HEIGHT = 480
FPS = 60
score = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
speed = 15
ground_speed = 10
cX = 150
cY = 375


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(f"fireball_sprite/{i}.jpg") for i in range(1, 6)
                       for x in range(6)]
        for im in self.images:
            im.set_colorkey((38, 36, 37))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(1000, 1400), 375)
        self.maxPosX = self.rect.center[1] * 2

    cordX = 1000
    cordY = 375

    def update(self):
        global score, speed, ground_speed
        self.cordX -= speed
        if self.cordX < -40:
            score += 1
            speed += 1 / 20 #Возможно стоит переделать 
            # ground_speed *= score / 1000 + 1

            obPlace = random.randint(0, 1)
            if obPlace == 0:
                self.cordY = 375
                self.cordX = random.randint(1000, 1400)
            else:
                self.cordY = 290
                self.cordX = random.randint(1000, 1400)
        else:
            self.index += 1
            if self.index >= 30:
                self.index = 0
            self.image = self.images[self.index]
            self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * 0.2, 40))
            self.rect = self.image.get_rect()
            self.rect.center = (self.cordX, self.cordY)


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('ground.png')
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.y = 395

    def update(self):
        global status, ground_speed
        if status == 'Intro':
            pass
        else:
            self.rect.x -= ground_speed
            if self.rect.right < 0:
                self.rect.left = self.image.get_size()[0] + self.image.get_size()[0] - \
                    (0 - self.rect.right)


class BackG(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bg.png')
        self.rect = self.image.get_rect()
        self.rect.center = (50, 200)


class MainChar(pygame.sprite.Sprite):
    cordX_2, cordY_2 = 150, 360

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(f"sprites/{i}.png") for i in range(1, 11) for x in range(3)]
        self.index = 0
        self.index_1 = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.cordX, self.cordY = 75, 360
        self.rect.center = (self.cordX, self.cordY)
        self.isJump = False
        self.jumpCount = 9
        self.isSlide = False

    def update(self):
        global status
        if status == 'Intro':
            self.image = self.images[self.index]
            self.image = pygame.transform.scale(self.image,
                                                (self.image.get_size()[0] * 0.6, 140))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.cordX, 290
            self.index += 1
            if self.index >= 30:
                self.index = 0
            elif self.rect.x < WIDTH + 100:
                self.cordX += 12
            else:
                self.cordX = -100
        else:
            self.index += 1
            if self.index >= 30:
                self.index = 0
            self.image = self.images[self.index]
            self.image.set_colorkey((255, 255, 255))
            self.image = pygame.transform.scale(self.image,
                                                (self.image.get_size()[0] * 0.6, 140))
            self.rect = self.image.get_rect()
            self.rect.center = (self.cordX_2, self.cordY_2)
            if self.isJump:
                if self.jumpCount >= -9:
                    if self.jumpCount > 0:
                        self.image = pygame.image.load("sprites/6.png")
                        self.image = pygame.transform.scale(self.image,
                                                            (self.image.get_size()[0] * 0.6, 140))
                        self.rect = self.image.get_rect()
                        self.cordY_2 -= self.jumpCount * self.jumpCount * 0.6
                        self.rect.center = (self.cordX_2, self.cordY_2)
                        self.jumpCount -= 1
                    else:
                        self.image = pygame.image.load("sprites/6.png")
                        self.image = pygame.transform.scale(self.image,
                                                            (self.image.get_size()[0] * 0.6, 140))
                        self.rect = self.image.get_rect()
                        self.cordY_2 += self.jumpCount * self.jumpCount * 0.6
                        self.rect.center = (self.cordX_2, self.cordY_2)
                        self.jumpCount -= 1
                else:
                    self.isJump = False
                    self.jumpCount = 9
            if self.isSlide:
                self.image = pygame.transform.scale(self.image,
                                                    (self.image.get_size()[0] * 0.8, 110))
                self.rect.center = (self.cordX_2 + 10, self.cordY_2 + 30)


class SmokeSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(f'smoke_sprite/{i}.png') for i in range(1, 11)
                       for x in range(3)]
        for n in self.images:
            n.set_colorkey((4, 142, 176))
        self.index = -1
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (-200, -200)
        self.smoke_bool = False

    x = 0
    y = 0

    def update(self):
        global cX, cY, my_bool
        if self.smoke_bool:
            self.index += 1
            if self.index == 0:
                self.x = cX
                self.y = cY
            if self.index >= 30:
                self.index = -1
                self.smoke_bool = False
            if self.index != -1:
                self.image = self.images[self.index]
                self.image = pygame.transform.scale(self.image, (200, 150))
                if self.index > 5:
                    self.rect = self.image.get_rect()
                    self.rect.center = (self.x, self.y)
                    self.x -= 10
                else:
                    self.rect = self.image.get_rect()
                    self.rect.center = (self.x, self.y)
        else:
            self.rect.center = (-230, -230)


def main():
    global screen, status, score, score_list, cY, cX
    pygame.init()
    status = 'Main'
    pygame.mixer.init()
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    obs_1 = Obstacle()
    char = MainChar()
    ground = Ground()
    ground_2 = Ground()
    ground_3 = Ground()
    ground_2.rect.left = (ground_2.image.get_size()[0])
    ground_3.rect.left = ground_2.image.get_size()[0] + ground_2.image.get_size()[0]
    smoke = SmokeSprite()
    bg = BackG()
    all_sprites.add(bg, ground, ground_2, ground_3, char, smoke, obs_1)
    running = True
    score = 0
    while running:
        global cX, cY
        clock.tick(FPS)
        score_text = "Score: " + str(score)
        record_text = "Record: " + str(score_list[0])
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    char.isJump = True
                elif event.key == pygame.K_DOWN:
                    smoke.smoke_bool = True
                    smoke.index = -1
                    if char.isJump:
                        cY = char.rect.center[1] + 50
                    else:
                        cX = char.rect.center[0]
                        cY = char.rect.center[1]
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    cX = char.rect.center[0]
                    cY = char.rect.center[1] - 30
                    char.isSlide = False
                    smoke.smoke_bool = True
                    smoke.index = -1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            char.isSlide = True
        guyCollide = pygame.sprite.collide_rect(char, obs_1)
        if guyCollide:
            running = False
        font = pygame.font.Font(None, 30)
        score_text = font.render(score_text, True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        font_2 = pygame.font.Font(None, 30)
        record_text = font_2.render(record_text, True, (0, 0, 0))
        all_sprites.draw(screen)
        screen.blit(score_text, (10, 10))
        screen.blit(record_text, (10, 30))
        all_sprites.update()
        pygame.display.flip()

    score_list.append(score)
    if int(score_list[0]) <= int(score_list[1]):
        score_list[0] = score_list[1]
        score_list.remove(score_list[1])
    else:
        score_list.remove(score_list[1])
    f = open('scores.txt', 'w')
    for i in score_list:
        f.write(str(i))
    f.close()
    game_over(score, score_list[0])


def game_over(g_score, record):
    global screen, speed, ground_speed
    pygame.display.set_caption("My Game")
    speed = 15
    ground_speed = 10
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    image = pygame.image.load('gameover_images/3.png')
    image = pygame.transform.scale(image, (image.get_size()[0] * 0.7, image.get_size()[1] * 0.7))
    image_1 = pygame.image.load('gameover_images/3.png')
    image_1 = pygame.transform.scale(image_1, (image.get_size()[0], image.get_size()[1]))
    screen.blit(image, (-40, -75))
    screen.blit(image_1, (600, 200))
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    # ground = Ground()
    # all_sprites = pygame.sprite.Group(ground)
    keepGoing = True
    while keepGoing:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    keepGoing = False

        intro_string = list()
        intro_string.append("Набрано очков: " + str(g_score))
        intro_string.append("Ваш рекорд: " + str(record))
        intro_string.append("Нажмите 'space', чтобы начать заново")
        i = 0
        ix = 100
        for i in range(len(intro_string)):
            font = pygame.font.Font(None, 40)
            intro_text = font.render(intro_string[i], True, (0, 0, 0))
            screen.blit(intro_text, (WIDTH / 2 - 280, HEIGHT / 3 + ix))
            i += 1
            ix -= 25
        f_1 = pygame.font.Font(None, 70)
        game_over_text = 'GAME OVER'
        game_over_text = f_1.render(game_over_text, True, (0, 0, 0))
        screen.blit(game_over_text, (WIDTH / 2 - 175, 100))
        # all_sprites.clear(screen, background)
        # all_sprites.update()
        # all_sprites.draw(screen)
        pygame.display.flip()

    main()


def intro():
    global status, screen
    pygame.init()
    pygame.display.set_caption("My Game")
    status = 'Intro'
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    clock = pygame.time.Clock()

    char = MainChar()
    ground = Ground()
    ground_2 = Ground()
    bg = BackG()
    ground_2.rect.left = (ground_2.image.get_size()[0])
    all_sprites = pygame.sprite.Group(bg, ground, ground_2, char)

    pygame.mouse.set_visible(True)

    keepGoing = True
    while keepGoing:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    keepGoing = False

        intro_string = list()
        intro_string.append("Не соприкасайся с препятствиями")
        intro_string.append("'key_up'(стрелка вверх), чтобы прыгать")
        intro_string.append("'key_down'(стрелка вниз), чтобы присесть")
        intro_string.append("'space', чтобы продолжить")
        # all_sprites.clear(screen, background)
        all_sprites.draw(screen)
        i = 0
        ix = 160
        for i in range(len(intro_string)):
            font = pygame.font.Font(None, 40)
            introText = font.render(intro_string[i], True, (0, 0, 0))
            screen.blit(introText, ((WIDTH / 2) - 270, HEIGHT / 2 - ix))
            i += 1
            ix -= 40

        all_sprites.update()
        pygame.display.flip()


def quit_game():
    pygame.display.quit()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    intro()
    main()
