import csv
import os

class GameLogger:
    def __init__(self, filename="logs/experiment_results.csv"):
        self.filename = filename
        # Tạo thư mục logs nếu chưa có
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        
        # Khởi tạo file với header nếu file chưa tồn tại
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Turn', 'Algorithm', 'Depth', 'Nodes_Visited', 'Time_Seconds', 'Score', 'Move'])
        self.turn = 0

    def log_result(self, algo, depth, nodes, duration, score, move):
        """Ghi kết quả thực nghiệm của một nước đi vào file CSV."""
        self.turn += 1
        with open(self.filename, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([self.turn, algo, depth, nodes, f"{duration:.6f}", score, str(move)])

    def log_human_move(self, move):
        """Ghi nước đi của người chơi vào file CSV."""
        self.turn += 1
        with open(self.filename, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([self.turn, 'Human', '-', '-', '-', '-', str(move)])

    def log_game_end(self, winner):
        """Ghi dấu kết thúc vào log."""
        label = {1: "Human_Win", 2: "AI_Win", -1: "Draw"}.get(winner, "Unknown")
        with open(self.filename, mode='a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow([self.turn + 1, label, '-', '-', '-', '-', '-'])

class TrainingLogger:
    def __init__(self, filename="logs/training_history.csv"):
        self.filename = filename
        # Tạo thư mục logs nếu chưa có
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        
        # Header ghi lại lịch sử tiến hóa
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Generation', 'Challenger_Weights', 'Challenger_Def', 'Is_Better', 'Best_Weights', 'Best_Def'])

    def log_generation(self, gen, c_weights, c_def, is_better, b_weights, b_def):
        """Ghi lại thông tin của một thế hệ huấn luyện."""
        with open(self.filename, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([gen, str(c_weights), c_def, is_better, str(b_weights), b_def])