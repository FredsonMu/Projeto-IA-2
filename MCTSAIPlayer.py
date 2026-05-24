import math
import random

from Player import Player


def other_piece(piece):
    return 2 if piece == 1 else 1


class MCTSNode:
    def __init__(self, board, parent=None, move=None, player_just_moved=None, next_piece=1):
        self.board = board
        self.parent = parent
        self.move = move
        self.player_just_moved = player_just_moved
        self.next_piece = next_piece
        self.children = []
        self.untried_moves = board.get_valid_moves()
        self.visits = 0
        self.wins = 0.0

    def select_child(self, exploration_weight):
        return max(
            self.children,
            key=lambda child: child.ucb1_score(exploration_weight),
        )

    def ucb1_score(self, exploration_weight):
        if self.visits == 0:
            return float("inf")

        exploitation = self.wins / self.visits
        parent_visits = max(1, self.parent.visits)
        exploration = exploration_weight * math.sqrt(math.log(parent_visits) / self.visits)
        return exploitation + exploration

    def expand(self, rng):
        move = rng.choice(self.untried_moves)
        self.untried_moves.remove(move)

        new_board = self.board.copy()
        new_board.drop_piece(move, self.next_piece)

        child = MCTSNode(
            board=new_board,
            parent=self,
            move=move,
            player_just_moved=self.next_piece,
            next_piece=other_piece(self.next_piece),
        )
        self.children.append(child)
        return child

    def backpropagate(self, winner):
        node = self
        while node is not None:
            node.visits += 1
            if winner == 0:
                node.wins += 0.5
            elif winner == node.player_just_moved:
                node.wins += 1.0
            node = node.parent


class MCTSAIPlayer(Player):
    def __init__(
        self,
        piece,
        max_iterations=1000,
        exploration_weight=math.sqrt(2),
        random_seed=None,
        use_tactical_checks=True,
    ):
        super().__init__(piece)
        self.max_iterations = max(1, int(max_iterations))
        self.exploration_weight = exploration_weight
        self.random = random.Random(random_seed)
        self.use_tactical_checks = use_tactical_checks

    def get_move(self, board):
        valid_moves = board.get_valid_moves()
        if not valid_moves:
            return None
        if len(valid_moves) == 1:
            return valid_moves[0]

        if self.use_tactical_checks:
            winning_move = self._find_winning_move(board, self.piece)
            if winning_move is not None:
                return winning_move

            blocking_move = self._find_winning_move(board, other_piece(self.piece))
            if blocking_move is not None:
                return blocking_move

        root = MCTSNode(
            board=board.copy(),
            player_just_moved=other_piece(self.piece),
            next_piece=self.piece,
        )

        for _ in range(self.max_iterations):
            node = root

            while (
                not node.untried_moves
                and node.children
                and self._terminal_result(node.board) is None
            ):
                node = node.select_child(self.exploration_weight)

            if node.untried_moves and self._terminal_result(node.board) is None:
                node = node.expand(self.random)

            winner = self._terminal_result(node.board)
            if winner is None:
                winner = self._simulate_random_game(node.board.copy(), node.next_piece)

            node.backpropagate(winner)

        best_child = max(
            root.children,
            key=lambda child: (
                child.visits,
                child.wins / child.visits if child.visits else 0.0,
            ),
        )
        return int(best_child.move)

    def _find_winning_move(self, board, piece):
        for move in board.get_valid_moves():
            test_board = board.copy()
            test_board.drop_piece(move, piece)
            if test_board.check_winner(piece):
                return move
        return None

    def _simulate_random_game(self, board, next_piece):
        current_piece = next_piece

        while True:
            valid_moves = board.get_valid_moves()
            if not valid_moves:
                return 0

            move = self.random.choice(valid_moves)
            board.drop_piece(move, current_piece)

            if board.check_winner(current_piece):
                return current_piece
            if board.is_board_full():
                return 0

            current_piece = other_piece(current_piece)

    def _terminal_result(self, board):
        if board.check_winner(1):
            return 1
        if board.check_winner(2):
            return 2
        if board.is_board_full():
            return 0
        return None
