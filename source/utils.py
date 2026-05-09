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
                writer.writerow(['Algorithm', 'Depth', 'Nodes_Visited', 'Time_Seconds', 'Score', 'Move'])

    def log_result(self, algo, depth, nodes, duration, score, move):
        """Ghi kết quả thực nghiệm của một nước đi vào file CSV."""
        with open(self.filename, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([algo, depth, nodes, f"{duration:.6f}", score, str(move)])

print("Utils module initialized with GameLogger.")