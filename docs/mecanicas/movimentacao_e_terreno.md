# Mecânicas — Movimentação e Terreno

## 1. Modos de Locomoção

Gabriel possui dois estados primários de movimentação em vista lateral 2.5D. Ele anda em todas as direções dentro da faixa de chão: `A`/`D` (ou ←/→) para os lados e `W`/`S` (ou ↑/↓) para o fundo/frente da sala, um pouco mais devagar (65%), passando na frente e atrás dos objetos:

| Ação | Tecla Padrão | Velocidade | Consumo de Estamina | Nível de Ruído Acústico |
|---|---|---|---|---|
| **Andar** | `WASD` ou Setas | Normal (100%) | Zero | Baixo (ouvido apenas na mesma sala) |
| **Correr** | `Shift` + Direção | Rápido (180%) | Constante (~4s contínuos) | **Alto** (propaga até 2 salas no grafo) |

### 1.1 Condução (como o movimento responde)

A regra é que o Gabriel **nunca patina**: os pés têm de bater com o chão e o corpo não pode ir para um lado olhando para o outro. Os valores ficam no Inspetor do Gabriel, grupo *Conducao* e *Caminhada*.

- **A velocidade é separada em duas partes** a cada quadro, em relação à direção pedida (`_conduzir` em `gabriel.gd`): a parte *ao longo* da direção e a parte *de lado* (projeção por produto escalar). A parte de lado é o que parece patinação, então ela morre rápido (`taxa_virada`). Numa inversão, a parte contrária também.
- **Arranque:** forte no começo e mais suave perto da velocidade final (`aceleracao_inicial` para `aceleracao_final`), cerca de 0,13 s.
- **Corrida:** do passo à corrida a aceleração é menor (`aceleracao_corrida`), cerca de 0,2 s: ele pega embalo.
- **Frenagem:** curta de propósito (`desaceleracao`). Andando ele escorrega cerca de 2 px; correndo, cerca de 7 px.
- **Pés:** a animação avança pela distância realmente andada (`_fase_passada`), então os pés acompanham o chão em qualquer velocidade. Correndo a passada é bem mais longa (`px_por_quadro_correndo` = 5,0, contra 2,8 andando), porque na corrida o pé no chão percorre cerca de 5,4 px a cada doze avos do ciclo. Com isso a cadência fica igual à da caminhada, cerca de 3,6 passos por segundo: o que muda na corrida é o tamanho do gesto, não a pressa das pernas. Pé mais rápido que o chão parece esforço; pé mais lento é que parece patinar.
- **Ao parar:** a animação corre até os pés se juntarem (quadros 0 ou 6 da tira) antes de ir para a respiração, em vez de pular de pose.
- **Animação de corrida:** é uma tira própria (`gabriel_correr_<vista>.png`, 24 quadros, o dobro da caminhada, para o movimento ficar mais contínuo), com o tronco inclinado, os cotovelos dobrados e os braços balançando bem mais. Ela entra quando o Gabriel passa de 30% do caminho entre andar e correr (`fracao_para_tira_de_correr`). A fase é a mesma da caminhada e um quadro de andar vale dois de correr (`quadros_correr`), então a troca acontece no mesmo ponto do ciclo, sem salto. As duas pernas usam os mesmos ângulos, para ele não mancar, e o quadril segue uma onda suave na frequência dos passos, sem tranco ao pisar. Vem de `assets/modelagem/personagens/gerar_gabriel_correr.py`, que também grava a mão da lanterna em `scripts/personagens/maos_correndo_gabriel.gd`.
- **Corpo:** andando, um balanço vertical de até 0,5 px (`balanco_andar`), que some na corrida porque a tira já traz o sobe e desce. E uma inclinação pelos pés (`skew` do sprite): um pouco para a frente em movimento, para trás freando. A lanterna acompanha, porque `ponto_do_quadro` usa a transformação do sprite.
- **Vista:** a direção é arredondada para um de 8 setores de 45°, com margem (`margem_virada_graus`) e uma espera curta (`segundos_para_virar`). Assim o analógico não faz o sprite piscar entre vistas, e soltar uma diagonal não o deixa olhando para o lado errado porque uma tecla subiu antes da outra. Virar mais de 90° é imediato.

### 1.2 Câmera

`cenas/sistemas/camera_conduzida.tscn` é filha do Gabriel e cuida da `Camera2D` que a sala coloca nele. Sala nova não precisa fazer nada.

- **Antecipação:** a câmera mira `velocidade × segundos_a_frente` à frente, suavizado. A suavização da `Camera2D` atrasa cerca de `velocidade / 6`, então o saldo é de uns 0,15 s de caminho à frente: o jogador vê mais para onde vai.
- **Sem tremor:** a câmera atualiza no passo de física, junto com o Gabriel, e `snap_2d_transforms_to_pixel` no `project.godot` arredonda tudo para pixels inteiros da janela.

### 1.3 Poeira e respiração

- `cenas/sistemas/poeira_dos_pes.tscn` solta alguns grãos a cada pisada de corrida, pelo sinal `passo_dado`.
- A respiração usa `gabriel_ofegante.wav` (`fadiga.gd`) e só toca **em fuga**. O cansaço não tem som desde 2026-11-05: nem abaixo de 30% de estamina, nem na exaustão. A exaustão continua emitindo o sinal `ofegante`, sem som.
- **Em fuga** quer dizer: algum robô está perseguindo (`Robo.esta_perseguindo`) ou parou de perseguir há menos de 3 s, para o Gabriel recuperar o fôlego depois de escapar. O tom varia um pouco a cada respiração. **Escondido, ele prende a respiração:** o som para enquanto `escondido` for verdadeiro. A respiração é só som: os robôs não a ouvem.

---

## 2. Dinâmica de Estamina

> **Fugir custa estamina (2026-11-04):** Rastreador, Mariposa e Caçador perseguem a 72, 70 e 68 px/s, mais rápido do que o Gabriel anda (60) e mais devagar do que ele corre (108). Carregando a Célula de Energia, ele não corre ([`mecanicas_de_fase.md`](mecanicas_de_fase.md)).

- Gabriel é um estudante comum: sua estamina se esgota rapidamente durante a corrida (~8 segundos contínuos).
- **Ansiedade:** robôs próximos aumentam a ansiedade de Gabriel. Quanto mais perto o robô mais próximo, mais rápido a barra cresce; quando todos se afastam, ela diminui gradualmente. A ansiedade aumenta o consumo de estamina durante a corrida em até 80%. A barra fica sempre visível abaixo da estamina.
- **Pressão externa:** um sistema pode impor um piso à ansiedade com `Ansiedade.definir_pressao(valor)`; a barra não desce abaixo dele. O relógio do Corredor do Tempo (Labirinto) usa isso: quanto menos tempo resta, maior o piso ([`corredor_do_tempo.md`](corredor_do_tempo.md)).
- Com ansiedade, a imagem ganha oscilação, separação de cores e uma vinheta avermelhada; os efeitos ficam mais fortes junto com a barra e desaparecem quando Gabriel se acalma.
- Quando a barra de estamina zera, Gabriel entra em estado de **Exaustão**: não pode correr por 3 segundos, move-se com 40% da velocidade de caminhada e emite o sinal `ofegante` (sem som; nenhum sistema escuta esse sinal hoje).
- Depois da exaustão, ele só volta a correr quando a estamina chega a 30% (`fracao_para_voltar_a_correr`), mesmo com a tecla de correr segura. Sem isso, segurar o Shift numa fuga prendia o Gabriel num ciclo de exaustão sem fim.
- A estamina se regenera gradualmente: em repouso (parado), recupera-se em ~4 segundos; andando, recupera-se em ~8 segundos.
- **Implementação técnica:**
  - Cena modular: `cenas/sistemas/fadiga.tscn` instanciada em `cenas/personagens/gabriel.tscn`.
  - Script: `scripts/sistemas/fadiga.gd` (`class_name Fadiga`).
  - Sinais: `mudou(atual, maxima)`, `exaustao_iniciada`, `exaustao_terminada`, `ofegante`.
  - Interface: o HUD monitora o jogador pelo grupo `jogador` e mantém a barra de estamina abaixo da vida sempre visível. Em exaustão, a barra muda para a cor de alerta. Carregando a Célula, ela fica cinza e o rótulo vira `CARGA: SEM CORRER [G]`.
  - Ansiedade: `cenas/sistemas/ansiedade.tscn` e `scripts/sistemas/ansiedade.gd` medem a distância até o robô mais próximo. O HUD exibe a barra e aplica o efeito visual por `shaders/ansiedade.gdshader`.

---

## 3. Tipos de Superfície e Propagação de Som

O som gerado pelos passos varia conforme o piso sobre o qual Gabriel se move:

- **Piso de Concreto / Cerâmica Antiga:** Emite ruído regular.
- **Dunas de Areia:** Abafam o som dos passos (excelente para passar despercebido), mas reduzem ligeiramente a velocidade de corrida.
- **Entulho com Cacos de Vidro e Vergalhões:** Correr sobre entulho produz ruído estridente e imediato, gerando um evento sonoro de alta magnitude propagado via BFS para salas vizinhas.
- **Já no jogo (Bloco de salas, 2026-10-12):** o piso muda o alcance do som dos passos por um fator: areia e mato **0,5**, lajota e tapete **1,0**, lajota solta e entulho **1,5**. Ver `docs/fases/bloco_de_salas.md`, seções 12.7 e 12.8, e `scripts/sistemas/zona_de_piso.gd`.
- **Pisos Alagados:** Geram ruído de chapinha d'água ritmado, exigindo que o jogador ande devagar, sem correr.

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

**Animação de abrir (por mapa):** a folha da porta é uma peça de parede animada, não parte da `Porta`. Cada mapa tem a sua:
- **Biblioteca:** `cenas/cenario/biblioteca/parede_porta_animada.tscn` (porta de correr de madeira com batente de aço e som `porta_correr.wav`). Os quadros foram gerados por `assets/modelagem/cenario/gerar_porta_biblioteca.py`.
- **Bloco de salas:** `cenas/cenario/bloco_de_salas/parede_porta_animada.tscn` (porta de aço correndo para o lado com visor de vidro aramado, trava eletromecânica e som `porta_bloco.wav`). Os quadros foram gerados por `assets/modelagem/cenario/gerar_porta_bloco.py`, e o áudio por `gerar_efeitos_porta_bloco.py`.

Para ligar a animação em uma porta, use a peça animada correspondente no vão em vez de `parede_porta.tscn`: a `Porta` acha sozinha a folha cujo centro fica a até 12 px dela (peça de 80 px de largura, `Porta` no meio do vão) e não precisa de campo no Inspetor. Ao apertar `E` a folha abre, durando o mesmo que `segundos_andando`; na sala de destino ela fecha. O som de abrir também vem da folha (`som_abrir` no nó `Folha`), valendo no lugar do `som_abrir` padrão da `Porta`. Sem peça animada por perto, a porta funciona como antes.

A porta de chegada é guardada numa variável estática da classe `Porta` (sobrevive à troca de cena sem precisar de autoload). Código: `scripts/sistemas/porta.gd`; o controle automático do Gabriel é `andar_sozinho()` / `devolver_controle()` em `scripts/personagens/gabriel.gd`.
