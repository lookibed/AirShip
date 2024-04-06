import pygame
import random
import math

# Инициализация Pygame
pygame.init()

# Установка параметров окна
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Car")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Параметры машинки
car_image = pygame.image.load("red.png")
car_rect = car_image.get_rect()
car_rect.center = (WIDTH // 2, HEIGHT // 2)
car_speed = 2
car_dist = 100
car_radius = 250
Canvas_Center = (WIDTH // 2, HEIGHT // 2)

clock = pygame.time.Clock()
running = True
move_timer = 0
# Генерация случайной задержки от 0.2 до 2 секунд
random_delay = random.uniform(0.2, 2)

def generate_random_point_around(center, radius):
    angle = random.uniform(0, 2*math.pi)
    distance = random.uniform(0, radius)
    offset_x = distance * math.cos(angle)
    offset_y = distance * math.sin(angle)
    return (center[0] + offset_x, center[1] + offset_y)

move_distance = 0
move_vector = pygame.math.Vector2(0, 0)

while running:
    screen.fill(WHITE)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    # Проверка условия времени
    time_passed = clock.tick(60) / 1000.0  # Время, прошедшее с последнего обновления в секундах
    random_delay -= time_passed

    if random_delay <= 0:
        # Генерация новой точки для перемещения
        new_point = generate_random_point_around(Canvas_Center, car_radius)
        move_vector = pygame.math.Vector2(new_point[0] - car_rect.centerx, new_point[1] - car_rect.centery)
        move_distance = move_vector.length()
        if move_distance > car_dist:
            move_vector.scale_to_length(car_dist)
        random_delay = random.uniform(0.2, 2)

    # Перемещение машинки
    if move_distance > 0:
        move_vector.scale_to_length(car_speed)
        car_rect.move_ip(move_vector)

    # Отрисовка машинки
    screen.blit(car_image, car_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
