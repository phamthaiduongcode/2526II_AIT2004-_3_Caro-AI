import random

class Board:
    def __init__(self, size=15):
        self.size = size
        # Khởi tạo bàn cờ với toàn bộ giá trị là 0 (ô trống)
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.current_player = 1  # 1 là X, 2 là O
        self.history = []  # Lưu lịch sử để phục vụ AI (Undo move)

        # Khởi tạo Zobrist Hashing để nhận diện trạng thái bàn cờ
        # Mỗi ô có 3 trạng thái: trống (0), X (1), O (2)
        self.zobrist_table = [[[random.getrandbits(64) for _ in range(3)] 
                               for _ in range(size)] for _ in range(size)]
        self.current_hash = random.getrandbits(64)

    def get_hash(self):
        return self.current_hash

    def is_valid_move(self, row, col):
        """Kiểm tra nước đi có nằm trong bàn cờ và ô đó có trống không."""
        return 0 <= row < self.size and 0 <= col < self.size and self.grid[row][col] == 0

    def check_win(self):
        """Kiểm tra xem có ai thắng chưa (4 quân liên tiếp)."""
        # Tối ưu: Chỉ kiểm tra xung quanh nước đi cuối cùng trong history
        if not self.history:
            return 0
        r, c, p = self.history[-1]
        win_player = self._check_at(r, c)
        if win_player != 0:
            return win_player
            
        if len(self.history) == self.size * self.size:
            return -1 # Hòa
        return 0 # Chưa kết thúc

    def _check_at(self, r, c):
        """Kiểm tra thắng thua tại một vị trí cụ thể (Tối ưu O(1))."""
        player = self.grid[r][c]
        if player == 0: return 0
        
        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
            count = 1
            # Kiểm tra hai phía của quân cờ vừa đánh
            for i in range(1, 4):
                nr, nc = r + dr * i, c + dc * i
                if 0 <= nr < self.size and 0 <= nc < self.size and self.grid[nr][nc] == player:
                    count += 1
                else: break
            for i in range(1, 4):
                nr, nc = r - dr * i, c - dc * i
                if 0 <= nr < self.size and 0 <= nc < self.size and self.grid[nr][nc] == player:
                    count += 1
                else: break
            
            if count >= 4: return player
        return 0

    def make_move(self, row, col):
        """Thực hiện nước đi và chuyển lượt."""
        if self.is_valid_move(row, col):
            # Update hash: XOR quân cờ cũ (0) và quân cờ mới
            self.current_hash ^= self.zobrist_table[row][col][self.grid[row][col]]
            self.grid[row][col] = self.current_player
            self.current_hash ^= self.zobrist_table[row][col][self.current_player]
            
            self.history.append((row, col, self.current_player))
            
            # Chuyển lượt: nếu là 1 thì thành 2, nếu là 2 thì thành 1
            self.current_player = 3 - self.current_player
            return True
        return False

    def undo_move(self):
        """Hoàn tác nước đi cuối cùng (Rất quan trọng cho thuật toán AI)."""
        if not self.history:
            return
        
        row, col, player = self.history.pop()
        # Update hash ngược lại
        self.current_hash ^= self.zobrist_table[row][col][self.grid[row][col]]
        self.grid[row][col] = 0
        self.current_hash ^= self.zobrist_table[row][col][0]
        
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

    def get_legal_moves(self):
        """Lấy danh sách các nước đi khả thi. 
        Tối ưu: Chỉ xét các ô trống trong bán kính 2 ô quanh các quân đã đánh.
        Tuy nhiên, luôn ưu tiên các nước đi thắng ngay lập tức hoặc chặn đối thủ thắng."""
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

        # Kiểm tra nước đi thắng/chặn ngay trong danh sách candidates để tăng tốc
        win_moves = []
        block_moves = []
        opponent = 3 - self.current_player
        for r, c in candidates:
            # Thử thắng
            self.grid[r][c] = self.current_player
            if self._check_at(r, c) == self.current_player:
                win_moves.append((r, c))
            self.grid[r][c] = 0
            
            # Thử chặn
            self.grid[r][c] = opponent
            if self._check_at(r, c) == opponent:
                block_moves.append((r, c))
            self.grid[r][c] = 0

        if win_moves:
            return list(set(win_moves))
        if block_moves:
            return list(set(block_moves))
        
        # Fallback: nếu không có ứng viên nào trong bán kính nhưng bàn cờ còn trống nhiều,
        # thì có thể cần mở rộng tìm kiếm bằng cách trả về tất cả các ô trống.
        # Điều này tránh trường hợp AI bị "kẹt" khi không có quân nào gần đó.
        if not candidates and len(occupied) < self.size * self.size / 2:
            all_empty_moves = []
            for r in range(self.size):
                for c in range(self.size):
                    if self.grid[r][c] == 0:
                        all_empty_moves.append((r,c))
            return all_empty_moves

        return list(candidates)

# Ví dụ sử dụng:
if __name__ == "__main__":
    board = Board(15)
    board.make_move(7, 7) # Đánh vào giữa
    board.make_move(8, 8) # Đánh vào ô kế tiếp
    board.display()
    board.undo_move()
    board.display()