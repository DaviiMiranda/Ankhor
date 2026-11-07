# Fase — Labirinto (subsolo)

> **Status:** Jogável (segunda versão: ampliado, com a oficina do Zane, três nós de controle, o Corredor do Tempo, opcional, e a câmara selada do fim, com o Zane jogável na ala do escritório)  
> **Área:** subsolo escuro do centro de pesquisa da Âncora  
> **Ordem na história:** **terceira fase**, depois do Bloco de salas e antes do Centro de Convivência ([`centro_de_convivencia.md`](centro_de_convivencia.md)). A saída do Bloco leva a ela; o alçapão da oficina do Zane leva à **câmara selada** (seção 5.1), e a câmara leva à passarela do Centro de Convivência. Também aparece pelo menu **Fases**.

---

## 1. Visão geral

Um labirinto de corredores de concreto no escuro. O Gabriel começa **fora da oficina do Zane, mas perto dela**: numa câmara logo acima do corredor de baixo, com a lanterna no chão ao lado, a 5 salinhas de caminho (uns 13 s a pé) da porta da **oficina**, no canto de baixo à esquerda. O Zane não consegue invadir de longe a rede do subsolo: entrega o **notebook** a Gabriel e pede que invada **três nós de controle**, em três salões espalhados pelo labirinto. Quando os três caem, o Zane o chama pelo rádio: o Gabriel **volta à oficina**, e o Zane mostra a saída, um **alçapão escondido** sob uma lona. No caminho, seis robôs patrulham os corredores. No meio do mapa, uma porta com luz âmbar leva ao **Corredor do Tempo**, uma sala opcional contra o relógio (seção 3).

- **Cena:** `cenas/salas/labirinto.tscn` · **Script:** `scripts/salas/labirinto.gd` (herda de `Sala`)
- **Mapa:** `dados/labirinto/mapa_labirinto.tres` (texto, uma letra por bloco)
- **Arte e mapa gerados por:** `assets/modelagem/salas/labirinto/gerar_labirinto.py` (mapa, paredes, piso), `gerar_oficina.py` (hologramas e peças eletrônicas) e `gerar_esconderijo.py` (a parede falsa e a bagunça do Baltazar)
- **Trilha:** `cenas/sistemas/musica_labirinto.tscn` (ver seção 7)

### Como a fase se joga

1. O Gabriel começa perto da oficina. Pega a lanterna (se ainda não tem), segue pelo corredor de baixo até a porta da oficina, abre (`E`) e fala com o Zane (`E`). Ao fim da primeira conversa recebe o **notebook**; a oficina é segura e tem um checkpoint.
2. Procura os três salões. Cada um tem **uma entrada só**, um **console** com a luz vermelha (o nó) e um **checkpoint**. Perto do console, o notebook (tecla do espaço dele) abre o minigame; vencer acende a luz verde.
3. O aviso "Nó N de 3 invadido" marca o progresso. No terceiro, aparece "Rede invadida. Volte ao Zane" e o Zane chama pelo rádio.
4. Volta aos poucos passos da oficina (fugindo dos robôs, que continuam patrulhando) e fala com o Zane de novo: outra conversa, em que ele revela o alçapão sob a lona e o abre.
5. Aperta `E` no alçapão ("Descer"): o Gabriel some no escuro e cai na **câmara selada**: a tampa fecha, uma grade desce e ele fica preso. O Zane vem salvá-lo (jogável), com travas e robôs no caminho. Depois do resgate, os dois ouvem o registro do Carlos e o Gabriel sobe pelo duto, até a passarela (seção 5.1).

**Opcional:** no corredor de cima, um trecho da parede é falso. Com a lanterna apontada para ele aparecem os riscos (o Cruzeiro do Sul e uma cruz); perto, `E` ("Afastar o painel") abre a passagem para a **sala onde o Baltazar morou**, vazia: ele não aparece em pessoa, e a sala é um dos rastros dele (seção 3).

---

## 2. Como o mapa é feito

O labirinto é **sorteado uma vez** (semente fixa, sempre o mesmo) pelo gerador em Python e salvo como texto. Duas grades:

- **Lógica (18 × 11 salinhas):** é onde o labirinto é sorteado por **busca em profundidade com volta atrás**, e é o **grafo** da patrulha dos robôs.
- **De blocos (55 × 40, blocos de 32 px = 1760 × 1280 px):** cada salinha vira 2 × 2 blocos de chão; paredes têm 1 bloco. É nela que rodam o **A\*** e a **BFS**. As 6 fileiras de cima (2 de salinhas) entram depois do sorteio, só para o esconderijo do Baltazar: o labirinto sorteado é o mesmo, deslocado 6 blocos para baixo.

A busca em profundidade gera uma árvore (um só caminho entre dois pontos). Depois, **18% das paredes internas são derrubadas** para criar ciclos: sempre dá para dar a volta num quarteirão e despistar. As paredes encostadas numa sala não entram nesse sorteio, para a entrada da sala continuar única.

Legenda do mapa:

| Letra | O que é |
|---|---|
| `#` | parede |
| `.` | chão |
| `G` | onde o Gabriel começa (câmara perto da porta da oficina, do lado de fora) |
| `T` | a lanterna, ao lado do início (só aparece se ele ainda não tem) |
| `C` | checkpoint (um na oficina e um dentro de cada salão de nó: 4) |
| `P` | pilha (5, em becos sem saída) |
| `L` | lampião de emergência (14 em cruzamentos, mais 2 dentro das salas) |
| `V` | Sentinela · `R` Rastreador · `O` Ronda · `K` Caçador (6 no total, nascem longe do início) |
| `A` | o alçapão da saída, na oficina (escondido até o Zane revelar) |
| `D` · `S` | porta de saída (na parede de cima) e gatilho: só existem no mapa de teste (`labirinto_teste`), não neste mapa |
| `Q` | a porta da **sala segura** (2 blocos de parede, `QQ`), na parede de cima da câmara onde o Gabriel começa. O gerador marca as duas letras logo acima do início |
| `H` | a porta do **Corredor do Tempo** (2 blocos de parede, `HH`, luz âmbar), na parede de cima da salinha `PORTA_DO_CORREDOR` = (11, 3), no meio do mapa |
| `Z` | o Zane |
| `N` | nó de controle (2 blocos de largura: `NN`) |
| `b` `c` `m` `x` | bancada eletrônica, console, mesa com computador, robô desmontado (largos: `bb`, `cc`...) |
| `r` `k` `a` `u` | rack, caixas de peças, braço robótico, cadeira |
| `h` `i` `j` | holograma de ondas, de barras, de código |
| `F` | a **parede falsa** do esconderijo do Baltazar (2 blocos, `FF`). Para o mapa é parede: o esconderijo fica fora do grafo |
| `B` | onde o Baltazar ficava. Hoje é só chão: ele não aparece mais em pessoa (decisão de 2026-10-30) |
| `1` `2` `3` | os **pingentes do chapéu** do Baltazar (colecionáveis, [`../mecanicas/colecionaveis.md`](../mecanicas/colecionaveis.md)). `1` e `2` ficam em becos sem saída do labirinto (o `2`, no corredor logo abaixo da parede falsa) e `3` fica dentro da sala dele, sem aparecer até a lanterna revelar a parede falsa |
| `y` `e` `n` `l` `v` | altar de velas, chapa com estrelas riscadas (larga: `ee`), ninho de panos (largo: `nn`), pilha de livros, tocos de vela |

Para mudar o mapa: altere o `.tres` à mão (mantendo o formato) ou mude `SEMENTE`, `FRACAO_CICLOS`, `INICIO`, `SALAS`, `MODELOS`, `ESCONDERIJO` e `MODELO_ESCONDERIJO` no gerador e rode `python assets/modelagem/salas/labirinto/gerar_labirinto.py` (com `PREVIA=<pasta>` ele salva uma imagem do mapa inteiro). O gerador falha com uma mensagem se o modelo de uma sala não bate com o tamanho dela, se o início ficar fora da faixa `CAMINHO_ATE_A_OFICINA` (de 3 a 8 salinhas de caminho até a oficina) ou se não couberem os robôs.

### Por que corredores de 2 blocos
Na vista do jogo (lateral com profundidade), a parede tem 40 px de altura e cobre o que está logo atrás dela. Com corredor de 1 bloco, a parede de baixo cobriria o corredor inteiro. Com 2 blocos, sobra uma faixa de chão visível, e quem anda rente à parede de baixo some da cintura para baixo. Por isso **os itens ficam sempre na fileira de cima** de cada corredor. Nas salas (5 fileiras de blocos), a última fileira fica parcialmente atrás da parede de baixo: nada importante nela.

### Como a sala se monta
`labirinto.gd` lê o mapa ao carregar e cria: o chão (uma textura repetida), um nó por bloco de parede (topo + face da frente, no y-sort), a colisão (retângulos juntando blocos vizinhos da mesma fileira), os oclusores de luz, os detalhes do chão (marcas de garra, poças, papéis, e as peças eletrônicas na oficina), os marcadores e as portas das salas (seção 3). Uma sequência de letras largas iguais (`bb`, `NN`) vira **um** objeto centrado.

---

## 3. As salas (e o Corredor do Tempo)

Uma sala é um retângulo de salinhas com as paredes internas derrubadas, e **uma entrada só** (no sorteio ela é uma folha da árvore: a busca entra e volta). O desenho de cada uma está em `MODELOS`, no gerador. O mapa guarda o miolo de cada sala em blocos (`salas`, sem as paredes), a área da oficina (`area_oficina`) e as salinhas seguras (`salinhas_seguras`).

| Sala | Onde | Tamanho | O que tem |
|---|---|---|---|
| **Oficina do Zane** | canto inferior esquerdo (o primeiro destino do Gabriel, perto de onde ele começa) | 4 × 2 salinhas (11 × 5 blocos) | O Zane, um checkpoint, bancada, racks, mesa com computador, caixas, braço robótico, cadeira, robô desmontado, 2 hologramas, 1 lampião e **26 peças eletrônicas** espalhadas pelo chão (placas, cabos, resistores, bandeja de chips) |
| **Nó 1** (sala dos servidores) | canto superior esquerdo | 3 × 2 (8 × 5) | Fileira de racks, 1 holograma de ondas, o console do nó (**fácil**) e o checkpoint |
| **Nó 2** (sala de controle) | centro | 3 × 2 | Dois consoles grandes, 2 hologramas, o console do nó (**médio**) e o checkpoint |
| **Nó 3** (laboratório) | canto inferior direito | 3 × 2 | Bancada, braço robótico, caixas, holograma, o console do nó (**difícil**) e o checkpoint |

- **A sala segura (salva o jogo)** fica atrás da porta `QQ`, na parede de cima da câmara do início: porta de metal com a **luz verde** e a casinha (`porta_sala_segura.png`). `labirinto.gd` põe ali uma `Porta` para `cenas/salas/labirinto/sala_segura.tscn` (campos `textura_porta_segura` e `cena_sala_segura` do `labirinto.tscn`). Ver [`../mecanicas/sala_segura.md`](../mecanicas/sala_segura.md).
- **A oficina é segura:** a patrulha dos robôs nunca escolhe uma salinha dela como destino (`MapaLabirinto.salinhas_seguras`), e nenhum robô nasce a menos de 5 salinhas de caminho da porta dela. Um robô que persegue o Gabriel entra normalmente.
- **Os salões dos nós não são seguros:** são becos sem saída. Quem entra com um robô atrás fica encurralado; é a tensão da fase.
- **Luz:** hologramas e consoles têm `PointLight2D` ciano (hologramas, com tremor) ou vermelha/verde (nó). Os hologramas são desenhados **sem luz**, como os olhos dos robôs, e brilham no escuro.

### As portas das salas
Cada sala tem uma **porta na entrada** (`cenas/sistemas/porta_da_sala.tscn`, script `porta_da_sala.gd`). `labirinto.gd` acha a entrada olhando o anel de blocos em volta de cada retângulo de `salas` (`MapaLabirinto.entrada_da_sala`): os blocos que não são parede formam a passagem, e a porta cobre todos eles (2 blocos, na horizontal ou na vertical).

| | Porta fechada | Porta aberta |
|---|---|---|
| Passagem | bloqueia o Gabriel e os robôs (camadas 1 e 8) | livre |
| Visão dos robôs | bloqueia (o raio contra a camada 8 bate nela) | livre |
| Luz | tem oclusor: a luz de dentro não vaza e a lanterna não entra | sem oclusor |
| Lâmpada | vermelha | verde |

- **Quem abre:** o Gabriel aperta `E` a até 24 px da porta (`[E] Abrir`). Um **robô** abre sozinha ao chegar a 14 px dela (a patrulha e a perseguição continuam entrando nas salas, sem o robô travar na porta). Um robô que só passa pelo corredor ao lado não abre.
- **Fecha sozinha:** 1,2 s depois que ninguém (nem o Gabriel nem robô) está a menos de 24 px dela. Quem estiver dentro da sala precisa apertar `E` de novo para sair.
- **Animação (placeholder):** duas folhas de aço (retângulos coloridos, sem sprite) que recolhem para as bordas em 0,35 s, com o som `porta_correr.wav` (mais grave ao fechar). A arte final entra depois sem mudar o script.
- **Não dá para ver a sala de fora:** enquanto a porta está fechada e o Gabriel fora do retângulo da sala, **todo o conteúdo da sala fica invisível** (props, luzes, nó, checkpoint, Zane, alçapão, peças do chão) e também os robôs que estiverem lá dentro. As paredes continuam à vista. Ao abrir a porta ou entrar na sala, tudo aparece; ao fechar de novo, some. Quem nasce ou renasce dentro de uma sala (checkpoint) a vê normalmente.

### O nó de controle
`cenas/sistemas/no_hackeavel.tscn` (script `no_hackeavel.gd`, herda de `Porta`): console, alcance de interação e luz. O notebook o trata como uma porta trancada e abre o minigame (ver [`../mecanicas/hackeamento.md`](../mecanicas/hackeamento.md)); **não gasta bateria**. As marcas `labirinto_no_1`, `_2` e `_3` ficam em `Progresso` e `rede_do_labirinto.gd` conta; no terceiro, marca `labirinto_rede_invadida`, avisa "Volte ao Zane" e toca a transmissão `zane_labirinto_01`.

### O Corredor do Tempo (opcional)
A porta `HH` (`porta_corredor_tempo.png`, luz âmbar) leva a `cenas/salas/labirinto/corredor_do_tempo.tscn` (campos `textura_porta_corredor`, `cena_corredor` e `id_porta_corredor` do `labirinto.tscn`). É onde quem construiu a Âncora testava a calibração com objetos dos anos 80: um corredor com quatro salinhas (jogos, filmes, micros e telefone), cada uma com um mecanismo para alinhar no tempo certo. Ao entrar, a porta tranca e um relógio de **2 minutos** começa a contar para o corredor inteiro. Errar desconta 5 s; quanto menos tempo resta, mais a **ansiedade** do Gabriel sobe; se o relógio zera, é **game over** (último checkpoint). Vencendo, a porta destrava e aparece a **Folha de calibração**, um bilhete do Carlos assinado só "C.". Não tem robôs, e não faz parte do caminho dos três nós. Regras, ajustes e arquivos em [`../mecanicas/corredor_do_tempo.md`](../mecanicas/corredor_do_tempo.md).

### O Zane
`cenas/personagens/zane_na_oficina.tscn` (script `zane_oficina.gd`, herda de `ConversaNpc`). Quatro conversas em `dados/dialogos/`:

| Arquivo | Quando |
|---|---|
| `zane_labirinto_primeiro_encontro.json` | Primeira vez. Ao terminar, entrega o notebook. Conta que a mesma trava lacra a saída e o bunker, e que desconfia do Henrique. Tem escolhas: como invadir, os robôs, "Por que desconfiar do Henrique?" e "Me dá esse notebook". No fim, avisa de **duas salas fora do mapa**: um vão atrás de uma parede do corredor de cima que não está em planta nenhuma (a sala do Baltazar: apontar a lanterna para ela) e a porta âmbar entre os nós (o Corredor do Tempo, opcional, com cronômetro). O Zane não sabe de quem é a sala |
| `zane_labirinto_notebook.json` | Se a primeira conversa terminou mas o notebook não coube no inventário |
| `zane_labirinto_de_novo.json` | Nas próximas vezes, enquanto faltam nós. Repete as escolhas, menos a do notebook, e ganha "E aquelas duas salas?", que repete a dica da parede e da porta âmbar |
| `zane_labirinto_alcapao.json` | Depois de os três nós caírem: o Zane revela e abre o alçapão, diz que a trava do bunker soltou junto e pede que o Gabriel fique de olho no Henrique. Ao terminar, marca `labirinto_alcapao_revelado` |
| `zane_labirinto_alcapao_de_novo.json` | Depois de o alçapão aberto: "Desce logo, eu vou atrás" |

### A sala do Baltazar (a sala que só a lanterna revela)
Uma quinta sala, **fora do grafo**: o miolo fica em `esconderijo` no mapa (8 × 5 blocos, nas fileiras novas de cima) e a entrada é a parede falsa `FF`, na parede de cima do corredor de cima, logo acima das colunas 19 e 20. Como `F` conta como parede para o A\*, a BFS e as salinhas, **nenhum robô acha caminho até lá** e o som não chega: é por isso que o Baltazar sobreviveu ali. **Ele não está mais lá** (decisão de 2026-10-30): a sala é um dos rastros dele, e o que houve com ele fica em aberto (Enredo, seção 5).

- **Por fora, parece parede.** Os dois blocos `FF` são desenhados como qualquer bloco (topo e frente), e o miolo da sala é coberto por topos de parede (a "tampa"), então o canto parece concreto maciço. A tampa some quando a passagem abre ou quando o Gabriel está dentro.
- **Só a lanterna revela.** `ParedeFalsa` (`scripts/sistemas/parede_falsa.gd`, cena `cenas/sistemas/parede_falsa.tscn`) desenha por cima da frente o `painel_solto.png` (as emendas do painel, o Cruzeiro do Sul e a cruz), com opacidade igual à força da lanterna naquele ponto. A força é calculada como o cone de luz do feixe, com **produto escalar**: o cosseno entre a direção para onde o Gabriel olha e a direção da mão dele até o meio da parede. Cheia até 20°, some até 32° (`smoothstep`, os mesmos ângulos da textura `luz_cone.png`), e cai com a distância até 120 px. Um raio contra as paredes (camada 8) impede que a luz "atravesse" outra parede. Sem lanterna acesa, a força é zero.
- **Abrir.** Com a marca visível (força acima de 0,5), perto, `E` ("Afastar o painel"): o painel sai, fica encostado no corredor ao lado (`painel_encostado.png`) e a passagem libera. Ao ser vista pela primeira vez, a parede marca `esconderijo_baltazar_descoberto`: daí em diante o `E` funciona mesmo de lanterna apagada (e sempre de dentro).
- **Fecha sozinha.** Como as portas das salas, 1,2 s depois de o Gabriel sair da passagem. Robôs **não** abrem a parede falsa.
- **Dentro:** a sala vazia, com a bagunça de quem morou ali: altar, ninho, livros, caixas, o robô desmontado, a chapa com estrelas e peças e papéis espalhados pelo chão (`quantidade_pecas_no_esconderijo`). As velas são `cenas/cenario/luzes/luz_vela.tscn` (luz quente que treme). A cena do Baltazar em pessoa e as duas conversas dele saíram do jogo.
- **Pingente do chapéu (peça 3).** No chão, ao lado do ninho, no pé do cartaz de estrelas. Fica invisível e sem aviso até a marca `esconderijo_baltazar_descoberto` (a lanterna revelou a parede falsa); depois aparece e dá para pegar. Faz parte da coleção do Labirinto. A marca fica em `marca_do_pingente_escondido`, no `labirinto.gd`.
- **Recorte de jornal (peça 3 dos recortes).** Num beco sem saída do labirinto (a letra `J` do mapa), à vista. É o boletim feito à mão de quem ficou, com a nota assinada "C." (ver [`../mecanicas/colecionaveis.md`](../mecanicas/colecionaveis.md)).
- **Falta:** a carta do Baltazar que fica nesta sala (Enredo, seção 5). Ainda não escrita: falta decidir a quem ele escreve.

---

## 4. Robôs

| | Sentinela | Rastreador |
|---|---|---|
| Quantos | 2 | 2 |
| Aparência | 2,1 m, curvada, braços longos, um olho-farol vermelho | quadrúpede baixo, três olhos, antenas parabólicas |
| Sentido forte | **Visão**: cone de 60° até 170 px (×1,7 com a lanterna acesa); o farol mostra para onde ela olha | **Audição**: ouve passos pelos corredores (×1,8); visão curta (80 px) e larga (100°) |
| Velocidade (patrulha / perseguição) | 18 / 36 px/s | 24 / 50 px/s |
| Como escapar | apagar a lanterna e sair do cone | andar sem correr (passos baixos), principalmente perto dele |

O Labirinto é a primeira fase com a **Ronda** e o **Caçador**, um de cada, nos lugares de duas Sentinelas:

- **Ronda:** monitor de tubo na cabeça, sirene e cassetete. Patrulha 20 px/s, perseguição 38 px/s, visão de 130 px. Repete sempre a mesma rota e bipa antes de virar (a rota sai de `_dar_rota_de_ronda`, em `labirinto.gd`: 4 pontos em 12 salinhas). Para escapar, decorar o caminho.
- **Caçador:** curvado como um gorila, anda apoiado nos punhos. Patrulha 20 px/s, perseguição 46 px/s, visão de 120 px. Depois de ver o Gabriel, continua sabendo onde ele está por 8 s, mesmo sem vê-lo (`rastreia_sem_ver`). Para escapar, sair de perto até o tempo acabar ou se esconder: escondido, ele não acompanha.

O Gabriel anda a 60 px/s e corre a 108 px/s: consegue fugir correndo, mas correr faz barulho e o Rastreador escuta de longe.

Eram 3 robôs na grade de 96 salinhas; na grade de 198 salinhas são 6. Os robôs nascem a pelo menos 10 salinhas de caminho do início, a pelo menos 5 da porta da oficina e a pelo menos 5 de distância entre si (em `gerar_labirinto.py`: `TIPOS_DE_ROBO`, `DISTANCIA_MINIMA_DO_INICIO`, `DISTANCIA_MINIMA_DA_OFICINA`, `SEPARACAO_ENTRE_ROBOS`).

A IA (máquina de estados, cone por produto escalar, BFS do som, A\*, Markov) está em [`../computacao/ia_e_perseguicao.md`](../computacao/ia_e_perseguicao.md) e [`../historia/personagens/robos.docx`](../historia/personagens/robos.docx).

---

## 5. A saída: o alçapão

- **Onde:** `A` no modelo da oficina, dois blocos à direita do Zane. Cena `cenas/sistemas/alcapao.tscn`, script `alcapao.gd` (herda de `Interagivel`).
- **Escondido:** até a marca `labirinto_alcapao_revelado`, o sprite é uma **lona velha** (`alcapao_escondido.png`) e não dá para interagir.
- **Revelado:** ao fim da conversa `zane_labirinto_alcapao.json` o Zane o abre: o sprite vira o alçapão aberto com escada (`alcapao_aberto.png`), uma luz ciano acende e aparece `[E] Descer`.
- **Descer:** o Gabriel para e escurece (0,7 s) e a cena troca direto para a câmara selada (`cena_da_saida` na cena do Labirinto, com `saida_com_tela = false`: sem a tela `SaidaFase`).
- **Se morrer e recarregar:** as marcas ficam em `Progresso`; o alçapão volta já aberto, se o Zane o tinha revelado.
- **Só com o Zane:** ele não abre o alçapão antes de os 3 nós caírem, mesmo que o jogador fale com ele.
- A tela "VOCÊ SAIU DO LABIRINTO · Próxima fase: o Centro de Convivência" agora aparece no fim da câmara selada, no duto de volta (seção 5.1).

### 5.1 A câmara selada (o fim da fase)

Uma parte secreta no fim do Labirinto. O alçapão da oficina não leva à passarela: leva a uma câmara sem janela, que o **Carlos** lacrou. O Zane, que mapeou o duto como saída, não sabia dela. A câmara sai de `assets/modelagem/salas/labirinto/gerar_camaras.py` (as paredes e o chão são as peças do bunker); o caminho do Zane, a **ala do escritório**, sai de `montar_escritorio.py`, na mesma pasta:

| Cena | Quem joga | O que acontece |
|---|---|---|
| `cenas/salas/labirinto/camara_selada.tscn` (1ª vez) | Gabriel | A tampa fecha e uma grade desce: ele fica numa cela. Conversa com o Zane pelo rádio (`camara_gabriel_preso.json`): o Zane diz que é armadilha, manda o Gabriel não encostar em nada e vai por outro lado. Ao fim, a tela escurece e a cena troca para a recepção do escritório |
| `cenas/salas/labirinto/escritorio/*.tscn` | **Zane** (jogável) | A ala do escritório: a recepção e três salas. Detalhes abaixo |
| `camara_selada.tscn` (2ª vez, marca `zane_passagem_concluida`) | Gabriel | O Zane espera do lado de fora da cela e a grade sobe (`camara_zane_resgate.json`). O terminal do fundo acende: `E` toca o **registro do Carlos** (`camara_plano_carlos.json`), em que o grupo descobre a mentira do Henrique. Só depois o duto de volta fica livre (`E`, "Subir"): tela "VOCÊ SAIU DO LABIRINTO" e a passarela do Centro de Convivência |

**A ala do escritório (a mini fase do Zane).** O duto de serviço desemboca num escritório escondido, montado como um prédio comercial dos anos 80 e abandonado: forro de placas, parede creme com lambri, carpete azul, piso vinílico, móveis bege, telas de tubo. O jogador controla o Zane com o mesmo corpo do Gabriel (`sala_do_zane.gd` aplica a ficha dele, como o `escolha_personagem.gd`): as mesmas regras de passos, esconderijo e dano, mas com lanterna infinita, 2 flashes, o **braço de hack** (invade robôs à distância, tecla `4`, no espaço próprio do HUD), estamina 160 e **sem ansiedade** ([`../mecanicas/zane_jogavel.md`](../mecanicas/zane_jogavel.md)). Sem o notebook do Gabriel, os puzzles são os painéis das salas.

```
              ARQUIVO          REUNIÕES         SEGURANÇA
            (Rastreador)      (Mariposa)       (Sentinela)
            ordenar pastas    código 1985      painel de chaves
                 |                |                 |
   +--duto--[porta]----------[porta]----------[porta]----------[RESTRITA]--+
   |  Zane                                                     3 lâmpadas |
   |        [cadeiras] [cadeiras]     [cadeiras] [cadeiras]     balcão    |
   |        [cadeiras] [cadeiras]     [cadeiras] [cadeiras]   (esconde)   |
   |        [cadeiras] [cadeiras]     [cadeiras] [cadeiras]               |
   |              a Ronda dá a volta nas cadeiras                         |
   +------------------------------------ RECEPÇÃO -------------------------+
```

| Sala | Tamanho | Robô | Puzzle | Trava (marca) |
|---|---|---|---|---|
| **Recepção** (`recepcao.tscn`) | 960 × 360 | **Ronda**, em volta das 12 longarinas de cadeiras de espera; bipa antes de virar | Nenhum: é o salão que liga as outras. Atrás do balcão há um esconderijo (parado, de lanterna apagada) | Acende uma lâmpada da porta restrita por trava solta |
| **Arquivo** (`arquivo.tscn`) | 480 × 360 | **Rastreador** (ouve; não corra) | **Arquivo deslizante** (`painel_ordenacao`): cinco pastas, da mais antiga para a mais nova (1979, 1981, 1983, 1985, 1988). Um vão entre os arquivos esconde o Zane | `escritorio_trava_arquivo` |
| **Reuniões** (`reunioes.tscn`) | 480 × 360 | **Mariposa** (vê de longe a lanterna acesa) | **Código `1985`** no `painel_codigo`. A pista é o quadro branco: "CALIBRAÇÃO — DATA-ALVO: 26/10/1985" e, de caneta vermelha (a cor do Carlos), "O ano basta." | `escritorio_trava_reunioes` |
| **Segurança** (`seguranca.tscn`) | 480 × 360 | **Sentinela** parada na frente do quadro de chaves | **Painel de chaves** (`painel_bits`, alvo 19 = 10011, cinco chaves). O caminho pensado é hackear a Sentinela de longe com o braço (ela fica lenta durante a invasão e, se der certo, 15 s desligada) e mexer nas chaves | `escritorio_trava_seguranca` |

- **Cobertura:** os móveis grandes (arquivos, longarinas, balcão, mesas, copiadora, console) ficam na camada 1 + 8: tapam a visão dos robôs e entram como obstáculo na grade do A*. Os pequenos (cadeira giratória, planta, lixeira, mesinha) não.
- **A porta restrita:** `recepcao_do_escritorio.gd` acende uma lâmpada por trava. Com as três, marca `escritorio_tres_travas`; o gatilho na frente da porta toca `zane_passagem_fim.json`, marca `zane_passagem_concluida` e a porta leva à câmara.
- **Checkpoints:** um na entrada de cada sala. Cada sala tem uma fala do Zane ao entrar (`zane_escritorio_<sala>.json`), que explica o robô e o puzzle.
- **Arte:** `assets/modelagem/cenario/gerar_escritorio.py` desenha o kit (16 peças de parede, 2 chãos, 15 móveis e as portas de madeira e de aço com a folha abrindo). As cenas do kit ficam em `cenas/cenario/escritorio/`.

**O registro do Carlos.** Só diz o que já é do Enredo (seção "A virada"): o Henrique acredita que vai voltar a antes da morte da mãe, o Carlos só o usa para manter cada um no seu canto enquanto termina de ajustar a Âncora para si. A voz fala como locutor de rádio dos anos 80, sem gírias, e o registro assina só "C.". Depois, o Zane diz que vai para a oficina manter a frequência (por isso, no Centro de Convivência, ele volta a ser só uma voz no rádio) e avisa que o Henrique tem as câmeras do campus.

**Marcas (`Progresso`):** `camara_gabriel_preso`, `zane_escritorio_recepcao_visto` (e `_arquivo_`, `_reunioes_`, `_seguranca_visto`), `escritorio_trava_arquivo`, `escritorio_trava_reunioes`, `escritorio_trava_seguranca`, `escritorio_tres_travas`, `zane_passagem_concluida`, `camara_cela_aberta`, `camara_registro_lido`.

**Para conferir em jogo:** a rota da Ronda entre as cadeiras e a folga para chegar às portas; se dá para hackear a Sentinela da segurança sem ser visto; a Mariposa no escuro da sala de reuniões; a claridade de cada sala (`Escuridao`). Na câmara, a arte ainda é placeholder (terminal feito de retângulos, o duto usa o sprite do alçapão, a cela usa a grade de aço); a música do escritório é só a de perseguição que o `RobosDaSala` põe.

---

## 6. Luz e escuridão

- `CanvasModulate` quase preto (0,13): sem luz, só se vê a silhueta das paredes.
- **Raio de visão:** o Gabriel só enxerga num círculo em volta dele (nó `RaioDeVisao`, `cenas/sistemas/raio_de_visao.tscn`): visão limpa até 56 px do mundo, escuridão crescente até 96 px e preto total depois. Vale por cima de tudo, inclusive da lanterna, dos olhos dos robôs e dos hologramas, mas fica abaixo da vinheta e da interface. Os raios se ajustam no Inspetor do nó. Os robôs não são afetados: a Sentinela vê o Gabriel a até 170 px, então ela pode ver o jogador antes de ele ver ela. Detalhes em [`../mecanicas/iluminacao_e_lanterna.md`](../mecanicas/iluminacao_e_lanterna.md).
- A lanterna do Gabriel, os lampiões, o farol vermelho da Sentinela, os olhos dos robôs (desenhados **sem luz**, sempre acesos), os hologramas, as luzes dos nós e a placa da saída.
- **De onde sai a luz:** o feixe da lanterna sai da mão do Gabriel e o farol da Sentinela sai da testa (as posições da testa de cada vista estão no Inspetor do robô, grupo *Testa*). A **sombra**, porém, é calculada a partir de um ponto no chão, e só a textura da luz é deslocada até a mão ou a testa (`offset` da `PointLight2D`). Sem isso, um robô encostado numa parede teria a testa "dentro" da sombra da parede e o farol apagaria.
- **Sombras:** cada fileira de parede tem um `LightOccluder2D`; a lanterna e o farol projetam sombra. As paredes em si ficam numa camada de luz separada (`light_mask = 2`), acesa por um segundo feixe sem sombra, para o bloco atingido pela luz aparecer.

---

## 7. Trilha adaptativa

Duas camadas, **mesmo andamento e mesma duração** (100 BPM, 38,4 s, Ré frígio), tocando juntas desde o início:

- **Tensão** (sempre): drone grave, coração, metal arrastado, máquinas ao longe, cordas agudas crescendo.
- **Perseguição** (começa muda): tambores, baixo martelando o meio-tom Ré–Mi♭, golpes de metal, tom de Shepard subindo sem parar e o alarme dos robôs.

Quando um robô vê o Gabriel, a camada de perseguição sobe em 0,8 s; quando todos desistem, desce em 4 s. Como as duas estão sincronizadas, a música "acorda" em vez de trocar. Composição e matemática em `assets/modelagem/audio/gerar_trilha_labirinto.py`.

---

## 8. Ainda não feito

- Esconderijos (armários) e distrações (arremesso) do GDD. Já há nichos nos becos com pilha (2026-11-04), o sonar e o Nó 3 sem pausa: [`../mecanicas/mecanicas_de_fase.md`](../mecanicas/mecanicas_de_fase.md), seção 4.
- Por que a rede do subsolo é fechada para o Zane (Enredo, seção 10.1). Já decidido: os três nós guardam a trava que lacra o bunker (Enredo, seção 8, Ato 2).
- Por onde o Gabriel chega do Bloco de salas ao subsolo (hoje a porta corta-fogo abre direto o Labirinto).
- **Revisar o Bunker:** o registro da câmara faz o grupo descobrir a mentira do Henrique já aqui. O Bunker (`bunker.md`, `bunker_encontro.json` e o pedido do Henrique pela Clarice) ainda trata o Henrique como aliado.
- Arte própria da câmara selada, e testar o equilíbrio da ala do escritório (seção 5.1).
- Rotina de patrulha por grade horária (coloração de grafos): hoje a patrulha é só a cadeia de Markov.
- Uma porta de entrada visível no ponto onde o Gabriel começa (hoje ele simplesmente aparece ali) e animação do Zane; ele está parado.
- Arte final das portas das salas (hoje são retângulos de aço com lâmpada, só para marcar a posição e a animação) e um som de trava ao fechar.
