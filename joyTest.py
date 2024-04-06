import pygame

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

    try:
        while True:
            pygame.event.pump()

            # Получаем данные с осей
            axes = [joystick.get_axis(i) for i in range(num_axes)]

            # Получаем состояние кнопок
            buttons = [joystick.get_button(i) for i in range(num_buttons)]

            print(f'\rAxes: {axes} Buttons: {buttons}', end='', flush=True)

    except KeyboardInterrupt:
        pygame.quit()

if __name__ == "__main__":
    main()