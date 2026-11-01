# Hora Morta

Hora Morta é o mini game de terror em 3D da Sala VR do cinema ([`../fases/centro_de_convivencia.md`](../fases/centro_de_convivencia.md), seção 7.7). Abre pelo botão **Começar** do menu ([`visor_3d.md`](visor_3d.md), seção 9). É um filme dentro do jogo: não muda a história, não salva e perder só devolve o jogador ao menu.

O nome é provisório. A inspiração é *Alien*: uma nave apertada, uma única criatura que não dá para matar e uma fuga numa nave menor. A criatura, as regras e o clima são nossos.

**O que existe hoje:** um trecho, o **corredor das janelas 1**, para testar se a ideia assusta. O resto da nave está na seção 6.

## 1. A regra da luz

**A criatura é uma imagem do filme e só existe onde há luz.** No escuro ela continua andando, e dá para ouvir os passos, mas não dá para vê-la e ela não encosta em ninguém. O jogador fica seguro no escuro, mas quase não enxerga, e acender a lanterna para achar o caminho o expõe.

| Situação | O que acontece |
|---|---|
| Criatura numa área acesa ou na lanterna | Aparece e pode tocar o jogador |
| Criatura no escuro | Só os passos |
| Jogador numa área acesa ou com a lanterna ligada, a até 9 m | Ela corre até ele, mais rápido do que ele anda |
| Jogador no escuro, sem lanterna | Ela volta à ronda, mesmo que passe por dentro dele |

Como o corredor é uma linha só, o jogador acaba tendo de cruzar com ela. O jeito é esperar no escuro enquanto os passos passam.

## 2. A Varredura

A nave gira, e a luz de uma estrela entra pelas janelas e passa pelo corredor. Ela tem três etapas:

| Etapa | Duração | O que acontece |
|---|---|---|
| **Aviso** | 2 s | Um estalo, as lâmpadas apagam, os passos e o zumbido param. Ainda dá para se mexer. |
| **Vigia** | 7 s | O corredor clareia e a criatura aparece a 2,6 m, chegando a 1,15 m. **Andar ou girar a câmera faz perder.** |
| **Saída** | 1,6 s | A luz some, ela desaparece, as lâmpadas voltam e ela recomeça a ronda na ponta mais longe. |

- **Primeira vez:** ao passar do meio do corredor (`z_da_primeira_varredura`), com **NÃO SE MEXA** na tela, e ela aparece do lado para onde o jogador olha.
- **Depois:** a cada 28 a 40 segundos, sem texto, e ela aparece de qualquer lado.

**O que conta como se mexer.** Andar perde na hora: a conta usa a velocidade real do jogador, nos eixos do chão. O mouse tem uma folga, para um tremor da mão não ser injusto: somamos o tamanho de cada movimento, e essa soma cai 8 px por segundo. Perde quando passa de 24 px (`tolerancia_do_mouse`).

$$m_{t} = \max(0,\ m_{t-1} - 8\,\Delta t) + |\vec{v}_{\text{mouse}}|$$

## 3. O que faz a criatura ser estranha

A silhueta é uma imagem chapada (`Sprite3D` que sempre vira para a câmera), com um quadro de película queimado no lugar do rosto. Ela anda só 7 vezes por segundo (`quadros_por_segundo`), mesmo o jogo rodando a 60: a posição real muda o tempo todo, mas a que aparece na tela só muda nesses quadros, com um pequeno tremor. Parece um filme com quadros faltando.

## 4. Matemática e computação

**Estar na lanterna (produto escalar).** Com $\hat{o}$ = direção do olhar e $\hat{t}$ = direção até a criatura, ela está na luz se $\hat{o} \cdot \hat{t} \geq 0{,}9$ (`cosseno_da_lanterna`), o que dá cerca de 26°, e a menos de 7 m.

**Estrelas (`shaders/ceu_do_espaco.gdshader`).** O céu é dividido em cubinhos, e uma função de sorteio acende só cerca de 0,25% deles. O sorteio depende só do cubinho, então as estrelas não piscam. Uma matriz de rotação em torno de Y gira as estrelas com a nave.

**Sombra das janelas.** A estrela é uma luz direcional com sombra, e cada parede é um bloco de verdade em volta do vão. Por isso a luz chega no chão no formato da janela, e a mancha desliza quando a luz gira em Y.

**Derrota (`shaders/filme_queimando.gdshader`).** A película queima do centro para fora. A borda irregular é uma soma de senos do ângulo, somada à distância até o centro.

**Máquina de estados.** A criatura tem `RONDA`, `CACA` e `PARADA`; a Varredura tem `PARADA`, `AVISO`, `VIGIA` e `SAIDA`.

**Áudio 3D.** Os passos são um `AudioStreamPlayer3D`. O `SubViewport` do mundo precisa de `audio_listener_enable_3d`, senão o som não sai de lado nenhum. No teste automático, com o jogador de lado para a criatura, um canal ficou cerca de 6 dB mais alto que o outro.

## 5. Onde está no projeto

| O quê | Onde |
|---|---|
| Corredor (coordena tudo) | `cenas/visor/hora_morta/corredor_janelas.tscn`, `scripts/visor/hora_morta/corredor_janelas.gd` |
| Paredes, janelas e colisão | `scripts/visor/hora_morta/casco_do_corredor.gd` |
| Lâmpadas (acesa, quebrada, morta) | `scripts/visor/hora_morta/lampada_da_nave.gd` |
| Criatura | `cenas/visor/hora_morta/criatura_da_projecao.tscn`, `scripts/visor/hora_morta/criatura_da_projecao.gd` |
| Varredura | `scripts/visor/hora_morta/varredura.gd` |
| Trocar a cena dentro do visor | `Visor.trocar`, em `scripts/sistemas/visor.gd` |
| Texturas e criatura | `assets/modelagem/cenario/gerar_nave_hora_morta.py`, `assets/modelagem/personagens/gerar_criatura_hora_morta.py` |

## 6. O que falta

**Sons provisórios.** Reaproveitados do jogo, até termos os definitivos: passos (`sentinela_passo.wav`, mais grave), estalo da nave (`estalo_laje.wav`) e ataque (`clarao_disparo.wav`).

**O resto da nave**, se este trecho funcionar:

| Área | Função |
|---|---|
| Alojamento | Onde o jogador começa |
| Corredor das janelas 1 | Este trecho |
| Cinema de bordo | Centro do mapa, com o 1º rolo de filme |
| Sala de máquinas | Disjuntores e o 2º rolo |
| Depósito | O 3º rolo, numa sala iluminada |
| Corredor das janelas 2 | Caminho para a fuga, com outra Varredura |
| Hangar | A nave menor |

- **Objetivo:** os projetores drenam a energia da nave. Tirar os 3 rolos devolve a energia: todas as luzes acendem, o hangar abre e a criatura persegue até a nave menor decolar.
- **Grafo:** as salas viram um grafo, e o A\* escolhe a rota dela. Falta decidir se ela atravessa salas apagadas, como faz neste corredor, ou se apagar uma sala corta o caminho, como foi sugerido.
- **Ficar parado no escuro:** hoje, o jogador pode esperar no escuro sem nenhum custo além das Varreduras. Falta testar se isso tira a tensão.
