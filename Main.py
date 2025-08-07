import pygame
import asyncio
import websockets
import component

pygame.init()

FPS = 144
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
DARK_GREEN = (0, 100, 0)
BURGUNDY = (128, 0, 32)
HOVER_COLOR = (255, 215, 0)

font = pygame.font.Font(None, 36)
input_font = pygame.font.Font(None, 48)

# Fonction d'envoi de message WebSocket
async def send_message(name, role):
    uri = "ws://192.168.0.72:8765"  # Remplace par l'IP du serveur
    message = f'Name:"{name}", Role:{role}'  # Format du message
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)  # Envoie du message
        response = await websocket.recv()
        print(f"Réponse du serveur: {response}")


def draw_button(x, y, width, height, text):
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 3)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def draw_text_input(x, y, width, height, text):
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)
    text_surface = input_font.render(text, True, BLACK)
    screen.blit(text_surface, (x + 5, y + 5))

run = True
username = ""
message_sent = False  # Variable pour vérifier si le message a déjà été envoyé
while run:
    xMouse, yMouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_player.collidepoint(xMouse, yMouse) and not message_sent:
                print("Joueur sélectionné")
                asyncio.get_event_loop().run_until_complete(send_message(username, "Joueur"))
                message_sent = True  # Empêche l'envoi d'un autre message
            elif button_master.collidepoint(xMouse, yMouse) and not message_sent:
                print("Maître du jeu sélectionné")
                asyncio.get_event_loop().run_until_complete(send_message(username, "Maître du jeu"))
                message_sent = True  # Empêche l'envoi d'un autre message
            elif button_quit.collidepoint(xMouse, yMouse):
                run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                username = username[:-1]
            elif event.key == pygame.K_RETURN and not message_sent:
                print(f"Pseudo: {username}")
                asyncio.get_event_loop().run_until_complete(send_message(username, "Joueur"))
                message_sent = True  # Empêche l'envoi d'un autre message
            else:
                username += event.unicode

    background = pygame.transform.scale(component.background_menu, (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))

    button_width = 250
    button_height = 60
    button_margin = 20
    input_width = 300
    input_height = 50

    button_player = pygame.Rect((WIDTH - button_width) // 2, 200, button_width, button_height)
    button_master = pygame.Rect((WIDTH - button_width) // 2, 200 + button_height + button_margin, button_width, button_height)
    button_quit = pygame.Rect((WIDTH - button_width) // 2, 200 + 2 * (button_height + button_margin), button_width, button_height)

    draw_button(button_player.x, button_player.y, button_player.width, button_player.height, "Joueur")
    draw_button(button_master.x, button_master.y, button_master.width, button_master.height, "Maitre du jeu")
    draw_button(button_quit.x, button_quit.y, button_quit.width, button_quit.height, "Quitter")

    draw_text_input((WIDTH - input_width) // 2, 100, input_width, input_height, username)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
