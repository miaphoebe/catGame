import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Catbus Adventure")

clock = pygame.time.Clock()


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.lastLeft = False
        self.walkCount = 0
        self.hitbox = (self.x, self.y + 15, 60, 50)
    walkRight = [pygame.image.load('cat0.png'), 
                pygame.image.load('cat1.png'),
                pygame.image.load('cat2.png'),
                pygame.image.load('cat3.png'),
                pygame.image.load('cat4.png'),
                pygame.image.load('cat5.png'),
                ]
    walkLeft = [pygame.transform.flip(img, True, False) for img in walkRight]
    char = pygame.image.load('cat4.png')
    leftChar = pygame.transform.flip(char, True, False)
    
    def draw(self, screen):
        if self.walkCount + 1 >= 18: 
            self.walkCount = 0
        if self.left:
            screen.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
            self.lastLeft = True
        elif self.right:
            self.lastLeft = False
            self.walkCount += 1
            screen.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
        elif self.lastLeft:
            screen.blit(self.leftChar, (self.x, self.y))
        else:
            screen.blit(self.char, (self.x, self.y))
        pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)

class projectile(object):
    def __init__(self, x, y, rad, color, direction):
        self.x = x
        self.y = y
        self.rad = rad
        self.color = color
        self.direction = direction
        self.vel = 10 * direction
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.rad)

class npc(object):
    walkRight = [
                pygame.image.load('man0.png'),
                pygame.image.load('man1.png'),
                pygame.image.load('man2.png'),
                pygame.image.load('man1.png'),
                ]
    walkLeft = [pygame.transform.flip(img, True, False) for img in walkRight]
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkCount = 0
        self.vel = 3
        self.path = [self.x, self.end]
    
    def draw(self, screen):
        self.move()
        if self.walkCount + 1 >= 12:
            self.walkCount = 0
        if self.vel > 0:
            screen.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else: 
            screen.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else: 
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0



def redrawGameWindow():
    screen.fill((0,100,0))
    cat.draw(screen)
    enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.update()

cat = player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 64, 64)
enemy = npc(0, SCREEN_HEIGHT // 2, 71, 131, SCREEN_WIDTH)
bullets = []
run = True
# main loop
while run: 
    clock.tick(27)

    redrawGameWindow()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < SCREEN_WIDTH and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_q]:
        if cat.lastLeft:
            direction = -1
        else: 
            direction = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(cat.x + cat.width // 2), 
                                      round(cat.y + cat.height // 2),
                                      6,
                                      (0,0,0), direction))
    if keys[pygame.K_a] or keys[pygame.K_LEFT] and cat.x > 0:
        cat.x -= cat.vel
        cat.left = True
        cat.right = False
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT] and cat.x < SCREEN_WIDTH - cat.height:
        cat.x += cat.vel
        cat.left = False
        cat.right = True
    else:
        cat.left = False
        cat.right = False
        cat.walkCount = 0
    if not(cat.isJump):
        if keys[pygame.K_w] or keys[pygame.K_UP] and cat.y > 0:
            cat.y -= cat.vel
        if keys[pygame.K_s] or keys[pygame.K_DOWN] and cat.y < SCREEN_HEIGHT - cat.width:
            cat.y += cat.vel
        if keys[pygame.K_SPACE]:
            cat.isJump = True
            cat.left = False
            cat.right = False
            cat.walkCount = 0
    else:
        if cat.jumpCount >= -10:
            neg = 1
            if cat.jumpCount < 0: 
                neg = -1
            cat.y -= (cat.jumpCount ** 2) / 2 * neg
            cat.jumpCount -= 1
        else: 
            cat.isJump = False
            cat.jumpCount = 10

pygame.quit()