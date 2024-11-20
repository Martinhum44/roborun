import pygame, sys
from pygame.locals import QUIT, KEYDOWN, K_SPACE, K_LEFT, K_RIGHT

pygame.init()
pygame.display.set_caption('Robot Run')

level = 1
SIZE = (800, 600)

screen = pygame.display.set_mode(SIZE)
background = pygame.image.load("background.png").convert()
clock = pygame.time.Clock()

class Sprt():

  def __init__(self, x, y, photo, speed_x, speed_y):
    self.photog = pygame.image.load(photo).convert()
    for i in range(10):
        self.photog.set_colorkey((i+240,i+240,i+240))
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
    self.rect.x = -100
    self.rect.y = 350
    

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

class Tree(Enemy):
    def __init__(self, where, ud):
        if ud == "up":
            super().__init__(where, 100, "downtree.png", 0, 0)
        elif ud == "down":
            super().__init__(where, 352, "tree.png", 0, 0)

class Key(Sprt):
    def __init__(self, where, ud):
        self.ogpos = where
        if ud == "up":
            super().__init__(where, 100, "key.png", 0, 0)
            self.ygpos = 100
        elif ud == "down":
            super().__init__(where, 500, "key.png", 0, 0)
            self.ygpos = 400

class Wall(Sprt): 
    def __init__(self):
        super().__init__(750, 0, "key.png", 0, 0)
       
sprites = [[[Player(350), Log(5), Log(500), Tree(300,"down"), Tree(600, "up")], False, False],
           [["Player()", Log(5), Log(500), Tree(200,"down"), Tree(600, "down")], False, False],
           [["Player()", Log(5), Log(500), Tree(200,"up"), Tree(450,"up"), Tree(640,"down")], False, False],
           [["Player()", Log(5), Log(500), Tree(200,"up"), Tree(450,"down")], False, False],
           [["Player()", Log(5), Log(500), Tree(175,"down"), Tree(400,"up"), Tree(450,"up"), Tree(625,"down")], False, False],
           [["Player()", Log(5), Log(500), Key(500,"down")], True, False],
           [["Player()", Log(5), Log(500), Tree(400,"up"), Key(300, "up")], True, False],
           [["Player()", Log(5), Log(500), Tree(150,"down"), Tree(550,"down"), Key(350, "down")], True, False],
           [["Player()", Log(5), Log(500), Tree(160, "up"), Tree(340, "down"), Key(450, "down")], True, False],
           [["Player()", Log(5), Log(500), Tree(150, "up"), Tree(400,"up"), Tree(600,"down"), Key(275, "up")], True, False]]
  
#GAME LOOP
time = 100000000000000000000000000000000
keypos = 0

while True:  
    player = sprites[level-1][0][0] 
    upperlog = sprites[level-1][0][1]
    lowerlog = sprites[level-1][0][2]
    if sprites[level-1][1]:
        enemies = sprites[level-1][0][3:len(sprites[level-1][0])-1]
    else:
        enemies = sprites[level-1][0][3:]

    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type  == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                player.change_side()
            if event.key == K_LEFT:
                print("YAY")
                if player.speedX != 1:
                    player.change_speedX(player.speedX - 1)
                    print(player.speedX)
            if event.key == K_RIGHT: 
                print("YAY")
                if player.speedX != 5:
                    player.change_speedX(player.speedX + 1)
                    print(player.speedX)
                    
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
        if player.rect.x > 760:
            if sprites[level-1][1] and not sprites[level-1][2]:
                player.die()
                if level > 2:
                    time = 300
                for sprite in sprites[level-1]:
                    sprite.die()
                key.rect.x = key.ogpos
                key.rect.y = key.ygpos
            sprites[level][0][0] = player
            player.rect.x = 0
            level += 1  
            if level > 2:
                time = 300
    except AttributeError:
        continue
    try:
        for tree in enemies:
            if player.rect.colliderect(tree):
                key = sprites[level-1][0][-1]
                print("no0", keypos)
                tree.kill()
                player.change_speedY(0)
                player.change_speedX(3)
                print("foo! ", sprites[level-1][1])
                if sprites[level-1][1] == True:
                    print("WUT!!!!!!!!!!")
                    print(key.rect.x)
                    key.rect.x = keypos
                    sprites[level-1][2] = False
                if level > 2:
                    time = 300
                key.rect.x = key.ogpos
                key.rect.y = key.ygpos
                for rab in enemies:
                    if type(rab) is Rabbit:
                        rab.rect.x = 800

    except AttributeError: 
        pass
    if sprites[level-1][1]:
        keys = sprites[level-1][0][-1]
        keypos = keys.rect.x
        if player.rect.colliderect(keys):
            keys.die()
            sprites[level-1][2] = True

    for sprite in sprites[level-1][0]:
        try:
            sprite.update()
        except AttributeError:
            continue
    pygame.draw.rect(screen, (255,255,255), (10, 520, 125, 50),0,5)
    levelf = pygame.font.SysFont('georgia', 30)
    levels = levelf.render("Level {}".format(level), True, (0, 0, 0))
    screen.blit(levels, (25, 530))
    if level > 2:
        time -= 1 
        print("time remaining: ", time)
        pygame.draw.rect(screen, (255,255,255), (380, 25, 300, 50),0,5)
        font = pygame.font.SysFont('georgia', 40)
        text_surface = font.render("Time Left: {:.2f}".format(time/60), True, (0, 0, 0))
        screen.blit(text_surface, (400, 25))
        if time == 0:
            player.die()
            time = 300
            if sprites[level-1][1]:
                key.rect.x = key.ogpos
                key.rect.y = key.ygpos
            player.change_speedX(3)
    pygame.draw.rect(screen, (0,0,0), (10, 15, 310, 70),0,5)
    for i in range(player.speedX):
        if i == 0 :
            color = (0,0,255)
        elif i == 1:
            color = (0,255,0)
        elif i == 2:
            color = (255,255,0) 
        elif i == 3:
            color = (255,128,0)
        elif i == 4:
            color = (255,0,0)
        pygame.draw.rect(screen, color, (60*i+20, 25, 50, 50),0,5)

    pygame.display.update()
    clock.tick(60)
