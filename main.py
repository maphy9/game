import pygame
from sys import exit
from random import randint
from math import sin


# screen setting
pygame.init()
screen = pygame.display.set_mode((720, 480))
pygame.display.set_caption("LOVE")
pygame_icon = pygame.image.load("./images/logo.png").convert_alpha()
pygame.display.set_icon(pygame_icon)


# frames setting
clock = pygame.time.Clock()


# score
score = 0


# music
bgMusic = pygame.mixer.Sound("./audio/bg.wav")
bgMusic.set_volume(0.3)
bgMusic.play(loops=-1)


# text
font = pygame.font.Font("./fonts/Timmy-Regular.ttf", 50)
mainScreenText = font.render("Game about LOVE!", False, "Black")
mainScreenText_rect = mainScreenText.get_rect(midbottom = (360, 120))
startText = font.render("To start press ENTER!", False, "Black")
startText_rect = startText.get_rect(midbottom = (360, 240))
scoreText = font.render(f"Your score is {score}", False, "Black")
scoreText_rect = scoreText.get_rect(midbottom = (360, 80))


# game state
isRunning = False


# scene
bg_surface = pygame.image.load("./images/bg.png").convert()
floor_surface = pygame.image.load("./images/floor.png").convert()
floor_rect = floor_surface.get_rect(topleft = (0, 400))


# player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.playerAnimationIndex = 0
        self.player1 = pygame.image.load("./images/player1.png").convert_alpha()
        self.player2 = pygame.image.load("./images/player2.png").convert_alpha()
        self.player3 = pygame.image.load("./images/player3.png").convert_alpha()
        self.playerAnimations = [self.player1, self.player2]
        self.image = self.playerAnimations[int(self.playerAnimationIndex) % 2]
        self.rect = self.image.get_rect(midbottom = (100, 400))
        self.speed = 20
        self.jumpSound = pygame.mixer.Sound('./audio/jump.mp3')
        self.jumpSound.set_volume(0.2)

    def jump(self):
        if self.rect.bottom >= 400: 
            self.rect.bottom = 400
            self.speed = 0
        elif keys[pygame.K_SPACE] and self.rect.bottom < 400: 
            self.speed -= 1
        else: self.speed -= 2
        
        if self.rect.bottom == 400 and keys[pygame.K_SPACE]:
            self.speed = 20
            self.jumpSound.play()
        
        self.rect.bottom -= self.speed
    
    def handleAnimation(self):
        if self.rect.bottom >= 400:
            self.image = self.playerAnimations[int(self.playerAnimationIndex) % 2]
            self.playerAnimationIndex += 0.1
        else:
            self.image = self.player3
        
    def restart(self):
        self.rect.bottom = 400
    
    def update(self):
        if isRunning:
            self.jump()
            self.handleAnimation()
        else:
            self.restart()

playerGroup = pygame.sprite.GroupSingle()
playerGroup.add(Player())


# enemies
class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.enemyAnimationIndex = 0
        self.type = type
        if type == "walking": 
            self.animation1 = pygame.image.load("./images/walkingCat1.png").convert_alpha()
            self.animation2 = pygame.image.load("./images/walkingCat2.png").convert_alpha()
            self.y = 400
        elif type == "flying":
            self.animation1 = pygame.image.load("./images/flyingCat1.png").convert_alpha()
            self.animation2 = pygame.image.load("./images/flyingCat2.png").convert_alpha()
            self.y = 120
            self.sinValue = 0
        self.frames = [self.animation1, self.animation2]
        self.image = self.frames[int(self.enemyAnimationIndex) % 2]
        self.rect = self.image.get_rect(bottomleft = (randint(720, 960), self.y))
    
    def animate(self):
        self.enemyAnimationIndex += 0.1
        self.image = self.frames[int(self.enemyAnimationIndex) % 2]

    def move(self):
        global score, scoreText
        if self.rect.right <= 0:
            score += 1
            scoreText = font.render(f"Your score is {score}", False, "Black")
            self.kill()

        if self.type == "walking":
            self.rect.left -= 8
        elif self.type == "flying":
            self.rect.left -= 12
            self.rect.bottom += int(5 * sin(self.sinValue))
            self.sinValue += 0.1

    def update(self):
        self.animate()
        self.move()
enemyGroup = pygame.sprite.Group()


# timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1000)

while True:
    clock.tick(60)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if isRunning:
            if event.type == enemy_timer:
                if randint(1, 4) % 3 == 0:
                    enemyGroup.add(Enemy("flying"))
                else:
                    enemyGroup.add(Enemy("walking"))

    # global things
    screen.blit(bg_surface, (0, 0))
    keys = pygame.key.get_pressed()


    if isRunning:
        # put everything on screen   
        screen.blit(floor_surface, (0, 400))
        screen.blit(scoreText, scoreText_rect)
        enemyGroup.draw(screen)
        enemyGroup.update()
        playerGroup.draw(screen)
        playerGroup.update()

        # check collision
        if pygame.sprite.spritecollide(playerGroup.sprite, enemyGroup, False):
            isRunning = False
    else:
        screen.blit(mainScreenText, mainScreenText_rect)
        screen.blit(startText, startText_rect)
        screen.blit(scoreText, scoreText_rect)
        playerGroup.update()

        if keys[pygame.K_RETURN]: 
            enemyGroup.empty()
            score = 0
            scoreText = font.render(f"Your score is {score}", False, "Black")
            isRunning = True


    pygame.display.update()