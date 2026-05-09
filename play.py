from source.gomoku import Board
from source.AI import CaroAI
from source.utils import GameLogger

if __name__ == "__main__":
    size = 9 # Tối thiểu theo đề bài
    board = Board(size)
    ai_depth = 2
    ai_mode = "alpha_beta" # Hoặc "minimax" để so sánh
    ai = CaroAI(player_id=2, depth=ai_depth) # Máy là O (2)
    logger = GameLogger()
    
    print("--- CHÀO MỪNG ĐẾN VỚI CARO AI (4 IN A ROW) ---")
    board.display()

    while True:
        if board.current_player == 1:
            print("\nLượt của bạn (X):")
            try:
                r, c = map(int, input("Nhập hàng và cột (vd: 4 4): ").split())
                if not board.make_move(r, c):
                    print("Nước đi không hợp lệ!")
                    continue
            except ValueError:
                continue
        else:
            print("\nAI đang suy nghĩ...")
            move, score, nodes, duration = ai.get_move(board, mode=ai_mode)
            if move:
                board.make_move(move[0], move[1])
                print(f"AI đánh vào: {move}")
                print(f"Thống kê: {nodes} trạng thái, thời gian: {duration:.4f}s, Score: {score}")
                
                # Ghi log dữ liệu vào file CSV để phục vụ thực nghiệm
                logger.log_result(ai_mode, ai_depth, nodes, duration, score, move)
        
        board.display()
        winner = board.check_win()
        if winner != 0:
            if winner == -1:
                print("Hòa!")
            else:
                print(f"Người chơi {winner} ('X' nếu là 1, 'O' nếu là 2) thắng!")
            break