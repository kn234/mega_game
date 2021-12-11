import pygame
import random
import sys
global screen, status


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


class Obstacle(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(f"fire_ball_sprite/{i}.jpg") for i in range(1, 6)
                       for x in range(12)]
        for im in self.images:
            im.set_colorkey((38, 36, 37))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(1000, 1400), 375)
        self.maxPosX = self.rect.center[1] * 2
        self.speed = 15

    cordX = 1000
    cordY = 375

    def update(self):
        global score
        self.cordX -= self.speed
        if self.cordX < -40:
            score += 1
            self.speed *= score / 1000 + 1
            obPlace = random.randint(0, 1)
            if obPlace == 0:
                self.cordY = 375
                self.cordX = random.randint(1000, 1400)
            else:
                self.cordY = 300
                self.cordX = random.randint(1000, 1400)
        else:
            self.index += 1
            if self.index >= 60:
                self.index = 0
            self.image = self.images[self.index]
            self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * 0.2, 40))
            self.rect = self.image.get_rect()
            self.rect.center = (self.cordX, self.cordY)


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('floor.png')
        self.image = pygame.transform.scale(self.image, (920, 115))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH, 479)
        self.speed = 15

    def update(self):
        global status
        if status == 'Intro':
            self.rect.center = (WIDTH / 2, 479)
        else:
            self.rect.x -= 10
            if self.rect.right == 0:
                self.rect.left = WIDTH

class Ground_2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('floor.png')
        self.image = pygame.transform.scale(self.image, (920, 115))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (0, 479)
        self.speed = 15

    def update(self):
        global status
        if status == 'Intro':
            self.rect.center = (WIDTH, -400)
        else:
            self.rect.x -= 10
            if self.rect.right == 0:
                self.rect.left = WIDTH


class MainChar(pygame.sprite.Sprite):
    cordX_2, cordY_2 = 150, 360

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(f"sprites/{i}.jpg") for i in range(1, 11) for x in range(3)]
        for im in self.images:
            im.set_colorkey((255, 255, 255))
        self.index = 0
        self.index_1 = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.cordX, self.cordY = 75, 360
        self.rect.center = (self.cordX, self.cordY)
        self.isJump = False
        self.jumpCount = 10
        self.isSlide = False

    def update(self):
        global status
        if status == 'Intro':
            self.image = self.images[self.index]
            self.image.set_colorkey((255, 255, 255))
            self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * 0.6, 140))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.cordX, 290
            self.index += 1
            if self.index >= 30:
                self.index = 0
            elif self.rect.x < WIDTH + 100:
                self.cordX += 11
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
                if self.jumpCount >= -10:
                    if self.jumpCount > 0:
                        # Вот сюда пихнуть пнг прыжка
                        self.image = pygame.image.load("sprites/6.jpg")
                        self.image.set_colorkey((255, 255, 255))
                        self.image = pygame.transform.scale(self.image,
                                                            (self.image.get_size()[0] * 0.6, 140))
                        self.rect = self.image.get_rect()
                        self.cordY_2 -= self.jumpCount * self.jumpCount * 0.5
                        self.rect.center = (self.cordX_2, self.cordY_2)
                        self.jumpCount -= 1
                    else:
                        # Вот сюда пихнуть пнг прыжка
                        self.image = pygame.image.load("sprites/6.jpg")
                        self.image.set_colorkey((255, 255, 255))
                        self.image = pygame.transform.scale(self.image,
                                                            (self.image.get_size()[0] * 0.6, 140))
                        self.rect = self.image.get_rect()
                        self.cordY_2 += self.jumpCount * self.jumpCount * 0.5
                        self.rect.center = (self.cordX_2, self.cordY_2)
                        self.jumpCount -= 1
                else:
                    self.isJump = False
                    self.jumpCount = 10
            if self.isSlide:
                self.image = pygame.transform.scale(self.image,
                                                    (self.image.get_size()[0] * 0.8, 110))
                # self.index += 1
                # if self.index >= 30:
                #     self.index = 0
                # self.image = self.images[self.index]
                # self.image = pygame.transform.scale(self.image,
                #                                     (self.image.get_size()[0] * 0.4, 100))
                # self.rect = self.image.get_rect()
                self.rect.center = (self.cordX_2 + 10, self.cordY_2 + 30)


class SmokeSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(f'smoke_sprite/{i}.png')for i in range(1, 11)
                       for x in range(3)]
        for n in self.images:
            n.set_colorkey((4, 142, 176))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (-200, -200)
        self.smoke_bool = False

    def update(self):
        if self.smoke_bool:
            self.index += 1
            if self.index >= 30:
                self.index = 0
                self.smoke_bool = False
            self.image = self.images[self.index]
            self.image = pygame.transform.scale(self.image, (200, 150))
            self.rect = self.image.get_rect()
            self.rect.center = (150, 375)


def main():
    pygame.init()
    global screen, status, score, score_list
    status = 'Main'
    pygame.mixer.init()
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    obs_1 = Obstacle()
    char = MainChar()
    ground = Ground()
    ground_2 = Ground_2()
    smoke = SmokeSprite()
    all_sprites.add(char, ground, ground_2, obs_1, smoke)
    running = True
    score = 0
    while running:
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
                    all_sprites.add(smoke)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    char.isSlide = False
                    smoke.smoke_bool = True
                    all_sprites.add(smoke)
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
        screen.blit(score_text, (10, 10))
        screen.blit(record_text, (10, 30))
        if not smoke.smoke_bool:
            all_sprites.remove(smoke)
        all_sprites.draw(screen)
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
    global screen
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))
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
        screen.blit(game_over_text, (WIDTH/ 2 - 175, 100))
        # all_sprites.clear(screen, background)
        # all_sprites.update()
        # all_sprites.draw(screen)

        pygame.display.flip()

    main()


def intro():
    global status, screen
    pygame.init()
    status = 'Intro'
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    clock = pygame.time.Clock()

    char = MainChar()
    ground = Ground()
    ground_2 = Ground_2()


    all_sprites = pygame.sprite.Group(char, ground, ground_2)

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

        intro_string = []
        intro_string.append("Не соприкасайся с препятствиями")
        intro_string.append("'key_up'(стрелка вверх), чтобы прыгать")
        intro_string.append("'key_down'(стрелка вниз), чтобы присесть")
        intro_string.append("'space', чтобы продолжить")
        i = 0
        ix = 160
        for i in range(len(intro_string)):
            font = pygame.font.Font(None, 40)
            introText = font.render(intro_string[i], True, (0, 0, 0))
            screen.blit(introText, ((WIDTH / 2) - 270, HEIGHT / 2 - ix))
            i += 1
            ix -= 40
        all_sprites.clear(screen, background)
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()


def quit_game():
    pygame.display.quit()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    intro()
    main()
