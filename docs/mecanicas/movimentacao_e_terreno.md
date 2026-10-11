# Mecânicas — Movimentação e Terreno

## 1. Modos de Locomoção

Gabriel possui dois estados primários de movimentação em vista lateral 2.5D. Ele anda em todas as direções dentro da faixa de chão: `A`/`D` (ou ←/→) para os lados e `W`/`S` (ou ↑/↓) para o fundo/frente da sala, um pouco mais devagar (65%), passando na frente e atrás dos objetos:

| Ação | Tecla Padrão | Velocidade | Consumo de Estamina | Nível de Ruído Acústico |
|---|---|---|---|---|
| **Andar** | `WASD` ou Setas | Normal (100%) | Zero | Baixo (ouvido apenas na mesma sala) |
| **Correr** | `Shift` + Direção | Rápido (180%) | Constante (~4s contínuos) | **Alto** (propaga até 2 salas no grafo) |

---

## 2. Dinâmica de Estamina

- Gabriel é um estudante comum: sua estamina se esgota rapidamente durante a corrida (~8 segundos contínuos).
- Quando a barra de estamina zera, Gabriel entra em estado de **Exaustão**: não pode correr por 3 segundos, move-se com 40% da velocidade de caminhada e emite suspiros ofegantes audíveis via sinal `ofegante` e efeito sonoro, aumentando o risco de detecção por robôs.
- A estamina se regenera gradualmente: em repouso (parado), recupera-se em ~4 segundos; andando, recupera-se em ~8 segundos.
- **Implementação técnica:**
  - Cena modular: `cenas/sistemas/fadiga.tscn` instanciada em `cenas/personagens/gabriel.tscn`.
  - Script: `scripts/sistemas/fadiga.gd` (`class_name Fadiga`).
  - Sinais: `mudou(atual, maxima)`, `exaustao_iniciada`, `exaustao_terminada`, `ofegante`.
  - Interface: o HUD monitora o jogador pelo grupo `jogador` e exibe uma barra discreta abaixo da vida, surgindo ao consumir estamina e esmaecendo suavemente quando cheia. Em exaustão, a barra muda para a cor de alerta.

---

## 3. Tipos de Superfície e Propagação de Som

O som gerado pelos passos varia conforme o piso sobre o qual Gabriel se move:

- **Piso de Concreto / Cerâmica Antiga:** Emite ruído regular.
- **Dunas de Areia:** Abafam o som dos passos (excelente para passar despercebido), mas reduzem ligeiramente a velocidade de corrida.
- **Entulho com Cacos de Vidro e Vergalhões:** Correr sobre entulho produz ruído estridente e imediato, gerando um evento sonoro de alta magnitude propagado via BFS para salas vizinhas.
- **Pisos Alagados (Subsolo do NAMI):** Geram ruído de chapinha d'água ritmado, exigindo que o jogador ande devagar, sem correr.

---

## 4. Obstáculos de Travessia e Camadas 2.5D

- **Subida por Troncos Caídos:** Certos caminhos verticais entre andares quebrados utilizam árvores e vigas retorcidas como rampas de acesso.
- **Transição de Planos de Profundidade:** Interagir com portas, escadarias e vãos (tecla a definir: `W` agora anda para o fundo da sala) permite que Gabriel alterne entre o plano frontal e o plano de fundo do cenário 2.5D.

---

## 5. Portas entre cenas

- Perto de uma porta aparece `[E]`. Ao apertar, o Gabriel perde o controle, anda para dentro da porta sumindo no escuro, a tela escurece e a próxima cena abre. Na outra cena ele sai pela porta correspondente, andando para fora e reaparecendo, e só então o jogador volta a controlar.
- Durante a animação o Gabriel atravessa paredes (a colisão é desligada) e não interage nem usa gadgets.

**Como colocar uma porta:** instancie `cenas/sistemas/porta.tscn` onde fica a passagem (o Gabriel entra e sai por esse ponto) e preencha no Inspetor:

| Campo | O que é |
|---|---|
| `id` | Nome desta porta, único no jogo (ex.: `biblioteca_corredor`) |
| `cena_destino` | A cena para onde ela leva |
| `porta_destino` | O `id` da porta, na outra cena, por onde o Gabriel vai sair |
| `direcao_entrar` | Para onde ele anda ao entrar (`(0, -1)` = para o fundo). Ao sair, anda para o lado oposto |
| `trancada` | Trancada, o `E` só mostra o aviso "Trancada". Abre com o notebook (e continua aberta até fechar o jogo) |
| `bloqueada` | Porta que ainda não leva a lugar nenhum (sala para fazer depois). O `E` mostra `aviso_bloqueada` e toca a maçaneta emperrada; o notebook não abre |
| `som_abrir` | O som ao atravessar. Padrão: `porta_abrir.wav`; o bunker usa `porta_blindada.wav` |

Ao atravessar toca `porta_abrir.wav` (trinco, dobradiça rangendo, porta batendo). O som toca fora da cena, então continua durante a troca.

**Animação de abrir (por mapa):** a folha da porta é uma peça de parede animada, não parte da `Porta`. Cada mapa tem a sua. A da Biblioteca é `cenas/cenario/biblioteca/parede_porta_animada.tscn` (filha de `parede_porta.tscn`, com o nó `Folha`, que está no grupo `folhas_de_porta`). Para ligar a animação em uma porta, use essa peça no vão em vez de `parede_porta.tscn`: a `Porta` acha sozinha a folha cujo centro fica a até 12 px dela (peça de 80 px de largura, `Porta` no meio do vão) e não precisa de campo no Inspetor. Ao apertar `E` a folha abre, durando o mesmo que `segundos_andando`; na sala de destino ela fecha. O som de abrir também vem da folha (`som_abrir` no nó `Folha`): na Biblioteca é `porta_correr.wav`, e vale no lugar do `som_abrir` da `Porta`. Sem peça animada por perto, a porta funciona como antes.

Os quadros saem de um vídeo, convertido por `assets/modelagem/cenario/gerar_porta_biblioteca.py` (recorta o batente, reduz para 80×88 e grava o `SpriteFrames` em `assets/sprites/cenario/biblioteca/porta/`). Para outro mapa, copie o script com o recorte e o caminho de saída próprios.

A porta de chegada é guardada numa variável estática da classe `Porta` (sobrevive à troca de cena sem precisar de autoload). Código: `scripts/sistemas/porta.gd`; o controle automático do Gabriel é `andar_sozinho()` / `devolver_controle()` em `scripts/personagens/gabriel.gd`.
