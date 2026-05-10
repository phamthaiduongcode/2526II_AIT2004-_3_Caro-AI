import sys
import os
import random
import copy

# Thêm thư mục gốc vào path để import được các module từ gói source
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from source.gomoku import Board
from source.AI import CaroAI
from source.utils import TrainingLogger

def mutate_params(best_weights, best_def, generation):
    """Tạo ra biến dị từ bộ thông số tốt nhất hiện tại với biên độ giảm dần (Simulated Annealing)."""
    # Giảm dần mutation range theo thế hệ: từ 100% xuống tối thiểu 30% sau 300 thế hệ
    scale = max(0.3, 1.0 - generation / 300)
    
    challenger_weights = {
        3: max(5000, best_weights[3] + random.randint(int(-800 * scale), int(800 * scale))),
        2: max(200, best_weights[2] + random.randint(int(-100 * scale), int(100 * scale))),
        1: max(10, best_weights.get(1, 50) + random.randint(int(-10 * scale), int(10 * scale)))
    }
    challenger_def = round(max(1.2, best_def + random.uniform(-0.2 * scale, 0.2 * scale)), 2)
    return challenger_weights, challenger_def

def play_match(ai1_weights, ai1_def, ai2_weights, ai2_def, rounds=6):
    """
    Thi đấu đối kháng để đánh giá chất lượng bộ trọng số.
    Sử dụng Double Round Robin: Mỗi thế trận ngẫu nhiên chơi 2 ván đảo quân để triệt tiêu lợi thế đi trước.
    """
    score1, score2 = 0, 0
    size = 9
    for r_idx in range(rounds):
        # 1. Tạo thế trận khởi đầu 3 nước ngẫu nhiên (tránh shadowing variable và đảm bảo đủ 3 nước)
        start_moves = []
        temp_board = Board(size)
        while len(start_moves) < 3:
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
                # Loại bỏ giới hạn thời gian trong training để AI luôn đạt đúng depth=3
                move, _, _, _ = curr.get_move(board, mode="alpha_beta", time_limit=None)
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
            
    return score1 - score2

def evolve():
    """Vòng lặp tiến hóa tham số Heuristic."""
    # Khởi đầu với bộ thông số "Vàng" từ thế hệ 564 của lần chạy trước
    best_weights = {3: 9466, 2: 559, 1: 68}
    best_def = 1.44

    train_logger = TrainingLogger()
    
    print(f"Bắt đầu huấn luyện... Gốc: {best_weights}, Def: {best_def}")

    # Chạy thêm 200 thế hệ để tinh chỉnh sâu (Fine-tuning)
    for generation in range(1, 201):
        challenger_weights, challenger_def = mutate_params(best_weights, best_def, generation)
        
        print(f"\nThế hệ {generation}: Challenger thử nghiệm {challenger_weights}, Def: {challenger_def}")
        
        # Chỉ chấp nhận challenger nếu thắng rõ ràng (margin >= 2)
        margin = play_match(challenger_weights, challenger_def, best_weights, best_def, rounds=6)
        is_better = margin >= 2
        
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