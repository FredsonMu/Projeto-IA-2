import argparse
import random
import time
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from Connect4Board import Connect4Board
from MCTSAIPlayer import MCTSAIPlayer
from RandomPlayer import RandomAIPlayer


COLUMNS = [
    "Comparacao",
    "Parametros usados",
    "No de Jogos",
    "Vitorias Jogador 1",
    "Vitorias Jogador 2",
    "Empates",
    "Taxa de Vitorias Jogador 1",
    "Taxa de Vitorias Jogador 2",
    "Duracao Media do Jogo",
    "Duracao Maxima",
    "Duracao Minima",
    "Diferencas de Comportamento Observadas",
]


def play_game(player1, player2, rows=6, cols=7, n_connect=4):
    board = Connect4Board(rows, cols, n_connect)
    players = [player1, player2]
    turn = 0
    moves = 0
    started_at = time.perf_counter()

    while True:
        current_player = players[turn]
        valid_moves = board.get_valid_moves()

        if not valid_moves:
            winner = 0
            break

        move = current_player.get_move(board)
        if move not in valid_moves:
            raise ValueError(
                f"Jogada invalida do jogador {current_player.piece}: {move}. "
                f"Jogadas validas: {valid_moves}"
            )

        board.drop_piece(move, current_player.piece)
        moves += 1

        if board.check_winner(current_player.piece):
            winner = current_player.piece
            break

        if board.is_board_full():
            winner = 0
            break

        turn = (turn + 1) % 2

    duration = time.perf_counter() - started_at
    return winner, duration, moves


def run_match(comparison, player1_factory, player2_factory, games, parameters, observations):
    wins_player1 = 0
    wins_player2 = 0
    draws = 0
    durations = []

    for game_index in range(games):
        random.seed(1000 + game_index)
        player1 = player1_factory(piece=1, game_index=game_index)
        player2 = player2_factory(piece=2, game_index=game_index)
        winner, duration, _ = play_game(player1, player2)

        durations.append(duration)
        if winner == 1:
            wins_player1 += 1
        elif winner == 2:
            wins_player2 += 1
        else:
            draws += 1

    return {
        "Comparacao": comparison,
        "Parametros usados": parameters,
        "No de Jogos": games,
        "Vitorias Jogador 1": wins_player1,
        "Vitorias Jogador 2": wins_player2,
        "Empates": draws,
        "Taxa de Vitorias Jogador 1": wins_player1 / games,
        "Taxa de Vitorias Jogador 2": wins_player2 / games,
        "Duracao Media do Jogo": sum(durations) / len(durations),
        "Duracao Maxima": max(durations),
        "Duracao Minima": min(durations),
        "Diferencas de Comportamento Observadas": observations,
    }


def write_results_xlsx(rows, output_path):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Resultados"
    sheet.append(COLUMNS)

    header_fill = PatternFill("solid", fgColor="D9EAF7")
    for cell in sheet[1]:
        cell.font = Font(bold=True)
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    for row in rows:
        sheet.append([row.get(column, "") for column in COLUMNS])

    for row in sheet.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)

    for column_index, column_name in enumerate(COLUMNS, start=1):
        column_letter = get_column_letter(column_index)
        width = 18
        if column_name in ("Comparacao", "Parametros usados"):
            width = 28
        elif column_name == "Diferencas de Comportamento Observadas":
            width = 55
        sheet.column_dimensions[column_letter].width = width

    for row in range(2, sheet.max_row + 1):
        for column in (7, 8):
            sheet.cell(row=row, column=column).number_format = "0.0%"
        for column in (9, 10, 11):
            sheet.cell(row=row, column=column).number_format = "0.000"

    workbook.save(output_path)


def placeholder(comparison, note):
    return {
        "Comparacao": comparison,
        "Parametros usados": "A preencher",
        "Diferencas de Comportamento Observadas": note,
    }


def main():
    parser = argparse.ArgumentParser(description="Corre testes automaticos e gera resultados.xlsx.")
    parser.add_argument("--games", type=int, default=20)
    parser.add_argument("--mcts-iterations", type=int, default=250)
    parser.add_argument("--output", default="resultados.xlsx")
    args = parser.parse_args()

    rows = [
        placeholder(
            "Minimax vs Aleatorio",
            "A preencher pelo colega depois de adicionar MinimaxAIPlayer e a heuristica.",
        )
    ]

    mcts_row = run_match(
        comparison="MCTS vs Aleatorio",
        player1_factory=lambda piece, game_index: MCTSAIPlayer(
            piece=piece,
            max_iterations=args.mcts_iterations,
            random_seed=2000 + game_index,
        ),
        player2_factory=lambda piece, game_index: RandomAIPlayer(piece=piece),
        games=args.games,
        parameters=f"MCTS max_iterations={args.mcts_iterations}; Random sem parametros",
        observations=(
            "MCTS escolhe jogadas com base em simulacoes aleatorias e tende a melhorar "
            "quando se aumenta max_iterations. O aleatorio nao planeia e escolhe apenas "
            "uma coluna valida ao acaso."
        ),
    )
    rows.append(mcts_row)

    rows.extend(
        [
            placeholder(
                "1a comb Minimax vs MCTS",
                "A preencher em conjunto, ajustando max_depth e max_iterations para tempos semelhantes.",
            ),
            placeholder(
                "2a comb Minimax vs MCTS",
                "A preencher em conjunto, usando uma segunda combinacao de parametros.",
            ),
            placeholder(
                "3a comb Minimax vs MCTS",
                "A preencher em conjunto, usando uma terceira combinacao de parametros.",
            ),
            placeholder(
                "Humano vs IA (Opcional)",
                "Opcional no enunciado.",
            ),
        ]
    )

    output_path = Path(args.output)
    write_results_xlsx(rows, output_path)

    print(f"Ficheiro criado: {output_path}")
    print(
        "MCTS vs Aleatorio: "
        f"{mcts_row['Vitorias Jogador 1']} vitorias J1, "
        f"{mcts_row['Vitorias Jogador 2']} vitorias J2, "
        f"{mcts_row['Empates']} empates, "
        f"duracao media {mcts_row['Duracao Media do Jogo']:.3f}s"
    )


if __name__ == "__main__":
    main()
