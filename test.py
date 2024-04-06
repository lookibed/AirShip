import pygame
import random
import math
import sys
from settings import *

def generate_random_point_around(center, radius):
    angle = random.uniform(0, 2*math.pi)
    distance = random.uniform(0, radius)
    offset_x = distance * math.cos(angle)
    offset_y = distance * math.sin(angle)
    return (center[0] + offset_x, center[1] + offset_y)

pygame.init()
# Установка размера экрана
if fullscreen:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Воздушный бой 1980")


# Загрузка фоновых изображений
background1 = pygame.image.load("back.png").convert()
#background1 = pygame.transform.scale(background1, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Масштабирование до размеров экрана
#background2 = pygame.image.load("back2.png").convert_alpha()
#background2 = pygame.transform.scale(background2, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Масштабирование до размеров экрана
# Загрузка изображения спрайта
green_airship = pygame.image.load("green.png")
green_airship_rect = green_airship.get_rect()
red_airship = pygame.image.load("red.png")
red_airship_rect = red_airship.get_rect()
yellow_airship = pygame.image.load("yellow.png")
yellow_airship_rect = yellow_airship.get_rect()
# Загрузка звуков
airplane_sound = pygame.mixer.Sound("airplane_sound.ogg")
gun_shot_sound = pygame.mixer.Sound("gun-shot.ogg")
boom_sound = pygame.mixer.Sound("boom.ogg")
recharge_start = pygame.mixer.Sound("recharge_start.ogg")
recharge_done = pygame.mixer.Sound("recharge_done.ogg")
# Установка зацикленного воспроизведения музыки
pygame.mixer.music.load("airplane_sound.ogg")
pygame.mixer.music.play(-1)  # -1 для зацикленного воспроизведения


green_airship_speed = ENEMY_SPEED  # Скорость перемещения в пикселях за кадр
center_x = SCREEN_WIDTH // 2
center_y = SCREEN_HEIGHT // 2
clock = pygame.time.Clock()
random_delay = random.uniform(0.2, 2)
car_dist = 100
car_radius = ENEMY_FLY_RADIUS
Canvas_Center = (center_x, center_y)
airCenter = (center_x, center_y)
new_point = generate_random_point_around(Canvas_Center, car_radius)
dx = new_point[0] - airCenter[0]
dy = new_point[1] - airCenter[1]
angle = math.atan2(dy, dx)
step = 0
dist = math.sqrt(abs(dx)**2 + abs(dy)**2)
max_steps = dist // green_airship_speed
is_moving = False
num_axes = 0
num_buttons = 0

# Установка начального положения спрайта
green_airship_rect.topleft = (airCenter[0]+18, airCenter[1]-314)
red_airship_rect.topleft = (airCenter[0]-56, airCenter[1]+26)
yellow_airship_rect.topleft = (airCenter[0]-382, airCenter[1]-198)
AirShips = [green_airship_rect, yellow_airship_rect, red_airship_rect]


class FireController:
    def __init__(self):
        self.clip_size = 8
        self.clip = self.clip_size
        self.fire_delay = 0.3
        self.fire_cooldown = 2.0
        self.timer_delay = 0
        self.timer_cooldown = self.fire_cooldown
        self.will_fire = False
        self.reload_start = False
        self.fire_start = False

    def update(self):
        if joystick.get_button(0) == 1:
            if self.clip > 0:
                print("FIRE..")
                if not self.fire_start:
                    gun_shot_sound.play(-1)
                    self.fire_start = True
                time_passed = dt
                self.timer_delay -= time_passed
                if self.timer_delay <= 0:
                    self.fire()
            else:
                gun_shot_sound.stop()
        elif self.will_fire:
            print("RELOAD..")
            self.fire_start = False
            gun_shot_sound.stop()
            if not self.reload_start:
                recharge_start.play(-1)
                self.reload_start = True
            self.clip = 0
            time_passed = dt
            self.timer_cooldown -= time_passed
            if self.timer_cooldown <= 0:
                print("RELOADED!")
                recharge_start.stop()
                recharge_done.play()
                self.clip = self.clip_size
                self.timer_cooldown = self.fire_cooldown
                self.will_fire = False
                self.reload_start = False
    def fire(self):
        print("FIRE!")
        self.will_fire = True
        Bullet(RIGHT_BULLET_POS)
        Bullet(LEFT_BULLET_POS)
        self.timer_delay = self.fire_delay - random.uniform(self.fire_delay/10.0, -self.fire_delay/10.0)
        self.clip -= 1
class BigFire:
    def __init__(self):
        self.image = pygame.image.load("boom.png").convert_alpha()
        self.visible = False
        self.delay_visible = BOOM_DELAY_VISIBLE
        self.timer = self.delay_visible

    def update(self):
        if self.visible:
            time_passed = dt  # Время, прошедшее с последнего обновления в секундах
            self.timer -= time_passed
            if self.timer <= 0:
                self.visible = False
    def go(self):
        boom_sound.play()
        self.visible = True
        self.timer = self.delay_visible
    def draw(self):
        if self.visible:
            screen.blit(self.image, (0, 0))
class SmollFire:
    def __init__(self):
        self.image = pygame.image.load("big_shot.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (center_x, center_y)
        self.visible = False
        self.delay_visible = SMOLL_FIRE_DELAY_VISIBLE
        self.timer = self.delay_visible

    def update(self):
        if self.visible:
            time_passed = dt
            self.timer -= time_passed
            if self.timer <= 0:
                self.visible = False

    def go(self):
        random_chance = random.randint(0, 100)
        if random_chance < SMOLL_FIRE_CHANCE:
            self.visible = True
            self.timer = self.delay_visible

    def draw(self):
        if self.visible:
            screen.blit(self.image, self.rect.topleft)
class Bullet:
    def __init__(self, pos):
        self.image = pygame.image.load("shot.png")
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = 1500
        self.realspeed = self.speed * dt
        #
        self.start_dist = math.sqrt((center_x - self.rect.centerx) ** 2 + (center_y - self.rect.centery) ** 2)
        self.dist = self.start_dist
        self.angle = 0
        self.scaler = 0
        self.deaceleration = 0
        self.desize = 0

        List_bullet.append(self)
    def update(self):
        dx = center_x - self.rect.centerx
        dy = center_y - self.rect.centery
        self.angle = math.atan2(dy, dx)
        self.scaler = 1 - ((self.dist/(self.start_dist/100)) / 100)
        self.deaceleration = (self.speed / 2) * self.scaler
        #self.desize = (1-(self.scaler/2))
        #self.rect.scale_by(self.desize)
        self.rect.centerx += (self.speed - self.deaceleration) * math.cos(self.angle) * dt
        self.rect.centery += (self.speed - self.deaceleration) * math.sin(self.angle) * dt
        if self.rect.collidepoint(center_x, center_y):
            for airship in AirShips:
                # - коллайдер
                if self.rect.colliderect(airship):
                    AirShips.remove(airship)
                    airship.width = 8
                    airship = None
                    # - большой буум
                    boom.go()
            # - ранд_спавн fire
            smoll_boom.go()
            # - уничтожится
            self.destroy()
    def destroy(self):
        List_bullet.remove(self)
        del self

    def draw(self):
        screen.blit(self.image, self.rect)

List_bullet = []
fire_controller = FireController()
boom = BigFire()
smoll_boom = SmollFire()
# Создание шрифта
font = pygame.font.SysFont('arial', 36)
# Создание объекта джойстика
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    num_axes = joystick.get_numaxes()
    num_buttons = joystick.get_numbuttons()
    print("Number of axes:", num_axes)
    print("Number of buttons:", num_buttons)


# Основной цикл игры
running = True
dt = 0
while running:
    dt = clock.tick() / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Проверяем нажатие клавиши для переключения режима
            if event.key == pygame.K_ESCAPE:
                # При нажатии клавиши "Esc" выходим из полноэкранного режима
                if fullscreen:
                    fullscreen = False
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Получаем данные с осей джойстика
    if joystick:
        pygame.event.pump()
        x_axis = joystick.get_axis(0)
        y_axis = joystick.get_axis(1)

        # Изменяем направление движения всех вражеского самолета
        airCenterX = airCenter[0]
        airCenterY = airCenter[1]
        airCenterX += int(x_axis * SPEED_JOY_X)
        airCenterY += int(y_axis * SPEED_JOY_Y)
        airCenter = (airCenterX, airCenterY)
        # for airship in AirShips:
        #     # Управление спрайтом с помощью осей джойстика
        #     airship.x += int(x_axis * 3)  # Управление по оси X
        #     airship.y += int(y_axis * 2)  # Управление по оси Y
        #
        #     # Ограничение перемещения спрайта в пределах экрана
        #     airship.x = max(0, min(airship.x, SCREEN_WIDTH - airship.width))
        #     airship.y = max(0, min(airship.y, SCREEN_HEIGHT - airship.height))

    if is_moving == False:
        # Проверка условия времени
        time_passed = dt  # Время, прошедшее с последнего обновления в секундах
        random_delay -= time_passed
        if random_delay <= 0:
            # Вычисляем угол между текущим положением самолета и центром экрана
            new_point = generate_random_point_around(Canvas_Center, car_radius)
            dx = new_point[0] - airCenter[0]
            dy = new_point[1] - airCenter[1]
            angle = math.atan2(dy, dx)
            step = 0
            dist = math.sqrt(abs(dx) ** 2 + abs(dy) ** 2)
            max_steps = dist / green_airship_speed
            is_moving = True

    else:
        # Изменяем направление движения всех вражеского самолета
        airCenterX = airCenter[0]
        airCenterY = airCenter[1]
        airCenterX += int(green_airship_speed * math.cos(angle))
        airCenterY += int(green_airship_speed * math.sin(angle))
        airCenter = (airCenterX, airCenterY)

        step += 1
        if step >= max_steps:
            is_moving = False
            random_delay = random.uniform(ENEMY_DELAY_FLY[0], ENEMY_DELAY_FLY[1])

    green_airship_rect.topleft = (airCenter[0] + 18, airCenter[1] - 314)
    red_airship_rect.topleft = (airCenter[0] - 56, airCenter[1] + 26)
    yellow_airship_rect.topleft = (airCenter[0] - 382, airCenter[1] - 198)



    # update fire_controller/bullet/boom/smoll_boom
    fire_controller.update()
    for bullet in List_bullet:
        bullet.update()
    boom.update()
    smoll_boom.update()

    # Очистка экрана
    screen.fill((0, 0, 0))
    # Отрисовка фоновых изображений
    screen.blit(background1, (0, 0))
    #screen.blit(background2, (0, 0))
    # Отрисовка спрайта
    screen.blit(green_airship, green_airship_rect)
    screen.blit(red_airship, red_airship_rect)
    screen.blit(yellow_airship, yellow_airship_rect)
    # draw bullet/boom/smoll_boom
    for bullet in List_bullet:
        bullet.draw()
    boom.draw()
    smoll_boom.draw()
    if DEBUG:
        # Получение FPS
        fps = str(int(clock.get_fps()))
        # Отрисовка текста
        text = font.render("FPS: " + fps, True, (255,255,255))
        screen.blit(text, (10, 10))

    # Обновление экрана
    pygame.display.flip()


    # # Получаем данные с осей
    # axes = [joystick.get_axis(i) for i in range(num_axes)]
    # # Получаем состояние кнопок
    # buttons = [joystick.get_button(i) for i in range(num_buttons)]
    # print(f'\rAxes: {axes} Buttons: {buttons} Fire: {joystick.get_button(0)}', end='', flush=True)
    # # print(f'\rRed: {yellow_airship_rect.x},{yellow_airship_rect.y}', end='', flush=True)

pygame.quit()
sys.exit()
