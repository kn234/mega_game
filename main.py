import pygame, random, sys

global screen
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
        self.image.fill((color))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, 480)


class MainChar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('122.png')
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (100, 130))
        self.rect = self.image.get_rect()
        self.rect.center = (75, 369)
        self.isJump = False
        self.jumpCount = 7

    def update(self):
        if self.isJump:
            if self.jumpCount >= -7:
                if self.jumpCount > 0:
                    self.rect.y -= self.jumpCount ** 2
                    self.jumpCount -= 1
                else:
                    self.rect.y += self.jumpCount ** 2
                    self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 7

    def slide(self):
        self.image = pygame.image.load("1222.png")
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (75, 380)


screen = pygame.display.set_mode((WIDTH, HEIGHT))


def main():
    pygame.init()
    global screen
    pygame.mixer.init()

    pygame.display.set_caption("My Game")

    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()

    obs_1 = Obstacle()

    char = MainChar()

    groundSprite = Ground()

    all_sprites.add(char, groundSprite, obs_1)

    score = 0

    running = True
    while running:
        clock.tick(FPS)
        scoreText = "Score: " + str(score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    char.isJump = True
                elif event.key == pygame.K_DOWN:
                    char.slide()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    char.__init__()
        guyCollide = pygame.sprite.collide_rect(char, obs_1)
        if guyCollide:
            running = False
        if obs_1.rect.right < 0:
            obs_1.reset()
            score += 1
            obs_1.speed *= score / 100 + 1
        font = pygame.font.Font(None, 30)
        screen.fill((255, 255, 255))
        score_text = font.render(scoreText, 1, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
    gameOver(score)


def gameOver(score):
    global screen
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    clock = pygame.time.Clock()

    ground = Ground()

    all_sprites = pygame.sprite.Group(ground)

    pygame.mouse.set_visible(False)

    keepGoing = True
    while keepGoing:

        clockTime = clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    keepGoing = False

        introString = []
        introString.append("Game Over")
        introString.append("Набрано очков: " + str(score))
        introString.append("Нажмите 'space', чтобы начать заново")
        i = 0
        ix = 100
        for i in range(len(introString)):
            font = pygame.font.Font(None, 30)
            introText = font.render(introString[i], 1, (0, 0, 0))
            screen.blit(introText, (WIDTH / 2 - 175, HEIGHT / 3 + ix))
            i += 1
            ix -= 25

        all_sprites.clear(screen, background)
        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()

    main()


def intro():
    pygame.init()
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

        clockTime = clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    keepGoing = False

        introString = []
        introString.append("Не прикасайся с блоками")
        introString.append("Нажми 'key_up'(стрелка вверх), чтобы прыгать")
        introString.append("Нажми 'key_down'(стрелка вниз), чтобы присесть")
        introString.append("Нажми 'space', чтобы продолжить")
        i = 0
        ix = 100
        for i in range(len(introString)):
            font = pygame.font.Font(None, 30)
            introText = font.render(introString[i], 1, (0, 0, 0))
            screen.blit(introText, ((WIDTH / 2) - 130, HEIGHT / 2 - ix))
            i += 1
            ix -= 25

        all_sprites.clear(screen, background)
        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()


def quit():
    pygame.display.quit()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    intro()
    main()
