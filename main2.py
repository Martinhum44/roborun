import pygame, sys
from pygame.locals import QUIT, KEYDOWN, K_SPACE, K_LEFT, K_RIGHT

pygame.init()
pygame.display.set_caption('Robot Run')

with open("bruh.txt","r") as bruh:
    level = int(bruh.read())

SIZE = (800, 600)

screen = pygame.display.set_mode(SIZE)
background = pygame.image.load("background.png").convert()
clock = pygame.time.Clock()

class Sprt():
  def __init__(self, x, y, photo, speed_x, speed_y):
    self.photog = pygame.image.load(photo).convert()
    self.photog.set_colorkey((0,0,0))
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
    self.rect.y = 385
  def harddie(self):
    self.rect.x = -10000
    self.rect.y = 350

class Player(Sprt):
  def __init__(self, where): 
    super().__init__(20, where, "robot.png", 3, 0)
    self.pos = "bottom"
    self.dead = False
    self.photog.set_colorkey((255,255,255))

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
            super().__init__(where, 338, "tree.png", 0, 0)

class Key(Sprt):
    def __init__(self, where, ud):
        self.ogpos = where
        if ud == "up":
            super().__init__(where, 120, "key.png", 0, 0)
            self.ygpos = 120
        elif ud == "down":
            super().__init__(where, 420, "key.png", 0, 0)
            self.ygpos = 420

class Stump(Enemy):
    def __init__(self, where, ud):
        if ud == "up":
            super().__init__(where, 100, "downstump.png", 0, 0)
        elif ud == "down":
            super().__init__(where, 500, "stump.png", 0, 0)
        self.rect.width = 50

class Wall(Enemy):
    def __init__(self): 
        super().__init__(725, 0, "wall.png", 0, 0)

class Rabbit(Enemy):
    def __init__(self, where, ud, speed):
        self.ud = ud 
        self.somewhattrue = True
        if self.ud == "up":
            super().__init__(where, 100, "rabbit.png", speed, 0)
        elif self.ud == "down":
            super().__init__(where, 800, "rabbit.png", speed, 0)

sprites = [[[Player(385), Log(5), Log(500), Tree(300,"down"), Tree(600, "up")], False, False, False],
           [[Player(385), Log(5), Log(500), Tree(200,"down"), Tree(600, "down")], False, False, False],
           [[Player(385), Log(5), Log(500), Tree(200,"up"), Tree(425,"up"), Tree(640,"down")], False, False, False],
           [[Player(385), Log(5), Log(500), Tree(200,"up"), Tree(450,"down")], False, False, False],
           [[Player(385), Log(5), Log(500), Tree(175,"down"), Tree(400,"up"), Tree(440,"up"), Tree(650,"down")], False, False, False],
           [[Player(385), Log(5), Log(500), Wall(), Key(500,"down")], True, False, False],
           [[Player(385), Log(5), Log(500), Tree(400,"up"), Wall(),Key(300, "up")], True, False, False],
           [[Player(385), Log(5), Log(500), Tree(150,"down"), Tree(450,"down"), Wall() , Key(350, "down")], True, False, False],
           [[Player(385), Log(5), Log(500), Tree(140, "up"), Tree(350, "down"), Wall(), Key(480, "down")], True, False, False],
           [[Player(385), Log(5), Log(500), Tree(130, "up"), Tree(400,"up"), Tree(625,"down"), Wall(), Key(275, "up")], True, False, False],
           [[Player(385), Log(5), Log(500), Tree(300,  "down"),Stump(700,"down"),Stump(700,"up")],False, False, False],
           [[Player(385), Log(5), Log(500), Stump(250,"down"),Stump(250,"up"), Tree(525,"down"), Wall(), Key(340,"down")],True, False, False],
           [[Player(385), Log(5), Log(500), Stump(300,"down"),Stump(300,"up"),Stump(600,"down"), Stump(600,"up")], False, False, False],
           [[Player(385), Log(5), Log(500), Tree(130,"down"), Tree(350,"up"), Stump(600,"down"), Stump(600,"up"), Tree(750,"down")], False, False, False],
           [[Player(385), Log(5), Log(500), Tree(150,"down"), Stump(300,"down"), Stump(300,"up"), Tree(425,"up"), Tree(700,"up"), Wall(), Key(575,"up")], True, False, False],
           [[Player(385), Log(5), Log(500), Rabbit(800,"down",-1)], False, False, True],
           [[Player(385), Log(5), Log(500), Rabbit(800,"down",-2), Tree(500, "up"), Tree(200, "up")], False, False, True],
           [[Player(385), Log(5), Log(500), Tree(200, "up"), Tree(500, "up"), Wall(), Rabbit(800,"down",-3), Key(650, "down")], False, False, True],
           [[Player(385), Log(5), Log(500)], False, False, False]
        ]

#GAME LOOP  
time = 330
keypos = 0
ti = 0
rabbits = []
while True:  
    player = sprites[level-1][0][0] 
    upperlog = sprites[level-1][0][1]
    lowerlog = sprites[level-1][0][2]
    if sprites[level-1][1]:
        enemies = sprites[level-1][0][3:len(sprites[level-1][0])-1]
        wall = sprites[level-1][0][-2]
    else:
        enemies = sprites[level-1][0][3:]

    if sprites[level-1][3]:
        rabbits = sprites[level-1][0][(len(enemies)+3)-1:]

    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
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
            if event.key == pygame.K_UP: 
                print("YAY")
                if player.speedX == 4:
                    player.change_speedX(player.speedX + 1)
                    print(player.speedX)
                elif player.speedX != 5:
                    player.change_speedX(player.speedX + 2)
                    print(player.speedX) 
                 
                
            if event.key == pygame.K_DOWN: 
                print("YAY")
                if player.speedX == 2:
                    player.change_speedX(player.speedX - 1)
                    print(player.speedX)
                elif player.speedX != 1:
                    player.change_speedX(player.speedX - 2)
                    print(player.speedX) 
                       
    #NO MORE EVENTS AFTER HERE 
    try:
        if player.rect.y < 112 and player.pos == "bottom": 
            player.change_speedY(0)      
            player.pos = "top"
    except AttributeError:
        continue

    try:
        if player.rect.y > 384 and player.pos == "top":
            player.change_speedY(0)
            player.pos = "bottom"
    except AttributeError:
        continue
    try:
        if player.rect.x > 800:
            sprites[level][0][0] = player
            player.rect.x = 0
            level += 1  
            if level > 2:
                time = 330
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
                    wall.rect.x = 725
                    wall.rect.y = 0
                    sprites[level-1][2] = False
                    key.rect.x = key.ogpos
                    key.rect.y = key.ygpos
                if level > 2:
                    time = 330
                if sprites[level-1][3]:
                    for rab in enemies:
                        print("THIS SPRITE IS "+str(type(rab)))
                        if type(rab) is Rabbit:
                            rab.rect.x = 750

    except AttributeError as e: 
        print("the error was: drumroll... \n", e,"!")
    if sprites[level-1][1]:
        keys = sprites[level-1][0][-1]
        keypos = keys.rect.x
        if player.rect.colliderect(keys):
            keys.die()
            wall.harddie()
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
        pygame.draw.rect(screen, (255,255,255), (380, 25, 300, 50),0,5)
        font = pygame.font.SysFont('georgia', 40)
        text_surface = font.render("Time Left: {:.2f}".format(time/60), True, (0, 0, 0))
        screen.blit(text_surface, (400, 25))
        if time == 0:
            player.die()
            time = 330
            if sprites[level-1][1]:
                key.rect.x = key.ogpos
                key.rect.y = key.ygpos
                wall.rect.x = 725
                wall.rect.y = 0
            player.change_speedX(3)
            if sprites[level-1][3]:
                for rab in enemies:
                    print("THIS SPRITE IS "+str(type(rab)))
                    if type(rab) is Rabbit:
                        rab.rect.x = 750

    pygame.draw.rect(screen,(0,0,0), (10, 15, 310, 70),0,5)
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
    
    if sprites[level-1][3]:
        for enemy in enemies:
            if type(enemy) is Rabbit:
                if enemy.ud == "down":
                    if enemy.somewhattrue:
                        if ti % 60 < 30:
                            enemy.change_speedY(-3)
                        else:
                            enemy.change_speedY(3)
                        enemy.rect.y = 450  
                    if (player.rect.y+player.rect.height > 420) and (player.rect.x+60 > enemy.rect.x and player.rect.x-50 < enemy.rect.x):
                        print("this if st8 ment is werking")
                        enemy.change_speedY(8)
                        enemy.change_speedX(0)      
                        enemy.somewhattrue = False 
    ti += 1       
    pygame.display.update()
    if player.rect.x < 0:
        player.dead = False
    clock.tick(60)

    