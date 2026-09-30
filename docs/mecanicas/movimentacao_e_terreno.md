# Mecânicas — Movimentação e Terreno

## 1. Modos de Locomoção

Gabriel possui três estados primários de movimentação em vista lateral 2.5D. Ele anda em todas as direções dentro da faixa de chão: `A`/`D` (ou ←/→) para os lados e `W`/`S` (ou ↑/↓) para o fundo/frente da sala, um pouco mais devagar (65%), passando na frente e atrás dos objetos:

| Ação | Tecla Padrão | Velocidade | Consumo de Estamina | Nível de Ruído Acústico |
|---|---|---|---|---|
| **Andar** | `WASD` ou Setas | Normal (100%) | Zero | Baixo (ouvido apenas na mesma sala) |
| **Correr** | `Shift` + Direção | Rápido (180%) | Constante (~4s contínuos) | **Alto** (propaga até 2 salas no grafo) |
| **Agachar / Esgueirar** | `Ctrl` ou `C` | Lento (50%) | Zero | **Silencioso** (ruído zero) |

---

## 2. Dinâmica de Estamina

- Gabriel é um estudante comum: sua estamina se esgota rapidamente durante a corrida.
- Quando a barra de estamina zera, Gabriel entra em estado de **Exaustão**: não pode correr por 3 segundos e emite suspiros ofegantes audíveis, aumentando o risco de detecção.
- A estamina se regenera gradualmente enquanto ele estiver parado ou andando.

---

## 3. Tipos de Superfície e Propagação de Som

O som gerado pelos passos varia conforme o piso sobre o qual Gabriel se move:

- **Piso de Concreto / Cerâmica Antiga:** Emite ruído regular.
- **Dunas de Areia:** Abafam o som dos passos (excelente para passar despercebido), mas reduzem ligeiramente a velocidade de corrida.
- **Entulho com Cacos de Vidro e Vergalhões:** Correr sobre entulho produz ruído estridente e imediato, gerando um evento sonoro de alta magnitude propagado via BFS para salas vizinhas.
- **Pisos Alagados (Subsolo do NAMI):** Geram ruído de chapinha d'água ritmado, exigindo que o jogador se mova estritamente agachado.

---

## 4. Obstáculos de Travessia e Camadas 2.5D

- **Frestas e Desabamentos:** Vãos baixos causados por tetos caídos exigem que o jogador se agache para atravessar.
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

A porta de chegada é guardada numa variável estática da classe `Porta` (sobrevive à troca de cena sem precisar de autoload). Código: `scripts/sistemas/porta.gd`; o controle automático do Gabriel é `andar_sozinho()` / `devolver_controle()` em `scripts/personagens/gabriel.gd`.
