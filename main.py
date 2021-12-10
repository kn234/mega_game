import pygame
import random
import sys

global screen, status

WIDTH = 920
HEIGHT = 480
FPS = 60


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.x, self.y = random.randint(800, 1500), 375
        self.rect.center = (self.x, self.y)
        self.maxPosX = self.x * 2
        self.speed = 15

    def update(self):
        self.rect.x -= self.speed

    def reset(self):
        obPlace = random.randint(0, 1)
        if obPlace == 0:
            self.rect.center = (random.randint(self.x, self.maxPosX), self.y)
        else:
            self.rect.center = (random.randint(self.x, self.maxPosX), self.y - 75)


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        color = (0, 0, 0)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH, 100))
        rect = pygame.Rect(20, 20, 20, 20)
        pygame.draw.rect(self.image, color, rect, 1)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, 480)


class MainChar(pygame.sprite.Sprite):
    cordX_2, cordY_2 = 150, 360

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(f"sprites/{i}.jpg") for i in range(1, 11) for x in range(3)]
        self.sl_images = [pygame.image.load(f"sprites1/slide{i}.jpg") for i in range(1, 3) for x in range(15)]
        for im in self.images:
            im.set_colorkey((255, 255, 255))
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
            self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * 0.6, 140))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.cordX, 300
            self.index += 1
            if self.index >= 30:
                self.index = 0
            elif self.rect.x < WIDTH + 100:
                self.cordX += 13
            else:
                self.cordX = -100
        else:
            self.index += 1
            if self.index >= 30:
                self.index = 0
            self.image = self.images[self.index]
            self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * 0.6, 140))
            self.rect = self.image.get_rect()
            self.rect.center = (self.cordX_2, self.cordY_2)
            if self.isJump:
                if self.jumpCount >= -9:
                    if self.jumpCount > 0:
                        # Вот сюда пихнуть пнг прыжка
                        self.image = pygame.image.load("sprites/6.jpg")
                        self.image.set_colorkey((255, 255, 255))
                        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * 0.6, 140))
                        self.rect = self.image.get_rect()
                        self.cordY_2 -= self.jumpCount * self.jumpCount * 0.5
                        self.rect.center = (self.cordX_2, self.cordY_2)
                        self.jumpCount -= 1
                    else:
                        # Вот сюда пихнуть пнг прыжка
                        self.image = pygame.image.load("sprites/6.jpg")
                        self.image.set_colorkey((255, 255, 255))
                        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * 0.6, 140))
                        self.rect = self.image.get_rect()
                        self.cordY_2 += self.jumpCount * self.jumpCount * 0.5
                        self.rect.center = (self.cordX_2, self.cordY_2)
                        self.jumpCount -= 1
                else:
                    self.isJump = False
                    self.jumpCount = 9
            if self.isSlide:
                self.index += 1
                if self.index >= 30:
                    self.index = 0
                self.image = self.sl_images[self.index_1]
                self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * 0.63, 100 * 0.88))
                self.rect = self.image.get_rect()
                self.rect.center = (self.cordX_2, self.cordY_2 + 33)


def main():
    pygame.init()
    global screen, status
    status = 'Main'
    pygame.mixer.init()
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    obs_1 = Obstacle()
    char = MainChar()
    ground = Ground()
    all_sprites.add(char, ground, obs_1)
    score = 0
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True
    while running:
        clock.tick(FPS)
        scoreText = "Score: " + str(score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    char.isJump = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    char.isSlide = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            char.isSlide = True
        guyCollide = pygame.sprite.collide_rect(char, obs_1)
        if guyCollide:
            running = False
        if obs_1.rect.right < 0:
            obs_1.reset()
            score += 1
            obs_1.speed *= score / 1000 + 1
        font = pygame.font.Font(None, 30)
        screen.fill((255, 255, 255))
        score_text = font.render(scoreText, True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()

    game_over(score)


def game_over(score):
    global screen
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    clock = pygame.time.Clock()
    ground = Ground()
    all_sprites = pygame.sprite.Group(ground)
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
        intro_string.append("Game Over")
        intro_string.append("Набрано очков: " + str(score))
        intro_string.append("Нажмите 'space', чтобы начать заново")
        i = 0
        ix = 100
        for i in range(len(intro_string)):
            font = pygame.font.Font(None, 30)
            introText = font.render(intro_string[i], True, (0, 0, 0))
            screen.blit(introText, (WIDTH / 2 - 175, HEIGHT / 3 + ix))
            i += 1
            ix -= 25

        all_sprites.clear(screen, background)
        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()

    main()


def intro():
    global status
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.init()
    status = 'Intro'
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    clock = pygame.time.Clock()

    char = MainChar()
    ground = Ground()

    ground.rect.top = char.rect.bottom

    all_sprites = pygame.sprite.Group(char, ground)

    pygame.mouse.set_visible(False)

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
        intro_string.append("Не прикасайся с блоками")
        intro_string.append("Нажми 'key_up'(стрелка вверх), чтобы прыгать")
        intro_string.append("Нажми 'key_down'(стрелка вниз), чтобы присесть")
        intro_string.append("Нажми 'space', чтобы продолжить")
        i = 0
        ix = 100
        for i in range(len(intro_string)):
            font = pygame.font.Font(None, 30)
            introText = font.render(intro_string[i], True, (0, 0, 0))
            screen.blit(introText, ((WIDTH / 2) - 130, HEIGHT / 2 - ix))
            i += 1
            ix -= 25


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
