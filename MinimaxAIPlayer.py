import math
from Player import Player


class MinimaxAIPlayer(Player):
    def __init__(self, piece, max_depth=4):
        super().__init__(piece)
        self.max_depth = max_depth
        self.opponent = 3 - piece

    # ------------------------------------------------------------------ #
    # Public interface                                                      #
    # ------------------------------------------------------------------ #

    def get_move(self, board):
        valid_moves = board.get_valid_moves()

        # Immediate win
        for col in valid_moves:
            b = board.copy()
            b.drop_piece(col, self.piece)
            if b.check_winner(self.piece):
                return col

        # Block opponent's immediate win
        for col in valid_moves:
            b = board.copy()
            b.drop_piece(col, self.opponent)
            if b.check_winner(self.opponent):
                return col

        # Minimax with alpha-beta pruning
        best_score = -math.inf
        best_col = self._center_sorted(valid_moves, board.cols)[0]

        for col in self._center_sorted(valid_moves, board.cols):
            b = board.copy()
            b.drop_piece(col, self.piece)
            score = self._minimax(b, self.max_depth - 1, -math.inf, math.inf, False)
            if score > best_score:
                best_score = score
                best_col = col

        return best_col

    def evaluate_board(self, board, player):
        """Heuristic evaluation of the board from the perspective of player."""
        opponent = 3 - player
        score = 0
        grid = board.grid
        rows, cols = board.rows, board.cols
        n = board.n_connect

        # Center column bonus
        center = cols // 2
        center_pieces = [int(grid[r][center]) for r in range(rows)]
        score += center_pieces.count(player) * 3

        # Horizontal windows
        for r in range(rows):
            for c in range(cols - n + 1):
                window = [int(grid[r][c + i]) for i in range(n)]
                score += self._score_window(window, player, opponent)

        # Vertical windows
        for c in range(cols):
            for r in range(rows - n + 1):
                window = [int(grid[r + i][c]) for i in range(n)]
                score += self._score_window(window, player, opponent)

        # Diagonal / windows
        for r in range(n - 1, rows):
            for c in range(cols - n + 1):
                window = [int(grid[r - i][c + i]) for i in range(n)]
                score += self._score_window(window, player, opponent)

        # Diagonal \ windows
        for r in range(rows - n + 1):
            for c in range(cols - n + 1):
                window = [int(grid[r + i][c + i]) for i in range(n)]
                score += self._score_window(window, player, opponent)

        return score

    # ------------------------------------------------------------------ #
    # Minimax                                                               #
    # ------------------------------------------------------------------ #

    def _minimax(self, board, depth, alpha, beta, is_maximizing):
        if board.check_winner(self.piece):
            return 100_000 + depth          # earlier win → higher score
        if board.check_winner(self.opponent):
            return -(100_000 + depth)       # earlier loss → lower score
        if board.is_board_full():
            return 0

        if depth == 0:
            return self.evaluate_board(board, self.piece)

        valid_moves = self._center_sorted(board.get_valid_moves(), board.cols)

        if is_maximizing:
            value = -math.inf
            for col in valid_moves:
                b = board.copy()
                b.drop_piece(col, self.piece)
                value = max(value, self._minimax(b, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = math.inf
            for col in valid_moves:
                b = board.copy()
                b.drop_piece(col, self.opponent)
                value = min(value, self._minimax(b, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    # ------------------------------------------------------------------ #
    # Helpers                                                               #
    # ------------------------------------------------------------------ #

    def _score_window(self, window, player, opponent):
        score = 0
        own   = window.count(player)
        empty = window.count(0)
        opp   = window.count(opponent)

        if own == 4:
            score += 100
        elif own == 3 and empty == 1:
            score += 5
        elif own == 2 and empty == 2:
            score += 2

        if opp == 3 and empty == 1:
            score -= 4

        return score

    @staticmethod
    def _center_sorted(moves, cols):
        """Sort moves from center outward for better alpha-beta pruning."""
        center = cols / 2
        return sorted(moves, key=lambda c: abs(c - center))
