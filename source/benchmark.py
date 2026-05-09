import sys
import os
import copy

# Thêm thư mục gốc vào path để import được các module từ source
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from source.gomoku import Board
from source.AI import CaroAI
from source.utils import GameLogger

def run_benchmark():
    # Sử dụng file log riêng cho benchmark để không lẫn với log khi chơi
    logger = GameLogger(filename="logs/benchmark_results.csv")
    size = 9
    ai_depth = 3 # Độ sâu 3 là đủ để thấy sự khác biệt rõ rệt về số node

    # Danh sách các kịch bản thử nghiệm
    test_cases = []

    # 1. Trạng thái trống (Bắt đầu ván - kiểm tra tốc độ khởi đầu)
    s1 = Board(size)
    s1.current_player = 2 # Giả định lượt của AI (O)
    test_cases.append(("Empty_Board", s1))

    # 2. Trạng thái AI có thể thắng ngay (Cần đánh vào hàng 0 để đủ 4 quân 'O')
    s2 = Board(size)
    for c in range(3): 
        s2.grid[0][c] = 2 # AI (O) đã có 3 quân
        s2.history.append((0, c, 2))
    s2.current_player = 2
    test_cases.append(("AI_Win_Move", s2))

    # 3. Trạng thái AI phải chặn người chơi (Người chơi đã có 3 quân 'X')
    s3 = Board(size)
    for c in range(3): 
        s3.grid[4][c+3] = 1 # Người chơi (X) đã có 3 quân
        s3.history.append((4, c+3, 1))
    s3.current_player = 2
    test_cases.append(("AI_Must_Block", s3))

    # 4. Trạng thái giữa ván (Giao tranh phức tạp ở trung tâm)
    s4 = Board(size)
    moves = [(4,4,1), (4,5,2), (5,5,1), (3,3,2), (5,4,1), (3,4,2)]
    for r, c, p in moves:
        s4.grid[r][c] = p
        s4.history.append((r, c, p))
    s4.current_player = 2
    test_cases.append(("Mid_Game_Battle", s4))

    # 5. Trạng thái nhiều lựa chọn (Kiểm tra khả năng lọc nước đi)
    s5 = Board(size)
    s5.grid[0][0] = 1; s5.grid[8][8] = 2
    s5.history = [(0,0,1), (8,8,2)]
    s5.current_player = 2
    test_cases.append(("Sparse_Board", s5))

    print(f"{'Algorithm':<15} | {'State':<15} | {'Nodes':<10} | {'Time (s)':<10} | {'Move'}")
    print("-" * 65)

    for name, board_state in test_cases:
        # Chạy Minimax
        ai_minimax = CaroAI(player_id=2, depth=ai_depth)
        board_m = copy.deepcopy(board_state) # Copy để không làm hỏng state gốc
        move_m, score_m, nodes_m, time_m = ai_minimax.get_move(board_m, mode="minimax")
        logger.log_result(f"Minimax_{name}", ai_depth, nodes_m, time_m, score_m, move_m)
        print(f"{'Minimax':<15} | {name[:15]:<15} | {nodes_m:<10} | {time_m:.4f} | {move_m}")

        # Chạy Alpha-Beta
        ai_ab = CaroAI(player_id=2, depth=ai_depth)
        board_ab = copy.deepcopy(board_state)
        move_ab, score_ab, nodes_ab, time_ab = ai_ab.get_move(board_ab, mode="alpha_beta")
        logger.log_result(f"AlphaBeta_{name}", ai_depth, nodes_ab, time_ab, score_ab, move_ab)
        print(f"{'Alpha-Beta':<15} | {name[:15]:<15} | {nodes_ab:<10} | {time_ab:.4f} | {move_ab}")
        
        # Kiểm tra tính đúng đắn: Minimax và Alpha-Beta PHẢI chọn cùng nước đi và điểm số
        if move_m != move_ab:
            print(f"--> [!] Cảnh báo: Kết quả nước đi khác nhau tại {name}!")

    print("\nBenchmark hoàn tất! Kết quả đã được lưu vào logs/benchmark_results.csv")

if __name__ == "__main__":
    run_benchmark()