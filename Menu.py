import pygame

pygame.init()

FPS = 144
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Couleurs du thème médiéval RPG
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
DARK_GREEN = (0, 100, 0)
BURGUNDY = (128, 0, 32)
HOVER_COLOR = (255, 215, 0)  # Or pour l'effet de survol

font = pygame.font.Font(None, 36)
input_font = pygame.font.Font(None, 48)

# Fonction pour dessiner un bouton
def draw_button(x, y, width, height, text, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width//2, y + height//2))
    screen.blit(text_surface, text_rect)

# Fonction pour dessiner le champ de texte
def draw_text_input(x, y, width, height, text):
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)
    text_surface = input_font.render(text, True, BLACK)
    screen.blit(text_surface, (x + 5, y + 5))

run = True
username = ""
while run:
    xMouse, yMouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_player.collidepoint(xMouse, yMouse):
                print("Joueur sélectionné")
            elif button_master.collidepoint(xMouse, yMouse):
                print("Maître du jeu sélectionné")
            elif button_quit.collidepoint(xMouse, yMouse):
                run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                username = username[:-1]
            elif event.key == pygame.K_RETURN:
                print(f"Pseudo: {username}")
            else:
                username += event.unicode

    screen.fill(WHITE)

    # Définir les dimensions des boutons et du champ de texte
    button_width = 250
    button_height = 60
    button_margin = 20
    input_width = 300
    input_height = 50

    # Calculer les positions centrées
    button_player = pygame.Rect((WIDTH - button_width) // 2, 200, button_width, button_height)
    button_master = pygame.Rect((WIDTH - button_width) // 2, 200 + button_height + button_margin, button_width, button_height)
    button_quit = pygame.Rect((WIDTH - button_width) // 2, 200 + 2 * (button_height + button_margin), button_width, button_height)
    input_box = pygame.Rect((WIDTH - input_width) // 2, 100, input_width, input_height)

    # Dessiner les boutons et champ de texte
    draw_button(button_player.x, button_player.y, button_player.width, button_player.height, "Joueur", GOLD if not button_player.collidepoint(xMouse, yMouse) else HOVER_COLOR)
    draw_button(button_master.x, button_master.y, button_master.width, button_master.height, "Maitre du jeu", DARK_GREEN if not button_master.collidepoint(xMouse, yMouse) else HOVER_COLOR)
    draw_button(button_quit.x, button_quit.y, button_quit.width, button_quit.height, "Quitter", BURGUNDY if not button_quit.collidepoint(xMouse, yMouse) else HOVER_COLOR)

    draw_text_input(input_box.x, input_box.y, input_box.width, input_box.height, username)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
