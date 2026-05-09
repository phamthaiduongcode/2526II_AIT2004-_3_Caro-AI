import pygame
import sys
from source.gomoku import Board
from source.AI import CaroAI

# Cấu hình màu sắc và kích thước
BOARD_SIZE = 9
CELL_SIZE = 60
MARGIN = 40
WINDOW_SIZE = BOARD_SIZE * CELL_SIZE + 2 * MARGIN
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

class CaroGUI:
    def __init__(self, board, ai):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 50))
        pygame.display.set_caption("UET Caro AI - 4 in a row")
        self.font = pygame.font.SysFont('Arial', 20)
        self.board = board
        self.ai = ai
        self.game_over = False

    def draw_board(self):
        self.screen.fill(WHITE)
        # Vẽ lưới
        for i in range(BOARD_SIZE + 1):
            start_pos_v = (MARGIN + i * CELL_SIZE, MARGIN)
            end_pos_v = (MARGIN + i * CELL_SIZE, MARGIN + BOARD_SIZE * CELL_SIZE)
            pygame.draw.line(self.screen, BLACK, start_pos_v, end_pos_v, 1)

            start_pos_h = (MARGIN, MARGIN + i * CELL_SIZE)
            end_pos_h = (MARGIN + BOARD_SIZE * CELL_SIZE, MARGIN + i * CELL_SIZE)
            pygame.draw.line(self.screen, BLACK, start_pos_h, end_pos_h, 1)

        # Vẽ quân cờ
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                center = (MARGIN + c * CELL_SIZE + CELL_SIZE // 2, MARGIN + r * CELL_SIZE + CELL_SIZE // 2)
                if self.board.grid[r][c] == 1: # Người (X)
                    pygame.draw.line(self.screen, RED, (center[0]-20, center[1]-20), (center[0]+20, center[1]+20), 3)
                    pygame.draw.line(self.screen, RED, (center[0]+20, center[1]-20), (center[0]-20, center[1]+20), 3)
                elif self.board.grid[r][c] == 2: # Máy (O)
                    pygame.draw.circle(self.screen, BLUE, center, 22, 3)

    def run(self):
        while True:
            self.draw_board()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if not self.game_over and self.board.current_player == 1 and event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    c = (x - MARGIN) // CELL_SIZE
                    r = (y - MARGIN) // CELL_SIZE
                    if self.board.make_move(r, c):
                        winner = self.board.check_win()
                        if winner != 0: self.game_over = True

            # Lượt của AI
            if not self.game_over and self.board.current_player == 2:
                self.draw_board()
                pygame.display.flip()
                move, _, _, _ = self.ai.get_move(self.board, mode="alpha_beta")
                if move:
                    self.board.make_move(move[0], move[1])
                    winner = self.board.check_win()
                    if winner != 0: self.game_over = True

            if self.game_over:
                msg = "Game Over!"
                winner = self.board.check_win()
                if winner == 1: msg = "Ban thang!"
                elif winner == 2: msg = "AI thang!"
                elif winner == -1: msg = "Hoa!"
                text = self.font.render(msg, True, BLACK)
                self.screen.blit(text, (WINDOW_SIZE // 2 - 50, WINDOW_SIZE + 10))

            pygame.display.flip()

if __name__ == "__main__":
    # Test nhanh UI
    from source.gomoku import Board
    from source.AI import CaroAI
    b = Board(9)
    a = CaroAI(player_id=2, depth=2)
    gui = CaroGUI(b, a)
    gui.run()