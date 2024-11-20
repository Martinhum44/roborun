import pygame, sys
from pygame.locals import QUIT, KEYDOWN, K_SPACE, K_LEFT, K_RIGHT

pygame.init()
pygame.display.set_caption('Robot Run')

SIZE = (800, 600)

screen = pygame.display.set_mode(SIZE)
background = pygame.image.load("background.png").convert()
clock = pygame.time.Clock()

class Sprt():

  def __init__(self, x, y, photo, speed_x, speed_y):
    self.photog = pygame.image.load(photo).convert()
    self.photog.set_colorkey((255,255,255))
    self.rect = self.photog.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.speedX = speed_x
    self.speedY = speed_y
    screen.blit(self.photog, (self.rect.x, self.rect.y))
  def update(self):
    self.rect.y += self.speedY
    self.rect.x += self.speedX
    screen.blit(self.photog, self.rect)
  def change_speedX(self, x):
    self.speedX = x
  def change_speedY(self, y):
    self.speedY = y
  def die(self):
    self.rect.y = 1000000
    self.rect.x = -1000000
    

class Player(Sprt):

  def __init__(self, where):
    super().__init__(20, where, "robot.png", 3, 0)
    self.pos = "bottom"

  def change_side(self):
    if self.pos == "bottom":
        self.change_speedY(-8)
        
    elif self.pos == "top":
        self.change_speedY(8)

class Log(Sprt):
  def __init__(self, where):
    super().__init__(0, where, "log.png", 0, 0)

class Enemy(Sprt):
    def kill(self):
        player.die()
        for sprite in sprites[level-1]:
           sprite.die()

class Tree(Enemy):
    def __init__(self, where, ud):
        if ud == "up":
            super().__init__(where, 100, "downtree.png", 0, 0)
        elif ud == "down":
            super().__init__(where, 352, "tree.png", 0, 0)

class Key(Sprt):
    def __init__(self, where, ud):
        if ud == "up":
            super().__init__(130, where, "key.png", 0, 0)
        elif ud == "down":
            super().__init__(332, where, "key.png", 0, 0)
       
class Level:
    aspects = []
    def __init__(self,keyed,timed,*args):
        for arg in args:
            self.aspects.append(arg)
            self.keyed = keyed
            self.timed = timed
        
level = 1
sprites = [[x for x in Level(False,False,Player(350), Log(5), Log(500), Tree(300,"down"), Tree(600, "up")).aspects],
          [x for x in Level("Player()", Log(5), Log(500), Tree(200,"down"), Tree(600, "down")).aspects],
          [x for x in Level("Player()", Log(5), Log(500), Tree(200,"down"), Tree(400,"up"), Tree(450,"up"), Tree(700,"down")).aspects],
          [x for x in Level("Player()", Log(5), Log(500), Tree(200,"down"), Tree(400,"up"), Tree(450,"up"), Tree(700,"down")).aspects],
          [x for x in Level("Player()", Log(5), Log(500), Tree(200,"down"), Tree(400,"up"), Tree(450,"up"), Tree(700,"down")).aspects],
          [x for x in Level("Player()", Log(5), Log(500), Tree(200,"down"), Tree(400,"up"), Tree(450,"up"), Tree(700,"down")).aspects]]

#GAME LOOP
while True:
    enemies = sprites[level-1][3:]
    player = sprites[level-1][0] 
    upperlog = sprites[level-1][1]
    lowerlog = sprites[level-1][2]
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type  == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                player.change_side()
            if event.key == K_LEFT:
                if player.speedX == 5:
                    player.change_speedX(player.speedX + 1)
            if event.key == K_RIGHT:
                if player.speedX == 1:
                    player.change_speedX(player.speedX + 1)
                    
    #NO MORE EVENTS AFTER HERE 
    try:
        if player.rect.y < 110 and player.pos == "bottom":
            player.change_speedY(0)
            player.pos = "top"
    except AttributeError:
        continue

    try:
        if player.rect.y > 349 and player.pos == "top":
            player.change_speedY(0)
            player.pos = "bottom"
    except AttributeError:
        continue
    try:
        if player.rect.x > 800:
            sprites[level][0] = player
            print("foo",sprites)
            player.rect.x = 0
            level += 1  
    except AttributeError:
        continue
           
    for tree in enemies:
        try:
            if player.rect.colliderect(tree):
                tree.kill()
        except AttributeError:
            continue
    print(player.rect)
    for sprite in sprites[level-1]:
        try:
            sprite.update()
        except AttributeError:
            continue
    pygame.display.update()
    clock.tick(60)
