import sys
import os
import random
import copy

# Thêm thư mục gốc vào path để import được các module từ gói source
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from source.gomoku import Board
from source.AI import CaroAI
from source.utils import TrainingLogger

def play_match(ai1_weights, ai1_def, ai2_weights, ai2_def, rounds=3):
    """
    Sử dụng Double Round Robin: Với mỗi thế trận ngẫu nhiên, cho 2 AI đấu 2 ván đảo quân.
    Điều này giúp loại bỏ hoàn toàn lợi thế đi trước.
    """
    score1, score2 = 0, 0
    size = 9
    for _ in range(rounds):
        # Tạo một thế trận khởi đầu ngẫu nhiên
        r_start, c_start = random.randint(2, size-3), random.randint(2, size-3)
        
        # Chơi 2 ván với cùng thế trận này
        for swap in [False, True]:
            board = Board(size)
            board.make_move(r_start, c_start)
            
            # Xác định ai là Player 1 (người đi nước tiếp theo sau nước ngẫu nhiên)
            # Ván 1: AI1 là P1, AI2 là P2. Ván 2: Đảo ngược.
            p1_is_challenger = not swap
            
            agent_challenger = CaroAI(player_id=1 if p1_is_challenger else 2, depth=4, weights=ai1_weights, defense_multiplier=ai1_def)
            agent_best = CaroAI(player_id=2 if p1_is_challenger else 1, depth=4, weights=ai2_weights, defense_multiplier=ai2_def)
            
            # Giảm time_limit để huấn luyện nhanh hơn (0.5s vẫn đủ cho depth 3-4 với Alpha-Beta)
            while board.check_win() == 0:
                curr_agent = agent_challenger if board.current_player == agent_challenger.player_id else agent_best
                move, _, _, _ = curr_agent.get_move(board, mode="alpha_beta", time_limit=0.5)
                if move:
                    board.make_move(move[0], move[1])
                else: break
            
            winner = board.check_win()
            if winner == agent_challenger.player_id:
                score1 += 2
            elif winner == agent_best.player_id:
                score2 += 2
            else:
                score1 += 1
                score2 += 1
            
    return score1 > score2

def evolve():
    # Khởi đầu
    best_weights = {3: 10000, 2: 500}
    best_def = 2.0
    # Khởi tạo logger huấn luyện
    train_logger = TrainingLogger()
    
    print(f"Bắt đầu huấn luyện... Gốc: {best_weights}, Def: {best_def}")

    for generation in range(1, 51): # Tăng số thế hệ lên để AI có thời gian tiến hóa
        # Tạo biến dị (Mutation)
        challenger_weights = {
            3: max(5000, best_weights[3] + random.randint(-800, 800)), # Biến dị nhỏ hơn để tinh chỉnh
            2: max(200, best_weights[2] + random.randint(-100, 100))
        }
        challenger_def = round(max(1.2, best_def + random.uniform(-0.2, 0.2)), 2)
        
        print(f"\nThế hệ {generation}: Challenger thử nghiệm {challenger_weights}, Def: {challenger_def}")
        
        # Chơi 3 vòng (6 ván đấu) để đánh giá
        is_better = play_match(challenger_weights, challenger_def, best_weights, best_def, rounds=3)
        
        # Ghi log kết quả thế hệ này vào file CSV
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