from pygame import *
from random import randint
from time import time as timer

win = display.set_mode((1200, 900))
background = transform.scale(image.load('galaxy.jpg'), (1000, 700))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
clock = time.Clock()
FPS = 60
font.init()
font1 = font.SysFont(None, 40)
lost = 0
kills = 0
num_fire = 0
life = 5
rel_time = False
lose = font.SysFont(None, 200).render('YOU LOSE!', True, (255, 0, 0))
win_text = font.SysFont(None, 200).render('YOU WIN!', True, (0, 255, 0))
enem = ['green.png', 'spiral.png']

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, width, height, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 800:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 680:
            self.rect.y += self.speed

    # метод "выстрел"
    def fire(self):
        bullet = Bullet('bubble.png', self.rect.centerx, self.rect.top, 30, 30, 10)
        bullets.add(bullet)



class Enemy(GameSprite):
    def update(self):
        global lost

        self.rect.y += self.speed
        if self.rect.y > 700:
            lost += 1
            self.rect.x = randint(50, 950)
            self.rect.y = 0

class Enemy2(GameSprite):
    def update(self):
        global lost

        self.rect.y += self.speed
        if self.rect.y > 700:
            self.rect.x = randint(50, 950)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

ship = Player('rocket23.png', 350, 400, 150, 200, 10)
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    monster = Enemy2(enem[randint(0, 1)], randint(20, 620), 0, 90, 90, randint(1, 2))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(20, 620), 0, 90, 90, randint(1, 2))
    asteroids.add(asteroid)

finish = False
run = True
while run:
    win.blit(background, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    end_time = timer()
                    rel_time = True

                
    if not finish:
        ship.reset()
        ship.update()
        monsters.draw(win)
        monsters.update()
        bullets.draw(win)
        bullets.update()
        asteroids.draw(win)
        asteroids.update()
        if rel_time == True:
            new_time = timer()
            if new_time - end_time < 3:
                win.blit(font1.render('Идет перезарядка..', True, (255, 255, 255)), (400, 350))
            else:
                rel_time = False
                num_fire = 0

        text = font1.render('Пропущено: ' + str(lost), True, (255, 255, 255))
        win.blit(text, (10, 20))
        text2 = font1.render('Убито: ' + str(kills), True, (255, 255, 255))
        win.blit(text2, (10, 60))
        text3 = font1.render('Жизни: ' + str(life), True, (255, 255, 255))
        win.blit(text3, (10, 100))

    collides = sprite.groupcollide(monsters, bullets, True, True)
    for collide in collides:
        kills += 1
        monster = Enemy2(enem[randint(0, 1)], randint(20, 620), 0, 90, 90, randint(1, 2))
        monsters.add(monster)
    if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
        sprite.spritecollide(ship, monsters, True)
        sprite.spritecollide(ship, asteroids, True)
        life -= 1
    if life == 0:
        finish = True
        win.blit(lose, (150, 250))
    if kills >= 3:
        finish = True
        win.blit(win_text, (150, 250))

    display.update()
    clock.tick(FPS)
