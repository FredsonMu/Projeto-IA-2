# Alpha4 - Projeto de IA

Este projeto implementa agentes de Inteligencia Artificial para jogar Connect 4 / Alpha4.

O objetivo e comparar duas abordagens diferentes:

- Minimax com poda Alpha-Beta;
- Monte Carlo Tree Search, tambem chamado MCTS.

## Estado atual

Neste momento ja temos as duas partes principais feitas:

- `MinimaxAIPlayer.py`: agente Minimax com Alpha-Beta, `max_depth` e heuristica.
- `MCTSAIPlayer.py`: agente MCTS com selecao UCB1, expansao, simulacao e retropropagacao.
- `run_experiments.py`: script para correr jogos automaticos e gerar `resultados.xlsx`.
- `play.py`: script para jogar Humano vs IA com interface grafica.
- `resultados.xlsx`: tabela com os resultados dos testes.

Tambem existem os ficheiros base do jogo:

- `Connect4Board.py`: representa o tabuleiro.
- `Connect4Game.py`: controla o loop do jogo.
- `Connect4Gui.py`: interface grafica em Pygame.
- `Player.py`: classe base dos jogadores.
- `HumanPlayer.py`: jogador humano.
- `RandomPlayer.py`: jogador aleatorio.

## Como estamos a trabalhar

Neste momento vamos trabalhar diretamente na branch `main`.

Antes de mexer no codigo, convem fazer:

```bash
git pull
```

Depois das alteracoes:

```bash
git add .
git commit -m "Mensagem curta sobre a alteracao"
git push
```

Assim os dois ficam sempre com a versao mais recente do projeto.

## Como instalar dependencias

Se o projeto nao correr no computador, instalar:

```bash
py -m pip install numpy pygame openpyxl
```

Dependencias usadas:

- `numpy`: tabuleiro.
- `pygame`: interface grafica.
- `openpyxl`: criacao e atualizacao do ficheiro Excel.

## Como jogar contra a IA

Para jogar manualmente contra uma IA:

```bash
py play.py
```

O programa vai pedir para escolher a IA adversaria:

```text
(1) Minimax
(2) MCTS
```

Depois abre a janela do jogo.

Funcionamento:

- o humano joga com a peca vermelha;
- a IA joga com a peca amarela;
- o humano clica numa coluna para colocar a peca;
- a peca cai para a posicao livre mais baixa dessa coluna;
- depois a IA escolhe automaticamente a jogada dela;
- o jogo continua ate alguem ganhar ou ate o tabuleiro ficar cheio.

No fim, o programa pergunta se queremos jogar novamente. Se forem feitos jogos Humano vs IA, o `play.py` tambem tenta guardar esses resultados no `resultados.xlsx`.

## Como correr testes automaticos

Para correr os testes e gerar de novo o Excel:

```bash
py run_experiments.py --games 20 --mcts-iterations 250 --output resultados.xlsx
```

Este script corre:

- `Minimax vs Aleatorio`;
- `MCTS vs Aleatorio`;
- `Minimax vs MCTS` com 3 combinacoes de parametros;
- deixa `Humano vs IA` como opcional.

As 3 combinacoes usadas sao:

```text
1a combinacao: Minimax max_depth=3 | MCTS max_iterations=25
2a combinacao: Minimax max_depth=4 | MCTS max_iterations=100
3a combinacao: Minimax max_depth=5 | MCTS max_iterations=430
```

A ideia e comparar os algoritmos com tempos de execucao semelhantes.

## Como o jogo funciona

O jogo e uma versao do Connect 4.

Regras:

- existem 2 jogadores;
- cada jogador joga uma peca por turno;
- o jogador escolhe uma coluna;
- a peca cai ate ao espaco vazio mais baixo dessa coluna;
- ganha quem conseguir ligar 4 pecas seguidas;
- as 4 pecas podem estar na horizontal, vertical ou diagonal;
- se o tabuleiro encher e ninguem ganhar, o jogo termina empatado.

No codigo, o tabuleiro e gerido pela classe `Connect4Board`.

Metodos principais:

- `get_valid_moves()`: devolve as colunas onde ainda se pode jogar.
- `drop_piece(col, piece)`: coloca uma peca numa coluna.
- `check_winner(piece)`: verifica se uma peca ganhou.
- `is_board_full()`: verifica se o tabuleiro esta cheio.
- `copy()`: cria uma copia do tabuleiro para simulacoes.

Os agentes recebem o tabuleiro no metodo:

```python
get_move(self, board)
```

E devolvem uma coluna valida.

## Como funciona o Minimax

O Minimax tenta prever jogadas futuras.

Ele assume que:

- o nosso jogador tenta escolher a melhor jogada;
- o adversario tambem tenta escolher a melhor resposta.

Como calcular todos os futuros ate ao fim seria muito pesado, o Minimax usa:

- `max_depth`: profundidade maxima da procura;
- Alpha-Beta: corta ramos que nao precisam de ser explorados;
- heuristica: avalia o tabuleiro quando a procura para.

A heuristica considera:

- vitorias;
- derrotas;
- sequencias de 2 pecas;
- sequencias de 3 pecas;
- ameacas do adversario;
- controlo do centro.

## Como funciona o MCTS

O MCTS escolhe jogadas atraves de simulacoes.

Em vez de avaliar manualmente todas as posicoes, ele faz varias experiencias aleatorias e observa que jogadas costumam levar a melhores resultados.

Cada iteracao tem 4 fases:

1. Selecao: escolhe um caminho na arvore usando UCB1.
2. Expansao: cria um novo no para uma jogada ainda nao testada.
3. Simulacao: joga aleatoriamente ate ao fim.
4. Retropropagacao: atualiza visitas e resultados nos nos usados.

O parametro principal e:

```text
max_iterations
```

Quanto maior for `max_iterations`, mais simulacoes o MCTS faz. Normalmente joga melhor, mas demora mais tempo.

O MCTS usa sempre `board.copy()` nas simulacoes, para nao alterar o tabuleiro real do jogo.

## Diferenca principal entre Minimax e MCTS

Frase curta para explicar na defesa:

```text
O Minimax decide atraves de procura e heuristica; o MCTS decide atraves de simulacoes. No fim, comparamos os dois pela taxa de vitorias e pelo tempo medio de jogo.
```

Resumo:

- Minimax: procura jogadas futuras e usa heuristica.
- MCTS: faz muitas simulacoes aleatorias e usa estatistica.
- Minimax depende mais de `max_depth`.
- MCTS depende mais de `max_iterations`.

## O que ainda falta verificar

Antes da entrega final:

- confirmar se `resultados.xlsx` esta atualizado;
- confirmar se o ZIP nao leva `.venv`, `.idea`, `__pycache__`, `docs`, `Doc Principal` nem `.git`;
- decidir se o ficheiro `Projeto2 - alpha4.pdf` deve sair do ZIP final, porque e o enunciado e nao codigo;
- correr pelo menos uma vez `py run_experiments.py`;
- testar `py play.py` para confirmar que a interface abre.

## Ficheiros que nao sao necessarios no ZIP final

Evitar colocar:

- `.venv/`;
- `.idea/`;
- `__pycache__/`;
- `.git/`;
- `docs/`;
- `Doc Principal/`;
- ficheiros `.pyc`;
- zips antigos;
- ficheiros duplicados;
- enunciado em PDF, salvo se a professora pedir.
