# Mecânicas — Sala segura e salvamento

Estilo *Resident Evil*: em cada fase há **uma sala segura**. É o único lugar onde o jogo salva, e nenhum robô entra nela.

## 1. Como funciona

- **Por fora, é uma sala comum.** A porta é igual às outras portas da fase. Quem não procura passa direto.
- **Por dentro, é calma:** luz quente e fixa (sem tremer), um tapete, o mural e uma cadeira VR. A música é um piano devagar em Lá menor, 64 s em loop (`assets/audio/musica/sala_segura/sala_segura_tema.ogg`).
- **Nenhum robô entra.** A sala remove qualquer robô que já esteja nela ao carregar e qualquer robô que seja adicionado depois (`SalaSegura`). Como cada sala é uma cena separada, um robô que persegue o Gabriel não atravessa a porta.
- **A máquina de salvar são os óculos do Zane:** o visor de 2123 (armação grafite, linha de luz ciano, detalhe amarelo-ácido) em cima de um pedestal. É a mesma arte da estante do menu principal (`assets/sprites/menu/menu_oculos_zane.png`), reaproveitada.

## 2. Salvar

1. O Gabriel chega perto do pedestal e aparece **[E] Pôr os óculos**.
2. A tela escurece (como numa porta), toca o som de salvar (`efeitos/interface/salvar_jogo.wav`) e a luz do pedestal acende.
3. No escuro, o jogo grava o arquivo, a **vida volta a 3** e o pedestal vira o **checkpoint** da fase (morrer volta para a sala segura, ao lado da máquina).
4. A tela clareia e o HUD mostra **Jogo salvo**.

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

## 5. Onde está no projeto

| O quê | Onde |
|---|---|
| Modelo da sala segura | `cenas/salas/modelo_safe_room.tscn`, `scripts/salas/sala_segura.gd` |
| Sala segura da Biblioteca | `cenas/salas/biblioteca/sala_segura.tscn` |
| Máquina de salvar (os óculos do Zane) | `cenas/sistemas/maquina_de_salvar.tscn`, `scripts/sistemas/maquina_de_salvar.gd` |
| Salvar e carregar (autoload `Salvamento`) | `scripts/sistemas/salvamento.gd` |
| Botão Continuar | `scripts/menu_principal.gd` |
| Sprites do pedestal | `assets/sprites/cenario/objetos/maquina_de_salvar.png` e `maquina_de_salvar_luz.png`, de `assets/modelagem/cenario/gerar_sala_segura.py` |
| Tema e som de salvar | `assets/modelagem/audio/gerar_trilha_sala_segura.py` |

## 6. Pendências

- **A porta da Biblioteca** fica no corredor de serviço, ao lado da porta do salão, com o letreiro DESCANSO (um nome que não entrega o que é). O plano antigo era a manutenção (sala 5); se o grupo preferir outra sala ou outro nome, é só mover a `PortaSalaSegura` e o letreiro em `corredor_servico.tscn`.
- **Dormir e sonhar** (GDD, `sono_e_sonhos.md`) continua pendente. Salvar passou para os óculos; o sonho ainda não tem lugar definido.
- **Os óculos do Zane como máquina** é uma decisão de jogo, não de história: o Enredo Principal ainda não explica por que o visor dele existe em cada fase (o Zane é o último a chegar). Confirmar com o Davi antes de escrever qualquer fala sobre isso.
- A arte do pedestal e o piano são placeholders gerados por código.
