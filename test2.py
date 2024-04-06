import pygame

# Размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def main():
    pygame.init()
    pygame.joystick.init()

    try:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print("Initialized Joystick : %s" % joystick.get_name())
    except pygame.error:
        print("Unable to initialize joystick")

    num_axes = joystick.get_numaxes()
    num_buttons = joystick.get_numbuttons()

    print("Number of axes:", num_axes)
    print("Number of buttons:", num_buttons)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Joystick Control")

    # Загрузка спрайта
    sprite = pygame.image.load("sprite.png")
    sprite_rect = sprite.get_rect()
    sprite_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    try:
        while True:
            pygame.event.pump()

            # Получаем данные с осей
            axes = [joystick.get_axis(i) for i in range(num_axes)]
            print("Axes:", axes)

            # Получаем состояние кнопок
            buttons = [joystick.get_button(i) for i in range(num_buttons)]
            print("Buttons:", buttons)

            # Передвижение спрайта в зависимости от значений осей
            sprite_rect.x += int(axes[0] * 5)  # Используем первую ось для горизонтального движения
            sprite_rect.y += int(axes[1] * 5)  # Используем вторую ось для вертикального движения

            # Ограничение положения спрайта в пределах экрана
            sprite_rect.x = max(0, min(sprite_rect.x, SCREEN_WIDTH - sprite_rect.width))
            sprite_rect.y = max(0, min(sprite_rect.y, SCREEN_HEIGHT - sprite_rect.height))

            # Отрисовка спрайта и обновление экрана
            screen.fill((255, 255, 255))  # Заливка экрана белым цветом
            screen.blit(sprite, sprite_rect)  # Отображение спрайта
            pygame.display.flip()

    except KeyboardInterrupt:
        pygame.quit()

if __name__ == "__main__":
    main()
