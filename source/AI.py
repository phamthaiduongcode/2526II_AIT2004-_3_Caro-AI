import time
import random

class CaroAI:
    def __init__(self, player_id, depth=3):
        self.player_id = player_id
        self.opponent_id = 3 - player_id
        self.depth = depth
        self.nodes_visited = 0

    def evaluate_board(self, board):
        """Hàm đánh giá Heuristic: tính điểm dựa trên các chuỗi 2, 3, 4."""
        score = 0
        # Đơn giản hóa: đếm các mẫu cho player và trừ đi mẫu của đối thủ
        score += self.count_score(board, self.player_id)
        score -= self.count_score(board, self.opponent_id) * 1.5 # Ưu tiên chặn đối thủ
        return score

    def count_score(self, board, p):
        s = 0
        # Các hướng: ngang, dọc, chéo xuôi, chéo ngược
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(board.size):
            for c in range(board.size):
                for dr, dc in directions:
                    line = []
                    for i in range(4): # Xét cửa sổ 4 ô
                        nr, nc = r + dr * i, c + dc * i
                        if 0 <= nr < board.size and 0 <= nc < board.size:
                            line.append(board.grid[nr][nc])
                        else:
                            break
                    
                    if len(line) == 4:
                        count_p = line.count(p)
                        count_empty = line.count(0)
                        if count_p == 4: s += 100000
                        elif count_p == 3 and count_empty == 1: s += 1000
                        elif count_p == 2 and count_empty == 2: s += 100
        return s

    def minimax(self, board, depth, is_maximizing):
        self.nodes_visited += 1
        result = board.check_win()
        if result == self.player_id: return 1000000, None
        if result == self.opponent_id: return -1000000, None
        if result == -1: return 0, None
        if depth == 0: return self.evaluate_board(board), None

        moves = board.get_legal_moves()
        best_move = random.choice(moves) if moves else None

        if is_maximizing:
            best_score = -float('inf')
            for r, c in moves:
                board.make_move(r, c)
                score, _ = self.minimax(board, depth - 1, False)
                board.undo_move()
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
            return best_score, best_move
        else:
            best_score = float('inf')
            for r, c in moves:
                board.make_move(r, c)
                score, _ = self.minimax(board, depth - 1, True)
                board.undo_move()
                if score < best_score:
                    best_score = score
                    best_move = (r, c)
            return best_score, best_move

    def alpha_beta(self, board, depth, alpha, beta, is_maximizing):
        self.nodes_visited += 1
        result = board.check_win()
        if result == self.player_id: return 1000000, None
        if result == self.opponent_id: return -1000000, None
        if result == -1: return 0, None
        if depth == 0: return self.evaluate_board(board), None

        moves = board.get_legal_moves()
        best_move = moves[0] if moves else None

        if is_maximizing:
            best_score = -float('inf')
            for r, c in moves:
                board.make_move(r, c)
                score, _ = self.alpha_beta(board, depth - 1, alpha, beta, False)
                board.undo_move()
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score, best_move
        else:
            best_score = float('inf')
            for r, c in moves:
                board.make_move(r, c)
                score, _ = self.alpha_beta(board, depth - 1, alpha, beta, True)
                board.undo_move()
                if score < best_score:
                    best_score = score
                    best_move = (r, c)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score, best_move

    def get_move(self, board, mode="alpha_beta"):
        self.nodes_visited = 0
        start_time = time.time()
        if mode == "minimax":
            score, move = self.minimax(board, self.depth, True)
        else:
            score, move = self.alpha_beta(board, self.depth, -float('inf'), float('inf'), True)
        
        end_time = time.time()
        return move, score, self.nodes_visited, end_time - start_time