# Alpha4 - Estado do Projeto

README temporario para o grupo perceber o que ja esta feito, o que falta fazer e qual e a ideia para apresentar o trabalho.

## Estado atual

Ja esta feita a parte do MCTS.

Ficheiros principais:

- `MCTSAIPlayer.py`: agente MCTS.
- `run_experiments.py`: script para correr jogos automaticos e gerar `resultados.xlsx`.
- `resultados.xlsx`: ja tem a linha `MCTS vs Aleatorio` preenchida.

Ainda falta juntar a parte do Minimax.

## O que foi feito na minha parte

Foi criada a classe `MCTSAIPlayer`, que herda de `Player` e implementa:

- `get_move(self, board)`;
- selecao com UCB1;
- expansao;
- simulacao aleatoria;
- retropropagacao;
- parametro `max_iterations`.

O agente usa sempre `board.copy()` para simular jogadas. Isto e importante porque o enunciado diz que o tabuleiro real deve ser tratado como read-only.

Tambem foram adicionadas duas verificacoes simples antes do MCTS:

- se o MCTS pode ganhar ja, joga essa coluna;
- se o adversario pode ganhar ja, bloqueia essa coluna.

Isto ajuda a evitar erros obvios quando o numero de iteracoes e baixo.

## Ideia do MCTS

O MCTS escolhe jogadas atraves de experiencias.

Em vez de calcular todos os futuros possiveis do jogo, o algoritmo faz varias simulacoes aleatorias. Cada simulacao joga ate ao fim e devolve um resultado: vitoria, derrota ou empate.

Com muitas simulacoes, o agente estima quais jogadas parecem melhores.

Cada iteracao tem 4 fases:

1. Selecao: desce pela arvore escolhendo nos com UCB1.
2. Expansao: cria um novo no para uma jogada ainda nao testada.
3. Simulacao: joga aleatoriamente ate ao fim.
4. Retropropagacao: atualiza visitas e resultados nos nos usados.

## UCB1

O UCB1 serve para equilibrar duas ideias:

- aproveitar jogadas que ja tiveram bons resultados;
- experimentar jogadas que ainda foram pouco testadas.

Formula usada:

```text
vitorias / visitas + C * sqrt(log(visitas_do_pai) / visitas)
```

No codigo, `C` e `exploration_weight`, com valor padrao `sqrt(2)`.

## Como testar a minha parte

Para correr jogos automaticos:

```bash
py run_experiments.py --games 20 --mcts-iterations 250 --output resultados.xlsx
```

Resultado atual:

```text
MCTS vs Aleatorio
Jogos: 20
Vitorias MCTS: 20
Vitorias Aleatorio: 0
Empates: 0
Duracao media: 3.634s
Duracao maxima: 8.440s
Duracao minima: 1.847s
```

## O que falta o colega fazer

Falta criar `MinimaxAIPlayer.py`.

O Minimax deve ter:

- classe `MinimaxAIPlayer`;
- herdar de `Player`;
- metodo `get_move(self, board)`;
- algoritmo Minimax;
- poda Alpha-Beta;
- parametro `max_depth`;
- funcao `evaluate_board(board, player)`;
- uso de `board.copy()` para simular jogadas.

A heuristica deve considerar:

- vitorias;
- derrotas;
- sequencias de 2 pecas;
- sequencias de 3 pecas;
- ameacas do adversario;
- controlo do centro.

## Como juntar as duas partes

Depois de existir `MinimaxAIPlayer.py`, podemos testar assim:

```python
from Connect4Game import Connect4Game
from MinimaxAIPlayer import MinimaxAIPlayer
from MCTSAIPlayer import MCTSAIPlayer

p1 = MinimaxAIPlayer(piece=1, max_depth=4)
p2 = MCTSAIPlayer(piece=2, max_iterations=500)

game = Connect4Game()
winner = game.run_game(p1, p2, headless=True)
print(winner)
```

Os dois agentes ligam ao jogo da mesma forma: ambos implementam `get_move(board)` e devolvem uma coluna valida.

## Testes finais que faltam

Ainda temos de preencher o resto de `resultados.xlsx`:

- `Minimax vs Aleatorio`;
- `MCTS vs Aleatorio` ja esta preenchido;
- `Minimax vs MCTS` com 3 combinacoes diferentes;
- `Humano vs IA` e opcional.

Sugestao inicial para as 3 combinacoes:

```text
Combinacao 1: Minimax max_depth=3 | MCTS max_iterations=250
Combinacao 2: Minimax max_depth=4 | MCTS max_iterations=500
Combinacao 3: Minimax max_depth=5 | MCTS max_iterations=1000
```

Depois ajustamos estes valores para tentar deixar os tempos de execucao parecidos, como o enunciado pede.

## Pitch / ideia para apresentar

A ideia do nosso projeto e comparar duas formas diferentes de tomar decisoes num jogo adversarial.

O Minimax tenta prever as jogadas futuras usando uma arvore de jogo. Como nao consegue ver tudo ate ao fim, usa uma profundidade maxima e uma heuristica para avaliar tabuleiros.

O MCTS usa outra estrategia: em vez de avaliar manualmente cada tabuleiro, faz muitas simulacoes aleatorias e aprende estatisticamente quais jogadas costumam dar melhores resultados.

Frase curta para a defesa:

```text
O Minimax decide atraves de procura e heuristica; o MCTS decide atraves de simulacoes. No fim, comparamos os dois pela taxa de vitorias e pelo tempo medio de jogo.
```

## Checklist final antes do ZIP

- Confirmar que `MCTSAIPlayer.py` funciona.
- Juntar `MinimaxAIPlayer.py`.
- Correr testes contra aleatorio.
- Correr `Minimax vs MCTS`.
- Completar `resultados.xlsx`.
- Remover ficheiros que nao devem ir no ZIP: `.venv`, `.idea`, `__pycache__`, `docs`, `Doc Principal`, `.git`.
- Decidir se este README vai ou nao no ZIP final.
