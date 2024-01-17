from os import path
from pygame import image, transform


# Функция для загрузки изображений и их преобразований в pygame-объект изображений
def sized(image, size):
    return transform.scale(image, size)


# Функция для конвентирования изображения в pygame-формат
def loader(folder, name):
    address = path.join(f'..\data\images\{folder}', name)
    return image.load(address)


# Класс для хранения всех изображений, задействованных в игре
class Images:
    # Изображения интерфейса
    arrow_left = [loader('interface', 'arrow_left.png'), loader('interface', 'arrow_left_hover.png')]  # кнопка "назад"
    menu_background = loader('interface', 'menu.jpg')  # фон меню
    lobby_background = loader('interface', 'lobby.png')  # фон лобби (авторское изображение)
    menu_buttons = loader('interface', 'button.png'), loader('interface', 'button_hover.png')  # кнопки меню
    farm_over_buttons = loader('interface', 'farm.png'), loader('interface', 'farm_hover.png')  # кнопки фермера
    builder_over_buttons = loader('interface', 'builder.png'), loader('interface', 'builder_hover.png')  # кнопки build
    plane_over_buttons = loader('interface', 'plane.png'), loader('interface', 'plane_hover.png')  # кнопки инженера

    # Изображения игры Весёлая Ферма
    apple = loader('farm', 'apple.png')  # яйцо
    egg = loader('farm', 'egg.png')  # яблоко
    cabbage = loader('farm', 'cabbage.png')  # капуста
    grass = loader('farm', 'grass.png')  # трава
    farm_background = loader('farm', 'game_background.jpg')  # задний фон игры
    farm_buttons = loader('farm', 'farm.png'), loader('farm', 'farm_hover.png')  # кнопки игры Веселая ферма
    heart = loader('farm', 'heart.png')  # сердца
    left = [loader('farm', f'left{i}.png') for i in range(1, 4)]  # фермер с пустой тележкой, идёт влево
    right = [loader('farm', f'right{i}.png') for i in range(1, 4)]  # фермер с пустой тележкой, идёт вправо
    half_left = [loader('farm', f'half_left{i}.png') for i in range(1, 4)]  # фермер с 50% тележкой, влево
    half_right = [loader('farm', f'half_right{i}.png') for i in range(1, 4)]  # фермер с 50% тележкой, вправо
    full_left = [loader('farm', f'full_left{i}.png') for i in range(1, 4)]  # фермер с полной тележкой, идёт влево
    full_right = [loader('farm', f'full_right{i}.png') for i in range(1, 4)]  # фермер с полной тележкой, идёт вправо

    # Изображения игры Строительный Тетрис
    build_buttons = loader('builder', 'build.png'), loader('builder', 'build_hover.png')  # кнопки локации строителя
    brick_names = ('yellow_brick', 'blue_brick', 'red_brick', 'green_brick', 'aqua_brick', 'brick', 'gray_brick',
                   'pink_brick')
    bricks = list(loader('builder', f'{color}.png') for color in brick_names)  # разноцветные кирпичики
    tetris_background = loader('builder', 'background.jpg')  # задний фон игрового окна тетриса (не всего окна)
    tetris_fullsize_background = loader('builder', 'background_window.png')  # фон окна тетриса (всего окна)

    # Изображения игры Юный Инженер
    engineer_buttons = loader('engineer', 'engineer.png'), loader('engineer', 'engineer_hover.png')
    engineer_background = loader('engineer', 'back.jpg')
    airplane0 = loader('engineer', 'empty.png')  # Пустое изображение
    airplane1 = loader('engineer', 'plane_no_cabine.png')  # Самолёт с фюзеляжем
    airplane2 = loader('engineer', 'plane_no_rubber.png')  # Добавлена кабина
    airplane3 = loader('engineer', 'plane_no_wings.png')  # добавлен хвост
    airplane4 = loader('engineer', 'plane_no_engine.png')  # добавлены крылья
    airplane5 = loader('engineer', 'airplane.png')  # добавлен двигатель
    airplane6 = loader('engineer', 'full_airplane.png')  # добавлены шасси (самолёт собран)
    fuselage = loader('engineer', 'fuselage.png')  # фюзеляж
    cabine = loader('engineer', 'cabine.png')  # кабина
    rudder = loader('engineer', 'rudder.png')  # хвост
    wing = loader('engineer', 'wing.png')  # крылья
    engine = loader('engineer', 'plane_engine.png')  # двигатель
    chassis = loader('engineer', 'chassis.png')  # шасси
    stand = loader('engineer', 'back.png')  # стенд, на котором собирается самолёт
