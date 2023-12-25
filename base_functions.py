from pygame import quit, mouse, QUIT


# Отрисовка кнопок и обработка наведения мыши на них
def draw_buttons_group(group, screen):
    for b in group:
        b.draw(screen)
        b.check_hover(mouse.get_pos())
