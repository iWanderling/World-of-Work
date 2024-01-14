from os import path
from pygame import image


# функция для конвентирования изображения в pygame-формат
def loader(folder, name):
    address = path.join(f'..\data\images\{folder}', name)
    return image.load(address)


# Класс для хранения всех изображений, задействованных в игре
class Images:
    # Изображения интерфейса
    arrow_left = loader('interface', 'arrow_left.png')
    menu_background = loader('interface', 'menu.jpg')
    lobby_background = loader('interface', 'lobby.png')
    menu_buttons = loader('interface', 'button.png'), loader('interface', 'button_hover.png')

    # Изображения игры Весёлая Ферма
    apple = loader('farm', 'apple.png')
    egg = loader('farm', 'egg.png')
    cabbage = loader('farm', 'cabbage.png')
    grass = loader('farm', 'grass.png')
    farm_background = loader('farm', 'game_background.jpg')
    farm_buttons = loader('farm', 'farm.png'), loader('farm', 'farm_hover.png')
    heart = loader('farm', 'heart.png')
    left = [loader('farm', f'left{i}.png') for i in range(1, 4)]  # фермер с пустой тележкой, идёт влево
    right = [loader('farm', f'right{i}.png') for i in range(1, 4)]  # фермер с пустой тележкой, идёт вправо
    half_left = [loader('farm', f'half_left{i}.png') for i in range(1, 4)]  # фермер с 50% тележкой, влево
    half_right = [loader('farm', f'half_right{i}.png') for i in range(1, 4)]  # фермер с 50% тележкой, вправо
    full_left = [loader('farm', f'full_left{i}.png') for i in range(1, 4)]  # фермер с полной тележкой, идёт влево
    full_right = [loader('farm', f'full_right{i}.png') for i in range(1, 4)]  # фермер с полной тележкой, идёт вправо

    # Изображения игры Строительный Тетрис
    build_buttons = loader('builder', 'build.png'), loader('builder', 'build_hover.png')

    # Изображения игры Юный Инженер
    engineer_buttons = loader('engineer', 'engineer.png'), loader('engineer', 'engineer_hover.png')
    engineer_background = loader('engineer', 'back.jpg')
    airplane0 = loader('engineer', 'empty.png')
    airplane1 = loader('engineer', 'plane_no_cabine.png')
    airplane2 = loader('engineer', 'plane_no_rubber.png')
    airplane3 = loader('engineer', 'plane_no_wings.png')
    airplane4 = loader('engineer', 'plane_no_engine.png')
    airplane5 = loader('engineer', 'airplane.png')
    airplane6 = airplane5
    fuselage = loader('engineer', 'fuselage.png')
    cabine = loader('engineer', 'cabine.png')
    rudder = loader('engineer', 'rudder.png')
    wing = loader('engineer', 'wing.png')
    engine = loader('engineer', 'plane_engine.png')
    chassis = loader('engineer', 'chassis.png')
    stand = loader('engineer', 'back.png')
