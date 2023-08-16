# Interface para o NeonFC

A interface tem foco em auxiliar nos testes do VSSS físico (real_life).

Para usar, é necessário que o NeonFC se comunique com o API: em config_real_life.json, "api" deve ser true.
Para iniciar a interface, rode em um terminal:
`python3 main.py`

Após iniciar a interface, rode o NeonFC.

### Funcionalidades

A interface tem um gráfico do campo que é atualizado a 60fps fixos.

Os primeiros botões realizam as funções de alterar o status do jogo:
- START = status GAME_ON
- STOP = status STOP
- HALT = status HALT

Também é possível alterar a cor dos dois times e o lado do campo.
