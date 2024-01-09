# Данный класс предназначен для быстрой смены картинки для того или иного объекта (кнопки, фона и так далее)
class Images:
    # фон главного меню
    mainmenu_img = 'files/img/interface/menu.jpg'

    # изображения, связанные с игровым лобби
    lobby_background = 'files/img/interface/game_background_secret_version.png'
    farm_button = 'files/img/farm_game/farm.png', 'files/img/farm_game/farm_hover.png'
    builder_button = 'files/img/builder_game/build.png', 'files/img/builder_game/build_hover.png'
    arrow_back_button = 'files/img/interface/arrow_left.png', 'files/img/interface/arrow_left.png'

    # изображения для игры "Весёлая ферма"
    egg_img = "files/img/farm_game/egg.png"
    apple_img = 'files/img/farm_game/apple.png'
    farmer_left_img = "files/img/farm_game/farmer_left.png"
    farmer_right_img = "files/img/farm_game/farmer_right.png"
    heart_img = "files/img/farm_game/heart.png"
    farm_img = 'files/img/farm_game/game_background.jpg'


# Переменные для ширины и высоты экрана
WIDTH, HEIGHT = 1200, 700

# Уровень сложности K (1 <= K <= 3)
with open('files/game_settings/settings.txt') as f:
    DIFFICULT_K = {'Легкий': 1, 'Средний': 2, 'Высокий': 3}[str(f.readlines()[0])]
