# размер окна(игра не адаптивна к другому размеру!)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
fullscreen = False
DEBUG = True

SPEED_JOY_X = 3  # горизонтальная скорость прицеливания
SPEED_JOY_Y = 2  # вертикальная скорость прицеливания

ENEMY_SPEED = 2  # скорость самолетов
ENEMY_FLY_RADIUS = 150  # радиус полета самолетиков вокруг центра
ENEMY_DELAY_FLY = (0.3,1.9)  # задержка в сек перелетов самолетов(случайная от 5 до 9)

BOOM_DELAY_VISIBLE = 1.5  # сколько виден взрыв самолета в секундах
SMOLL_FIRE_DELAY_VISIBLE = 0.4  # сколько маленький взрыв пули попавшей в центр
SMOLL_FIRE_CHANCE = 80  # 20 % шанс появления малого взрыва

LEFT_BULLET_POS = (20, (SCREEN_HEIGHT // 2)+220)
RIGHT_BULLET_POS = (SCREEN_WIDTH-20, (SCREEN_HEIGHT // 2)+220)