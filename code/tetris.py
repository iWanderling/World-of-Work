from copy import deepcopy
from random import choice
from buttons import Button
from data import *


# Размеры монитора игрока
WINDOW_SIZE = pygame.display.set_mode().get_size()


# Создаем отдельный поверхностный объект для затемнения экрана (для паузы)
dim_surface = pygame.Surface(WINDOW_SIZE)
dim_surface.set_alpha(150)  # Устанавливаем прозрачность


# Размеры окон
WIDTH, HEIGHT = WINDOW_SIZE  # ширина и высота игрового окна
TILE_WIDTH, TILE_HEIGHT = 10, 20  # ширина и высота одной плитки
TILE = 35  # размер плитки
GAME_WINDOW_SIZE = TILE_WIDTH * TILE, TILE_HEIGHT * TILE  # игровое окно
step_x = WIDTH // 2 - GAME_WINDOW_SIZE[0] // 2  # сдвиг игрового поля вправо
step_y = 75  # сдвиг игрового поля вниз


def TetrisGame(function):
    global current_figure, next_figure

    # Проверка на выход фигуры за границы (левой, правой, а также столкновения с полом)
    def check_borders(index) -> bool:
        if current_figure[index].x < 0 or current_figure[i].x > TILE_WIDTH - 1:
            return False
        elif current_figure[index].y > TILE_HEIGHT - 1 or GAME_FIELD[current_figure[i].y][current_figure[i].x]:
            return False
        return True

    """ Работа с переменными (Падающие блоки, игровое поле) """

    # Игровое поле (нужно для отрисовки игрового процесса)
    GAME_FIELD = [[0 for x in range(TILE_WIDTH)] for y in range(TILE_HEIGHT)]

    # Координаты фигур (для отрисовки)
    FIGURES_POSITION = [[(-1, 0), (-1, 1), (0, 0), (0, -1)],  # ⚡
                        [(0, -1), (0, -2), (0, 0), (0, 1)],  # |
                        [(0, -1), (-1, -1), (-1, 0), (0, 0)],  # █
                        [(0, 0), (0, -1), (0, 1), (-1, -1)],  # ⅃
                        [(0, 0), (0, -1), (0, 1), (-1, 0)],  # -|
                        [(0, 0), (0, -1), (0, 1), (1, -1)],  # L
                        [(0, 0), (-1, 0), (0, 1), (-1, -1)]]  # .-

    # начальное расположение новой фигуры
    figures = [[pygame.Rect(x + TILE_WIDTH // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in FIGURES_POSITION]

    # квадратик (1/4 часть) одной фигуры
    figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)

    # Текущая и следующая фигура
    current_figure = deepcopy(choice(figures))
    next_figure = deepcopy(choice(figures))

    sound_parameter = get_volume()  # параметр громкости

    """ Инициализация игры """
    pygame.init()
    pygame.mixer.stop()
    pygame.display.set_caption('Строительный Тетрис')
    screen = pygame.display.set_mode(WINDOW_SIZE)  # окно

    # Подключение к БД
    connect = sqlite3.connect('../settings/records.sqlite')
    cursor = connect.cursor()
    data = cursor.execute('SELECT * from data WHERE game="builder"').fetchone()
    is_played = data[3]

    # Фоны игровых окон
    game_window_background = pygame.transform.scale(Images.tetris_background, GAME_WINDOW_SIZE)
    window_background = pygame.transform.scale(Images.tetris_fullsize_background, WINDOW_SIZE)

    # Работаем со шрифтом игры
    font_scale = 22
    game_font = pygame.font.Font(f'../data/{"fonts"}/{"sunday.ttf"}', font_scale)

    if not is_played:
        get_instruction(screen, window_background, game_font, '../settings/tetris_i.txt', 'builder')
    # Изображения кирпичика текущей фигуры и следующей фигуры
    brick = pygame.transform.scale(choice(Images.bricks), (TILE, TILE))  # создание кирпичика
    next_brick = pygame.transform.scale(choice(Images.bricks), (TILE, TILE))

    # Загрузка звуков для игры
    fall_sound = pygame.mixer.Sound('../data/sounds/fall.mp3')  # звук падения фигуры
    fall_sound.set_volume(sound_parameter)

    sound = pygame.mixer.Sound('../data/sounds/collect-row.mp3')  # звук, который проигрывается при создании ряда
    sound.set_volume(sound_parameter)

    end_music = pygame.mixer.Sound('../data/sounds/builder_end.mp3')  # конец игры
    end_music.set_volume(sound_parameter)

    game_music = pygame.mixer.Sound('../data/sounds/builder_music.mp3')  # игровая музыка
    game_music.set_volume(sound_parameter)
    game_music.play()  # проигрываем фоновую музыку

    # Отрисовка текстов, которые не меняются:
    NEXT_FIGURE_FONT = game_font.render(f'Следующая фигура', True, pygame.Color('aqua'))  # Следующая фигура
    w2, h2 = NEXT_FIGURE_FONT.get_size()  # размеры шрифта NEXT_FIGURE_FONT

    GAME_TITLE = game_font.render('Строительный Тетрис', True, pygame.Color('aqua'))  # Название игры сверху игр. Окна
    w3, h3 = GAME_TITLE.get_size()  # размеры

    # Игровые переменные
    score = ROWS = 0  # очки, собранные ряды
    PAUSED = False  # поставлена ли игра на паузу
    wanna_quit = False  # если игрок нажимает на Esc, то спрашиваем, желает ли он завершить игру (флаг)
    # Координаты падающей фигуры, скорость падения фигуры (пикселей/сек.)
    FALL_CURRENT_POSITION, FALL_SPEED = 0, 300
    FPS = 240
    clock = pygame.time.Clock()
    running = True
    while running:
        is_row_collected = False  # собран ли ряд
        is_fall = False  # упала ли фигура

        # Загрузка фонов игры:
        screen.blit(window_background, (0, 0))
        screen.blit(game_window_background, (step_x, step_y))

        # Текст, отображающий текущий счёт:
        SCORE_FONT = game_font.render(f'Текущий счёт: {score}', True, pygame.Color('aqua'))
        w1, h1 = SCORE_FONT.get_size()  # размеры шрифта SCORE_FONT

        # Отрисовка шрифтов (текста)
        screen.blit(SCORE_FONT, (step_x // 2 - w1 // 2, HEIGHT // 2 - h1 // 2))
        screen.blit(NEXT_FIGURE_FONT, (WIDTH - 475, HEIGHT // 2 - h2 // 2 - 50))
        screen.blit(GAME_TITLE, (WIDTH // 2 - w3 // 2, 5))

        # отрисовка следующей фигуры
        for i in range(4):
            figure_rect.x = next_figure[i].x * TILE + WIDTH - w2 * 1.36
            figure_rect.y = next_figure[i].y * TILE + HEIGHT // 2 + TILE * 2
            screen.blit(next_brick, figure_rect)

        X_DIRECTION = 0  # перемещение по оси X
        ROTATION = False  # переменная для переворачивания фигуры
        old_figure = deepcopy(current_figure)  # копия текущей фигуры (читайте далее)

        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # выход
                exit()
            if event.type == pygame.KEYDOWN:  # обработка перемещения фигуры влево и вправо
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    X_DIRECTION += 1  # перемещение по x ->>
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    X_DIRECTION -= 1  # перемещение по x <<-
                elif event.key == pygame.K_SPACE or event.key == pygame.K_w:  # переворачивание текущей фигуры
                    ROTATION = True
                elif event.key == pygame.K_p and not wanna_quit:
                    PAUSED = not PAUSED
                elif event.key == pygame.K_ESCAPE:  # Попытка завершения игры блокирует паузу
                    wanna_quit = not wanna_quit
                    PAUSED = False
                elif event.key == pygame.K_RETURN and wanna_quit:
                    running = False

        # переворачивание текущей фигуры (по часовой стрелке, на клавишу SPACE)
        if ROTATION:
            FIGURE_CENTER = current_figure[0]
            for i in range(4):
                x = current_figure[i].y - FIGURE_CENTER.y
                y = current_figure[i].x - FIGURE_CENTER.x
                current_figure[i].x = FIGURE_CENTER.x - x
                current_figure[i].y = FIGURE_CENTER.y + y

        # отрисовка текущей фигуры
        for i in range(4):
            figure_rect.x = current_figure[i].x * TILE + step_x
            figure_rect.y = current_figure[i].y * TILE + step_y
            screen.blit(brick, figure_rect)

        # движение текущей фигуры по горизонтальной оси (все квадратики фигуры смещаются на +-1 квадратик)
        # фигура не может забежать за границу, поэтому сохраняем копию текущей фигуры, и если граница будет пересечена,
        # то возвратим копию, иначе разрешаем передвижение
        for i in range(4):
            current_figure[i].x += X_DIRECTION
            if not check_borders(i):
                current_figure = deepcopy(old_figure)
                break

        # движение фигуры вниз (обработка падения)
        FALL_CURRENT_POSITION += FALL_SPEED

        # Обработка столкновения фигуры с "полом" экрана. Если фигура упала, то она сохраняется на игровом поле в том
        # виде, в котором она приземлилась, включая цвет. Также создаём следующую фигуру
        if FALL_CURRENT_POSITION > 2000 and not PAUSED and not wanna_quit:
            FALL_CURRENT_POSITION = 0
            for i in range(4):
                current_figure[i].y += 1
                if not check_borders(i):
                    is_fall = True
                    for i in range(4):
                        # Запоминаем позицию и цвет упавшей фигуры, сохраняем её на поле
                        GAME_FIELD[old_figure[i].y][old_figure[i].x] = brick
                    # создаём новую фигуру
                    current_figure = next_figure
                    brick = next_brick

                    # создаём следующую фигуру
                    next_figure = deepcopy(choice(figures))
                    next_brick = pygame.transform.scale(choice(Images.bricks), (TILE, TILE))
                    break

        # Если игра поставлена на паузу:
        if PAUSED:
            pause(screen, game_font)
        elif wanna_quit:
            pause(screen, game_font, text='Вы хотите выйти? Нажмите ENTER, чтобы завершить игру')

        # поиск заполненных рядов в игровом поле
        row = TILE_HEIGHT - 1
        for r in range(TILE_HEIGHT - 1, -1, -1):
            count = 0
            for i in range(TILE_WIDTH):
                if GAME_FIELD[r][i]:
                    count += 1
                GAME_FIELD[row][i] = GAME_FIELD[r][i]
            if count < TILE_WIDTH:
                row -= 1
            # проигрываем звук если создан полный ряд
            else:
                is_row_collected = True
                sound.play()
                ROWS += 1
                score = ROWS * 100

        # Если упала фигура - проигрываем звук падения
        if not is_row_collected and is_fall:
            fall_sound.play()

        # отрисовка игрового поля
        for y, row in enumerate(GAME_FIELD):
            for x, col in enumerate(row):
                if col:  # отрисовка упавших фигур
                    figure_rect.x, figure_rect.y = x * TILE + step_x, y * TILE + step_y
                    screen.blit(col, figure_rect)

        # проверка окончания игры
        for i in range(TILE_WIDTH):
            if GAME_FIELD[0][i]:
                running = False
                break

        pygame.display.flip()
        clock.tick(FPS)

    # Функция окончания игры:
    game_over(screen, game_font, 'builder', score, TetrisGame, function, Images.builder_over_buttons, window_background,
              'Конец игры!', 'Набрано очков', Button, color="aqua", sound=end_music)
