class Board:
    def __init__(self, size=15):
        self.size = size
        # Khởi tạo bàn cờ với toàn bộ giá trị là 0 (ô trống)
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.current_player = 1  # 1 là X, 2 là O
        self.history = []  # Lưu lịch sử để phục vụ AI (Undo move)

    def is_valid_move(self, row, col):
        """Kiểm tra nước đi có nằm trong bàn cờ và ô đó có trống không."""
        return 0 <= row < self.size and 0 <= col < self.size and self.grid[row][col] == 0

    def check_win(self):
        """Kiểm tra xem có ai thắng chưa (4 quân liên tiếp)."""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(self.size):
            for c in range(self.size):
                player = self.grid[r][c]
                if player == 0:
                    continue
                
                for dr, dc in directions:
                    count = 1
                    for i in range(1, 4): # Đề bài yêu cầu 4 quân
                        nr, nc = r + dr * i, c + dc * i
                        if 0 <= nr < self.size and 0 <= nc < self.size and self.grid[nr][nc] == player:
                            count += 1
                        else:
                            break
                    if count == 4:
                        return player
        
        if all(cell != 0 for row in self.grid for cell in row):
            return -1 # Hòa
        return 0 # Chưa kết thúc

    def get_legal_moves(self):
        """Lấy danh sách các nước đi khả thi. 
        Tối ưu: Chỉ xét các ô trống trong bán kính 2 ô quanh các quân đã đánh."""
        moves = []
        if not self.history:
            return [(self.size // 2, self.size // 2)]
            
        look_range = 2
        occupied = set((r, c) for r, c, p in self.history)
        candidates = set()
        for r, c in occupied:
            for dr in range(-look_range, look_range + 1):
                for dc in range(-look_range, look_range + 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size and self.grid[nr][nc] == 0:
                        candidates.add((nr, nc))
        return list(candidates)

    def make_move(self, row, col):
        """Thực hiện nước đi và chuyển lượt."""
        if self.is_valid_move(row, col):
            self.grid[row][col] = self.current_player
            self.history.append((row, col, self.current_player))
            
            # Chuyển lượt: nếu là 1 thì thành 2, nếu là 2 thì thành 1
            self.current_player = 3 - self.current_player
            return True
        return False

    def undo_move(self):
        """Hoàn tác nước đi cuối cùng (Rất quan trọng cho thuật toán Minimax)."""
        if not self.history:
            return
        
        row, col, player = self.history.pop()
        self.grid[row][col] = 0
        self.current_player = player # Quay lại lượt của người vừa đánh

    def display(self):
        """Hiển thị bàn cờ cơ bản ra console để debug."""
        print("  " + " ".join([f"{i:x}" for i in range(self.size)])) # In chỉ số cột (hex)
        for r in range(self.size):
            row_str = f"{r:x} "
            for c in range(self.size):
                val = self.grid[r][c]
                if val == 0: row_str += ". "
                elif val == 1: row_str += "X "
                else: row_str += "O "
            print(row_str)

# Ví dụ sử dụng:
if __name__ == "__main__":
    board = Board(15)
    board.make_move(7, 7) # Đánh vào giữa
    board.make_move(8, 8) # Đánh vào ô kế tiếp
    board.display()
    board.undo_move()
    board.display()