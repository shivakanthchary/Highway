import pygame as pg
import sys
import random

W = 800
H = 600
BG = (100, 100, 100)
car_accident = 0
drove_cars = 0

player_image = pg.image.load('img/Car.png')
tree_image = pg.image.load('img/d.png')
CARS = [pg.image.load('img/car1.png'), pg.image.load('img/car2.png'),
        pg.image.load('img/car3.png')]
n = len(CARS)
COLOR = ['red3', 'dark green', 'navy', 'orange']
imgColor = pg.image.load('img/car4.png')
originalColor = imgColor.get_at((imgColor.get_width()//2, imgColor.get_height()//2))
ar = pg.PixelArray(imgColor)
ar.replace(originalColor, pg.Color(COLOR[random.randint(0, len(COLOR)-1)]), 0.1)
del ar
CARS.append(imgColor)

FPS = 120
clock = pg.time.Clock()
speed = 2
acceleration = 0.05

pg.init()
pg.time.set_timer(pg.USEREVENT, 300)

screen = pg.display.set_mode((W, H))
pg.display.set_caption('Автомагистраль')
pg.display.set_icon(pg.image.load('img/car.png'))
pg.mouse.set_visible(False)

text = pg.font.SysFont('Arial', 24, True, True)

fscreen = [1, 2]
SIZE = pg.display.list_modes()[0]


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, angle, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.orig_image = self.image
        self.angle = angle
        self.speed = speed
        self.rect = self.image.get_rect()
        self.position = pg.math.Vector2(x, y)
        self.velocity = pg.math.Vector2()

    def update(self):
        self.image = pg.transform.rotate(self.orig_image, self.angle)
        self.position += self.velocity
        self.rect.center = self.position
        self.rect = self.image.get_rect(center=self.rect.center)


class Car(pg.sprite.Sprite):
    def __init__(self, x, y, image, dy, group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.flip(image, False, dy)
        self.x = x
        self.y = y
        self.h = image.get_height()
        self.w = image.get_width() // 2
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.add(group)
        self.speed = random.randint(3, 5)

    def render(self):
        block = 0
        direction = random.randint(0, 1)
        if direction == 0:
            y = - self.h
            dy = True
            car_x = random.randrange(80, W/2, 80)
        elif direction == 1:
            y = H + self.h
            dy = False
            car_x = random.randrange(480, W, 80)
        for img in cars:
            if car_x == img.rect.x + img.w:
                block = 1
        if block == 0:
            num = random.randint(0, n)
            if num == 3:
                originalColor = CARS[num].get_at((CARS[num].get_width()//2, CARS[num].get_height()//2))
                ar = pg.PixelArray(CARS[num])
                ar.replace(originalColor, pg.Color(COLOR[random.randint(0, len(COLOR)-1)]), 0.1)
                del ar
            car_new = Car(car_x, y, CARS[num], dy, cars)
            all_sprites.add(car_new, layer=2)

    def update(self):
        global drove_cars
        if self.x < W / 2:
            if self.rect.y < H + self.h:
                self.rect.y += self.speed
            else:
                self.kill()
                drove_cars += 1
        if self.x > W / 2:
            if self.rect.y > 0 - self.h:
                self.rect.y -= self.speed - 1
            else:
                self.kill()
                drove_cars += 1


class Background(pg.sprite.Sprite):
    def __init__(self, x, y, group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((W, H), pg.SRCALPHA)
        pg.draw.line(self.image, (0, 128, 0), [20, 0], [20, 600], 40)
        pg.draw.line(self.image, (0, 128, 0), [780, 0], [780, 600], 40)
        pg.draw.line(self.image, (0, 128, 0), [400, 0], [400, 600], 80)
        for xx in range(10):
            for yy in range(10):
                pg.draw.line(self.image, (200, 200, 200),
                             [40+xx*80, 0 if xx == 0 or xx == 4 or xx == 5 or xx == 9 else 10+yy*60],
                             [40+xx*80, 600 if xx == 0 or xx == 4 or xx == 5 or xx == 9 else 50+yy*60], 5)
        self.speed = speed
        self.add(group)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= H:
            self.rect.y = - H


class Tree(pg.sprite.Sprite):
    def __init__(self, x, y, image, group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(image, (image.get_width()//2,
                                        image.get_height()//2))
        self.speed = speed
        self.add(group)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= H:
            self.rect.y = - H


cars = pg.sprite.Group()
roads = pg.sprite.Group()
trees = pg.sprite.Group()

player = Player(x=W/2+80, y=H/2, angle=0, image=player_image)
car = Car(random.randrange(0, W/2, 80), 0, CARS[random.randint(0, n)], True, cars)
for i in range(2):
    bg = Background(x=0, y=0 if i == 0 else -H, group=roads)
for ix in range(3):
    for iy in range(6):
        tree = Tree(x=ix*380, y=-H+iy*200, image=tree_image, group=trees)

all_sprites = pg.sprite.LayeredUpdates()
all_sprites.add(roads, layer=1)
all_sprites.add(cars, layer=2)
all_sprites.add(player, layer=3)
all_sprites.add(trees, layer=4)

game = True
while game:
    clock.tick(FPS)
    for e in pg.event.get():
        if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            game = False
            print(f'car accident: {car_accident}\ndrove cars: {drove_cars}')
        elif e.type == pg.USEREVENT:
            car.render()
        elif e.type == pg.KEYDOWN and e.key == pg.K_f:
            fscreen.reverse()
            if fscreen[0] == 1:
                pg.display.set_mode((W, H))
            elif fscreen[0] == 2:
                pg.display.set_mode((W, H), pg.FULLSCREEN)

    keys = pg.key.get_pressed()
    if keys[pg.K_RIGHT]:
        player.velocity.x = speed
        player.angle -= 1
        if player.angle < -20:
            player.angle = -20
    elif keys[pg.K_LEFT]:
        player.velocity.x = -speed
        player.angle += 1
        if player.angle > 20:
            player.angle = 20
    else:
        player.velocity.x = 0
        if player.angle < 0:
            player.angle += 1
        elif player.angle > 0:
            player.angle -= 1
    if keys[pg.K_UP]:
        player.velocity.y -= acceleration
        if player.velocity.y < -4:
            player.velocity.y = -4
    elif keys[pg.K_DOWN]:
        player.velocity.y += acceleration
        if player.velocity.y > speed + 1:
            player.velocity.y = speed + 1
    else:
        if player.velocity.y < 0:
            player.velocity.y += acceleration
            if player.velocity.y > 0:
                player.velocity.y = 0
        elif player.velocity.y > 0:
            player.velocity.y -= acceleration
            if player.velocity.y < 0:
                player.velocity.y = 0

    if player.position.x > W - 40:
        player.position.x = W - 40
    elif player.position.x < 40:
        player.position.x = 40
    elif player.position.y > H:
        player.position.y = H
    elif player.position.y < 0:
        player.position.y = 0

    if pg.sprite.spritecollide(player, cars, True):
        player.angle = random.randrange(-65, 65, 25)
        car_accident += 1
    elif pg.sprite.spritecollideany(player, trees):
        player.angle = -60
        player.velocity.y = speed

    screen.fill(BG)
    all_sprites.update()
    all_sprites.draw(screen)
    screen.blit(text.render(f'Аварий: {car_accident} Проехало машин: {drove_cars}',
                            True, pg.Color('lime green'), BG), (50, 570))
    s = 150+abs(player.velocity.y)*100 if player.velocity.y <= 0 else 200-player.velocity.y*100
    screen.blit(text.render(f'Скорость: {int(s)} км/ч',
                            True, pg.Color('lime green'), None), (480, 0))
    screen.blit(text.render(f'FPS: {int(clock.get_fps())}',
                            True, pg.Color('lime green'), None), (150, 0))
    pg.display.update()

sys.exit(0)
