# Mecânicas — Sala segura e salvamento

Estilo *Resident Evil*: em cada fase há **uma sala segura**. É o único lugar onde o jogo salva, e nenhum robô entra nela.

## 1. Como funciona

- **Por fora, é fácil de achar.** A porta fica perto de onde o Gabriel chega na fase e leva o **sinal da sala segura**: uma lâmpada verde acesa, que pulsa devagar, com uma plaquinha de casinha embaixo (`cenas/cenario/objetos/sinal_sala_segura.tscn`). O sinal é o mesmo em todas as fases, para o jogador aprender a reconhecê-lo. Onde a fase tem placas nas portas, a placa diz DESCANSO.
- **Por dentro, é calma:** luz quente e fixa (sem tremer), um tapete, o mural e uma cadeira VR. A música é um piano devagar em Lá menor, 64 s em loop (`assets/audio/musica/sala_segura/sala_segura_tema.ogg`).
- **Nenhum robô entra.** A sala remove qualquer robô que já esteja nela ao carregar e qualquer robô que seja adicionado depois (`SalaSegura`). Como cada sala é uma cena separada, um robô que persegue o Gabriel não atravessa a porta.
- **A máquina de salvar são os óculos do Zane:** o visor de 2123 (armação grafite, linha de luz ciano, detalhe amarelo-ácido) em cima de um pedestal. É a mesma arte da estante do menu principal (`assets/sprites/menu/menu_oculos_zane.png`), reaproveitada.

### Onde fica a de cada fase

| Fase | Cena | A porta |
|---|---|---|
| Biblioteca | `cenas/salas/biblioteca/sala_segura.tscn` | Corredor de serviço, ao lado da porta do salão (DESCANSO) |
| Bloco de salas | `cenas/salas/bloco_de_salas/sala_segura.tscn` | Corredor do térreo, logo depois da chegada, antes da 101 (DESCANSO) |
| Labirinto | `cenas/salas/labirinto/sala_segura.tscn` | Parede de cima da câmara onde o Gabriel começa (`QQ` no mapa) |
| Centro de Convivência | `cenas/salas/centro_de_convivencia/sala_segura.tscn` | Passarela de acesso, a porta de vidro verde entre as janelas |
| Bunker | `cenas/salas/bunker/sala_segura.tscn` | Corredor A, ao lado da entrada (DESCANSO) |
| Laboratório | `cenas/salas/dtec/sala_segura.tscn` | Corredor sul, ao lado da Emergência, onde o Gabriel chega (DESCANSO) |

As seis herdam do mesmo modelo e mudam só a cor da `Escuridao` e da `LuzAmbiente`. Outros cantos protegidos da história (a sala 103 da Clarice, a oficina do Zane, a Tapioca Orbital) continuam sem robôs e com checkpoint, mas não salvam.

## 2. Salvar

1. O Gabriel chega perto do pedestal e aparece **[E] Pôr os óculos**.
2. Ele anda sozinho até o lado esquerdo do pedestal, de lado, e **pega os óculos do Zane**: inclina, estende o braço, pega, leva ao rosto e põe (12 quadros, 0,1 s cada).
3. Com os óculos no rosto, a luz do pedestal acende, a tela escurece (como numa porta) e o jogo **vira 3D em primeira pessoa**: o Gabriel está no próprio quarto, a mente dele materializada, com o que ele já leu e anotou nas paredes e na mesa. Ele anda até a TV e salva pelo menu da tela (detalhes em [`visor_3d.md`](visor_3d.md)).
4. Ao salvar, toca o som de salvar (`efeitos/interface/salvar_jogo.wav`), o jogo grava o arquivo, a **vida volta a 3** e o pedestal vira o **checkpoint** da fase (morrer volta para a sala segura, ao lado da máquina).
5. Ao tirar os óculos (Esc ou **Voltar** na TV), o jogo volta para a sala segura 2D, a tela clareia e ele **tira os óculos e devolve ao pedestal**: a mesma animação de trás para a frente. Se salvou, o HUD mostra **Jogo salvo**. O jogador volta a controlar o Gabriel.

### A animação de pegar e pôr os óculos

- A tira `gabriel_oculos_lado.png` (12 quadros de 96 × 112, na paleta do Gabriel) é renderizada no Blender pelo `assets/modelagem/personagens/gerar_gabriel_oculos.py`, com o mesmo modelo dele. Para ajustar o gesto, mude a tabela `POSES` (ângulos do ombro, cotovelo, tronco e cabeça) e rode o script (`blender -b --factory-startup --python ...`).
- Os óculos **não** estão desenhados na tira: o script grava em `scripts/personagens/quadros_oculos_gabriel.gd` o ponto (em pixels do quadro) onde eles estão em cada quadro, e a fase: `pedestal`, `mao` ou `rosto`. O `MaquinaDeSalvar` move o sprite do Zane até esse ponto e o afina de lado (a escala em x cai para 45% na mão e 30% no rosto), porque o Gabriel está de perfil.
- O lugar onde o Gabriel para é calculado para a mão dele coincidir com os óculos no pedestal, então vale para qualquer posição do pedestal na sala. Ele sempre fica à esquerda, olhando para a direita (só existe a vista de lado). Se o pedestal ficar encostado na parede esquerda, mude o pedestal de lugar.
- No `gabriel.gd`: `tocar_tira`, `mostrar_quadro_tira`, `terminar_tira` (tocam uma tira especial no lugar da caminhada/respiração), `olhar_para` e `ponto_do_quadro`.

## 3. Continuar

O botão **Continuar** do menu principal fica habilitado quando existe um save. Ele carrega o último save: o Gabriel reaparece na sala segura, ao lado da máquina, com tudo o que tinha.

Novo jogo e a lista de fases **não apagam** o save: ele só é sobrescrito na próxima vez que o jogador salvar.

### O que o arquivo guarda (`user://salvamento.cfg`, `scripts/sistemas/salvamento.gd`)

| O quê | De onde vem |
|---|---|
| Sala e posição do Gabriel | a cena da sala segura e o pé do pedestal |
| Inventário: itens, gadgets equipados, cargas e unidades, itens já pegos do chão | `Inventario` |
| Anotações do caderno | `Caderno` |
| Transmissões de rádio já ouvidas | `Radio` |
| Marcas de progresso (energia, grade aberta, invasões...) | `Progresso` |
| Portas destrancadas | `Porta` |
| Diálogos já vistos | `Dialogos` |

**Não é guardado:** a posição dos robôs (a fase recarrega do zero, como ao morrer) e estados soltos dentro das salas que não passam por `Progresso`. Se uma sala nova guardar o estado fora desses sistemas, ele se perde ao carregar: use `Progresso.marcar`.

## 4. Como fazer a sala segura de uma fase nova

1. Crie uma cena que **herde** de `cenas/salas/modelo_safe_room.tscn` (Cena → Nova cena herdada). Veja `cenas/salas/biblioteca/sala_segura.tscn` como exemplo.
2. Preencha o `id` da sala (ex.: `bloco_sala_segura`).
3. Na `PortaSaida`, preencha `cena_destino` e `porta_destino` (a porta da sala por onde o Gabriel volta).
4. **Mude só um pouco o visual para combinar com a fase.** O que dá para variar sem mexer na estrutura:
   - a cor do nó `Escuridao` (luz ambiente da sala);
   - a cor e a energia de `Luzes/LuzAmbiente`;
   - as peças de `Paredes` e de `Chao` (trocar o tapete por outro piso, o mural por outra parede);
   - a música, no nó `MusicaFase` (campo `stream`), se a fase pedir outro tema suave.
   - **Não mexa** na `MaquinaDeSalvar`: ela é a mesma em todas as fases.
5. Na sala da fase, ponha uma porta normal (`cenas/sistemas/porta.tscn`) com `cena_destino` = a cena da sala segura e `porta_destino = "safe_room_saida"` (o `id` da `PortaSaida`). A `PortaSaida` da sala segura faz o caminho de volta: o `porta_destino` dela é o `id` dessa porta.
6. **Ponha o sinal em cima da porta:** uma instância de `cenas/cenario/objetos/sinal_sala_segura.tscn` dentro de `Paredes`, com o x da porta e o y logo acima da placa (o ponto do nó é o meio da borda de cima do sinal, que tem 16 × 18 px). Escolha uma porta **perto de onde o Gabriel chega**, num lugar de passagem. Nas salas montadas por script, o sinal entra pela descrição: `"sinais_sala_segura"` no Centro de Convivência e `"sala_segura": True` na porta, no `montar_dtec.py`.

## 5. Onde está no projeto

| O quê | Onde |
|---|---|
| Modelo da sala segura | `cenas/salas/modelo_safe_room.tscn`, `scripts/salas/sala_segura.gd` |
| Salas seguras de cada fase | `cenas/salas/<fase>/sala_segura.tscn` (tabela da seção 1) |
| Sinal da sala segura (lâmpada verde e casinha) | `cenas/cenario/objetos/sinal_sala_segura.tscn`, sprite de `assets/modelagem/cenario/gerar_sinal_sala_segura.py`; no Labirinto, a porta inteira é o sprite `porta_sala_segura.png` de `gerar_labirinto.py` |
| Máquina de salvar (os óculos do Zane) | `cenas/sistemas/maquina_de_salvar.tscn`, `scripts/sistemas/maquina_de_salvar.gd` |
| Quarto 3D com a TV de salvar (autoload `Visor`) | `scripts/sistemas/visor.gd`, `cenas/visor/`, `scripts/visor/` (ver [`visor_3d.md`](visor_3d.md)) |
| Salvar e carregar (autoload `Salvamento`) | `scripts/sistemas/salvamento.gd` |
| Botão Continuar | `scripts/menu_principal.gd` |
| Animação do Gabriel e tabela dos óculos | `assets/sprites/personagens/gabriel/gabriel_oculos_lado.png`, `scripts/personagens/quadros_oculos_gabriel.gd`, de `assets/modelagem/personagens/gerar_gabriel_oculos.py` |
| Sprites do pedestal | `assets/sprites/cenario/objetos/maquina_de_salvar.png` e `maquina_de_salvar_luz.png`, de `assets/modelagem/cenario/gerar_sala_segura.py` |
| Tema e som de salvar | `assets/modelagem/audio/gerar_trilha_sala_segura.py` |

## 6. Pendências

- **A porta da Biblioteca** fica no corredor de serviço, ao lado da porta do salão, com o letreiro DESCANSO e a luz verde. É a única que não fica na sala onde o Gabriel chega; se o grupo preferir outro lugar, é só mover a `PortaSalaSegura`, o letreiro e o `SinalSalaSegura` em `corredor_servico.tscn`.
- **Dormir e sonhar** (GDD, `sono_e_sonhos.md`) continua pendente. Salvar passou para os óculos; o sonho ainda não tem lugar definido.
- **Os óculos do Zane como máquina** é uma decisão de jogo, não de história: o Enredo Principal ainda não explica por que o visor dele existe em cada fase (o Zane é o último a chegar). Confirmar com o Davi antes de escrever qualquer fala sobre isso.
- A arte do pedestal e o piano são placeholders gerados por código.
