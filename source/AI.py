import time
import math

class CaroAI:
    def __init__(self, player_id, depth=4, weights=None, defense_multiplier=2.0):
        self.player_id = player_id
        self.opponent_id = 3 - player_id
        self.depth = depth
        self.nodes_visited = 0
        # Nếu không truyền weights, sử dụng bộ trọng số mặc định
        self.weights = weights if weights else {3: 10000, 2: 500}
        self.defense_multiplier = defense_multiplier
        self.transposition_table = {}  # {hash: (depth, flag, value, best_move)}
        self.killer_moves = [[None] * 2 for _ in range(20)]  # Lưu 2 nước killer mỗi độ sâu
        self.start_time = 0
        self.time_limit = 2.0  # Mặc định mỗi nước đi có tối đa 2 giây

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
        score += self.calculate_player_score(board, self.player_id, self.weights)
        # Hệ số phòng thủ cao để AI cực kỳ cẩn thận với chuỗi của đối thủ
        score -= self.calculate_player_score(board, self.opponent_id, self.weights) * self.defense_multiplier
        return score

    def calculate_player_score(self, board, player, weights):
        total_score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for r in range(board.size):
            for c in range(board.size):
                for dr, dc in directions:
                    p_count = 0
                    empty_count = 0
                    possible = True
                    
                    # Kiểm tra nhanh 4 ô liên tiếp
                    for i in range(4):
                        nr, nc = r + dr * i, c + dc * i
                        if not (0 <= nr < board.size and 0 <= nc < board.size):
                            possible = False
                            break
                        val = board.grid[nr][nc]
                        if val == player:
                            p_count += 1
                        elif val == 0:
                            empty_count += 1
                        else: # Gặp quân đối thủ
                            possible = False
                            break

                    if possible and p_count >= 2:
                        total_score += weights.get(p_count, 0)
        return total_score

    def score_move_quick(self, board, r, c):
        """Đánh giá nhanh độ 'hot' của một ô để sắp xếp nước đi."""
        score = 0
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0: continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < board.size and 0 <= nc < board.size and board.grid[nr][nc] != 0:
                    score += 1
        return score

    def minimax(self, board, depth, is_maximizing):
        self.nodes_visited += 1
        result = board.check_win()
        if result == self.player_id: return 1000000, None
        if result == self.opponent_id: return -1000000, None
        if result == -1: return 0, None
        if depth == 0: return self.evaluate_board(board), None

        moves = board.get_legal_moves()
        # Sắp xếp nước đi: Ưu tiên ô có nhiều quân xung quanh + gần trung tâm
        moves.sort(key=lambda m: (
            self.score_move_quick(board, m[0], m[1]), 
            -abs(m[0] - board.size // 2) - abs(m[1] - board.size // 2)
        ), reverse=True)
        
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
        
        # Kiểm tra thời gian định kỳ (cứ mỗi 1000 node)
        if self.nodes_visited % 1000 == 0:
            if time.time() - self.start_time > self.time_limit:
                return None, None # Trả về None để báo hiệu hết thời gian

        board_hash = board.get_hash()
        alpha_orig = alpha
        beta_orig = beta

        # 1. Tra cứu bảng Transposition (Bộ nhớ đệm trạng thái)
        if board_hash in self.transposition_table:
            tt_depth, tt_flag, tt_val, tt_move = self.transposition_table[board_hash]
            if tt_depth >= depth:
                if tt_flag == "EXACT": return tt_val, tt_move
                elif tt_flag == "LOWER": alpha = max(alpha, tt_val)
                elif tt_flag == "UPPER": beta = min(beta, tt_val)
                if alpha >= beta: return tt_val, tt_move

        result = board.check_win()
        if result == self.player_id: return 1000000, None
        if result == self.opponent_id: return -1000000, None
        if result == -1: return 0, None
        if depth == 0: return self.evaluate_board(board), None

        moves = board.get_legal_moves()
        # 2. Cải tiến Move Ordering với Killer Heuristic
        killers = self.killer_moves[depth]
        moves.sort(key=lambda m: (
            m in killers, # Ưu tiên các nước đi "sát thủ" đã tìm thấy trước đó
            self.score_move_quick(board, m[0], m[1]), 
            -abs(m[0] - board.size // 2) - abs(m[1] - board.size // 2)
        ), reverse=True)
        
        best_move = moves[0] if moves else None

        if is_maximizing:
            best_score = -float('inf')
            for r, c in moves:
                board.make_move(r, c)
                score, _ = self.alpha_beta(board, depth - 1, alpha, beta, False)
                board.undo_move()
                
                if score is None: return None, None # Thoát nhanh do hết thời gian

                if score > best_score:
                    best_score = score
                    best_move = (r, c)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    # Lưu Killer move
                    if killers[0] != (r, c):
                        killers[1] = killers[0]
                        killers[0] = (r, c)
                    break
        else:
            best_score = float('inf')
            for r, c in moves:
                board.make_move(r, c)
                score, _ = self.alpha_beta(board, depth - 1, alpha, beta, True)
                board.undo_move()
                
                if score is None: return None, None # Thoát nhanh do hết thời gian

                if score < best_score:
                    best_score = score
                    best_move = (r, c)
                beta = min(beta, best_score)
                if beta <= alpha:
                    # Lưu Killer move
                    if killers[0] != (r, c):
                        killers[1] = killers[0]
                        killers[0] = (r, c)
                    break

        # 3. Lưu kết quả vào Transposition Table
        if best_score <= alpha_orig:
            flag = "UPPER"
        elif best_score >= beta_orig:
            flag = "LOWER"
        else:
            flag = "EXACT"
        self.transposition_table[board_hash] = (depth, flag, best_score, best_move)
        
        return best_score, best_move

    def get_move(self, board, mode="alpha_beta", time_limit=2.0):
        self.nodes_visited = 0
        self.start_time = time.time()
        self.time_limit = time_limit
        
        final_best_move = None
        final_best_score = 0
        
        # Iterative Deepening Loop
        # Thay vì chỉ chạy 1 lần độ sâu self.depth, ta chạy từ 1 đến depth
        for current_depth in range(1, self.depth + 1):
            if mode == "minimax":
                score, move = self.minimax(board, current_depth, True)
            else:
                score, move = self.alpha_beta(board, current_depth, -float('inf'), float('inf'), True)
            
            # Nếu bị ngắt do hết thời gian, lấy kết quả của độ sâu hoàn thiện gần nhất
            if score is None:
                break
            
            final_best_move = move
            final_best_score = score
            
            # Nếu đã tìm thấy nước thắng, không cần đào sâu thêm
            if abs(final_best_score) >= 900000:
                break

        end_time = time.time()
        return final_best_move, final_best_score, self.nodes_visited, end_time - self.start_time