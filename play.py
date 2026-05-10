from source.gomoku import Board
from source.AI import CaroAI
from source.utils import GameLogger
import os

def run_combined_game():
    try:
        from gui.interface import CaroGUI
    except ImportError:
        print("\n[!] Lỗi: Bạn chưa cài đặt thư viện 'pygame' để chạy chế độ GUI.")
        print("[!] Hãy chạy lệnh: pip install pygame")
        return

    # Khởi tạo các thành phần
    size = 9
    board = Board(size)
    ai_depth = 3
    ai_mode = "alpha_beta"
    ai = CaroAI(player_id=2, depth=ai_depth)
    logger = GameLogger()

    print(f"\n--- CARO AI: GUI MODE WITH TERMINAL LOGGING ---")
    print(f"AI Depth: {ai_depth} | Algorithm: {ai_mode}")
    board.display()
    
    gui = CaroGUI(board, ai, logger)
    gui.run()

if __name__ == "__main__":
    run_combined_game()