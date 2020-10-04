import pygame as pg
from pygame import mixer
import numpy as np

class ShootingGame:
    def __init__(self):
        pg.init()
        # set parameters
        self.setScreen()
        self.setPlayerState()
        self.setEnemyState()
        self.setBulletState()
        self.setTextManager()

        # GAME PARAMETERS
        self.PLAYER_DELTA = 5
        self.ENEMY_DELTA = 7

        # keep window running
        self.running = True

    def setScreen(self):
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1280, 720
        self.screen = pg.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        # title and display
        pg.display.set_caption('Dummy Game')
        icon = pg.image.load('images/project.png')
        pg.display.set_icon(icon)

        # background create
        self.backgroundImg = pg.image.load('images/background_small.jpg')

        # background music
        mixer.music.load('music/Lush-pad-synth-sound-96.mp3')
        mixer.music.set_volume(0.1)
        mixer.music.play(-1)

    def setTextManager(self):
        # score manager
        self.player_score = 0
        self.font = pg.font.Font('freesansbold.ttf', 32)
        self.textX, self.textY = 10, 10

    def showScore(self, x, y):
        score = self.font.render("Kills: " + str(self.player_score), True, (255, 0, 0))
        # draw score of the player
        self.screen.blit(score, (x, y))

    def setPlayerState(self):
        # player create
        self.playerImg = pg.image.load('images/spaceship.png')
        self.PLAYER_ICON_SIZE = 64
        self.playerX, self.playerY = self.WINDOW_WIDTH // 2 - self.PLAYER_ICON_SIZE, self.WINDOW_HEIGHT - self.PLAYER_ICON_SIZE
        self.playerx_delta = 0
        self.playery_delta = 0

    def player(self, x, y):
        # draw image of the player
        self.screen.blit(self.playerImg, (x, y))

    def setEnemyState(self):
        # enemy create
        self.enemyImg = pg.image.load('images/ufo.png')
        self.ENEMY_ICON_SIZE = 64
        self.ENEMY_OSCILATION_AMPLITUDE = 80
        self.enemyX, self.enemyY = np.random.randint(0, self.WINDOW_WIDTH - self.ENEMY_ICON_SIZE), np.random.randint(
            self.ENEMY_OSCILATION_AMPLITUDE, self.WINDOW_HEIGHT // 4)
        self.enemyx_delta = 7
        self.enemyy_delta = 0
        self.enemy_oscilation_angle = 0

    def enemy(self, x, y):
        # draw image of the enemy
        self.screen.blit(self.enemyImg, (x, y))

    def setBulletState(self):
        # bullet create
        # ready state - bullet is ready for fire
        # fire state - it is moving
        self.bulletImg = pg.image.load('images/bullet.png')
        self.BULLET_ICON_SIZE = 24
        self.bulletX, self.bulletY = self.WINDOW_WIDTH // 2 - self.BULLET_ICON_SIZE, self.WINDOW_HEIGHT - self.BULLET_ICON_SIZE
        self.bulletx_delta = 0
        self.bullety_delta = 10
        self.bullet_state = 'ready'

    # check collison
    def isCollison(self):
        dist = np.sqrt(np.power(self.bulletX - self.enemyX, 2) + np.power(self.bulletY - self.enemyY, 2))
        if dist <= self.BULLET_ICON_SIZE:
            return True
        return False

    def fire_bullet(self, x, y):
        self.bullet_state = 'fire'
        # draw image of the bullet
        self.screen.blit(self.bulletImg, (x + self.PLAYER_ICON_SIZE // 2 - self.BULLET_ICON_SIZE // 2, y - self.BULLET_ICON_SIZE))

    def StartGame(self):
        while self.running:
            # set screen color to black
            self.screen.fill((0, 0, 0))
            # set background image
            self.screen.blit(self.backgroundImg, (0, 0))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        self.playerx_delta = -self.PLAYER_DELTA
                    if event.key == pg.K_RIGHT:
                        self.playerx_delta = self.PLAYER_DELTA
                    if event.key == pg.K_UP:
                        self.playery_delta = -self.PLAYER_DELTA
                    if event.key == pg.K_DOWN:
                        self.playery_delta = self.PLAYER_DELTA
                    if event.key == pg.K_SPACE:
                        if self.bullet_state == 'ready':
                            bullet_sound = mixer.Sound('music/Missile.wav')
                            bullet_sound.play()
                            self.bullet_state = 'fire'
                            self.bulletY = self.playerY
                            self.bulletX = self.playerX

                if event.type == pg.KEYUP:
                    if event.key == pg.K_LEFT or event.key == pg.K_RIGHT or event.key == pg.K_UP or event.key == pg.K_DOWN:
                        self.playerx_delta, self.playery_delta = 0, 0

            # playerX += np.random.randint(-100,100)/100
            # playerY += np.random.randint(-100,100)/100
            self.playerX += self.playerx_delta
            self.playerY += self.playery_delta
            if self.playerX < 0:
                self.playerX = 0
            if self.playerX > self.WINDOW_WIDTH - self.PLAYER_ICON_SIZE:
                self.playerX = self.WINDOW_WIDTH - self.PLAYER_ICON_SIZE
            if self.playerY < self.WINDOW_HEIGHT // 2:
                self.playerY = self.WINDOW_HEIGHT // 2
            if self.playerY > self.WINDOW_HEIGHT - 3 * self.PLAYER_ICON_SIZE:
                self.playerY = self.WINDOW_HEIGHT - 3 * self.PLAYER_ICON_SIZE

            self.player(self.playerX, self.playerY)

            if self.enemyX < 0:
                self.enemyx_delta = 6 + np.random.randint(-2, 7) / 10
            if self.enemyX > self.WINDOW_WIDTH - self.ENEMY_ICON_SIZE:
                self.enemyx_delta = -6 + np.random.randint(-7, 2) / 10

            self.enemy_oscilation_angle = (self.enemy_oscilation_angle + 0.05) % 360

            self.enemyX = self.enemyX + self.enemyx_delta
            self.enemyY_temp = self.enemyY + self.ENEMY_OSCILATION_AMPLITUDE * np.sin(self.enemy_oscilation_angle)

            # collison condition
            collsion = self.isCollison()
            if not collsion:
                self.enemy(self.enemyX, self.enemyY_temp)
                if self.bullet_state == 'fire':
                    self.bulletY = self.bulletY - self.bullety_delta
                    if self.bulletY >= 0:
                        self.fire_bullet(self.bulletX, self.bulletY)
                    else:
                        self.bullet_state = 'ready'
            else:
                explosion_sound = mixer.Sound('music/Explosion+6.wav')
                explosion_sound.play()
                self.player_score += 1
                self.bulletX, self.bulletY = 1080, 1080
                self.enemyX, self.enemyY = np.random.randint(0, self.WINDOW_WIDTH - self.ENEMY_ICON_SIZE), \
                                 np.random.randint(self.ENEMY_OSCILATION_AMPLITUDE, self.WINDOW_HEIGHT // 4)
                self.enemy_oscilation_angle = 0
                self.bullet_state = 'ready'

            self.showScore(self.textX, self.textY)

            pg.display.update()
