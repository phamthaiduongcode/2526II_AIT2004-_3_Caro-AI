from source.gomoku import Board
from source.AI import CaroAI
from source.utils import GameLogger

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

    # Kỹ thuật Monkey Patching: Ghi đè phương thức để in ra terminal khi chơi trên GUI
    original_make_move = board.make_move
    def patched_make_move(r, c):
        current_p = board.current_player
        success = original_make_move(r, c)
        if success:
            symbol = 'X' if current_p == 1 else 'O'
            print(f"\n[Move] Người chơi {current_p} ({symbol}) đánh vào: ({r}, {c})")
            board.display()
            winner = board.check_win()
            if winner != 0:
                if winner == -1: print(">>> KẾT THÚC: HÒA <<<")
                else: print(f">>> KẾT THÚC: NGƯỜI CHƠI {winner} THẮNG <<<")
        return success
    
    original_get_move = ai.get_move
    def patched_get_move(board_state, mode=ai_mode):
        move, score, nodes, duration = original_get_move(board_state, mode)
        print(f"\n[AI Thinking] {nodes} nodes duyệt, thời gian: {duration:.4f}s")
        print(f"[AI Choice] Đánh vào {move} với điểm đánh giá: {score}")
        logger.log_result(mode, ai_depth, nodes, duration, score, move)
        return move, score, nodes, duration

    # Gán các hàm đã được "nâng cấp" vào đối tượng
    board.make_move = patched_make_move
    ai.get_move = patched_get_move

    gui = CaroGUI(board, ai)
    gui.run()

if __name__ == "__main__":
    run_combined_game()