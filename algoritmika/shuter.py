import pygame
import sys
import random
from time import time as timer

# инициализирование игры
pygame.init()
clock = pygame.time.Clock()
FPS = 120

# создание пустого окна
WIDTH = 700  # ширина
HEIGHT = 500  # высота
window = pygame.display.set_mode((WIDTH, HEIGHT))  # создали окно размера (ширина, высота)
pygame.display.set_caption('Шутер')  # установили название окна

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# задаем фон сцены
img = pygame.image.load('background.png')
new_img = pygame.transform.scale(img, (700, 500))


# настройка музыки
pygame.mixer.music.load('music.mp3')  # фоновая музыка
pygame.mixer.music.play()

fire_sound = pygame.mixer.Sound('fire.mp3')
#шрифты и надписи
pygame.font.init()
font2 = pygame.font.Font(None, 36)
font1 = pygame.font.Font(None, 80)
win = font1.render('ПОБЕДА', True, 'WHITE')
lose = font1.render('ПОРАЖЕНИЕ', True, (180, 0, 0))

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        """

        :rtype: object
        """
        # иницализируем картинку спрайта, его положение по x, y и скорость спрайта
        super().__init__()

        # каждый спрайт должен хранить свойство image - изображение
        self.image = pygame.transform.scale(pygame.image.load(player_image), (size_x, size_y))  # добавляем изображние спрайта
        self.speed = player_speed  # скорость спрайта

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x  # положение прямоугольника по x
        self.rect.y = player_y  # положение прямоугольника по y

    def reset(self):
        # отрисовка изображения с помощью blit
        # при размещении указываются координаты
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    """класс со спрайтом-ракетой"""
    def update(self):
        """метод для управления спрайтом стрелками клавиатуры"""
        keys = pygame.key.get_pressed()  # создаем событие "нажатия клавиши"
        if keys[pygame.K_LEFT] and self.rect.x > 0:  # если левая стрелка нажата и спрайт не уходит за пределы левой части экрана
            self.rect.x -= self.speed  # прямоугольник спрайта будет двигаться влево
        if keys[pygame.K_RIGHT] and self.rect.x <= 630:  # если правая стрелка нажата и спрайт не уходит за пределы правой части экрана
            self.rect.x += self.speed  # прямоугольник спрайта будет двигаться вправо

    def fire(self):
        """метод выстрела"""
        bullet = Bullet('bullet.png', self.rect.centerx,self.rect.top, -10, 25, 25)
        bullets.add(bullet)


# класс спрайта-врага
class Enemy(GameSprite):

    # движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        # исчезает, если дойдет до края экрана
        if self.rect.y > HEIGHT:
            self.rect.x = random.randint(80, HEIGHT - 80)
            self.rect.y = 0
            lost = lost + 1


# класс с пулями
class Bullet(GameSprite):
    # движение пули
    def update(self):
        self.rect.y += self.speed  # у прямоугольнику пули прибавляем скорость
        # исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()


# создаем спрайты
ship = Player('ship.png', WIDTH/2.2, HEIGHT - 80, 4, 80, 80)  # картинка, расположение по x, расположение по y, скорость

monsters = pygame.sprite.Group()
for i in range(1, 4):
    monster = Enemy('monster.jpg', random.randint(80, WIDTH - 80), -40, 2, 65, 65)
    monsters.add(monster)




asteroids = pygame.sprite.Group()
for i in range(1, 4):
    asteroid = Enemy('baiden.png', random.randint(80, WIDTH - 80), -40, 2, 65, 65)
    asteroids.add(asteroid)

bullets = pygame.sprite.Group()

# переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False

# переменная-счетчик пропущенных кораблей
lost = 0
max_lost = 5
score = 0
goal = 10
rel_time = False
num_fire = 0
life = 3


# Запуск игрового цикла
while True:
    # проверка наличия события выхода из игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:  # если произошло событие нажатия на клавишу
            if event.key == pygame.K_SPACE:
                if num_fire < 5:
                    num_fire += 1
                fire_sound.play()
                ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = pygame.timer()
                    rel_time = True


    if not finish:
        # Нанесение на поверхность белого фона
        window.fill(WHITE)

        # отображение картинки на поверхности (в окне)
        window.blit(new_img, (0, 0))

        # текст на экране
        text_lose = font2.render("Пропущено: " + str(lost), 1, (BLACK))
        window.blit(text_lose, (10, 50))


        text_win = font2.render("СЧЕТ:" + str(score), 1, (0, 0, 0 ))
        window.blit(text_win, (10, 20))

        # производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        # обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)


        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Перезарядка', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = pygame.sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('monster.jpg', random.randint(80,WIDTH - 80), -40, 3, 65, 65)
            monsters.add(monster)

        if pygame.sprite.spritecollide(ship, monsters, False) or pygame.sprite.spritecollide(ship, asteroids, False):
            pygame.sprite.spritecollide(ship, monsters, True)
            pygame.sprite.spritecollide(ship, asteroids, True)
            life = life - 1

        if life == 3:
            life_color = (0, 0 ,0)
        if life == 2:
            life_color = ( 0, 150, 0)
        if life == 1:
            life_color = (150, 150, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))


        if score >= goal:
            finish = True
            window.fill(win, [200, 200])


        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        # Отображение окна на экране
        pygame.display.update()
    else:
        finish = False
        lost = 0
        score = 0
        life = 3
        num_fire = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        pygame.time.delay(2000)
        for i in range(1, 4):
            monster = Enemy('monster.jpg', random.randint(80, WIDTH - 80), -40, 3, 65, 65)
            monsters.add(monster)

        for i in range(1, 4):
            asteroid = Enemy('baiden.png', random.randint(80, WIDTH - 80), -40, 2, 65, 65)
            asteroids.add(asteroid)

    pygame.time.delay(2)
    clock.tick(FPS)
