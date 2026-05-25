# Alpha4 - Projeto de Inteligencia Artificial

Este projeto implementa agentes de Inteligencia Artificial para jogar Alpha4 / Connect 4.

O objetivo do trabalho e comparar duas formas de tomar decisoes num jogo adversarial:

- `MinimaxAIPlayer`: procura adversaria com Minimax, poda Alpha-Beta e heuristica.
- `MCTSAIPlayer`: procura baseada em simulacoes com Monte Carlo Tree Search.

O jogo base foi fornecido pela professora. A nossa parte foi criar os agentes automaticos, correr testes e preencher o ficheiro `resultados.xlsx`.

## Estado atual do projeto

Ja estao implementadas as duas IAs pedidas:

- `MinimaxAIPlayer.py`: parte do Minimax.
- `MCTSAIPlayer.py`: parte do MCTS.
- `run_experiments.py`: corre varios jogos automaticamente e gera/atualiza `resultados.xlsx`.
- `play.py`: permite jogar Humano vs IA com interface grafica.
- `resultados.xlsx`: tabela de resultados pedida no enunciado.

Ficheiros base do jogo:

- `Connect4Board.py`: guarda o estado do tabuleiro.
- `Connect4Game.py`: controla o ciclo do jogo.
- `Connect4Gui.py`: desenha a interface grafica com Pygame.
- `Player.py`: classe base dos jogadores.
- `HumanPlayer.py`: jogador humano.
- `RandomPlayer.py`: jogador aleatorio.

## Como correr o projeto

Instalar dependencias, se for necessario:

```bash
py -m pip install numpy pygame openpyxl
```

Jogar contra a IA:

```bash
py play.py
```

Correr testes automaticos:

```bash
py run_experiments.py --games 20 --mcts-iterations 250 --output resultados.xlsx
```

## Como jogar contra a IA

Ao executar:

```bash
py play.py
```

o programa pede para escolher o adversario:

```text
(1) Minimax
(2) MCTS
```

Depois abre a janela do jogo.

Funcionamento:

- o humano joga como Jogador 1, com pecas vermelhas;
- a IA joga como Jogador 2, com pecas amarelas;
- o humano clica numa coluna para jogar;
- a peca cai para a posicao vazia mais baixa dessa coluna;
- depois a IA calcula a sua jogada e joga automaticamente;
- ganha quem fizer 4 pecas seguidas na horizontal, vertical ou diagonal;
- se o tabuleiro encher sem vencedor, o resultado e empate.

No final, o `play.py` permite jogar novamente e pode acrescentar resultados Humano vs IA ao `resultados.xlsx`.

## Como o jogo funciona no codigo

O centro do jogo e o objeto `Connect4Board`.

Ele guarda:

- numero de linhas;
- numero de colunas;
- numero de pecas necessarias para ganhar;
- grelha do tabuleiro.

Os metodos mais importantes sao:

- `get_valid_moves()`: devolve as colunas onde ainda e possivel jogar.
- `drop_piece(col, piece)`: coloca uma peca numa coluna.
- `check_winner(piece)`: verifica se uma certa peca ganhou.
- `is_board_full()`: verifica se o tabuleiro esta cheio.
- `copy()`: cria uma copia independente do tabuleiro.

O enunciado dizia que os agentes deviam usar apenas a API permitida do tabuleiro. Por isso, tanto o Minimax como o MCTS usam `board.copy()` para simular jogadas sem estragar o tabuleiro real.

Todos os jogadores seguem a mesma interface:

```python
get_move(self, board)
```

Esse metodo recebe o estado atual do tabuleiro e devolve uma coluna valida.

## Ligacao com a materia das aulas

Nas aulas vimos que problemas de procura podem ser representados como estados e acoes.

Neste projeto:

- o estado e o tabuleiro atual;
- as acoes sao as colunas onde se pode jogar;
- o objetivo e chegar a um estado vencedor;
- como existem dois jogadores, o problema e adversarial.

Isto liga diretamente a procura adversaria. O nosso agente nao decide sozinho num mundo parado: ele decide sabendo que o adversario tambem vai tentar ganhar.

## Minimax

O `MinimaxAIPlayer` usa a ideia vista na materia de procura adversaria.

A logica e:

- o jogador MAX tenta maximizar a pontuacao;
- o jogador MIN tenta minimizar a pontuacao;
- cada nivel da arvore representa uma jogada futura;
- o algoritmo alterna entre jogadas nossas e jogadas do adversario.

Como a arvore do Connect 4 pode ficar muito grande, usamos uma profundidade maxima:

```python
max_depth
```

Quando o algoritmo chega ao limite da profundidade, ele nao sabe ainda se o jogo vai acabar em vitoria ou derrota. Por isso usa uma heuristica.

## Heuristica do Minimax

A funcao:

```python
evaluate_board(board, player)
```

atribui uma pontuacao ao tabuleiro.

A heuristica valoriza:

- vitorias;
- sequencias de 3 pecas com espaco para completar;
- sequencias de 2 pecas;
- pecas no centro do tabuleiro;
- bloqueio de ameacas do adversario.

Tambem penaliza:

- derrotas;
- situacoes em que o adversario esta perto de ganhar.

Isto segue a ideia vista nas aulas: quando nao conseguimos procurar ate ao fim, usamos uma funcao de avaliacao para estimar se o estado parece bom ou mau.

## Alpha-Beta

O Minimax tambem usa poda Alpha-Beta.

A poda Alpha-Beta nao muda a decisao final do Minimax. Ela apenas evita explorar ramos que ja sabemos que nao vao melhorar a resposta.

Ideia simples:

- `alpha` guarda a melhor opcao encontrada para MAX;
- `beta` guarda a melhor opcao encontrada para MIN;
- se um ramo ja nao pode influenciar a decisao final, o algoritmo corta esse ramo.

Isto torna a procura mais rapida, especialmente quando ha muitas jogadas possiveis.

## MCTS

O `MCTSAIPlayer` usa Monte Carlo Tree Search.

A ideia do MCTS e diferente da do Minimax. Em vez de tentar avaliar manualmente todos os estados, o MCTS faz muitas simulacoes e aprende estatisticamente que jogadas parecem melhores.

Cada iteracao do MCTS tem 4 fases:

1. Selecao.
2. Expansao.
3. Simulacao.
4. Retropropagacao.

O parametro principal e:

```python
max_iterations
```

Quanto maior for `max_iterations`, mais simulacoes sao feitas. Isso normalmente melhora a decisao, mas aumenta o tempo de calculo.

## Selecao com UCB1

Na fase de selecao, o MCTS desce na arvore escolhendo nos promissores.

Para isso usa UCB1:

```text
vitorias / visitas + C * sqrt(log(visitas_do_pai) / visitas)
```

Esta formula equilibra duas coisas:

- explorar jogadas pouco testadas;
- aproveitar jogadas que ja tiveram bons resultados.

Isto e importante porque, se o algoritmo so escolhesse a melhor jogada atual, podia ignorar outras jogadas que ainda nao foram testadas o suficiente.

## Expansao

Quando o MCTS chega a um no que ainda tem jogadas possiveis nao testadas, ele cria um novo filho na arvore.

Esse filho representa o tabuleiro depois de uma jogada.

No codigo, isto e feito sempre numa copia:

```python
new_board = self.board.copy()
new_board.drop_piece(move, self.next_piece)
```

Assim a simulacao nao altera o jogo real.

## Simulacao

Depois da expansao, o MCTS joga uma partida aleatoria ate ao fim.

Nesta fase, as jogadas nao sao inteligentes. Sao escolhidas aleatoriamente entre as jogadas validas.

O objetivo nao e jogar perfeitamente numa simulacao isolada. O objetivo e repetir muitas simulacoes para perceber, em media, que jogadas levam a bons resultados.

## Retropropagacao

Quando a simulacao termina, o resultado volta para tras pela arvore.

Cada no visitado aumenta o numero de visitas.

Pontuacao usada:

- vitoria: soma `1.0`;
- empate: soma `0.5`;
- derrota: soma `0.0`.

Assim, ao longo de muitas iteracoes, a arvore guarda estatisticas sobre as jogadas.

## Diferenca entre Minimax e MCTS

Resumo simples:

- Minimax: procura futuras jogadas e usa heuristica.
- MCTS: faz simulacoes aleatorias e usa estatistica.
- Minimax depende muito de `max_depth`.
- MCTS depende muito de `max_iterations`.

Frase para defesa:

```text
O Minimax tenta prever o adversario com uma arvore de procura e uma heuristica. O MCTS estima a qualidade das jogadas fazendo muitas simulacoes e reforcando as jogadas que dao melhores resultados.
```

## Testes e resultados

O enunciado pede comparar:

- Minimax vs Aleatorio;
- MCTS vs Aleatorio;
- Minimax vs MCTS;
- Humano vs IA e opcional.

O ficheiro `run_experiments.py` corre jogos automaticamente e mede:

- numero de jogos;
- vitorias do Jogador 1;
- vitorias do Jogador 2;
- empates;
- taxa de vitoria;
- duracao media;
- duracao maxima;
- duracao minima;
- diferencas observadas.

As combinacoes usadas para Minimax vs MCTS sao:

```text
1a combinacao: Minimax max_depth=3 | MCTS max_iterations=25
2a combinacao: Minimax max_depth=4 | MCTS max_iterations=100
3a combinacao: Minimax max_depth=5 | MCTS max_iterations=430
```

A intencao e aproximar os tempos de decisao dos dois algoritmos para a comparacao ser mais justa.

## Explicacao dos ficheiros criados

`MinimaxAIPlayer.py`

Contem a IA baseada em Minimax. O metodo principal e `get_move`, que testa jogadas possiveis, chama o Minimax e devolve a melhor coluna. Tambem tem a heuristica `evaluate_board`.

`MCTSAIPlayer.py`

Contem a IA baseada em MCTS. Tem a classe `MCTSNode`, que representa nos da arvore, e a classe `MCTSAIPlayer`, que executa as iteracoes e escolhe a melhor jogada.

`run_experiments.py`

Serve para automatizar testes. Em vez de jogar manualmente muitas vezes, o script cria jogadores, executa varios jogos e escreve os resultados no Excel.

`play.py`

Serve para jogar contra uma IA. Permite escolher Minimax ou MCTS e usa a interface grafica do projeto base.

`resultados.xlsx`

E a tabela pedida no enunciado. Contem as comparacoes e os resultados obtidos.

## Como explicar que entendemos o trabalho

Pontos que devemos saber dizer:

- O tabuleiro real nao deve ser alterado durante simulacoes, por isso usamos `board.copy()`.
- O Minimax procura jogadas futuras, mas precisa de `max_depth` porque a arvore cresce muito.
- A heuristica serve para avaliar tabuleiros quando a procura para antes do fim.
- Alpha-Beta melhora o tempo cortando ramos desnecessarios.
- O MCTS nao usa uma heuristica forte: usa simulacoes e estatistica.
- UCB1 equilibra testar jogadas novas e repetir jogadas que ja deram bons resultados.
- `max_depth` e `max_iterations` controlam o compromisso entre qualidade da jogada e tempo de execucao.

## Perguntas provaveis da professora

Pergunta: Porque e que usamos `board.copy()`?

Resposta: Porque o tabuleiro recebido no `get_move` e o tabuleiro real do jogo. Se simulassemos diretamente nele, iriamos alterar a partida. A copia permite experimentar jogadas sem mexer no jogo verdadeiro.

Pergunta: O que faz o Minimax?

Resposta: O Minimax simula jogadas futuras assumindo que nos queremos maximizar a pontuacao e o adversario quer minimiza-la.

Pergunta: Para que serve a heuristica?

Resposta: Serve para dar uma pontuacao a um tabuleiro quando nao conseguimos procurar ate ao fim do jogo.

Pergunta: O que e Alpha-Beta?

Resposta: E uma otimizacao do Minimax que corta ramos que nao precisam de ser analisados porque nao vao alterar a decisao final.

Pergunta: O que faz o MCTS?

Resposta: O MCTS faz muitas simulacoes aleatorias a partir do estado atual e usa os resultados para escolher a jogada mais promissora.

Pergunta: O que e UCB1?

Resposta: E a formula usada na selecao do MCTS para equilibrar exploracao e aproveitamento.

Pergunta: Qual e a principal diferenca entre Minimax e MCTS?

Resposta: O Minimax usa procura e heuristica. O MCTS usa simulacoes e estatistica.

## Checklist antes da entrega

Antes de criar o ZIP final:

- correr `py run_experiments.py`;
- confirmar que `resultados.xlsx` esta atualizado;
- testar `py play.py`;
- confirmar que `MinimaxAIPlayer.py` e `MCTSAIPlayer.py` estao no projeto;
- remover ficheiros que nao sao necessarios;
- criar o ZIP com o nome pedido pela professora.

Nao colocar no ZIP:

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
