#https://www.youtube.com/watch?v=Okm3-OKzWa8
#https://www.youtube.com/watch?v=vz8YnvnAPp4&list=PLkkm3wcQHjT7gn81Wn-e78cAyhwBW3FIc&index=9

#https://devpost.com/software/517823/joins/T2Zj47mMDaOkGpK_84yr3A

#https://jamboard.google.com/d/10ZXIohIPc1deLZ-cWgSykuwrGZmiIUuuDFErZGy688U/edit?usp=sharing

import pygame, sys
from pygame.locals import QUIT
from sprites import *
from config import *

#counter = 0
walls = []


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.screen.fill(BLACK)
        self.caption = pygame.display.set_caption('First Game')
        self.clock = pygame.time.Clock()  #how many time screen updates
        self.running = True
        self.key = False
        self.health = HEALTH
        self.level = 0

        self.font = pygame.font.Font("CormorantGaramond-Bold.ttf", 50)
        #self.intro_bg = pygame.image.load("filename")

        print("Current lives: 1")
      

    def createMap(self, level):
        self.walls = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()
        self.keys = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.boss = pygame.sprite.Group()

        for i, row in enumerate(level):
            for j, column in enumerate(row):
                if column == 'W':
                    w = Wall(self, j, i)
                    self.walls.add(w)

                if column == 'P':
                    p = Player(self, j, i, 3)
                    self.players.add(p)
                if column == 'H':
                    h = Heart(self, j, i)
                    self.hearts.add(h)
                if column == 'K':
                    k = Key(self, j, i)
                    self.keys.add(k)

                if column == 'M':
                    m = Monster(self, j, i)
                    self.monsters.add(m)

                if column == 'L':
                    if row[j + 1] == 'M':
                        direction = "left"
                    if row[j - 1] == 'M':
                        direction = 'right'
                    if level[i + 1][j] == 'M':
                        direction = 'down'
                    if level[i - 1][j] == 'M':
                        direction = 'up'
                    l = Laser(self, j, i, 1, direction, "zError.png")
                    self.lasers.add(l)


                if column == 'B':
                    b = Boss(self, j, i)
                    self.boss.add(b)

              

    def new(self, level):
        # a new game starts
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.wall = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.collectables = pygame.sprite.LayeredUpdates()

        self.createMap(level)

    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        # game loop updates
        self.all_sprites.update()

    def draw(self):
        # game loop draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:
            self.events()  # press keys
            self.update()  # make changes
            self.draw()  # display


    def display_text(self):
        t_heart = Text(self, 780, 20, "Heart: ")
        t_key = Text(self, 20, 20, "Key: ")

        t_heart.displaying(self.health)
        t_key.displaying(self.key)

    def game_over(self):
        print("Game Over. Failed to de\"bug\". You lose.")
        pygame.quit()
        sys.exit()
        #text = self.font.render('Game Over', True, BLACK)
        #text_rect = text.get_rect()
        #restart_button = Button(10, )

    def intro_screen(self):
        intro = True

        title = self.font.render("Hack Crushers", True, WHITE)
        title_rect = title.get_rect(x=20, y=20)
        subtitle = self.font.render("Find the button to start.", True, WHITE)
        subtitle_rect = subtitle.get_rect(x=100, y=100)

        button = Button(0, 0)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro == False
                    self.running == False

            mouse_pos = pygame.mouse.get_pos()
            mouse_press = pygame.mouse.get_pressed()

            if button.is_pressed(mouse_pos, mouse_press):  #???
                intro = False

            #self.screen.fill(WHITE)
            self.screen.blit(title, title_rect)
            self.screen.blit(subtitle, subtitle_rect)
            #button.draw("Start.png")
            image = pygame.image.load("zStart.png")
            button.image.blit(image, (0, 0))
            self.clock.tick(FPS)
            pygame.display.update()

    def next_level(self):
      if self.level < 3:
        self.level += 1
      self.key = False


g = Game()
#g.display_text()

g.intro_screen()
#g.new(map)
#for i in range(0,3):
#g.new(levelnum[i])
while g.running:
    g.new(levelnum[2])#g.level
    g.main()

    if g.health <= 0:
        g.game_over()

    for wall in g.walls:
        wall.kill()
        g.screen.fill(BLACK)
        continue

pygame.quit()
sys.exit()
