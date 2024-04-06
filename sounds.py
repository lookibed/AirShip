import pygame
import os

# Инициализация Pygame
pygame.init()

# Инициализация звука
pygame.mixer.init()

# Установка размера окна
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Пример звуков в Pygame")

# Загрузка звуков
airplane_sound = pygame.mixer.Sound("airplane_sound.ogg")
gun_shot_sound = pygame.mixer.Sound("gun-shot.ogg")
boom_sound = pygame.mixer.Sound("boom.ogg")

# Установка зацикленного воспроизведения музыки
pygame.mixer.music.load("airplane_sound.ogg")
pygame.mixer.music.play(-1)  # -1 для зацикленного воспроизведения

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Воспроизведение звука выстрела при нажатии 'Space'
            if event.key == pygame.K_SPACE:
                gun_shot_sound.play(-1)  # -1 для зацикленного воспроизведения
            # Воспроизведение звука взрыва при нажатии 'b'
            elif event.key == pygame.K_b:
                boom_sound.play()

        elif event.type == pygame.KEYUP:
            # Остановка звука выстрела при отпускании 'Space'
            if event.key == pygame.K_SPACE:
                gun_shot_sound.stop()

# Выход из игры
pygame.quit()
