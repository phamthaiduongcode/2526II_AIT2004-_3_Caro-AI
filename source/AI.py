import time
import random

class CaroAI:
    def __init__(self, player_id, depth=3):
        self.player_id = player_id
        self.opponent_id = 3 - player_id
        self.depth = depth
        self.nodes_visited = 0

    def evaluate_board(self, board):
        """
        Hàm đánh giá Heuristic nâng cao.
        Gán điểm số dựa trên các mẫu hình (patterns) của cửa sổ 4 ô.
        """
        score = 0
        # Trọng số điểm cho các tình huống:
        # 4 quân: Thắng tuyệt đối.
        # 3 quân + 1 ô trống: Cực kỳ nguy hiểm.
        # 2 quân + 2 ô trống: Tiềm năng tạo thế công.
        weights = {4: 100000, 3: 1000, 2: 100}

        score += self.calculate_player_score(board, self.player_id, weights)
        # Nhân hệ số 1.2 cho đối thủ để AI có xu hướng chơi phòng thủ/chặn nước đi nguy hiểm của người chơi
        score -= self.calculate_player_score(board, self.opponent_id, weights) * 1.2
        return score

    def calculate_player_score(self, board, player, weights):
        total_score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for r in range(board.size):
            for c in range(board.size):
                for dr, dc in directions:
                    window = []
                    for i in range(4):
                        nr, nc = r + dr * i, c + dc * i
                        if 0 <= nr < board.size and 0 <= nc < board.size:
                            window.append(board.grid[nr][nc])

                    if len(window) == 4:
                        p_count = window.count(player)
                        empty_count = window.count(0)
                        
                        # Một cửa sổ 4 ô chỉ có giá trị nếu nó không bị quân đối thủ chặn đứng
                        if p_count + empty_count == 4:
                            if p_count >= 2:
                                total_score += weights.get(p_count, 0)
        return total_score

    def minimax(self, board, depth, is_maximizing):
        self.nodes_visited += 1
        result = board.check_win()
        if result == self.player_id: return 1000000, None
        if result == self.opponent_id: return -1000000, None
        if result == -1: return 0, None
        if depth == 0: return self.evaluate_board(board), None

        moves = board.get_legal_moves()
        # Move Ordering: Ưu tiên các nước đi gần trung tâm bàn cờ
        moves.sort(key=lambda m: abs(m[0] - board.size//2) + abs(m[1] - board.size//2))
        
        best_move = moves[0] if moves else None

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
        # Move Ordering: Giúp Alpha-Beta cắt nhánh sớm hơn rất nhiều
        moves.sort(key=lambda m: abs(m[0] - board.size//2) + abs(m[1] - board.size//2))
        
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