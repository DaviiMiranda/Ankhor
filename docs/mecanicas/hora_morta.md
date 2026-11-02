# Hora Morta

Hora Morta é o mini game de terror em 3D da Sala VR do cinema ([`../fases/centro_de_convivencia.md`](../fases/centro_de_convivencia.md), seção 7.7). Abre pelo botão **Começar** do menu ([`visor_3d.md`](visor_3d.md), seção 9). É um jogo dentro do jogo, baseado numa teoria sobre a Nave 67: não salva e não muda a história principal. Perder só leva o jogador de volta ao alojamento da nave.

O nome é provisório. A inspiração é *Alien*: uma nave apertada, uma única criatura que não dá para matar e uma fuga numa nave menor. A criatura, as regras e o clima são nossos.

## 1. A fase

```text
                      [Cabine do comandante]
                                |
[Alojamento] == C1 == [Sala de reuniões] == C2 == [Hangar]
                         |          |
                         C3         C4
                         |          |
                    [Depósito] -- [Sala de máquinas]
```

No mapa real, a cabine fica a leste da sala de reuniões, e o hangar segue em linha reta depois do C2. O anel entre a sala de reuniões, o depósito e a sala de máquinas permite fugir por outro lado quando a criatura vem por um deles.

| Área | Função |
|---|---|
| **Alojamento** | Início e volta depois de morrer. A criatura não entra. |
| **C1 e C2** | Corredores com janelas, onde acontece a Varredura |
| **Sala de reuniões** | Centro do mapa, escura, com uma mesa longa no meio, que obriga a dar a volta, cadeiras e um holograma |
| **C3 e C4** | Corredores de serviço, mais estreitos e sem janelas |
| **Depósito** | Três armários, e um deles, sorteado a cada partida, guarda o fusível |
| **Sala de máquinas** | O quadro de energia. O zumbido dos geradores atrapalha ouvir os passos. |
| **Cabine do comandante** | A chave do hangar |
| **Hangar** | A nave menor |

**A sequência:**

1. A porta do hangar está trancada e pede a chave do comandante.
2. A porta da cabine está sem energia.
3. O fusível está em um dos armários do depósito. Vasculhar leva 3 segundos e atrai a criatura.
4. O fusível vai no quadro da sala de máquinas (2 segundos). A cabine abre, mas o C4, a sala de reuniões e a cabine acendem, e o caminho fica mais perigoso.
5. Pegar a chave (1 segundo) dispara o alarme: todas as luzes acendem em vermelho, e a criatura persegue o jogador em qualquer lugar da nave.
6. Abrir o hangar leva 4 segundos, e entrar na nave menor, mais 1,5 segundo. Ao decolar, aparece a tela de parabéns, com a história da Nave 67, e depois o jogador tira o visor e volta à Sala VR.

O objetivo no canto da tela muda conforme o que o jogador já tentou, e nada obriga a seguir essa ordem.

**Morrer:** o jogador volta ao alojamento e mantém o que já pegou. Se o alarme estava tocando, ele para, para a corrida não virar uma derrota atrás da outra.

**Controles:** WASD anda, o clique liga a lanterna, E usa o objeto mirado (segurando, nos que levam tempo) e Esc tira o visor.

## 2. A regra da luz

**A criatura é uma imagem, como uma película estragada, e só existe onde há luz.** No escuro ela continua andando, e dá para ouvir os passos, mas não dá para vê-la e ela não encosta em ninguém. O jogador fica seguro no escuro, mas quase não enxerga, e acender a lanterna para achar o caminho o expõe.

| Situação | O que acontece |
|---|---|
| Criatura numa área acesa ou na lanterna | Aparece e pode tocar o jogador |
| Criatura no escuro | Só os passos |
| Jogador numa área acesa ou com a lanterna ligada, a até 14 m de caminho | Ela corre até ele, mais rápido do que ele anda |
| Jogador no escuro, sem lanterna | Ela volta à ronda, mesmo que passe por dentro dele |
| Alarme tocando | Ela persegue de qualquer distância, um pouco mais devagar que o jogador |

## 3. A Varredura

A nave gira, e a luz de uma estrela entra pelas janelas e passa pelo corredor. Ela tem três etapas:

| Etapa | Duração | O que acontece |
|---|---|---|
| **Aviso** | 2 s | Um estalo, as lâmpadas apagam, os passos e o zumbido param. Ainda dá para se mexer. |
| **Vigia** | 7 s | O corredor clareia e a criatura aparece a 2,6 m, chegando a 1,15 m. **Andar ou girar a câmera faz perder.** |
| **Saída** | 1,6 s | A luz some, ela desaparece, as lâmpadas voltam e ela recomeça a ronda longe do jogador. |

- **Primeira vez:** ao passar do meio do C1 (`z_da_primeira_varredura`), com **NÃO SE MEXA** na tela, e ela aparece do lado para onde o jogador olha.
- **Depois:** só com o jogador no C1 ou no C2, a cada 28 a 40 segundos, sem texto, e ela aparece de qualquer lado. A primeira entrada no C2 adianta a próxima para 6 segundos.
- **Saiu do corredor durante o aviso:** a vigia não vale, porque ali não há janela.
- **Alarme:** não há Varredura durante a fuga.

**O que conta como se mexer.** Andar perde na hora: a conta usa a velocidade real do jogador, nos eixos do chão. O mouse tem uma folga, para um tremor da mão não ser injusto: somamos o tamanho de cada movimento, e essa soma cai 8 px por segundo. Perde quando passa de 24 px (`tolerancia_do_mouse`).

$$m_{t} = \max(0,\ m_{t-1} - 8\,\Delta t) + |\vec{v}_{\text{mouse}}|$$

## 4. O que faz a criatura ser estranha

A silhueta é uma imagem chapada (`Sprite3D` que sempre vira para a câmera), com um quadro de película queimado no lugar do rosto. Ela anda só 7 vezes por segundo (`quadros_por_segundo`), mesmo o jogo rodando a 60: a posição real muda o tempo todo, mas a que aparece na tela só muda nesses quadros, com um pequeno tremor. Parece uma película com quadros faltando. Por ser uma imagem, ela atravessa portas e móveis.

## 5. O visual da nave

Toda a nave segue uma imagem de referência escolhida pelo Davi: seção chanfrada, janelões arredondados, luz fria de um lado e quente do outro, canos à mostra, chão de chapa e grade e faixas de LED nos cantos do piso. É mais realista que o resto do jogo de propósito, porque é um jogo dentro do jogo, e a criatura pixelada e chapada se destaca justamente por isso.

- **Geometria:** as áreas são montadas por código a partir de um kit de peças (`KitDaNave`), com malhas feitas à mão (`SurfaceTool`). A parede da janela é uma faixa de triângulos entre o contorno do buraco e a borda do vão.
- **Texturas:** cada uma nasce de um mapa de altura, que também gera o mapa de normais. A normal de cada pixel vem da inclinação da altura, $\hat{n} \propto (-\partial_x h,\ -\partial_y h,\ 1)$, e por isso a luz parece pegar nos rebites e nas emendas. O ruído é periódico (filtrado por Fourier), então a textura repete sem emenda.
- **Faixas de LED:** só brilham, não contam como luz para a regra da seção 2. Servem para o jogador achar o caminho no escuro, e apagam na Varredura.
- **Só o necessário aparece:** só ficam visíveis a área do jogador e as vizinhas dela (`AREAS_VIZINHAS`).

## 6. Matemática e computação

**Grafo (`GrafoDaNave`).** Os pontos são lugares da nave (corredores, centros de sala, passagens), e as arestas são os trechos que ela anda em linha reta. O alojamento fica de fora, por isso ela não entra lá.

**A\*.** Traça a rota da criatura até o jogador, escolhendo sempre o ponto aberto de menor $f(n) = g(n) + h(n)$: $g$ é o caminho já andado, e $h$, a distância em linha reta até o destino. A rota é refeita a cada 0,4 segundo, e o comprimento dela decide se o jogador está ao alcance da visão.

**Cadeia de Markov.** Na ronda, o próximo ponto depende só do ponto atual e de onde ela veio. Cada vizinho tem peso 1, voltar tem peso 0,25, e quem aproxima da atração soma mais 0,5 (o jogador) ou mais 4 (um barulho recente, como vasculhar um armário). A probabilidade é o peso dividido pela soma dos pesos.

**Estar na lanterna e mirar (produto escalar).** Com $\hat{o}$ = direção do olhar e $\hat{t}$ = direção até o alvo, a criatura está na luz se $\hat{o} \cdot \hat{t} \geq 0{,}9$ (`cosseno_da_lanterna`), cerca de 26°, e a menos de 7 m. Um objeto está mirado se o valor for pelo menos $0{,}93$ (`cosseno_da_mira`), cerca de 22°, dentro da distância de uso.

**Céu (`shaders/ceu_do_espaco.gdshader`).** O céu é dividido em cubinhos, e uma função de sorteio acende só uma pequena parte deles. O sorteio depende só do cubinho, então as estrelas não piscam. Uma matriz de rotação em torno de Y gira o céu com a nave. O planeta usa o produto escalar entre o olhar e o centro dele, e a borda iluminada desenha um crescente.

**Sombra das janelas.** A estrela é uma luz direcional com sombra, e a parede tem um buraco de verdade no lugar da janela. Por isso a luz chega no chão no formato da janela, e a mancha desliza quando a luz gira em Y.

**Derrota (`shaders/filme_queimando.gdshader`).** A película queima do centro para fora. A borda irregular é uma soma de senos do ângulo, somada à distância até o centro.

**Máquina de estados.** A criatura tem `RONDA`, `CACA` e `PARADA`; a Varredura tem `PARADA`, `AVISO`, `VIGIA` e `SAIDA`.

**Áudio 3D.** Os passos são um `AudioStreamPlayer3D`. O `SubViewport` do mundo precisa de `audio_listener_enable_3d`, senão o som não sai de lado nenhum.

## 7. Onde está no projeto

| O quê | Onde |
|---|---|
| A fase (coordena tudo) | `cenas/visor/hora_morta/fase_nave.tscn`, `scripts/visor/hora_morta/fase_nave.gd` |
| Sequência do fusível, da energia e da chave | `scripts/visor/hora_morta/objetivos_da_nave.gd` |
| Kit de peças da nave | `scripts/visor/hora_morta/kit_da_nave.gd` |
| Corredores | `cenas/visor/hora_morta/areas/corredor.tscn`, `scripts/visor/hora_morta/casco_do_corredor.gd` |
| Salas | `cenas/visor/hora_morta/areas/sala_*.tscn`, `scripts/visor/hora_morta/sala_*.gd` |
| Portas e objetos de usar | `cenas/visor/hora_morta/porta_da_nave.tscn`, `scripts/visor/hora_morta/porta_da_nave.gd`, `objeto_da_nave.gd` |
| Lâmpadas (acesa, quebrada, morta) | `scripts/visor/hora_morta/lampada_da_nave.gd` |
| Grafo, A\* e Markov | `scripts/visor/hora_morta/grafo_da_nave.gd` |
| Criatura | `cenas/visor/hora_morta/criatura_da_projecao.tscn`, `scripts/visor/hora_morta/criatura_da_projecao.gd` |
| Varredura | `scripts/visor/hora_morta/varredura.gd` |
| Sala de reuniões | `cenas/visor/hora_morta/areas/sala_reunioes.tscn`, `scripts/visor/hora_morta/sala_reunioes.gd` |
| Cabine do menu | `cenas/visor/hora_morta/areas/cabine_da_nave_pequena.tscn`, `scripts/visor/hora_morta/cabine_da_nave_pequena.gd` |
| Tela de parabéns | `cenas/visor/hora_morta/tela_de_parabens.tscn`, `scripts/visor/hora_morta/tela_de_parabens.gd` |
| Trocar a cena dentro do visor | `Visor.trocar`, em `scripts/sistemas/visor.gd` |
| Texturas e criatura | `assets/modelagem/cenario/gerar_nave_hora_morta.py`, `assets/modelagem/personagens/gerar_criatura_hora_morta.py` |

## 8. O que falta

- **Teste:** a fase não teve uma rodada completa de teste. Falta jogar do começo ao fim, com mouse e fone, e ajustar a dificuldade. A velocidade dela na fuga final (`velocidade_da_fuga`) saiu de uma conta, e não de um teste.
- **Sons provisórios:** reaproveitados do jogo, até termos os definitivos: passos (`sentinela_passo.wav`, mais grave), estalo da nave (`estalo_laje.wav`), ataque (`clarao_disparo.wav`), geradores (`robo_zumbido.wav`) e alarme (`sirene.wav`).
- **Ficar parado no escuro:** o jogador pode esperar no escuro sem nenhum custo além das Varreduras. Falta ver se isso tira a tensão.
