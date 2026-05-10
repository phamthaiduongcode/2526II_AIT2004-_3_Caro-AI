import sys
import os
import random
import copy

# Thêm thư mục gốc vào path để import được các module từ gói source
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from source.gomoku import Board
from source.AI import CaroAI
from source.utils import TrainingLogger

def mutate_params(best_weights, best_def):
    """Tạo ra biến dị từ bộ thông số tốt nhất hiện tại."""
    challenger_weights = {
        3: max(5000, best_weights[3] + random.randint(-800, 800)),
        2: max(200, best_weights[2] + random.randint(-100, 100)),
        1: max(10, best_weights.get(1, 50) + random.randint(-10, 10))
    }
    challenger_def = round(max(1.2, best_def + random.uniform(-0.2, 0.2)), 2)
    return challenger_weights, challenger_def

def play_match(ai1_weights, ai1_def, ai2_weights, ai2_def, rounds=3):
    """
    Thi đấu đối kháng để đánh giá chất lượng bộ trọng số.
    Sử dụng Double Round Robin: Mỗi thế trận ngẫu nhiên chơi 2 ván đảo quân để triệt tiêu lợi thế đi trước.
    """
    score1, score2 = 0, 0
    size = 9
    for _ in range(rounds):
        # 1. Tạo thế trận khởi đầu 3 nước ngẫu nhiên để phá vỡ tính lặp lại (Asymmetric Starts)
        start_moves = []
        temp_board = Board(size)
        for _ in range(3):
            r, c = random.randint(2, size-3), random.randint(2, size-3)
            if temp_board.make_move(r, c):
                start_moves.append((r, c))
        
        # 2. Thi đấu đảo ngược quân cờ (Double Round Robin)
        for swap in [False, True]:
            board = Board(size)
            for r, c in start_moves: board.make_move(r, c)
            board.recalculate_hash() # Đảm bảo Hash Zobrist đồng bộ với thế trận khởi đầu

            p1_is_challenger = not swap
            # Gán ID dựa trên lượt đi hiện tại của bàn cờ
            cid = board.current_player if p1_is_challenger else 3 - board.current_player
            bid = 3 - cid
            
            agent_c = CaroAI(player_id=cid, depth=3, weights=ai1_weights, defense_multiplier=ai1_def)
            agent_b = CaroAI(player_id=bid, depth=3, weights=ai2_weights, defense_multiplier=ai2_def)

            while board.check_win() == 0:
                curr = agent_c if board.current_player == cid else agent_b
                # Sử dụng Time Limit ngắn (0.2s) để tăng tốc độ huấn luyện
                move, _, _, _ = curr.get_move(board, mode="alpha_beta", time_limit=0.2)
                if move:
                    board.make_move(move[0], move[1])
                else:
                    break # Trường hợp bàn cờ đầy hoặc không tìm được nước
            
            winner = board.check_win()
            if winner == cid:
                score1 += 2 # Challenger thắng
            elif winner == bid:
                score2 += 2 # Best thắng
            elif winner == -1:
                score1 += 1
                score2 += 1
            
    return score1 > score2

def evolve():
    """Vòng lặp tiến hóa tham số Heuristic."""
    # Khởi đầu với bộ thông số "Vàng" từ thế hệ 564 của lần chạy trước
    best_weights = {3: 9256, 2: 585, 1: 55}
    best_def = 1.45

    train_logger = TrainingLogger()
    
    print(f"Bắt đầu huấn luyện... Gốc: {best_weights}, Def: {best_def}")

    # Chạy thêm 200 thế hệ để tinh chỉnh sâu (Fine-tuning)
    for generation in range(1, 201):
        challenger_weights, challenger_def = mutate_params(best_weights, best_def)
        
        print(f"\nThế hệ {generation}: Challenger thử nghiệm {challenger_weights}, Def: {challenger_def}")
        
        is_better = play_match(challenger_weights, challenger_def, best_weights, best_def, rounds=3)
        
        train_logger.log_generation(generation, challenger_weights, challenger_def, is_better, best_weights, best_def)

        if is_better:
            print(f"--> [MỚI] Challenger chiến thắng! Cập nhật bộ trọng số.")
            best_weights = challenger_weights
            best_def = challenger_def
        else:
            print(f"--> Giữ lại bộ trọng số cũ.")

    print("\n" + "="*30)
    print(f"KẾT QUẢ HUẤN LUYỆN CUỐI CÙNG:")
    print(f"Weights: {best_weights}")
    print(f"Defense Multiplier: {best_def}")
    print("="*30)
    print("Bạn có thể copy bộ số này vào file AI.py để máy đánh khôn hơn!")

if __name__ == "__main__":
    evolve()