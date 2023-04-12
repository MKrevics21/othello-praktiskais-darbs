#Miks Krevics, 211RDB420, 10.grupa
import pygame
from copy import deepcopy
import sys
import time

#Krāsu definīcijas tekstam, pogām, laukumam, kauliņiem.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 102, 0)
RED = (255, 0, 0)

#Spēles parametri - laukuma izmēri
BOARD_SIZE = 8
WINDOW_SIZE = 640
SEARCH_DEPTH = 3
HUMAN_PLAYER = 1
COMPUTER_PLAYER = 2

#Pogu parametri
class Button:
    def __init__(self, color, x, y, width, height, text=""):
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface((width, height))
        self.surface.fill(color)
        font = pygame.font.Font(None, 30)
        text_surf = font.render(text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(text_surf, text_rect)

#Uzzīmē spēles laukumu un kauliņus
def draw_board(screen, board):
    screen.fill(DARK_GREEN)
    grid_size = WINDOW_SIZE // BOARD_SIZE

    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            rect = pygame.Rect(x * grid_size, y * grid_size, grid_size, grid_size)
            pygame.draw.rect(screen, BLACK, rect, 1)

            if board[y][x] == HUMAN_PLAYER:
                pygame.draw.circle(screen, WHITE, rect.center, grid_size // 2 - 4)
            elif board[y][x] == COMPUTER_PLAYER:
                pygame.draw.circle(screen, BLACK, rect.center, grid_size // 2 - 4)

#Izveido spēles sākuma laukumu
def create_board():
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    board[3][3] = board[4][4] = HUMAN_PLAYER
    board[3][4] = board[4][3] = COMPUTER_PLAYER
    return board

#Izvelne pirms spēles sākuma - lietotājs vai dators
def choose_starting_player(screen):
    while True:
        screen.fill(DARK_GREEN)
        font = pygame.font.Font(None, 50)
        text = font.render("Izvēlies, kurš uzsāk spēli:", True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_SIZE // 2, 100))
        screen.blit(text, text_rect)

        human_button = Button(WHITE, 200, 200, 240, 60, "Lietotājs")
        computer_button = Button(WHITE, 200, 300, 240, 60, "Dators")
        screen.blit(human_button.surface, human_button.rect)
        screen.blit(computer_button.surface, computer_button.rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if human_button.rect.collidepoint(event.pos):
                    return HUMAN_PLAYER
                elif computer_button.rect.collidepoint(event.pos):
                    return COMPUTER_PLAYER

#Pārbauda, vai datora/lietotāja gājiens ir derīgs
def is_valid_move(board, x, y, player):
    if board[y][x] != 0:
        return False

    board = deepcopy(board)
    board[y][x] = player
    opponent = 3 - player

    for direction in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
        dx, dy = direction
        nx, ny = x + dx, y + dy
        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == opponent:
            while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                if board[ny][nx] == 0:
                    break
                if board[ny][nx] == player:
                    return True
                nx, ny = nx + dx, ny + dy

    return False

#Pārbauda vai spēlētājam ir iespēja veikt gājienu
def has_valid_moves(board, player):
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if is_valid_move(board, x, y, player):
                return True
    return False

#Noteikta gājiena veikšana
def make_move(board, x, y, player):
    board[y][x] = player
    opponent = 3 - player

    for direction in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
        dx, dy = direction
        nx, ny = x + dx, y + dy
        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == opponent:
            while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                if board[ny][nx] == 0:
                    break
                if board[ny][nx] == player:
                    while (nx, ny) != (x, y):
                        nx, ny = nx - dx, ny - dy
                        board[ny][nx] = player
                    break
                nx, ny = nx + dx, ny + dy

#Spēles punktu sistēma
def evaluate(board, player):
    score = 0
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == player:
                score += 1
    return score

#Gājiena noteikšana ar koordinātēm
def get_valid_moves(board, player):
    moves = []
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if is_valid_move(board, x, y, player):
                moves.append((x, y))
    return moves



#Minimaksa algoritms
def minimax(board, depth, is_maximizing_player, player, start_time, max_time, moves):
    if depth == 0 or time.time() - start_time > max_time or has_valid_moves(board, player) == False:
        return evaluate(board, player)

    if is_maximizing_player:
        best_score = float('-inf')
        for move in moves:
            new_board = deepcopy(board)
            make_move(new_board, *move, player)
            score = minimax(new_board, depth - 1, False, 3 - player, start_time, max_time, moves)
            best_score = max(best_score, score)
            if time.time() - start_time > max_time:
                break
        return best_score
    else:
        best_score = float('inf')
        for move in moves:
            new_board = deepcopy(board)
            make_move(new_board, *move, player)
            score = minimax(new_board, depth - 1, True, 3 - player, start_time, max_time, moves)
            best_score = min(best_score, score)
            if time.time() - start_time > max_time:
                break
        return best_score


#Pārbauda kurā brīdi lietotājs vai dators ir zaudējis
def game_over(board):
    return not has_valid_moves(board, HUMAN_PLAYER) and not has_valid_moves(board, COMPUTER_PLAYER)


#Pārbauda kurš ir uzvarējis
def draw_winner(screen, message):
    font = pygame.font.Font(None, 50)
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_SIZE//2, 200))
    screen.blit(text, text_rect)

#Parāda spēles rezultātu vai lietotājs ir uzvarējis, zaudējis, vai spēlē ir neizšķirta
def show_game_over_screen(screen, board, message):
    while True:
        draw_board(screen, board)
        font = pygame.font.Font(None, 40)
        text = font.render(message, True, RED)
        text_rect = text.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2 - 100))
        screen.blit(text, text_rect)

        retry_button = pygame.draw.rect(screen, WHITE, (200, 300, 240, 60))
        quit_button = pygame.draw.rect(screen, WHITE, (200, 370, 240, 60))

        font = pygame.font.Font(None, 30)
        text = font.render("Vēlreiz", True, BLACK)
        text_rect = text.get_rect(center=retry_button.center)
        screen.blit(text, text_rect)

        text = font.render("Aizvērt", True, BLACK)
        text_rect = text.get_rect(center=quit_button.center)
        screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(event.pos):
                    return True
                elif quit_button.collidepoint(event.pos):
                    return False


#Reģistrē lietotāja peles klikšķus
def get_mouse_click_position():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Kreisais peles klikšķis
                    x, y = pygame.mouse.get_pos()
                    grid_x, grid_y = x // (WINDOW_SIZE // BOARD_SIZE), y // (WINDOW_SIZE // BOARD_SIZE)
                    return grid_x, grid_y
pass

#Visu notikumu reģistrēšana
def process_ui_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


#Fona krāsas uzstādišana
def draw_text_background(screen, text, text_rect):
        padding = 10
        background_rect = pygame.Rect(text_rect.left - padding, text_rect.top - padding, text_rect.width + padding * 2, text_rect.height + padding * 2)
        pygame.draw.rect(screen, DARK_GREEN, background_rect)

MAX_SEARCH_TIME = 5 
#Galvenā spēles funkcija. 
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption('Othello Spele')
    clock = pygame.time.Clock()

    while True:
        board = create_board()
        current_player = choose_starting_player(screen)
        message = ""

        while not game_over(board):
            clock.tick(60)
            draw_board(screen, board)
            pygame.display.update()
            pygame.display.flip()

            while not has_valid_moves(board, current_player):
                current_player = 3 - current_player
                continue

            if current_player == HUMAN_PLAYER:
                process_ui_events()
                x, y = get_mouse_click_position()

                if is_valid_move(board, x, y, current_player):
                    make_move(board, x, y, current_player)
                    current_player = COMPUTER_PLAYER

            else:
                process_ui_events()
                moves = get_valid_moves(board, COMPUTER_PLAYER)
                if moves:
                    # Pass start_time to minimax function
                    start_time = time.time()
                    score = minimax(board, SEARCH_DEPTH, False, COMPUTER_PLAYER, start_time, MAX_SEARCH_TIME, moves)
                    best_score = float('-inf')
                    best_move = None
                    for move in moves:
                        new_board = deepcopy(board)
                        make_move(new_board, *move, COMPUTER_PLAYER)
                        score = minimax(new_board, SEARCH_DEPTH, False, HUMAN_PLAYER, start_time, MAX_SEARCH_TIME, get_valid_moves(new_board, HUMAN_PLAYER))
                        if score > best_score:
                            best_score = score
                            best_move = move
                    if best_move:
                        make_move(board, *best_move, COMPUTER_PLAYER)
                        current_player = HUMAN_PLAYER
                else:
                    current_player = HUMAN_PLAYER

        if not message:
            if evaluate(board, HUMAN_PLAYER) > evaluate(board, COMPUTER_PLAYER):
                message = "Tu uzvarēji! Vai vēlies mēģināt velreiz?"
            elif evaluate(board, HUMAN_PLAYER) < evaluate(board, COMPUTER_PLAYER):
                message = "Tu zaudēji. Vai vēlies mēģināt velreiz?"
            else:
                message = "Neizšķirts. Vai vēlies mēģināt velreiz?"
        if not show_game_over_screen(screen, board, message):
            break  

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()



   
