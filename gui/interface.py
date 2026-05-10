import pygame
import sys
import threading
import copy
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
    def __init__(self, board, ai, logger=None):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 50))
        pygame.display.set_caption("UET Caro AI - 4 in a row")
        self.font = pygame.font.SysFont('Arial', 20)
        self.board = board
        self.ai = ai
        self.logger = logger
        self.game_over = False
        self.ai_thinking = False

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

    def ai_move_wrapper(self):
        """Hàm bọc để chạy AI trong Thread riêng."""
        board_copy = copy.deepcopy(self.board)
        move, score, nodes, duration = self.ai.get_move(board_copy, mode="alpha_beta")
        
        if not self.game_over:
            print(f"\n[AI Thinking] {nodes} nodes duyệt, thời gian: {duration:.4f}s")
            print(f"[AI Choice] AI chọn {move} với Score: {score}")
            if self.logger:
                self.logger.log_result("alpha_beta", self.ai.depth, nodes, duration, score, move)
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"move": move, "score": score}))
        self.ai_thinking = False

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
                        print(f"\n[Move] Người chơi 1 (X) đánh vào: ({r}, {c})")
                        self.board.display()
                        if self.logger:
                            self.logger.log_human_move((r, c))
                        winner = self.board.check_win()
                        if winner != 0: self.handle_end_game(winner)
                        if winner != 0: self.game_over = True

                if event.type == pygame.USEREVENT:
                    if event.move is None:
                        # Nếu AI không có nước đi, kiểm tra thắng thua để kết thúc game
                        if self.board.check_win() != 0:
                            self.game_over = True
                    else:
                        r, c = event.move
                        if self.board.make_move(r, c):
                            if self.board.check_win() != 0: self.game_over = True

            # Lượt của AI
            if not self.game_over and self.board.current_player == 2 and not self.ai_thinking:
                self.ai_thinking = True
                threading.Thread(target=self.ai_move_wrapper, daemon=True).start()

            if self.game_over:
                msg = "Game Over!"
                winner = self.board.check_win()
                if winner == 1: msg = "Ban thang!"
                elif winner == 2: msg = "AI thang!"
                elif winner == -1: msg = "Hoa!"
                text = self.font.render(msg, True, BLACK)
                self.screen.blit(text, (WINDOW_SIZE // 2 - 50, WINDOW_SIZE + 10))

            pygame.display.flip()

    def handle_end_game(self, winner):
        """Xử lý kết thúc ván — in log ra terminal và ghi file."""
        self.game_over = True
        if winner == 1:
            print("\n[KẾT THÚC] Người chơi (X) thắng!")
        elif winner == 2:
            print("\n[KẾT THÚC] AI (O) thắng!")
        elif winner == -1:
            print("\n[KẾT THÚC] Hòa!")
        if self.logger:
            self.logger.log_game_end(winner)

if __name__ == "__main__":
    # Test nhanh UI
    from source.gomoku import Board
    from source.AI import CaroAI
    b = Board(9)
    a = CaroAI(player_id=2, depth=2)
    gui = CaroGUI(b, a)
    gui.run()