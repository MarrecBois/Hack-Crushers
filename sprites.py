from config import *
import pygame

#import g.lst from main()


#optional wall colour option
#self.colour
class Stat(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        #different for each?

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def moveIt(self):
        self.rect.x = 15 * SCALER
        self.rect.y = 20 * SCALER


class Monster(Stat):
    counter = 0

    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        image = pygame.image.load("zBug.png")
        self.image = pygame.Surface([self.width + 120, self.height + 60])
        self.image.set_colorkey(WHITE)
        self.image.blit(image, (x, y - 10))

        self._layer = COLLECT_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

    #def update(self):
    # counter += 1
    #if counter >= FPS*90:
    # counter = 0
    #l = Laser(self, self.x, self.y, 2, "zGeek.png")


#Wall Class
class Wall(Stat):
    #takes in x and y of wall, the length and height are constants
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.image.fill(BLUE)
        self._layer = WALL_LAYER
        self.groups = self.game.all_sprites, self.game.wall
        pygame.sprite.Sprite.__init__(self, self.groups)


class Heart(Stat):

    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        image = pygame.image.load("zHeart.png")
        self.image = pygame.Surface([self.width + 20, self.height + 10])
        self.image.set_colorkey(WHITE)
        self.image.blit(image, (x, y))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self._layer = COLLECT_LAYER
        self.groups = self.game.all_sprites, self.game.collectables
        pygame.sprite.Sprite.__init__(self, self.groups)

    #def collide(self):
    # hits = pygame.sprite.spritecollide(self, self.game.player, False)
    #if hits:
    # print(1)

    #def update(self):
    # self.collide()


class Key(Stat):

    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        image = pygame.image.load("zKey.png")
        self.image = pygame.Surface([self.width + 95, self.height + 10])
        self.image.set_colorkey(WHITE)
        self.image.blit(image, (x, y))

        self._layer = COLLECT_LAYER
        self.groups = self.game.all_sprites, self.game.collectables
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect.update(self.rect.x, self.rect.y, 4 * SCALER, 1 * SCALER)


#Object class
class Obj(Stat):

    def __init__(self, game, x, y, velocity):
        super().__init__(game, x, y)
        self.velocity = velocity

        self.x_change = 0
        self.y_change = 0

    def update(self):
        self.movement()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        pass


#button class to interact with monsters and puzzles
#Button(400, 400)
class Button:

    def __init__(self, x, y):
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = pygame.Surface([self.width * 4, self.height * 2])
        self._layer = PLAYER_LAYER

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, image_name):
        #draw the button on screen
        image = pygame.image.load(image_name)
        self.image.blit(image, (self.rect.x, self.rect.y))

    def is_pressed(self, mouse_pos, mouse_press):  # ??
        if self.rect.collidepoint(mouse_pos):
            if mouse_press[0]:
                return True
        return False


class Laser(Obj):

    def __init__(self, game, x, y, velocity, direction, image_name):
        super().__init__(game, x, y, velocity)
        self.direction = direction
        self.load_image = pygame.image.load(image_name)

        self._layer = LASER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect.update(self.rect.x, self.rect.y, 3 * SCALER, 1 * SCALER)

    def update(self):
        ##self.y += self.velocity
        self.moving(self.direction)

    def moving(self, direction):
        for laser in self.game.lasers:
            self.game.screen.blit(laser.load_image,
                                  (laser.rect.x, laser.rect.y))

        if direction == 'right' or direction == 'left':
            d = 'x'
        elif direction == 'up' or direction == 'down':
            d = 'y'
        if self.collide_blocks(d):
            self.moveIt()
        #else:
        ##self.game.screen.fill(BLACK)

        if direction == "right":
            self.rect.x += self.velocity
        elif direction == "left":
            self.rect.x -= self.velocity
        elif direction == "up":
            self.rect.y += self.velocity
        elif direction == "down":
            self.rect.y -= self.velocity

            #self.game.screen.blit(self.load_image, (self.rect.x, self.rect.y))

            pygame.display.update()
            self.game.clock.tick(FPS)

    def moveIt(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def collide_blocks(self, direction):
        if direction == 'x':
            return pygame.sprite.spritecollide(self, self.game.walls, False)

        if direction == 'y':
            return pygame.sprite.spritecollide(self, self.game.walls, False)


#def collide_blocks(self, direction):
#if direction == 'x':
#pygame.sprite.spritecollide(self, self.game.walls, True)

#if direction == 'y':
#hits = pygame.sprite.spritecollide(self, self.game.walls, True)


class Player(Obj):

    def __init__(self, game, x, y, velocity):
        super().__init__(game, x, y, velocity)

        image = pygame.image.load("zGeek.png")
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(WHITE)
        self.image.blit(image, (x, y))

        self.font = pygame.font.Font("CormorantGaramond-Bold.ttf", 30)

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            #for sprite in self.game.all_sprites:
            #  sprite.rect.x += self.velocity
            self.x_change -= self.velocity
        if keys[pygame.K_d]:
            #for sprite in self.game.all_sprites:
            #  sprite.rect.x -= self.velocity
            self.x_change += self.velocity
        if keys[pygame.K_w]:
            #for sprite in self.game.all_sprites:
            #  sprite.rect.y += self.velocity
            self.y_change -= self.velocity
        if keys[pygame.K_s]:
            #for sprite in self.game.all_sprites:
            #  sprite.rect.x -= self.velocity
            self.y_change += self.velocity

    #Collision detection
    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    #Collision with heart
    def collide_heart(self):
        for heart in self.game.hearts:
            if (self.rect).colliderect(heart.rect):
                heart.moveIt()
                self.game.health += 1
                print("Current lives: " + str(self.game.health))

  
    def collide_key(self):
        for key in self.game.keys:
            if (self.rect).colliderect(key.rect):
                key.moveIt()

                self.game.key = True

        #for i in self.game.hearts:
        # print(1)
        #if((self.x-i.x)**2+(self.y-i.y)**2) < SCALERz:
        # print(0)

    def collide_laser(self):
        for laser in self.game.lasers:
            if (self.rect).colliderect(laser.rect):
                laser.moveIt()
              
                if self.game.health >= 1:
                    print("Current lives: " + str(self.game.health))
                    self.game.health -= 1
                else:
                    self.game.game_over()
                  
                self.rect.x = self.x
                self.rect.y = self.y
              
    def collide_exit(self):
        if (self.rect).colliderect(pygame.Rect(19 * SCALER, 6 * SCALER, 40, 120)):
            if self.game.key:
                self.game.next_level()
                self.game.playing = False
            else:
                self.rect.x = 18 * SCALER

    def collide_boss(self):
      for boss in self.game.boss:
        if (self.rect).colliderect(boss.rect):
          boss.form += 1
          boss.image.blit(boss.change_form, (17 * SCALER, 7 * SCALER))
          

    def update(self):
        super().update()
        self.collide_heart()
        self.collide_key()
        self.collide_laser()
        self.collide_exit()
        self.collide_boss()


class Text(Stat):

    def __init__(self, game, x, y, thing):
        super().__init__(game, x, y)

        self.thing = thing
        self.font = pygame.font.Font("CormorantGaramond-Bold.ttf", 40)

    def displaying(self, value):
        while self.game.running:
            self.text = self.font.render(self.thing + str(value), True, WHITE)
            self.game.screen.blit(self.text, (self.x, self.y))

            pygame.display.update()


class Boss(Monster):
  def __init__(self, game, x, y):
    super().__init__(game, x, y)
    self.form = 1

  def change_form(self):
    if self.form == 1:
      self.image_name = "zBoss1.png"
    if self.form == 2:
      self.image_name = "zBoss2.png"
    elif self.form == 3:
      self.image_name = "zBoss3.png"

    return self.image_name
      
