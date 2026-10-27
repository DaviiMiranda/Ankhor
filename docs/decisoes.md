# Registro de decisões

## 2026-10-26 — Mais duas coleções: disquetes da Clarice no Bloco de salas e pingentes do chapéu do Baltazar no Labirinto
**Decisão:** o sistema de colecionáveis (`docs/mecanicas/colecionaveis.md`) ganha duas coleções, no mesmo esquema dos pingentes de farol da Biblioteca (3 peças no chão, tela "Novo item" com a contagem, sem ir para a mochila, uma linha no quadro branco do quarto e uma recompensa 3D no quarto do Gabriel):
- **Bloco de salas, "Disquetes da Clarice":** três disquetes pretos com os adesivos rosa e amarelo dela (para não se confundir com o disquete azul das senhas), nas salas 105, 106 e 202, fora do caminho obrigatório. Recompensa: uma pilha de três disquetes na **mesa** do Gabriel, ao lado do farol.
- **Labirinto, "Pingentes do chapéu":** três borlas de fio vinho com argola de latão, as do tricórnio do Baltazar (o objeto-símbolo dele). Dois ficam em becos sem saída do labirinto e o **terceiro fica dentro do esconderijo e só aparece depois do primeiro encontro com o Baltazar** (a marca `conheceu_baltazar`); antes disso não tem desenho, brilho nem aviso. Recompensa: o tricórnio sobre o teclado do notebook, também na **mesa**, com os três pingentes nas pontas (em escala menor, porque a faixa livre do tampo é pequena).
- **Peça com trava:** o `ColecionavelNoMundo` ganhou `marca_necessaria`; enquanto a marca não existe, a peça fica escondida e não responde. As recompensas novas usam um script simples (`RecompensaDoQuarto`): aparecem quando a coleção fecha, sem pulso de luz.
- **Os textos não afirmam nada de história:** o disquete só "parece coisa da Clarice" e o pingente é "dessas borlas que enfeitam as abas de um tricórnio". Por que estão espalhados e como foram parar ali ficam sem resposta, como no pingente de farol.
**Por quê:** pedido do Davi: repetir o esquema dos pingentes do farol para a Clarice (com disquetes, no Bloco de salas) e para o Baltazar (com pingentes do chapéu dele), com um deles liberado só depois da fase da sala escondida. Interpretei "a sala escondida" como o esconderijo do Baltazar no Labirinto e "passar dela" como terminar o primeiro encontro com ele; se a ideia era outra (por exemplo, só depois de sair do Labirinto), é trocar a marca `marca_do_pingente_escondido` do `labirinto.gd`.
**Afeta:** `docs/mecanicas/colecionaveis.md` (reescrito para três coleções), `visor_3d.md`, `README.md` das mecânicas, `docs/fases/bloco_de_salas.md` e `labirinto.md`; `dados/colecoes/` e `dados/itens/` (um arquivo novo de cada por coleção); `scripts/itens/colecionavel_no_mundo.gd`, `scripts/salas/labirinto.gd`, `scripts/visor/recompensa_do_quarto.gd` (novo); `cenas/salas/bloco_de_salas/sala_105.tscn`, `sala_106.tscn` e `sala_202.tscn`, `cenas/salas/labirinto.tscn`, `cenas/visor/sala_visor.tscn`, `disquetes_da_mesa.tscn` e `chapeu_do_notebook.tscn` (novas); o mapa do Labirinto (`dados/labirinto/mapa_labirinto.tres` e `gerar_labirinto.py`, letras `1`, `2` e `3`); os geradores `gerar_disquete_colecionavel.py`, `gerar_pingente_chapeu.py`, `gerar_disquetes_mesa.py` e `gerar_chapeu_baltazar.py` e as imagens e modelos que eles criam. A história não mudou. As posições das peças e dos modelos no quarto são primeira versão, para ajustar jogando.

## 2026-10-26 — As falas saem do Roteiro e vão para o Dialogos.docx
**Decisão:** dois documentos Word, cada um com uma função:
- **`docs/historia/dialogos/Dialogos.docx`** (novo): todas as falas do jogo, fase por fase e com os mesmos números de cena do roteiro. Estão lá o prólogo, as conversas em pessoa (com trechos e escolhas), o rádio e o telefone. Também ficam ali as falas novas ainda fora do jogo, com a barra azul, as revisões dessas falas, a lista de conversas de cada ato e um resumo de como cada personagem fala.
- **`docs/historia/roteiro/Roteiro.docx`** (versão 0.9): só a descrição do que acontece ao longo do jogo (cenas, ações, jogabilidade, caderno e documentos). Cada conversa vira uma linha **FALAS**, com o id e um resumo.
- **Saem** `docs/dialogos/README.md` (o guia técnico do sistema de diálogos) e `docs/dialogos/template_dialogo.md` (o modelo de JSON). O texto deles continua no histórico do git.
**Por quê:** pedido do Davi: um documento só com os diálogos, e o roteiro só com a descrição do jogo.
**Afeta:** os dois `.docx`, `docs/gdd.md`, `docs/README.md`, `docs/historia/roteiro/README.md` e `docs/mecanicas/registros_e_caderno.md` (links). O que toca no jogo continua sendo `dados/dialogos/` e `dados/transmissoes/`: mudar uma fala no Word não muda o jogo.

## 2026-10-26 — Conversas do grupo pelo rádio, gírias e medo do Zane, e as relações que faltavam
**Decisão:**
- **História (decidida pelo Davi):**
  - **O medo do Zane é uma máquina sem conserto:** dar de cara com uma máquina que ele não entende e não consegue consertar. Combina com o defeito dele (acha que toda máquina tem conserto), e a Âncora é essa máquina. Sai da pendência 10.4.
  - **A frequência do rádio é aberta:** a Clarice, a Diana e o Zane conversam entre si e com o Gabriel, que também responde. O Henrique não fala nela: o que ele diz chega pela Clarice, como já dizia a ficha.
  - **O grupo descobre pelo rádio que existe alguém de 1750**, no Labirinto, quando o Gabriel conta do acampamento e do diário. O roteiro já registrava isso (decisão de 18/10: "o grupo só descobre o Baltazar no Ato 3, pelo Zane"). Onde ele está e quando o Gabriel o encontra continua pendente.
  - **O Henrique pede, pela Clarice, que o Gabriel não desça ao bunker** quando o elevador do Centro de Convivência liga. É um caso concreto do que "A virada" já dizia: ele mantém cada um no seu canto.
  - **Relações novas nas fichas:** Zane e Clarice, rivalidade de tecnologia entre duas épocas da computação ("analógica", com respeito por baixo); Zane e Diana, ele provoca o drama dela ("despluga"); Diana e Gabriel, ela exagera e ele responde seco.
  - **Gírias do Zane** (ficha, seção 2): *cromado* (muito bom), *zerado* (tudo certo), *analógico* (antiquado), *deu lag* (travou), *despluga* (calma), *fritou* (deu errado).
- **Dez conversas novas pelo rádio** (`dados/transmissoes/grupo_*.tres`), com duas a quatro vozes cada. **Nenhuma fala que já existia foi mudada.** A Diana passa a falar no jogo pela primeira vez.

| Id | Onde e quando | Quem fala | O que conta |
|---|---|---|---|
| `grupo_biblioteca_01` | Salão da Biblioteca, depois de religar a energia | Diana, Clarice, Gabriel | A Diana aparece; com as luzes acesas, a Sentinela muda a ronda |
| `grupo_bloco_01` | Corredor do 1º andar, depois de abrir o claviculário | Clarice, Diana, Gabriel | O depósito (206) e o Rastreador; o mapa da Diana e o "é o fim" |
| `grupo_bloco_02` | Corredor do 1º andar, logo depois de `clarice_03` | Zane, Clarice, Diana, Gabriel | O Zane entra na frequência e espera o Gabriel do outro lado da porta |
| `grupo_labirinto_01` | Labirinto, depois de receber o notebook | Clarice, Zane, Gabriel | O Henrique diz que as câmeras do subsolo não chegam até ele; o Zane acha estranho |
| `grupo_labirinto_02` | Labirinto, depois do segundo nó | Zane, Gabriel, Clarice, Diana | Alguém de 1750, fora da rede |
| `grupo_convivencia_01` | Praça central, depois de `zane_convivencia_01` | Zane, Diana, Gabriel, Clarice | As árvores da praça, que a Diana acha que viu plantar |
| `grupo_convivencia_02` | Cine Andrômeda (opcional) | Clarice, Gabriel, Zane, Diana | O cinema e a dica de juntar os canhotos |
| `grupo_convivencia_03` | Churrasco Solar, depois de `zane_convivencia_02` | Clarice, Gabriel, Zane, Diana | O recado do Henrique: não descer |
| `grupo_bunker_01` | Entrada do bunker | Diana, Clarice, Zane, Gabriel | Robôs no bunker; o Henrique vai abrir a porta; "repara no que ele não fala" |
| `grupo_bunker_02` | Corredor A, depois da conversa com o Henrique | Zane, Gabriel, Clarice, Diana | O que o Henrique faz; ir ao gerador |

- **Mecânica:** a transmissão ganha `falantes` (um nome por fala); o gatilho ganha `na_sala_inteira`, `depois_da_transmissao` e `depois_do_dialogo`; e o `Radio` guarda as transmissões que ainda não terminaram, para a legenda da sala seguinte recomeçar a que foi cortada por uma troca de sala (antes ela se perdia, e a anotação nunca chegava ao caderno). Medido na fonte: cada fala cabe ~170 caracteres em duas linhas, e não mais ~85.
**Por quê:** pedido do Davi: mais conversas entre os personagens, pelo rádio e com mais de duas pessoas, sem mexer nas que já existem; conferir as personalidades nas fichas; e todos os diálogos documentados no roteiro. Decidiu também o medo do Zane, as gírias e as relações novas.
**Afeta:** a História Completa (Ato 2, "A virada" e pendência 10.4) e o `História_Completa.docx`; as fichas do Zane, da Clarice, da Diana e do Gabriel e o `resumo.md`; `scripts/sistemas/transmissao.gd`, `radio.gd` e `gatilho_transmissao.gd`, `scripts/interface/legenda_radio.gd`; as salas `biblioteca/salao`, `bloco_de_salas/corredor_primeiro_andar`, `labirinto`, `centro_de_convivencia/praca_central`, `cinema` e `loja_4`, `bunker/entrada` e `corredor_a` (só um gatilho novo em cada); `docs/mecanicas/registros_e_caderno.md`; o `Roteiro.docx`. **Para conferir:** a fala 2 e a 3 de `zane_convivencia_01`, que já existiam, passam de duas linhas e são cortadas na caixa.

## 2026-10-26 — Falas alinhadas com o Enredo: o Zane desconfia do Henrique, e saem as conversas antigas da Clarice
**Decisão:** duas correções de texto, sem mudar a história (as duas só põem no jogo o que a História Completa já diz):
- **O Zane, no Labirinto, passa a falar do Henrique.** Na primeira conversa ele conta que a trava que lacra a saída do subsolo também lacra o bunker, que o Henrique está trancado lá "consertando tudo" sem nunca ter mostrado nada, e que tudo o que o grupo sabe passa por ele. Uma escolha nova, "Por que desconfiar do Henrique?", mostra o lado do Gabriel (as dicas funcionaram) e deixa a dúvida aberta: o Zane admite que pode ser "só o jeito dele". Quando os três nós caem, ele diz que a trava do bunker soltou junto e pede que o Gabriel fique de olho no Henrique. Usa o retrato `zane_retrato_desconfiado`, que ainda não aparecia.
- **Saem as conversas `clarice_primeiro_encontro.json` e `clarice_de_novo.json`**, da versão em que a Clarice morava no bunker e falava dos loops ("você *sempre* lê"). Não apareciam no jogo: a cena `clarice.tscn` (ela sentada numa estação) não está em nenhuma sala. A cena fica, sem conversa, para ser reaproveitada.
**Por quê:** pedido do Davi, para começar o trabalho de diálogos e documentos corrigindo o que contradizia o Enredo. A ficha do Zane e o Ato 2 já diziam que ele desconfia do Henrique e que os três nós guardam a trava do bunker, mas as falas dele não diziam nada disso.
**Afeta:** `dados/dialogos/zane_labirinto_primeiro_encontro.json`, `zane_labirinto_de_novo.json` e `zane_labirinto_alcapao.json`; `cenas/personagens/clarice.tscn` (sem conversa); `docs/fases/labirinto.md` e `bunker.md`, `docs/dialogos/README.md` e `template_dialogo.md` (o exemplo agora é o Zane), a ficha da Clarice, `assets/sprites/personagens/clarice/visual.md` e `docs/pendencias_de_producao.md`. A História Completa não muda.

## 2026-10-26 — Corredor do Tempo, sala opcional do Labirinto contra o relógio, e o primeiro registro do Carlos
**Decisão:**
- O Labirinto ganha uma porta com luz âmbar (`HH` no mapa, no meio, entre os nós 1 e 2) para o **Corredor do Tempo**: um corredor com quatro salinhas dos anos 80, cada uma com um mecanismo para alinhar no tempo certo, na ordem que o jogador quiser: **toca-discos**, **relógio de ponteiros** (bater no ritmo), **pêndulo** e **três anéis**.
- **Um relógio só**, de 2 minutos, para o corredor inteiro. Ao entrar, a porta tranca e só destrava quando os quatro estão alinhados. Errar desconta 5 s. Quanto menos tempo resta, mais sobe a **ansiedade** do Gabriel (o relógio impõe um piso à barra de ansiedade, `pressão = fração gasta^1,6`), e o tique-taque acelera. **Tempo zerado é game over** (volta ao último checkpoint, e o corredor recomeça do zero).
- A sala é **opcional**: não faz parte do caminho dos três nós. O prêmio é só a **Folha de calibração**, o primeiro registro do Carlos no jogo. Ele conta que testava a Âncora ali, que ela errou de novo e puxou alguém que ele nem foi ver, que já foi um Faroleiro e que só quer os anos 80. **Assina só "C."**: quando o jogador descobre o nome dele continua pendente.
**Por quê:** pedido do Davi: uma sala "contra o tempo" no Labirinto, em que quanto menos tempo resta, maior a ansiedade, com um bilhete do Carlos que conte um pouco da história dele. Os quatro mecanismos (anos 80), o relógio único, o game over e o prêmio foram escolhidos por ele entre opções.
**Afeta:** `docs/historia/História_Completa.md` (seções 4.3 e 8, Ato 2), `docs/historia/personagens/carlos.md` (seções 4 e 5), `docs/fases/labirinto.md`, `docs/mecanicas/corredor_do_tempo.md` e `docs/computacao/oscilacao_e_ritmo.md` (novos), `docs/mecanicas/movimentacao_e_terreno.md`; `scripts/sistemas/ansiedade.gd` (`definir_pressao`), `scripts/salas/labirinto.gd`, `scripts/labirinto/mapa_labirinto.gd`, `cenas/salas/labirinto.tscn`, `dados/labirinto/mapa_labirinto.tres` e `gerar_labirinto.py`; cenas e scripts novos do corredor, das salinhas, do relógio e dos mecanismos; `dados/documentos/folha_calibracao_carlos.tres`; os geradores `gerar_corredor_tempo.py` e `gerar_efeitos_corredor_tempo.py`.

## 2026-10-26 — O esconderijo do Baltazar é uma sala secreta no Labirinto, e o primeiro encontro é lá
**Decisão:**
- **História:** o esconderijo do Baltazar **sai da Biblioteca** e vai para o **Labirinto**. Ele deixou o acampamento entre as raízes seguindo a luz ("Hei de seguir a luz até onde ella nasce"), desceu ao subsolo e se escondeu numa sala atrás de um painel solto, que os robôs nunca acharam. É lá o **primeiro encontro** com Gabriel: o Baltazar se assusta, acha que é o fim do mundo, conta que seguiu a luz e **não quer sair**. Gabriel diz só o primeiro nome, e o **parentesco não aparece** nesse encontro (continua para depois, com o anel). A sala de obras raras da Biblioteca, barrada por dentro, deixa de ser a candidata; quem está do outro lado virou pendência.
- **Jogo:** a entrada é uma **parede falsa** que parece parede e **só aparece com a lanterna apontada para ela** (riscada com o Cruzeiro do Sul e uma cruz). A força da luz é calculada com o cone do feixe (produto escalar). Perto, `E` afasta o painel; ele fecha sozinho quando o Gabriel sai, e os robôs não o abrem. A sala fica fora do grafo do labirinto: nenhum robô acha caminho até ela. Dentro, uma sala bagunçada (ninho de panos, altar de velas, livros, robô desmontado, chapa com estrelas). O primeiro diálogo começa sozinho ao chegar perto dele; depois, ele repete a dica do diário sobre os olhos dos robôs. Por enquanto o encontro é **opcional**.
- **Mapa:** o labirinto sorteado continua o mesmo; ganha 6 fileiras de blocos em cima (55 × 40), onde fica o esconderijo.

**Por quê:** pedido do Davi: uma sala escondida no labirinto, que só se vê com a lanterna apontada, como esconderijo do Baltazar e lugar do primeiro diálogo entre os dois. Responde à pendência "onde fica o esconderijo e quando Gabriel o encontra".
**Afeta:** `docs/historia/História_Completa.md` (seções 6, 6.1, Ato 2 e pendências 10.4 e 10.5), as fichas `baltazar.md` e `resumo.md`, `docs/fases/labirinto.md` e `biblioteca.md`, `docs/mecanicas/iluminacao_e_lanterna.md`; `assets/modelagem/salas/labirinto/gerar_labirinto.py` e `gerar_esconderijo.py` (novo), `dados/labirinto/mapa_labirinto.tres`, `scripts/labirinto/mapa_labirinto.gd`, `scripts/salas/labirinto.gd`, `scripts/sistemas/parede_falsa.gd` e `cenas/sistemas/parede_falsa.tscn` (novos), `cenas/personagens/baltazar_no_esconderijo.tscn`, os objetos novos `altar_baltazar`, `chapa_estrelas`, `ninho_baltazar`, `velas_no_chao` e a luz `luz_vela`, e os diálogos `baltazar_labirinto_primeiro_encontro.json` e `baltazar_labirinto_de_novo.json`. O `História_Completa.docx` ainda não recebeu esta mudança.

## 2026-10-24 — Ansiedade causada pela proximidade dos robôs
**Decisão:** Gabriel ganha uma barra de ansiedade que aumenta conforme o robô mais próximo chega a até 240 px e diminui quando os robôs se afastam. As barras de ansiedade e estamina ficam sempre visíveis. A ansiedade pode aumentar em até 80% o consumo de estamina ao correr. A tela recebe oscilação, separação de cores e vinheta avermelhada proporcionais ao nível de ansiedade.
**Por quê:** pedido do usuário para mostrar a tensão da aproximação dos robôs e fazer Gabriel perder estamina mais rápido sob pressão.
**Afeta:** `scripts/sistemas/ansiedade.gd` e `cenas/sistemas/ansiedade.tscn` (novos), `scripts/personagens/gabriel.gd`, `scripts/sistemas/fadiga.gd`, `scripts/interface/hud.gd`, `shaders/ansiedade.gdshader` (novo) e `docs/mecanicas/movimentacao_e_terreno.md`.

Toda decisão de design, história ou técnica que muda o jogo entra aqui, **a mais recente no topo**. Se algo contradiz o GDD, vale o que está aqui.

> [!IMPORTANT]
> Para **história, mundo e personagens**, a lei do projeto é o [Enredo Principal](historia/História_Completa.md), que vale acima deste registro. Toda decisão de história entra **no mesmo PR** aqui (o histórico de quando e por que mudou) e no Enredo Principal (como a história está agora). Entradas antigas abaixo podem citar nomes e ideias que não valem mais.

Formato:

```
## AAAA-MM-DD — título curto
**Decisão:** o que ficou decidido.
**Por quê:** o motivo, em uma ou duas frases.
**Afeta:** o que precisa mudar (GDD, código, arte, roteiro).
```

---

## 2026-10-23 — Colecionáveis por fase: três pingentes de farol na Biblioteca acendem um farol no quarto do Gabriel
**Decisão:** cada fase passa a ter uma **coleção** escondida, e completá-la libera uma coisa no **quarto do visor 3D** (a mente do Gabriel). A primeira é a da Biblioteca: **três pingentes de farol** (o símbolo dos Faroleiros, em âmbar) espalhados pelo salão, pela sala de terminais e pelo acervo sul. Com os três, aparece na **mesa do Gabriel** um **farol** em 3D, aceso, com luz âmbar pulsando. O quadro branco do quarto mostra o progresso (*Pingentes de farol: 2 de 3*). A peça aparece como item no chão com a tela "Novo item" (contagem 1 de 3...), mas **não vai para a mochila**. O estado entra no save e zera no "Novo jogo".
**Por quê:** pedido do Davi: dar um motivo para explorar além do caminho principal e uma recompensa que se vê no quarto.
**Afeta:** sistema novo (`docs/mecanicas/colecionaveis.md`): autoload `Colecionaveis`, recurso `Colecao` em `dados/colecoes/`, cena `colecionavel_no_mundo.tscn`, `farol_da_mesa.tscn` no `sala_visor.tscn`, modelo `farol_mesa.glb`, `Salvamento` e `menu_principal.gd`. Também `docs/mecanicas/visor_3d.md` e `docs/fases/biblioteca.md`. A história não mudou: o texto do pingente não diz de quem ele é, porque o Enredo Principal ainda não decidiu onde os Faroleiros estão hoje (Pendências dele). As posições dos pingentes e o desenho do farol 3D são primeira versão, para ajustar jogando.

## 2026-10-23 — Cada personagem principal tem um objeto-símbolo
**Decisão:** cada um dos cinco tem um objeto que o representa, registrado na seção 1 da ficha de `docs/historia/personagens/`:
- **Gabriel:** o anel desgastado da avó.
- **Zane:** os óculos.
- **Clarice:** o disquete.
- **Diana:** a jaqueta dela.
- **Baltazar:** o chapéu (o tricórnio). O anel dele continua sendo o elo com o Gabriel.
**Por quê:** pedido do Davi: dar a cada personagem uma marca reconhecível, para a arte, os itens e os cenários poderem usá-la.
**Afeta:** as fichas dos cinco personagens. Pendências de arte: os óculos do Zane (hoje fora do `visual.md` e do `gerar_zane.py`; a Clarice também usa óculos, então os pares precisam se distinguir) e a jaqueta da Diana (ela ainda não tem visual). O Enredo Principal não foi alterado.

## 2026-10-23 — Aba Objetivo na pausa do inventário e a sala de projeção do cinema separada, com porta e fileiras com letras
**Decisão:** três mudanças, sem mexer na história:
- **Aba OBJETIVO** no inventário (terceira aba, depois de ITENS e ANOTAÇÕES; `Q` passa para a próxima, ou clica). Mostra o nome da fase, o **objetivo principal** dela e o que fazer **agora** (o primeiro passo ainda não cumprido, lido das marcas de `Progresso` e do inventário). Fora das fases, mostra o objetivo geral do jogo. Os textos vêm de `docs/fases/` e ficam em `scripts/sistemas/objetivos.gd`.
- **Sala de projeção do cinema separada do hall.** O `cinema` tinha o hall e a sala numa cena só, sem parede nem porta entre os dois. Agora o `cinema` é só o hall (640 × 320), e o arco **SALA 1**, que já estava desenhado na parede, é uma porta (`Porta`) para a nova cena `cinema_sala` (480 × 320), que tem a tela, as poltronas, o canhoto da Bia, uma pedra e a porta da cabine de projeção. A cabine agora volta para a `cinema_sala`.
- **Letras nas fileiras.** As três fileiras da sala ganham as letras **A** (a mais perto da tela), **B** e **C**, em plaquinhas de âmbar no carpete, na ponta e nos dois corredores de cada fileira (`letra_fileira_a/b/c`).
- **Canhotos:** a Bia passa da fileira F para a **A** (poltrona 7, igual) e o canhoto sem nome passa de F-12 para **A-12**, porque a sala só tem as fileiras A, B e C. O Léo (C4) e o Caio (B2) ficam como estavam. O código do cofre continua **7-2-4**.
**Por quê:** pedido do Davi: uma aba Objetivo no pause do inventário, letras nas fileiras do cinema e uma porta/parede para entrar na sala de cinema.
**Afeta:** `scripts/interface/tela_inventario.gd`, `cenas/interface/tela_inventario.tscn`, `painel_objetivo` (script e cena), `scripts/sistemas/objetivos.gd`, `docs/mecanicas/itens_e_inventario.md`; `assets/modelagem/cenario/gerar_interiores_andar2.py`, `gerar_andar2_objetos.py` (letras), `assets/modelagem/salas/centro_de_convivencia/salas_convivencia.py` e `montar_convivencia.py`; cenas `cinema`, `cinema_sala` (nova) e `cinema_cabine`; `dados/documentos/canhoto_bia.tres` e `ingresso_cine_andromeda.tres`; `docs/fases/centro_de_convivencia.md`.

## 2026-10-23 — Quarto do visor mais detalhado: notebook, mesa, caixas jogadas e texturas novas
**Decisão:** o quarto do Gabriel no visor 3D ganha mais detalhe e menos cara de bloco. Notebook de verdade (teclado, trackpad, tampa inclinada e tela acesa com código e um gráfico), mesa com tampo próprio e três gavetas, caneca, canetas e luminária articulada, cadeira com rodízios e moletom macio, cama com dois travesseiros e uma ponta de cobertor caída, criado-mudo com despertador, mochila com alças, porta com almofadas e uma jaqueta pendurada, cacto no peitoril, objetos na estante (o robozinho de brinquedo, uma planta, um porta-retrato) e o videogame na TV. Para a bagunça, **caixas de papelão** jogadas pelo quarto (empilhadas no canto, aberta com livros, caída, pequena na porta), tênis e bolas de papel. Texturas novas ou refeitas: tampo da mesa, papelão, moletom em malha canelada, parede (agora 1 m, com riscos e furinhos) e piso com arranhões.
**Por quê:** pedido do Davi: o quarto estava com móveis lisos e em blocos.
**Afeta:** `assets/modelagem/cenario/gerar_sala_visor.py` (chanfro e quads com UV), `gerar_texturas_quarto.py`, `scripts/visor/texturas_do_quarto.gd` (materiais com UV, brilho e recorte), `cenas/visor/sala_visor.tscn` (colisão das caixas) e `docs/mecanicas/visor_3d.md`. Sem mudança de história.

## 2026-10-21 — Cartas dos Faroleiros e de desconhecidos no Centro de Convivência e no Bloco de salas
**Decisão:** entram seis documentos opcionais que contam um pouco do mundo de 3026, só com o que a História Completa já diz (seções 2.1 a 2.4): quem foi embora (os *Homo sideralis*, que aguentam implantes e vivem "lá em cima"), quem ficou (os *sapiens*, os Faroleiros), o juramento dos três raios (ficar, cuidar, esperar), as marcas do farol (inteiro = seguro, sem raios = perigo), o campus sem cidade em volta e as máquinas que não pensam e repetem o caminho.
- **Centro de Convivência:** a carta da **Neide**, Faroleira (passarela), a carta sem assinatura para a **Lia** (praça) e a carta do **Tião**, Faroleiro, para o Zé (segundo andar).
- **Bloco de salas:** a **lição da Tainá**, uma criança corrigida pela tia Socorro (101), a **carta de uma mãe** para o filho que virou Faroleiro (106) e a carta do **Joaquim**, Faroleiro, para um novato (206).
- **Papéis novos:** `carta` (papel cru, dobrado em três) e `carta_faroleiro` (o mesmo, com o farol âmbar carimbado no canto). No chão, `papel_carta` e `papel_carta_faroleiro` (este com um tracinho âmbar).
- **Não entrou:** onde os Faroleiros estão hoje, se sabem do Carlos e da Âncora, por que o Carlos saiu, há quantos anos os *Homo sideralis* partiram e para onde, o farol riscado em vermelho e a sala 205 (pendências 10.1, 10.2 e 10.4). As cartas não têm data.
**Por quê:** pedido do Davi: cartas de Faroleiros e de desconhecidos que expliquem um pouco do mundo ao redor.
**Afeta:** `dados/documentos/` (seis novos), `scripts/itens/documento.gd`, `scripts/interface/tela_documento.gd`, `scripts/visor/mesa_do_visor.gd`, `assets/modelagem/interface/gerar_interface.py`, `assets/modelagem/cenario/gerar_papeis.py`, `assets/modelagem/salas/centro_de_convivencia/` (e as cenas `passarela_acesso`, `praca_central`, `segundo_andar`), as cenas `sala_101`, `sala_106` e `sala_206` do Bloco de salas, `docs/fases/`, `docs/mecanicas/registros_e_caderno.md` e `docs/historia/template_documento.md`. **A História Completa não foi mexida:** os nomes novos (Neide, Tião, Zé, Joaquim, Lia, Tainá, tia Socorro) são gente comum, sem peso na história, e as cartas são uma forma de os Faroleiros aparecerem no jogo (pendência 10.1); se o Davi quiser, isso entra no Enredo.

## 2026-10-21 — Bunker ampliado: robôs, quadro de religação, salas antigas, marcas dos Faroleiros e o encontro do grupo
**Decisão:**
- **História (decidida pelo Davi):**
  - **Duas salas antigas:** a sala de visitas de um casarão do fim do século XIX e a sala de estar de uma casa dos anos 80, no setor B (portas B-02 e B-07). Continuam sem explicação.
  - **As pichações assinadas "C." saem e viram marcas dos Faroleiros:** o farol inteiro perto da sala segura e o farol apagado perto da comporta do núcleo, em âmbar. O texto "NÃO CONFIE NAS LUZES" saiu porque é o bordão da Clarice, que nunca morou no bunker. "ROTAS = GRAFO", sem assinatura, ficou.
  - **O fim do Bunker é o encontro do grupo:** na sala de dados, Gabriel, o Henrique, o Zane, a Clarice e a Diana se encontram pela primeira vez numa sala só. O Zane quebra a senha do setor B quando a energia volta, e o encontro destrava a comporta do núcleo. A cena é **provisória**: as falas são rascunho (o Davi vai refinar as do Zane), e como a Clarice e a Diana chegam ao bunker fica em aberto. O Baltazar não está no encontro, porque onde e quando Gabriel o encontra continua pendente.
- **Mecânica:**
  - Uma Sentinela no Corredor A e um Rastreador no Corredor B.
  - Nichos novos (`bunker_nicho`, o vão do posto de máscaras de gás): três no A e dois no B.
  - Checkpoints na entrada e no setor B.
  - **O quadro de religação** no gerador: levar energia aos sete pontos do bunker com os 23 m de cabo do carretel. A única resposta é a **árvore geradora mínima** (Kruskal).
  - A energia libera o elevador (atalho da entrada ao Corredor B) e o arsenal (sala nova, com clarões), e faz o Zane chamar pelo rádio.
  - A comporta do núcleo só abre depois do encontro.
**Por quê:** pedido do Davi: aumentar o escopo do Bunker, a fase mais vazia (sem robôs, sem checkpoint, sem desafio), com duas salas antigas, o encontro de todos no fim e as pichações resolvidas.
**Afeta:** a História Completa (seção 6, Ato 3 e as pendências 10.4) e as fichas da Clarice e do Zane; `docs/fases/bunker.md`; `docs/computacao/arvore_geradora_minima.md` (novo) e `README.md`; `docs/mecanicas/furtividade_e_esconderijos.md`; `scripts/sistemas/painel_religacao.gd` e `gatilho_dialogo.gd` (novos); `cenas/sistemas/painel_religacao.tscn` e `gatilho_dialogo.tscn` (novos); `dados/dialogos/bunker_encontro.json` e `dados/transmissoes/zane_bunker_01.tres` (novos, rascunho); `assets/modelagem/cenario/gerar_bunker.py` (`bunker_nicho`), `gerar_salas_antigas.py` e `gerar_marcas_faroleiros.py` (novos); `assets/modelagem/salas/bunker/montar_salas_bunker.py` (novo); as salas `entrada`, `corredor_a`, `corredor_b`, `gerador` e `central_dados`, e as novas `arsenal`, `sala_antiga_xix` e `sala_antiga_80`. O `História_Completa.docx` recebeu as mesmas mudanças (editado no lugar, com a mesma formatação, e conferido contra o `.md`).


## 2026-10-21 — Laboratório, passos 3 e 4: a arena do Carlos e a diretoria
**Decisão:** entram no jogo os dois últimos passos do level design do Laboratório (`docs/fases/dtec.md`, seção 3.1), **só com o que a História Completa já diz**. O que depende das pendências do Enredo ficou de fora.
- **A arena** (Lab Central): o Carlos fica no console do fundo, parado e calado. A lupa vermelha dele (a da ficha) varre a sala como um cone de visão; ser visto enche a suspeita e dispara o alarme, que chama robôs pelas portas. O Gabriel nunca encosta nele (o Enredo diz que o grupo o enfrenta sem lutar). Dois consoles hackeáveis mudam as fases: na B a onda da Âncora (no ritmo da animação, a cada 2,4 s) passa a revelar quem não está na sombra e a porta norte trava; na C o núcleo abre. A cápsula de clarão atordoa a lupa. Cada console invadido vira checkpoint.
- **O fim da arena:** entrar no núcleo da Âncora mostra "VOCÊ CHEGOU AO NÚCLEO DA ÂNCORA / Fim da versão de teste." e volta ao menu. **A cena final não foi feita:** o que acontece com o Carlos e com a Âncora está nas pendências 10.2 e 10.6.
- **A diretoria** (corredor norte) deixou de ser lacrada e mostra só o que o Enredo e as fases já dizem: as relíquias dos anos 80 que a Biblioteca atribui ao Carlos (monitor de tubo verde, telefone, disquetes, numa mesa nova, `mesa_anos80`) e a marca dos Faroleiros com os raios riscados em vermelho (peça nova `dtec_farol_riscado`, desenhada pela regra da seção 2.4 do Enredo: a traição do Carlos, sem explicação).
- **Não entrou:** falas do Carlos (como ele fala está pendente), registros dele (pendentes na ficha), dizer que a diretoria é o quarto dele ou que ele dorme ali, por que os robôs caçam, e a cena final.
- **O clarão** (`scripts/itens/clarao.gd`) passou a atordoar também os nós do grupo `atordoaveis`, perto (110 px) ou que estejam vendo o clarão. Os robôs continuam iguais.
**Por quê:** pedido do Davi: fazer os passos 3 e 4 sem inventar nada que não esteja na história principal.
**Afeta:** `scripts/personagens/carlos_chefe.gd`, `scripts/sistemas/onda_ancora.gd` e `nucleo_ancora.gd` (novos), `cenas/personagens/carlos_chefe.tscn`, `cenas/sistemas/onda_ancora.tscn` e `nucleo_ancora.tscn` (novas), `scripts/itens/clarao.gd`, `assets/modelagem/cenario/gerar_dtec.py` (`dtec_farol_riscado`, `mesa_anos80` e as rampas âmbar e bege), `assets/modelagem/salas/dtec/montar_dtec.py` (arena e diretoria), `cenas/salas/dtec/lab_central.tscn`, `corredor_norte.tscn` e `diretoria.tscn` (nova), `docs/fases/dtec.md`, `docs/computacao/arena_do_carlos.md` (novo) e `docs/computacao/README.md`. **A História Completa e a ficha do Carlos não foram mexidas.** A ficha ainda diz que a cena do Carlos está "só na sala de teste"; quem decide atualizar é o Davi.

## 2026-10-21 — Laboratório, passo 2: a rede de energia da Âncora
**Decisão:** entra no jogo o passo 2 do level design do Laboratório (`docs/fases/dtec.md`, seção 3.1, parte 2).
- **A rede é um grafo com pesos:** dois geradores no subsolo, seis relés (um em cada laboratório: Eletrônica, Informática, Servidores, Química, Robótica e Controle) e a Âncora, ligados por 13 cabos com o comprimento em metros (`scripts/sistemas/rede_energia_dtec.gd`).
- **A energia corre pelo caminho mais curto** de um gerador até a Âncora (Dijkstra, rodado a partir da Âncora). No começo, Gerador Sul > Química > Robótica > Âncora.
- **Os relés** (`cenas/sistemas/rele_rede.tscn`, um nó hackeável como os do Labirinto, sem gasto de bateria) são cortados com o notebook. O aviso diz se a energia desviou (e por onde) ou se nem passava por ali.
- **O corte mínimo é Eletrônica + Servidores + Robótica**, e é o único de 3 relés (teorema de Menger: há três caminhos sem relé em comum). Quando a Âncora fica sem caminho, o relé grava `dtec_rede_cortada` e a grade do Lab Central abre.
- **O telão da Sala de Controle** (`cenas/sistemas/telao_rede.tscn`) mostra o grafo em tela cheia, com o caminho ativo, os relés cortados e o comprimento dos cabos.
- **Os robôs vigiam o caminho:** em cada corredor, o robô troca a ronda pela vigia da porta do relé do caminho ativo que fica no corredor dele (`scripts/sistemas/vigia_da_rede.gd`, rotas `Vigia_<relé>`). Sem mudança no `robo.gd`: a rota é escolhida quando o corredor carrega, e os relés ficam dentro das salas.
- **Ficou para depois:** a fala do Carlos a cada corte (como ele fala está pendente no Enredo), as luzes que apagam, o pulso da Âncora que desacelera e os robôs desmontados da Robótica que se levantam.
**Por quê:** pedido do Davi: implementar o passo 2 do Laboratório. É conteúdo de computação da disciplina (Dijkstra e corte mínimo), explicado em `docs/computacao/rede_e_corte_minimo.md`.
**Afeta:** `scripts/sistemas/rede_energia_dtec.gd`, `rele_rede.gd`, `telao_rede.gd` e `vigia_da_rede.gd` (novos), `cenas/sistemas/rele_rede.tscn` e `telao_rede.tscn` (novos), `assets/modelagem/salas/dtec/montar_dtec.py` (relés, telão e vigias), as salas `corredor_norte`, `corredor_sul`, `lab_eletronica`, `lab_informatica`, `sala_servidores`, `lab_quimica`, `lab_robotica` e `sala_controle`, `docs/fases/dtec.md`, `docs/computacao/rede_e_corte_minimo.md` (novo) e `docs/computacao/README.md`.

## 2026-10-21 — Laboratório, passo 1: mapa novo, robôs, nichos e checkpoints
**Decisão:** entra no jogo o passo 1 do level design "A Última Tentativa" (`docs/fases/dtec.md`, seção 3.1).
- **Chegada pela Emergência** (`cenas/salas/dtec/emergencia.tscn`, nova): a comporta do bunker (`fim_do_bunker.tscn`) e a fase do menu (`09_dtec.tres`) levam para lá. A escada que desce para o bunker é a peça `bunker_escada_desce`. Checkpoint `dtec_chegada`. A lanterna saiu da recepção e foi para a Emergência (só aparece para quem começa pelo menu).
- **Sala segura no corredor sul**, ao lado da Emergência, seguindo a regra de ficar perto da chegada. A porta DESCANSO saiu do corredor norte.
- **Corredor de serviço** (`corredor_servico.tscn`, nova), no lugar do depósito (norte) e do arquivo (sul): liga as pontas dos dois corredores. Checkpoint `dtec_servico`.
- **Lab Central fechado por grade** nas duas portas (`liberada_por = "dtec_rede_cortada"`). Nada grava a marca ainda: o salão só abre com a rede de energia (passo 2).
- **Robôs:** uma Sentinela no corredor norte e um Rastreador no corredor sul, cada um com a sua rota.
- **Nichos:** peça nova `dtec_nicho` (o vão da estação de emergência, com chuveiro e lava-olhos), quatro em cada corredor e um no serviço, com o `NichoEsconderijo` na frente.
- **O montador** (`montar_dtec.py`) aceita robôs, checkpoints, nichos, porta com `liberada_por` (e a grade na porta central) e peça de outro kit, e deixa de sobrescrever a cena animada da máquina.
**Por quê:** pedido do Davi: implementar o passo 1 do level design do Laboratório.
**Afeta:** `assets/modelagem/cenario/gerar_dtec.py` (`dtec_nicho` e `grade_central`, novos), `assets/modelagem/salas/dtec/montar_dtec.py`, `assets/sprites/cenario/dtec/` (as duas imagens novas), `cenas/cenario/dtec/paredes/dtec_nicho.tscn`, `cenas/salas/dtec/` (`emergencia` e `corredor_servico` novas; `corredor_norte`, `corredor_sul`, `recepcao` e `sala_segura`), `cenas/salas/bunker/fim_do_bunker.tscn`, `dados/fases/09_dtec.tres`, `docs/fases/dtec.md`, `docs/mecanicas/sala_segura.md` e `furtividade_e_esconderijos.md`.

## 2026-10-21 — Level design novo do Laboratório, com o confronto final com o Carlos
**Decisão:** o Laboratório (D-Tec) ganha um level design novo, "A Última Tentativa", descrito em `docs/fases/dtec.md`, seção 3.1. Ainda não foi implementado.
- **Mapa:** o Gabriel chega pela **Emergência** (escada que sobe da comporta do núcleo do bunker), e a sala segura vai para perto dela, no corredor sul. O **Lab Central começa fechado** por grades. Um **corredor de serviço** (no lugar do depósito e do arquivo) liga as pontas dos dois corredores e fecha um ciclo no mapa. A diretoria vira o **quarto do Carlos**. Entram nichos, uma Sentinela no corredor norte, um Rastreador no sul e checkpoints.
- **Objetivo:** cortar a rede de energia da Âncora. O telão da Sala de Controle mostra a rede como um grafo; a cada relé cortado, o Carlos redistribui a energia pelo caminho mais curto (Dijkstra) e um robô passa a vigiar o relé seguinte. O **corte mínimo são 3 relés** (Eletrônica, Servidores e Robótica); com os três cortados, a grade do Lab Central abre.
- **O confronto:** o Carlos fica no console do Lab Central e **o Gabriel nunca encosta nele**. A lupa vermelha varre a arena (cone de visão por produto escalar), a Âncora solta uma onda a cada 2,4 s que revela quem não está atrás de cobertura, e quem pega o Gabriel são os robôs. O Gabriel invade dois consoles, atordoa a lupa com a cápsula de clarão e chega ao núcleo.
- **O que fica em aberto:** as falas do Carlos, o quarto e os registros dele, quem guia pelo rádio, se os robôs capturam ou eliminam e a cena final (o destino do Carlos e da Âncora) dependem das pendências 10.2 e 10.6 do Enredo e ficam como espaços vazios.
**Por quê:** pedido do Davi: analisar a fase do laboratório e propor um level design melhor, com uma luta final com o Carlos. A fase não tinha ameaça nem objetivo, a chegada pelo bunker não batia com a recepção, e faltava conteúdo de computação (Dijkstra e corte mínimo entram aqui). O confronto sem combate segue o Enredo, que diz que o grupo enfrenta o Carlos sem lutar.
**Afeta:** `docs/fases/dtec.md` (seção 3.1). Quando for implementado: as salas de `cenas/salas/dtec/` e o `montar_dtec.py`, as salas novas (`emergencia`, `corredor_servico`, `quarto_carlos`), `scripts/sistemas/rede_energia_dtec.gd`, `carlos_chefe.gd` e `onda_ancora.gd` (novos) e `docs/computacao/`. **A História Completa não foi mexida:** a forma de enfrentar o Carlos continua na pendência 10.2 até o grupo aprovar.

## 2026-10-21 — Puzzles nas salas do Centro de Convivência e sala segura visível em todas as fases
**Decisão:**
- **Quatro puzzles novos no Centro de Convivência**, todos opcionais, cada um com um prêmio que cai no chão ao resolver (como o cofre do cinema):
  - **Gráfica Quântica:** a **trava do plotter**, 7 chaves binárias (64 a 1). A etiqueta do plotter diz que o código é quantos avisos faltam imprimir na Ordem de Impressão (4.000 − 3.912 = **88**). Prêmio: 1 cápsula de clarão.
  - **Loja Universitária:** a **arara inteligente**, moletons fora de ordem (G, PP, GG, M, P); trocar vizinhos até ficar do PP ao GG. O painel mostra as trocas usadas e o mínimo (6, o número de inversões). Prêmio: 2 pilhas.
  - **Self Nebulosa:** o **cofre do bufê**. O bilhete da gerência (perto da porta) diz que a senha são as cubas do prato do dia, na ordem do cardápio; o cardápio fica no meio do salão, perto dos cacos e do Rastreador: **619**. Prêmio: 1 cápsula de clarão.
  - **Churrasco Solar:** o **quadro do bar**, disjuntores com nome (GELAD, EXAUST, NEON, GRELHA). O checklist do bar dá a ordem pelas regras (exaustor antes da grelha, geladeira depois da grelha, neon por último). Errar desarma e faz um estalo que a Sentinela ouve. Prêmio: 2 pilhas.
- **A sala segura passa a ser visível.** Toda porta de sala segura leva o mesmo **sinal**: uma lâmpada verde acesa, que pulsa devagar, e uma plaquinha com uma casinha, em cima da porta, mais a placa DESCANSO onde a fase tem placas. A sala fica perto de onde o Gabriel chega na fase.
- **Cada fase ganha a sua sala segura do modelo** (herdada de `modelo_safe_room.tscn`, com os óculos do Zane e o piano), além da que já existia na Biblioteca:
  - **Bloco de salas:** porta DESCANSO no corredor do térreo, logo depois da chegada, antes da 101.
  - **Labirinto:** porta na parede de cima da câmara onde o Gabriel começa (letra `QQ` no mapa).
  - **Centro de Convivência:** porta de vidro verde na passarela de acesso, onde o Gabriel chega pelo duto.
  - **Bunker:** porta DESCANSO no corredor A, ao lado da entrada.
  - **Laboratório:** porta DESCANSO no corredor norte, entre a Recepção e a Eletrônica.
- A **sala 103** (Clarice) e a **Tapioca Orbital** continuam lugares protegidos, com checkpoint, como dizem as falas da Clarice e do Zane; só não salvam. A oficina do Zane também.

**Por quê:** pedido do Davi: enriquecer o Centro de Convivência com puzzles nas outras salas e pôr uma safe room em cada fase num lugar visível. Os puzzles da Gráfica, da Loja Universitária e do bar também contam como conteúdo de computação (sistema binário, inversões e ordenação topológica).
**Afeta:** `scripts/sistemas/painel_bits.gd`, `painel_ordenacao.gd` e `recompensa.gd` (novos), `cenas/sistemas/painel_bits.tscn` e `painel_ordenacao.tscn` (novos), `scripts/sistemas/quadro_energia.gd` (título, nomes, barulho e prêmio; a Biblioteca não muda), `scripts/sistemas/cofre.gd`, `dados/documentos/` (etiqueta do plotter, bilhete e cardápio do Self Nebulosa, checklist do bar), `assets/modelagem/cenario/gerar_papeis.py`, `assets/modelagem/salas/centro_de_convivencia/`, as salas do Centro de Convivência; o sinal da sala segura (`assets/modelagem/cenario/gerar_sinal_sala_segura.py`, `cenas/cenario/objetos/sinal_sala_segura.tscn`); as salas seguras novas (`cenas/salas/*/sala_segura.tscn`); as portas em `biblioteca/corredor_servico.tscn`, `bloco_de_salas/corredor_terreo.tscn`, `bunker/corredor_a.tscn`, `dtec/corredor_norte.tscn` (e `montar_dtec.py`), `centro_de_convivencia/passarela_acesso.tscn` (e `gerar_interiores.py`, o fundo da passarela), o Labirinto (`gerar_labirinto.py`, `mapa_labirinto.tres`, `labirinto.gd`, `mapa_labirinto.gd`, `labirinto.tscn`); `docs/mecanicas/sala_segura.md`, `docs/computacao/binario_e_ordenacao.md` (novo) e os documentos das fases. **A História Completa não foi mexida:** os puzzles são objetos e papéis do lugar, sem fato novo de história.

## 2026-10-20 — Quarto do visor com texturas, mais pôsteres e estrelas cadentes
**Decisão:** o quarto do Gabriel ganha **texturas em pixel art** (tábuas no chão, papel de parede listrado, cortiça, tapete com losango, cobertor xadrez, veio nos móveis e na porta, cortina, lençol, moletom, mochila), aplicadas por **mapeamento triplanar**, e **mais pôsteres**: Fortaleza com jangada, um jogo de nave inventado (ASTRO 8), a folha de equações de Modelagem e Simulação, um calendário de 2026 e a flâmula da Unifor, além do robô e do de 8 bits do prólogo. No céu, de vez em quando passam **estrelas cadentes e luzes coloridas rápidas**, sempre acima do quarto.
**Por quê:** pedido do Davi, para o quarto ter mais detalhe e o céu mais vida. A folha de Modelagem e Simulação vem da ficha do Gabriel (o caderno de equações da cadeira); os outros pôsteres são objetos de quarto, sem peso de história.
**Afeta:** `assets/modelagem/cenario/gerar_texturas_quarto.py` e `assets/sprites/cenario/visor/` (novos), `assets/modelagem/cenario/gerar_sala_visor.py` e `assets/modelos/sala_visor.glb` (sem as frestas, que viraram textura), `scripts/visor/texturas_do_quarto.gd`, `scripts/visor/estrelas_cadentes.gd` e `cenas/visor/estrelas_cadentes.tscn` (novos), `cenas/visor/sala_visor.tscn`, `docs/mecanicas/visor_3d.md`.

## 2026-10-20 — Visor 3D sem CRT, na resolução da janela, com estrelas coloridas no céu
**Decisão:** o quarto do visor deixa de ter o efeito CRT por cima da visão (só a tela da TV mantém o dela) e passa a ser desenhado **na resolução real da janela**, em vez de 640 × 360 ampliado. As texturas continuam em pixel art com filtro Nearest; as bordas dos móveis ficam lisas, com MSAA 2×. Acima das paredes, o céu ganha **centenas de pontos de luz coloridos** que acendem e apagam; dentro do quarto não há partículas.
**Por quê:** pedido do Davi: os textos do mural, da mesa e do quadro precisam ser legíveis mesmo de longe, e o céu aberto pedia mais vida.
**Afeta:** `cenas/visor/sala_visor.tscn`, `scripts/visor/sala_visor.gd` (`resolucao_do_3d`, `_ajustar_resolucao`), `docs/mecanicas/visor_3d.md`.

## 2026-10-20 — O visor é o quarto do Gabriel, a mente dele materializada
**Decisão:** a sala 3D do visor passa a ser **o quarto do Gabriel**, o mesmo de 2026 da ilustração do prólogo (janela com o pôr do sol, escrivaninha, estante, cama, pôsteres), como **a mente dele materializada**: sem teto, as paredes terminam numa linha ciano e acima é o escuro. O quarto **guarda o jogo até ali**: um **mural de cortiça** com um cartão para cada anotação do caderno, ligados por um fio vermelho; os **documentos já lidos jogados na escrivaninha**; e um **quadro branco com os números** (fase, documentos lidos, transmissões ouvidas, anotações, portas destrancadas, itens na mochila, último save). O jogador chega perto, aperta E e a câmera vai até o lugar; no mural e na mesa escolhe um papel e lê o texto inteiro. A TV de salvar continua no fundo. Nada é texto novo: tudo vem do save.
**Por quê:** pedido do Davi. O caderno já é, na história, "o único lugar onde o quadro inteiro existe" (ficha do Gabriel); o quarto dá corpo a isso e abre caminho para o quarto ser, no futuro, a materialização do save de cada jogador.
**Afeta:** `assets/modelagem/cenario/gerar_sala_visor.py` e `assets/modelos/sala_visor.glb` (refeitos), `cenas/visor/` e `scripts/visor/` (`FocoVisor` e as cenas da TV, do mural, da mesa e do quadro), `docs/mecanicas/visor_3d.md`, `docs/mecanicas/sala_segura.md`. **A História Completa não foi mudada:** a ideia do quarto como a mente do Gabriel ainda precisa entrar lá, se o Davi quiser.

## 2026-10-20 — Salvar numa sala 3D em primeira pessoa, pelo menu de uma TV
**Decisão:** ao pôr os óculos do Zane na sala segura, o jogo **vira 3D em primeira pessoa**. O Gabriel aparece numa sala escura com uma grade ciano no chão e uma **TV de tubo** num móvel baixo; anda com WASD, olha com o mouse e, perto da TV, aperta E para a câmera deslizar até a tela. O **menu de salvar é a tela da TV** (Salvar jogo, com a data do último save, e Voltar), só por teclado, com o tema, a fonte e o efeito CRT do menu principal. Esc afasta da tela e, andando, tira os óculos. Salvar continua fazendo o mesmo (vida a 3, checkpoint no pedestal), mas agora é opcional: sair sem salvar não muda nada. O 3D é desenhado em 640 × 360 e ampliado com filtro Nearest, para ficar pixelado como o resto do jogo. A sala, o móvel e a TV são modelados por um script do Blender e exportados em glTF.
**Por quê:** pedido do Davi, para o momento de salvar ser uma cena marcante e para o trabalho de Computação Gráfica mostrar também 3D (câmera em perspectiva, iluminação, textura renderizada em tempo real).
**Afeta:** `scripts/sistemas/visor.gd` (autoload novo `Visor`, que guarda a sala 2D na memória enquanto o 3D roda), `cenas/visor/` e `scripts/visor/` (novos), `assets/modelos/sala_visor.glb` e `assets/modelagem/cenario/gerar_sala_visor.py` (novos), `scripts/sistemas/maquina_de_salvar.gd` e `cenas/sistemas/maquina_de_salvar.tscn` (abrem o visor em vez de gravar no escuro; o som de salvar foi para a TV), `scripts/sistemas/salvamento.gd` (guarda a data do save), `scripts/salas/sala_segura.gd`, `shaders/tela_crt.gdshader` (linhas configuráveis), `project.godot`, `docs/mecanicas/visor_3d.md` (novo) e `docs/mecanicas/sala_segura.md`. Não toca na história: o que é essa sala continua pendente, junto com os óculos como máquina.

## 2026-10-20 — Sala segura por fase, com os óculos do Zane como máquina de salvar
**Decisão:** cada fase terá **uma sala segura**, no estilo *Resident Evil*. Ela é **a única que salva o jogo** e **nenhum robô entra**. Por fora é uma sala comum; por dentro é calma, com luz quente e um piano suave em loop. A **máquina de salvar** são os **óculos do Zane** (o visor de 2123 que já estava na estante do menu), num pedestal: o jogador põe os óculos, a tela escurece, o jogo grava, a vida volta a 3 e o pedestal vira o checkpoint. Existe um **modelo de sala** (`modelo_safe_room.tscn`) que cada fase herda, mudando só um pouco o visual. O botão **Continuar** do menu passa a carregar o último save. Ao salvar, o Gabriel anda até o pedestal, **pega os óculos e põe no rosto** (animação de 12 quadros feita no Blender, tocada de trás para a frente para tirar). Por enquanto só existe a da Biblioteca.
**Por quê:** pedido do Davi. O save em arquivo ainda não existia, e o GDD previa "dormir" como a forma de salvar; os óculos substituem o sono **só para salvar**. O sono e o sonho continuam pendentes.
**Afeta:** `cenas/salas/modelo_safe_room.tscn`, `cenas/salas/biblioteca/sala_segura.tscn`, `cenas/sistemas/maquina_de_salvar.tscn`, `scripts/salas/sala_segura.gd`, `scripts/sistemas/maquina_de_salvar.gd`, `assets/modelagem/personagens/gerar_gabriel_oculos.py`, `assets/sprites/personagens/gabriel/gabriel_oculos_lado.png`, `scripts/personagens/quadros_oculos_gabriel.gd`, `scripts/personagens/gabriel.gd` (tira especial), `scripts/sistemas/salvamento.gd` (autoload `Salvamento`, em `project.godot`), `scripts/sistemas/porta.gd` (portas destrancadas entram no save), `scripts/menu_principal.gd` (Continuar), `cenas/salas/biblioteca/corredor_servico.tscn` (porta da sala segura), `assets/modelagem/audio/gerar_trilha_sala_segura.py`, `assets/modelagem/cenario/gerar_sala_segura.py`, `assets/audio/musica/sala_segura/`, `assets/audio/efeitos/interface/salvar_jogo.wav`, `docs/mecanicas/sala_segura.md` (novo), `docs/mecanicas/vida_e_checkpoint.md`, `docs/mecanicas/sono_e_sonhos.md`, `docs/fases/biblioteca.md`, `assets/audio/README.md`. A porta de entrada fica no corredor de serviço (`corredor_servico.tscn`, letreiro DESCANSO, id `bib_servico_sala_segura`). Pendente: o Enredo Principal ainda não diz por que o visor do Zane está em cada fase.

## 2026-10-20 — A lanterna volta para a mão do Gabriel, com o visual novo
**Decisão:** a lanterna deixa de ficar presa ao peito e passa a ser **empunhada**: o sprite (`lanterna_mao.png`, 14 × 8 px em resolução dobrada, mostrado com escala 0,5, então 7 × 4 px no mundo) fica na mão do Gabriel e acompanha a mão na caminhada, usando uma tabela com a posição da mão em cada quadro (`scripts/personagens/maos_do_gabriel.gd`, gerada por `assets/modelagem/personagens/medir_maos_gabriel.py`). O visual novo, a partir da foto de referência do Davi, é uma lanterna de aço azulado escuro com botão vermelho, pegada quadriculada, lente quente e alça de pulso de nylon preto, no lugar da verde-oliva. A imagem da tela de "item novo" (`lanterna_detalhe.png`), o ícone do inventário (`lanterna.png`) e a lanterna no chão (`lanterna_chao.png`) foram refeitos com esse visual. A luz continua nascendo na lente, que agora fica uns 3,75 px à frente da mão. Nas vistas de costas ela continua escondida.
**Por quê:** pedido do Davi, com a nova arte de referência. A primeira versão na mão (7 × 4 px de corpo) tinha sido trocada pelo peito por chamar atenção; desta vez o corpo da lanterna tem só uns 6 × 3 px, e o sprite do peito (`lanterna_peito.png`) foi apagado.
**Afeta:** `scripts/itens/lanterna.gd`, `cenas/itens/lanterna.tscn`, `scripts/personagens/gabriel.gd` (`posicao_da_mao()`), `scripts/personagens/maos_do_gabriel.gd`, `assets/modelagem/interface/gerar_interface.py`, `assets/sprites/itens/lanterna*.png`, `dados/itens/lanterna.tres`, `docs/mecanicas/iluminacao_e_lanterna.md`. `posicao_do_peito()` continua existindo para a pedra. Se o sprite do Gabriel mudar, rode `medir_maos_gabriel.py` de novo.

## 2026-10-18 — Cada pessoa chega a 3026 três dias depois da anterior
**Decisão:** entre uma chegada e a seguinte passam **3 dias**, e a fenda pulsa a cada 3 dias. Pela ordem já fechada (Henrique, Zane, Clarice, Diana, Gabriel), o Gabriel chega 3 dias depois da Diana, 6 depois da Clarice, 9 depois do Zane e 12 depois do Henrique. A posição do Baltazar continua pendente: se ele entrar no meio da ordem, quem veio antes dele ganha mais 3 dias.
**Por quê:** pedido do Davi, para as falas poderem dizer há quantos dias cada um está lá.
**Afeta:** a História Completa (seções da fenda, 4.1, 7.2 e 10.4), o GDD e as falas que citam dias (a Clarice, na cena 2.2 do `Roteiro.docx`).

## 2026-10-18 — A Clarice passa a ser de 1990
**Decisão:** a Clarice vem de **1990**, não mais de 1994. Continua aluna de processamento de dados, com cerca de 20 anos, e o resto da ficha não muda.
**Por quê:** pedido do Davi.
**Afeta:** a História Completa (tabelas de personagens e linha do tempo), a ficha e o resumo da Clarice, o GDD, `docs/` (registros e modelo de documento), os arquivos do jogo (`dados/documentos/bilhete_clarice.tres`, `disquete_clarice.tres` e `dados/transmissoes/clarice_*.tres`, cujo título no Caderno agora é "Clarice, 1990"), os textos dos geradores de arte, o agente roteirista e o `Roteiro.docx`. Entradas antigas deste registro que citam 1994 ficam como histórico. O número 1994 que sobra nos geradores de som e de bunker é só semente de sorteio, e não foi mexido para não mudar os arquivos gerados.

## 2026-10-18 — Primeira beta (0.1.0-beta.1): versão no menu, ícone do jogo e `.exe` para Windows
**Decisão:**
- **A primeira versão de teste do jogo é a `0.1.0-beta.1`.** O formato é `MAIOR.MENOR.CORREÇÃO-beta.N`, e o número vive num lugar só, `application/config/version` em `project.godot`. Ele aparece **no canto de baixo do menu principal** (`cenas/interface/rotulo_versao.tscn`), para qualquer relato de erro dizer qual versão o testador jogava, e dá o nome da pasta e do `.zip` da beta.
- **O ícone do jogo é a arte do "A" que o Davi mandou** (`assets/icone/ankhor_icone.png` e `.ico`, com os cantos transparentes). Ele é o ícone do projeto, da janela e do `.exe`, e as propriedades do `.exe` mostram nome, empresa e versão.
- **O `.exe` sai do preset "Windows Desktop"** (`export_presets.cfg`, que entra no git): arquivo único com o jogo dentro, só 64 bits, sem `docs/`, `assets/modelagem/` e `ferramentas/`, com os `.json` dos diálogos. O `ferramentas/gerar_beta.py` roda a exportação, confere que a versão do projeto e a do `.exe` batem e monta o `.zip` com o `LEIAME.txt` para o testador. O processo e o que fazer antes de enviar estão em `docs/producao/beta.md`.
- **Sem assinatura digital** (certificado pago): o Windows avisa "O Windows protegeu o computador", e o `LEIAME.txt` ensina a seguir.
- **Verificação da primeira beta:** o `.exe` exportado abre no menu com a versão no canto, os 1307 arquivos de cena, dados e arte estão dentro do pacote, e as 63 cenas de salas e cutscenes carregam do pacote sem erro. O jogo não foi jogado de ponta a ponta à mão.
**Por quê:** pedido do Davi: fazer a primeira beta do jogo, com a arte dele de ícone, e mostrar a versão da beta no menu principal.
**Afeta:** `project.godot` (versão e ícone), `export_presets.cfg` (novo), `assets/icone/` (novo), `cenas/interface/rotulo_versao.tscn` e `scripts/interface/rotulo_versao.gd` (novos), `cenas/menu_principal.tscn` (instancia o rótulo), `ferramentas/` (novo: `gerar_beta.py` e `leiame_beta.txt`), `docs/producao/beta.md` (novo), `docs/README.md` e `README.md` (links).

---

## 2026-10-18 — A trilha sonora oficial toca em loop no menu principal
**Decisão:**
- **O menu principal passa a tocar a trilha sonora oficial do jogo** (`trilha_sonora_oficial_ANKHOR.ogg`, enviada pelo Davi), em **loop**, no lugar da música `menu_whispers_in_the_dark.mp3` que tocava antes. A música continua tocando enquanto o jogador troca de tela dentro do menu (fases, opções, controles) e para ao começar o jogo, quando cada fase usa a sua própria trilha.
- **O arquivo foi convertido de Opus para Ogg Vorbis** (`ffmpeg -c:a libvorbis -q:a 5`): o `.ogg` original está em Opus, que o Godot não reproduz (ele marca o arquivo como inválido e fica mudo). O arquivo do projeto é `assets/audio/musica/oficial/trilha_sonora_oficial_ankhor.ogg`, com **Loop** ligado na importação, e o nó `Musica` do menu toca a −4 dB (a trilha nova é 2 dB mais baixa que a anterior, e o menu usava −6 dB).
- As trilhas antigas do menu (`menu_whispers_in_the_dark.mp3` e `menu_trilha.ogg`) **ficaram no repositório, sem uso**. A autoria e a licença da trilha oficial estão como "(preencher)" em `assets/audio/creditos.md`.
**Por quê:** pedido do Davi: colocar essa música como trilha sonora do jogo, em loop no menu principal.
**Afeta:** `cenas/menu_principal.tscn` (o arquivo e o volume do nó `Musica`), `assets/audio/musica/oficial/` (novo), `assets/audio/README.md` e `assets/audio/creditos.md`.

---

## 2026-10-17 — A máquina do Laboratório é a Âncora e ganha animação
**Decisão:**
- **A máquina do Lab Central é a Âncora.** Até aqui o `docs/fases/dtec.md` dizia que ela não tinha nome nem papel na história e que não era a Âncora. O Enredo Principal já põe a Âncora no D-Tec, junto do laboratório do Carlos, e a máquina do salão central é essa. Os dois passam a dizer a mesma coisa. O Enredo Principal não muda: ele não dizia em que sala a Âncora está e não contradiz isso. O que a Âncora faz nessa fase (consertá-la, o final) continua nas pendências do Enredo (seções 10.2 e 10.6).
- **A animação, o que mexe:** a máquina do Lab Central (`maquina.tscn`) deixa de ser uma imagem parada e passa a tocar uma animação em laço de **24 quadros a 10 por segundo (2,4 s)**: o núcleo bate (raio de 18 px ± 10%) e gira lóbulos de brilho por dentro, uma onda de choque pontilhada sai dele e bate no anel, raios de energia mudam de lugar a cada 2 quadros (mais raios na hora da descarga), a trilha de luz do anel gira com um cometa e acende os parafusos por onde passa, um pulso de energia sobe pelas bobinas das torres e as luzes delas dão um clarão em cruz quando ele chega ao topo.
- **Como entra no jogo:** o `Sprite2D` da máquina vira um `AnimatedSprite2D` (`Animacao`) com autoplay na animação `ativa`. Sem script novo. A folha de quadros e o `SpriteFrames` saem do `gerar_dtec.py`.
- **Sincronia:** o laço tem o mesmo período da luz ciano da cena (`LuzPulsante.periodo = 2.4`) e a mesma fase (os dois são `sin(2π t)`), então o núcleo e a luz pulsam juntos. A segunda luz, de 1,2 s, é o dobro da frequência e também fecha com o laço.
- **O que não mudou:** o `maquina.png` parado continua sendo gerado, idêntico ao de antes. As faíscas (`CPUParticles2D`), a colisão e as luzes ficam como estavam.
**Por quê:** pedido do Davi: uma animação para a máquina do laboratório. Ao pedir, ele confirmou que ela é a Âncora.
**Afeta:** `cenas/cenario/dtec/objetos/maquina.tscn`, `assets/modelagem/cenario/gerar_dtec.py`, `assets/sprites/cenario/dtec/objetos/maquina_folha.png` e `maquina_quadros.tres` (novos) e `docs/fases/dtec.md`.

---

## 2026-10-17 — Os documentos da fase ganham sprite no chão, e o cofre do cinema vai para uma cabine de projeção
**Decisão:**
- **Os papéis têm sprite.** Os documentos do Centro de Convivência eram áreas invisíveis: o Gabriel só os achava por acaso. Agora cada um é um **sprite pequeno no chão**, com o brilho dos itens colecionáveis (cena nova `papel_no_mundo.tscn`): um bilhete, quatro canhotos (uma cor por amigo no cinema), o aviso da loja, a ordem da gráfica, a ordem de serviço e o panfleto.
- **O cofre do cinema muda de lugar:** em vez de ficar no saguão, ele fica numa **sala pequena nova, a cabine de projeção** (`cinema_cabine`, 400 × 220 px), atrás da sala de cinema. A porta cinza, com a plaquinha CABINE, fica na ponta direita da parede da sala. A cabine tem o projetor de rolo, a mesa do lanterninha, latas de filme, o quadro de sessões, os ganchos com o paletó do Tadeu e o cofre.
- **O bilhete do lanterninha foi atualizado:** agora diz que as coisas dele estão no cofre da cabine de projeção, a porta cinza ao lado da tela, que está aberta. O código continua o mesmo (7-2-4, a ordem embaralhada das poltronas dos três amigos) e os canhotos continuam espalhados pelo cinema.
- **As poltronas da sala ganharam numeração em ordem:** cada fileira vai de 1 a 16, da esquerda para a direita, atravessando os corredores (antes os números se repetiam sem sentido: 8, 2, 5, 8). Os trechos de fileira viraram quatro sprites (`poltronas_1`, `_5`, `_9` e `_13`), no lugar de `poltronas_3` e `poltronas_4`.
- **O hall do cinema ficou maior** (o cinema foi de 800 × 280 para 1040 × 320 px): o hall foi de 400 para 640 px de largura e ganhou fliperamas, um sofá de veludo, uma jardineira, um relógio de parede e uma segunda caixa de cartazes; a sala ganhou uma terceira fileira de poltronas e fica agora depois do batente de latão em x = 640. Os canhotos foram **espalhados pelo hall, pela sala e pela cabine** (Léo, Bia e Caio); antes dois estavam no saguão.
- O cartaz recortado do saguão e a pedra do fundo da sala mudaram de lugar para abrir espaço à porta.
**Por quê:** pedido do Davi: os bilhetes estavam invisíveis no jogo, e o cofre deveria ficar numa sala pequena à parte no cinema.
**Afeta:** `assets/modelagem/cenario/gerar_papeis.py` (novo), `cenas/itens/papel_no_mundo.tscn` e `scripts/itens/papel_no_mundo.gd` (novos), `assets/sprites/cenario/objetos/papel_*.png`, `assets/modelagem/cenario/gerar_interiores_andar2.py` e `gerar_andar2_objetos.py` (a cabine e três objetos novos), `assets/modelagem/salas/centro_de_convivencia/` (a sala nova, a porta e o mapa de sprites dos documentos), `cenas/salas/centro_de_convivencia/cinema.tscn`, `cinema_cabine.tscn` (nova) e as cenas das salas com documento, `dados/documentos/bilhete_lanterninha_cofre.tres`, `docs/fases/centro_de_convivencia.md` (seções 7.5 e 7.6).

---

## 2026-10-17 — Os robôs do Centro de Convivência passam a contornar os objetos
**Decisão:**
- **O bug:** o Rastreador (o "cachorro" do Self Nebulosa) e a Sentinela do Churrasco Solar atravessavam mesas, cadeiras e balcões. Os robôs só enxergam a **camada 8** (a das paredes): é com ela que `RobosDaSala` monta o mapa de caminhos e que o robô risca a linha de visão. Os objetos do Centro de Convivência estavam só na camada 1, a que o Gabriel enxerga, e por isso eram invisíveis para os robôs (que também viam o Gabriel através deles).
- **A correção:** os objetos do kit da praça (`cenas/cenario/praca/objetos/`) e o corpo do cofre passam para as camadas **1 e 8** (`collision_layer = 9`), como já eram as paredes em arco. Agora os robôs desviam deles e as mesas, as árvores e os postes cortam a linha de visão, como o texto da fase sempre disse.
- **A folga:** o mapa de caminhos engorda cada objeto em 4 px, pouco para o Rastreador (18 px de largura) numa grade de células de 16 px: ele raspava na quina das cadeiras e parava. As salas com robôs passam a usar `folga_obstaculos = 10`.
- **Teste:** com o Gabriel escondido, cada robô patrulhou 150 s no jogo, em todas as salas com robô (Self Nebulosa, Churrasco Solar, praça e mezanino): nenhum entrou num objeto e a maior parada foi de 1,4 s (a pausa normal do ponto de ronda).
**Por quê:** relato do Davi: o cachorro robô atravessava os objetos na sala mais à esquerda da praça.
**Afeta:** `assets/modelagem/salas/centro_de_convivencia/montar_convivencia.py` (a camada dos objetos e a folga), os 60 objetos de `cenas/cenario/praca/objetos/`, `cenas/sistemas/cofre.tscn` e as cenas `loja_2`, `loja_4`, `praca_central` e `segundo_andar`. Nada nas salas das outras fases.

---

## 2026-10-17 — Cada sala do mezanino ganha um puzzle; o do cinema é um cofre de código
**Decisão:**
- **Cada sala do segundo andar terá um puzzle próprio**, mesmo que não leve a história adiante. Por enquanto só o do **Cine Andrômeda** está feito; a gráfica e a loja universitária ficam para depois.
- **O cofre do cinema:** um cofre cinza no saguão guarda uma **cápsula de clarão** (que cai no chão ao abrir). O código é de **3 dígitos** e **nunca aparece escrito**: o **bilhete do lanterninha** diz que são as poltronas dos amigos dele (**Léo**, **Bia** e **Caio**, só o número, sem a fileira), numa **ordem embaralhada de propósito**. Os **três canhotos** estão espalhados pelo cinema (saguão, sala e o nicho da cortina), cada um com um número. O jogador testa as ordens (no máximo 6) até abrir; errar não tem castigo. A combinação certa é Bia, Caio, Léo: **7-2-4**.
- **O sistema é reutilizável** (`cenas/sistemas/cofre.tscn`, `scripts/sistemas/cofre.gd`, que herda do `PainelCodigo` da Biblioteca): código com qualquer número de dígitos, item e quantidade de prêmio, marca de abertura própria. O prêmio cai no chão, para não se perder se o inventário estiver no limite do item. Está descrito em `docs/mecanicas/cofre_e_codigos.md`.
- **Mudanças pequenas no cinema:** o clarão que estava no chão virou uma pedra (o clarão agora é o prêmio do cofre) e o cartaz recortado mudou de lugar para abrir espaço ao cofre.

**Por quê:** pedido do Davi: um puzzle em cada sala do mezanino, o do cinema sendo um cofre cujo código vem dos assentos dos amigos de quem deixou as coisas lá, com os bilhetes espalhados pela sala e o jogador testando as ordens.
**Afeta:** `cenas/sistemas/cofre.tscn` e `scripts/sistemas/cofre.gd` (novos), `assets/sprites/cenario/objetos/cofre.png` e `cofre_aberto.png` (novos), `assets/modelagem/cenario/gerar_andar2_objetos.py` (o desenho do cofre), `assets/modelagem/salas/centro_de_convivencia/` (lista `cofres` da sala e o montador), `cenas/salas/centro_de_convivencia/cinema.tscn`, `dados/documentos/` (4 novos: o bilhete do lanterninha e os canhotos), `docs/fases/centro_de_convivencia.md` (seção 7.5), `docs/mecanicas/cofre_e_codigos.md` (novo) e o índice `docs/mecanicas/README.md`. Os nomes do lanterninha e dos amigos e o texto dos bilhetes são meus; o Enredo Principal não foi mexido.

---

## 2026-10-16 — A praça de alimentação ganha um segundo andar (o mezanino), com gráfica, loja da universidade e cinema
**Decisão:**
- **O segundo andar é um anel em volta do vazio da praça**, como na planta que o Davi desenhou: o hall com a escada no meio de cima, a **Gráfica Quântica** e a **Loja Universitária** de um lado, o **Cine Andrômeda** do outro, **corrimão de vidro nas bordas** e o andar de baixo escuro, que não aparece. Em vista lateral, o corredor é uma faixa de 112 px que acompanha o arco (a beirada da laje é a mesma equação, `y_frente = y_base + 112`), e o corrimão é um sprite na frente do Gabriel.
- **A escada** fica ao lado da entrada da praça (coluna 14). A da coluna 10 está **interditada** (a Ordem de Impressão da gráfica diz que a fila parou no meio de milhares de avisos de área interditada).
- **É uma área opcional**: não muda o caminho da fase (Célula de Energia, comutador, elevador de carga). Tem uma **Sentinela** de ronda no corredor, dois nichos de manutenção, pedras e pilhas (e uma cápsula de clarão no cinema) e três documentos curtos: o **aviso da Loja Universitária** (2025), a **ordem de impressão** (3026) e o **canhoto do ingresso**.
- **Cada loja tem a sua cor de neon** (limão, azul e violeta), a mesma da porta de vidro, do letreiro e da luz da vitrine; as escadas são ciano, como as outras passagens. O cinema tem uma **tela animada** que chia "sem sinal" e um saguão com bilheteria e bomboniere.
- **Sprites novos**: fachadas das três lojas, as escadas, o corrimão e uns 30 objetos (máquina de venda, totem de informações, plotter, copiadora, impressora 3D, araras, manequins, bilheteria, bomboniere, poltronas...). Os nomes das lojas e as cores são sugestões minhas.

**Por quê:** pedido do Davi: adicionar à praça um segundo andar, com a gráfica e uma loja de roupas da universidade de um lado e um cinema do outro, como no desenho dele.
**Afeta:** `cenas/salas/centro_de_convivencia/` (entram `segundo_andar`, `loja_uni`, `grafica` e `cinema`; `praca_central` ganha as duas escadas e a luz), `cenas/cenario/praca/` (portas azul, limão e violeta; letreiros novos; objetos novos), `assets/sprites/cenario/praca/`, `assets/modelagem/cenario/gerar_andar2.py`, `gerar_interiores_andar2.py`, `gerar_andar2_objetos.py`, `gerar_praca.py` (as escadas), `gerar_praca_base.py` (geometria do mezanino e rampas novas), `gerar_porta_restaurante.py`, `gerar_restaurantes.py` (o letreiro da entrada fica com 240 px, para não cobrir as escadas), `assets/modelagem/audio/gerar_efeitos_escada.py`, `assets/modelagem/salas/centro_de_convivencia/`, `dados/documentos/` (3 novos), `docs/fases/centro_de_convivencia.md` (seção 7). **O Enredo Principal não foi mexido**: além da divergência já registrada (a Cantina, a Gráfica Rápida, o Posto de Manutenção e a Rampa do Subsolo, na seção 6, Ato 2), ele não cita o mezanino. Se o Davi quiser, é só pedir para atualizar.

---

## 2026-10-16 — O Centro de Convivência vira uma praça de alimentação em arco, com restaurantes
**Decisão:**
- **O mapa tem formato de arco**, como a planta desenhada pelo Davi: a entrada no meio de cima e **quatro restaurantes** na curva. Em vista lateral, a parede de trás desce para as pontas (a equação está em `docs/fases/centro_de_convivencia.md`, seção 6), e a praça fica sob uma **cúpula de vidro quebrada**, de noite. A praça tem 2000 × 560 px.
- **As salas viram restaurantes**, cada um com a sua cor de neon e a sua decoração: **Tapioca Orbital** (âmbar, a sala segura), **Self Nebulosa** (verde, o bufê com a faixa de louça quebrada), **Pizzaria Quasar** (vermelho, a cozinha com o quadro de comutação) e **Churrasco Solar** (magenta, o bar com o elevador de carga). A **câmara fria** do Self Nebulosa guarda a Célula de Energia. A saída para o Bunker passa a ser um **elevador de carga**, e não mais uma rampa.
- **As funções das salas antigas continuam:** o Posto de Manutenção (sala segura) virou a Tapioca Orbital, a Cantina e o seu depósito viraram o Self Nebulosa e a câmara fria, a Gráfica (o puzzle) virou a cozinha da Pizzaria, e a Rampa do Subsolo virou o Churrasco Solar. As mesmas marcas e os mesmos itens valem (`convivencia_energia`, `celula_energia`).
- **Sprites novos, e futuristas:** mesas com projetor de holograma, cadeiras de casca, guarda-sóis de luz, totens de pedido, postes, árvores de cúpula, balcões, forno de plasma, grelha solar, tanque criogênico... Os sprites antigos da fase (mesa de concreto, balcão da cantina, comporta da rampa e cacos de vidro) saíram.
- **Porta nova nos restaurantes:** porta de vidro automática de duas folhas que correm para os lados, com batente de aço e friso de neon da cor do restaurante, e um som próprio (`porta_restaurante.wav`).
- **A energia acende a praça:** com `convivencia_energia`, os letreiros, as vitrines e os frisos de luz acendem (um mapa de luz por sala), além dos holofotes.
- **Cada sala é um fundo pronto** (uma imagem com a parede e o piso), e não mais peças de 80 e 128 px, porque a parede em arco muda de altura a cada coluna. Os objetos, as portas e os letreiros continuam em peças separadas.

**Por quê:** pedido do Davi: mudar o formato do mapa para o arco do desenho dele, parar de reutilizar os mesmos sprites, deixar tudo futurista e trocar as salas por restaurantes, com uma porta diferente.
**Afeta:** `cenas/salas/centro_de_convivencia/` (as 6 salas antigas saíram; entram `praca_central`, `loja_1` a `loja_4` e `camara_fria`; `passarela_acesso` e `fim_da_convivencia` foram refeitas), `cenas/cenario/praca/` (novo; `cenas/cenario/convivencia/` saiu), `assets/sprites/cenario/praca/` (novo; `assets/sprites/cenario/convivencia/` saiu), `assets/modelagem/cenario/gerar_praca*.py`, `gerar_restaurantes.py`, `gerar_interiores.py`, `gerar_porta_restaurante.py`, `assets/modelagem/audio/gerar_efeitos_porta_restaurante.py`, `assets/modelagem/salas/centro_de_convivencia/` (`montar_convivencia.py` e `salas_convivencia.py`), os textos de `dados/transmissoes/zane_convivencia_*.tres`, `dados/documentos/ordem_manutencao_convivencia.tres` e `panfleto_universitario.tres`, `dados/itens/celula_energia.tres`, `dados/dialogos/zane_labirinto_alcapao.json`, `scripts/sistemas/painel_comutacao.gd`, `docs/fases/centro_de_convivencia.md`, `docs/fases.md`, `docs/gdd.md`. **O Enredo Principal (seção 6, Ato 2) ainda cita a Cantina, a Gráfica Rápida, o Posto de Manutenção e a Rampa do Subsolo, e precisa ser atualizado pelo Davi.**

## 2026-10-16 — Fase Centro de Convivência e sequência final das 6 fases
**Decisão:**
- **A sequência oficial de fases do jogo passa a ser de 6 fases:** **Biblioteca → Bloco de salas → Labirinto → Centro de Convivência → Bunker → Laboratório** (antigo D-Tec, renomeado para "Laboratório" no menu).
- **Saem do jogo e da documentação** as fases descartadas **Espaço Cultural**, **NAMI** e **Reitoria** (inclusive do menu principal e de `dados/fases/`).
- **Fase 4 — Centro de Convivência (`cenas/salas/centro_de_convivencia/`):** implementada com 7 salas jogáveis (`passarela_acesso`, `patio_central`, `cantina`, `deposito_cantina`, `grafica_rapida`, `posto_manutencao` e `rampa_subsolo`) mais a transição `fim_da_convivencia`, seguindo o documento de projeto da fase.
- **Sem NPC presencial no Centro de Convivência:** nenhum personagem ajuda o Gabriel presencialmente na fase; todo o apoio é feito pelo **Zane via rádio** (`zane_convivencia_01` na chegada pela passarela e `zane_convivencia_02` ao pegar a célula de energia no depósito).
- **Novo item e puzzle de Coloração de Grafos:** adicionada a **Célula de Energia de Alta Densidade** (`dados/itens/celula_energia.tres`) no Depósito da Cantina e o **Painel de Comutação Trifásico** (`cenas/sistemas/painel_comutacao.tscn`, `scripts/sistemas/painel_comutacao.gd`) no Posto de Manutenção, que exige 3-coloração de um grafo planar de 4 nós e 5 arestas para destravar a comporta da Rampa do Subsolo rumo ao Bunker.
- **Conexões entre fases:** o alçapão da oficina do Zane no Labirinto leva à Passarela de Acesso do Centro de Convivência; a Rampa do Subsolo leva ao Bunker; e a porta blindada no fim do Corredor B do Bunker leva ao Laboratório (`fim_do_bunker.tscn` → `cenas/salas/dtec/recepcao.tscn`).

**Por quê:** pedido do usuário para implementar o Centro de Convivência depois do Labirinto e antes do Bunker, com o Zane ajudando pelo rádio, seguido pelo Laboratório após o Bunker, removendo qualquer menção a outras fases.
**Afeta:** `cenas/salas/centro_de_convivencia/` (8 cenas novas), `cenas/cenario/convivencia/` (3 cenas de kit), `cenas/sistemas/painel_comutacao.tscn` e `scripts/sistemas/painel_comutacao.gd`, `dados/itens/celula_energia.tres`, `dados/documentos/panfleto_universitario.tres` e `ordem_manutencao_convivencia.tres`, `dados/transmissoes/zane_convivencia_01.tres` e `02.tres`, `cenas/salas/labirinto.tscn`, `dados/dialogos/zane_labirinto_alcapao.json`, `cenas/salas/bunker/corredor_b.tscn` e `fim_do_bunker.tscn`, `cenas/menu_principal.tscn`, `dados/fases/` (atualizados `04_convivencia.tres` e `09_dtec.tres`; removidos `05_espaco_cultural.tres`, `06_nami.tres` e `07_reitoria.tres`), `assets/modelagem/cenario/gerar_convivencia.py`, `assets/modelagem/salas/centro_de_convivencia/montar_convivencia.py` e toda a documentação em `docs/`.

---

## 2026-10-16 — Resolução base 640×360 (o mundo continua em zoom 2)
**Decisão:** a resolução base do projeto passa de 320×180 para **640×360**. O mundo não muda: a câmera de cada sala usa `zoom = 2`, então ela ainda enxerga 320×180 de cenário e salas, colisões, velocidades, luzes, IA e sprites ficam como estavam. O que muda é a interface, que agora é desenhada em 640×360 com a mesma fonte (Galmuri 8 e 16): o texto ocupa **metade do tamanho na tela** (uma maiúscula tinha 42 px em Full HD e passa a ter 21 px). Como o stretch já era `canvas_items`, a imagem sempre foi desenhada na resolução da janela, então isso **não pesa na GPU**. Janela do F11: 1280×720 (2×); Full HD: 3×.
Regras para montar telas daqui em diante:
- **Sala nova** herda de `cenas/salas/modelo_sala.tscn` (já tem o zoom e as camadas de vinheta e fade em tela cheia). Cobertura de tela inteira se faz com âncora total (`anchors_preset = 15`), nunca com `320 × 180`.
- **Painéis centrais** (pausa, inventário, documentos, item novo, hackeamento, painel de código, quadro de energia) continuam desenhados em 320×180 e o `CanvasLayer` tem `offset = (160, 90)`, que os põe no centro. O fundo escuro desses painéis usa o retângulo `(-160, -90)` a `(480, 270)`.
- **HUD, caixa de diálogo, legenda do rádio, legenda de cutscene e telas de morte e de saída de fase** têm posições em 640×360, coladas nas bordas. Os corações e os espaços de gadget do HUD são desenhados em 1× e ampliados com `scale = Vector2(2, 2)` no container.
- **Cutscenes:** as ilustrações de 640×360 passam a escala 1 (antes 0,5). **Menu principal:** a raiz tem `scale = Vector2(2, 2)`, então a mesa, o monitor e o texto ficam como estavam.
- **Retratos** do diálogo: 80×80 em escala 1 (antes 40×40 com escala 0,5).
- O aviso `[E]` sobre os objetos usa a transformada da câmera (`get_global_transform_with_canvas`), então segue o objeto com o zoom.
**Por quê:** pedido do Davi: as letras ficavam grandes demais e a interface tomava espaço demais. Foi a opção 1 de uma comparação de quatro: ela resolve o texto sem refazer nenhuma sala. Ver mais cenário (480×270, salas mais altas) ficou como uma decisão à parte, porque exigiria refazer a altura das cerca de 45 salas.
**Afeta:** `project.godot` (viewport 640×360), as câmeras de `modelo_sala.tscn`, `salao.tscn` e `labirinto.tscn` (zoom 2), as cenas de `cenas/interface/`, `painel_codigo.tscn`, `quadro_energia.tscn`, `saida_fase.tscn`, `menu_principal.tscn`, `seg_prologo.tscn` e `seg_acordar.tscn`, `hud.gd` e `caixa_dialogo.gd`, o comentário de `shaders/vinheta.gdshader`, `CLAUDE.md` e os documentos de estilo e de cutscenes.

## 2026-10-15 — O Enredo Principal fica só com a história
**Decisão:** o Enredo Principal passa a ter só o que é história, mundo e personagens. As antigas seções 9 ("Temas e tom") e 10 ("Como a história chega ao jogador") foram para o guia de escrita em `docs/historia/roteiro/README.md`. O Vocabulário oficial vira a seção 9. As pendências viram a **seção 10**, a última, e passam a ser só **perguntas sobre a história**, em seis grupos: o mundo de 3026, o Carlos, o Henrique e a mentira, os outros personagens, a estrutura da história, e a volta e o fim. O que era de arte, mecânica, fases e textos antigos foi para o documento novo `docs/pendencias_de_producao.md`.
**Por quê:** pedido do Davi: as seções 9, 10 e as pendências misturavam roteiro com produção.
**Afeta:** `docs/historia/História_Completa.md`, `docs/historia/roteiro/README.md`, `docs/pendencias_de_producao.md` (novo) e as referências às seções antigas nas fichas, no resumo, nos modelos, nas fases (Biblioteca, Bloco de salas, Centro de Convivência, Labirinto) e no agente `roteirista`. A referência em `docs/fases/bunker.md` fica para o PR #119, que reescreve aquela linha.

## 2026-10-15 — Objetos discretos dos personagens no menu principal (teste)
**Decisão:** a mesa do menu principal ganha três objetos pequenos, só para quem procura: o **anel da avó do Gabriel**, gasto, deitado na madeira entre o teclado e a caneca; os **óculos do Zane**, um visor de 2123 com armação grafite, linha de luz ciano e um detalhe amarelo-ácido, em pé na prateleira do meio da estante do fundo, na frente dos livros; e o **símbolo dos Faroleiros** rabiscado a caneta no post-it da moldura do monitor, feito a partir da pintura do símbolo que o Davi mandou (com as cores invertidas: tinta escura no papel). Cada objeto é um Sprite2D por cima da arte, no nó `ObjetosDosPersonagens`; a `menu_cena.png` não mudou. Os óculos não estão na ficha do Zane: são um objeto novo, que combina com o visual dele.
**Por quê:** pedido do Davi: o menu lembrar alguns personagens bem discretamente. É um teste, para o grupo ver se fica.
**Afeta:** `assets/modelagem/menu/gerar_objetos_menu.py` (novo), `assets/sprites/menu/menu_anel_gabriel.png`, `menu_oculos_zane.png` e `menu_farol_postit.png` (novos), `cenas/menu_principal.tscn`.

## 2026-10-15 — *Homo sideralis*, os Faroleiros e a mentira do Henrique
**Decisão:**
- **Quem foi embora:** os ***Homo sideralis***, uma espécie humana evoluída que aceita melhor os implantes e vive melhor no espaço e em planetas com outra temperatura ou gravidade. Partiram para outro planeta há menos de 100 anos.
- **Quem ficou:** os *sapiens* que não partiram formaram uma resistência que defende o planeta, os **Faroleiros**, que ainda existem longe do campus. O símbolo é um farol âmbar com três raios para o céu (Enredo, seção 2.4).
- **O Carlos era um Faroleiro.** Saiu do grupo e se isolou na Unifor, sozinho durante anos, para ir viver nos anos 80.
- **A IA** é avançada, mas **sem consciência**: é uma ferramenta. Saem as pendências da IA que domina a Terra e da super IA.
- **O Henrique** foi o primeiro a chegar e é quem está há mais tempo em 3026. O Carlos prometeu levá-lo para **antes da morte da mãe** e o usa para **atrasar o grupo** enquanto conserta a Âncora; não se importa com os puxados. O Henrique diz que está consertando tudo, mas não faz nada pelo grupo: usa a IA de 3026 na própria pesquisa sobre viagem no tempo, só para voltar a antes da morte da mãe. Fica **sozinho** numa sala trancada do bunker. Em 2026 é a **lenda do aluno que sumiu na Biblioteca**, e a pesquisa dele virou a cadeira de **Modelagem e Simulação**.
- **O Zane** tem a base na **oficina do Labirinto**, de onde mantém a frequência. Desconfia do Henrique e passa dias tentando invadir o bunker; os três nós do Labirinto guardam a trava do bunker. O final antigo (ficar para domar a IA) sai; medo e final ficam pendentes.
- **O rádio do balcão** existe por causa da Clarice, que passou dias sozinha antes de alguém achá-la.
- **O bilhete da Clarice** passa a pedir que, se mais alguém chegou, a procure no Bloco de salas.
- **O bunker** tem robôs, é difícil de alcançar e tem salas montadas como interiores dos séculos XIX e XX, que mostram a obsessão do Carlos sem explicar.
- **A Diana** passa a ser **estagiária de arquitetura** na obra de 1978 (não mais recruta da polícia). O lote sumiu sob a responsabilidade dela, e a parte dela são as galerias da obra.
- **A parte do Gabriel** deixa de ser as equações: o caderno é o lugar onde as partes de todos se juntam, porque ele é o único que passa por todos os esconderijos.

**Por quê:** conversa do Davi com o Claude no papel de roteirista: fechar os furos da história (a idade do Carlos, o Zane no bunker lacrado, a Clarice sozinha com um rádio já no balcão) e dar conteúdo à mentira do Henrique.
**Afeta:** `docs/historia/História_Completa.md` (seções 1, 2.1, 2.3, 2.4 nova, 3.1, 4.1, 4.3, 6, 6.1, 7.1, 7.2, 8, 11 e 12); as fichas de Henrique, Carlos, Diana, Zane, Clarice, Gabriel e robôs; `resumo.md`; `docs/README.md`. Ainda não foram atualizados (listados no Enredo, seção 12.4): `dados/documentos/bilhete_clarice.tres`, `docs/fases/bunker.md`, as conversas do Henrique no bunker e a "aula de cálculo" do prólogo.

## 2026-10-15 — O menu principal perde o sombreamento escuro nas bordas da tela
**Decisão:** o menu principal não tem mais a **vinheta pixelada** escura que cobria as bordas e os cantos da tela inteira (o nó `Vinheta`, com `shaders/vinheta.gdshader`). A cena do monitor aparece clara até a borda. O efeito CRT dentro do vidro do monitor (linhas, cantos arredondados e um leve escurecimento nas pontas do vidro) continua.
**Por quê:** pedido do Davi: o sombreamento ao redor da tela do jogo, no menu, escurecia a cena e não era desejado.
**Afeta:** `cenas/menu_principal.tscn` (nó `Vinheta` e seus recursos saíram). O `vinheta.gdshader` continua em uso nas salas.

## 2026-10-15 — A Biblioteca fica futurista, e a tecnologia acorda com a energia
**Decisão:** a Biblioteca ganha o visual de 3026 que o vídeo da abertura (`seg_acordar`) já mostrava: racks de arquivo no lugar de parte das estantes (mesma medida, pegada e camada de colisão, então a visão dos robôs e os esconderijos não mudam), mesas holográficas, cabines de vidro ciano, torres de equipamentos, vãos de servidores nas paredes e no fundo pintado, letreiros das portas e a placa SILÊNCIO holográficos, conduítes, gerador e painel de distribuição na manutenção e um robô bibliotecário desligado na doca do balcão (só cenário). A tecnologia **acorda com a energia**: antes de religar os disjuntores as peças novas aparecem apagadas, e quando a marca `energia` chega elas acendem em ciano, piscando como as luzes de emergência; só a cabine começa acesa. As relíquias dos anos 80 do Carlos (monitores de tubo, telefone, disquete, quadro de chaves) continuam. Luz nova não revela o Gabriel (`revela_quem_passa` desligado). Nenhum item, gatilho, posição de interação, rota de robô ou puzzle mudou.
**Por quê:** pedido do Davi (Enredo, seção 12.5: cenários mais futuristas). O jogo contradizia o vídeo logo no primeiro minuto, e a Fase 1 parecia mais antiga que o Bloco de salas, que já ficou futurista.
**Afeta:** `assets/modelagem/cenario/gerar_biblioteca_moderna.py` (novo), `cenas/cenario/objetos/` (rack de arquivo, mesa holográfica, cabine ciano, torre, gerador, painel), `cenas/cenario/paredes/` (servidores, conduítes, painel ciano, doca do bibliotecário), `cenas/cenario/biblioteca/letreiro_holografico.tscn`, `assets/sprites/salas/biblioteca/biblioteca_fundo_moderna*.png` (o fundo antigo continua), as 8 cenas de `cenas/salas/biblioteca/` e `docs/fases/biblioteca.md` (seção 1.2). Em aberto, para o Davi: se o robô bibliotecário e a tecnologia na Biblioteca precisam de explicação na história (o Enredo Principal não foi tocado e nenhuma fala nem bilhete novo foi escrito).

## 2026-10-15 — Salas de aula do Bloco ficam futuristas
**Decisão:** o Bloco de salas ganha um visual de alta tecnologia em ruínas, em todas as 12 salas e nos dois corredores, sem mudar objetivo, robôs, itens nem puzzles.
- **Cadeira com óculos VR no lugar da carteira** (`cadeira_vr`, `cadeira_vr_caida`; friso âmbar na 203 e versão nova em folha na 205). A pegada é a mesma de 14×4 px da carteira, então a navegação não muda. Nas cadeiras, a lente dos óculos acesa é uma camada de luz (`lente_acesa`): poucas por sala (a 104, o laboratório, tem 9; o auditório 201, 14) e **todas** na 205, a "intacta demais".
- **Lousa holográfica que mantém os tracinhos**: 7 na 101, 3 na 201, 8 gravados e firmes na 205, o código 738 continua legível. As lousas "distratoras" ficam com 25. Cada sala tem um estado: soterrada de areia (102), mapa a giz da Clarice no vidro apagado (103), trincada (105), com musgo (106), simples (202, 201).
- **Professor robô desligado, só cenário**, de propósito claro, baixo e arredondado para não ser confundido com os robôs inimigos (Rastreador e Sentinela): na doca de recarga (101, 201, 202, 203; nova em folha na 205), sem cabeça com a cabeça aos pés (204), doca vazia (105), caído (102, 103, 106) e desmontado no chão (105, 206). A luz da doca em âmbar indica sem carga.
- **Rack de óculos VR para os alunos** (`estante_oculos_vr`, com musgo em 106, 202 e 206) no lugar de estantes vazias da 203 e do depósito 206, e painel de óculos na parede (104, 201).
- Avisos novos nas docas e no mapa da 103 ("no vidro do painel apagado"); os avisos dos tracinhos dizem "de luz" em vez de "de giz".
**Por quê:** pedido do Davi: deixar o jogo mais futurista, trocando o visual tradicional de sala de aula, com diferenças visuais entre as salas.
**Afeta:** `assets/modelagem/cenario/gerar_salas_futuristas.py` (novo, gera os sprites e as camadas de luz), `cenas/cenario/objetos/` (cadeiras, racks, professor caído e desmontado, óculos no chão), `cenas/cenario/paredes/` (lousas holográficas, docas, painel de óculos), `scripts/cenario/cadeira_vr.gd`, as 14 cenas de `cenas/salas/bloco_de_salas/` e `docs/fases/bloco_de_salas.md`. Em aberto, para o Davi: se o professor robô e os óculos VR cabem na história (o Enredo Principal não foi tocado) e se os textos dos avisos servem. O Centro de Convivência e as outras fases não mudam.

## 2026-10-15 — O Gabriel volta ao visual antigo (modelo 3D), como os outros personagens
**Decisão:** os sprites e retratos do Gabriel voltam a ser os do **modelo 3D do Blender** (`gerar_gabriel.py`), os mesmos que existiam antes do #74 (2026-10-07, "Gabriel em pixel art desenhada"): moletom vermelho-tijolo de capuz, calça jeans, tênis claro e **mochila** nas costas. Os tamanhos, os nomes de arquivo e a quantidade de quadros são os mesmos (96 × 112, 12 quadros andando, 8 respirando), então `gabriel.tscn` e o ponto do peito da lanterna (`PEITO_NO_QUADRO`, que continua caindo no moletom na linha 40) não mudam. Os retratos voltam a ser três (`normal`, `preocupado` e `surpreso`, os que os diálogos usam); `bravo` e `envergonhado`, que só existiam na versão desenhada e nenhum diálogo usa, saem. O aviso no cabeçalho do `gerar_gabriel.py` sai e o `pixelar_gabriel.py` ganha o aviso contrário: **não rodar como programa**, porque sobrescreveria os sprites. Ele e `gabriel_referencia/` ficam no repositório, pois o `pixelar_clarice.py` e o `pixelar_seg_prologo.py` importam as ferramentas dele.
**Por quê:** pedido do Davi: voltar o Gabriel à versão antiga, como estão os outros personagens (Zane, Baltazar, Henrique, Carlos), que têm o visual do Blender.
**Afeta:** `assets/sprites/personagens/gabriel/` (todos os sprites e retratos, `visual.md`), `assets/modelagem/personagens/gerar_gabriel.py` (cabeçalho) e `pixelar_gabriel.py` (cabeçalho). Substitui a entrada de 2026-10-07 "Gabriel em pixel art desenhada" (que fica abaixo, como histórico). A Clarice continua em pixel art desenhada (#83).

## 2026-10-14 — As salas do Labirinto têm porta e não se vê o que há dentro de fora
**Decisão:** cada uma das 4 salas do Labirinto (a oficina do Zane e os 3 salões dos nós) ganha uma **porta na entrada**. Fechada, ela bloqueia o Gabriel e os robôs, a visão dos robôs e a luz. O Gabriel abre com `E`; um robô abre sozinho ao chegar nela; fecha sozinha 1,2 s depois que ninguém está perto. Enquanto a porta está fechada e o Gabriel está fora da sala, **tudo o que há dentro dela fica invisível** (props, luzes, nó, checkpoint, Zane, alçapão, peças do chão e os robôs que estiverem lá); as paredes continuam à vista. A animação é um **placeholder**: duas folhas de aço (retângulos coloridos) que recolhem para as bordas em 0,35 s, com lâmpada vermelha/verde e o som `porta_correr.wav`.
**Por quê:** pedido do Davi: dava para ver as salas de fora (luzes, hologramas, consoles) e não havia porta para entrar nelas.
**Afeta:** `scripts/sistemas/porta_da_sala.gd` e `cenas/sistemas/porta_da_sala.tscn` (novos); `scripts/salas/labirinto.gd` (`_colocar_portas`, `_guardar_na_sala`); `scripts/labirinto/mapa_labirinto.gd` (`salas`, `indice_da_sala`, `entrada_da_sala`); `dados/labirinto/mapa_labirinto.tres` e o gerador `gerar_labirinto.py` (campo `salas`); `docs/fases/labirinto.md` (seção 3). A arte final da porta (sprite) entra depois sem mudar o script.

## 2026-10-14 — Animação de abrir porta e som próprio no Bloco de salas
**Decisão:** a porta do Bloco de salas ganha animação de abrir e som próprio de porta pesada de aço com trinco eletromecânico (`cenas/cenario/bloco_de_salas/parede_porta_animada.tscn`), seguindo o padrão de uma porta animada por mapa da Biblioteca. A peça base de parede é `parede_porta_bloco.png` (80×112 px) e a folha animada (`porta_bloco_quadros.tres`, 80×88 px) roda a 36 fps, com a folha de aço com visor de vidro aramado correndo para o lado (deslizando para dentro do bolso de parede em trilho superior). O som ao atravessar passa a ser `porta_bloco.wav` (destrave de solenóide, desengate mecânico de aço, rolamento no trilho e descompressão do amortecedor pneumático).
**Por quê:** pedido do usuário a partir da arte e do sprite da porta de correr do bloco.
**Afeta:** `cenas/cenario/bloco_de_salas/parede_porta_animada.tscn`, `assets/sprites/cenario/bloco_de_salas/porta/`, `assets/modelagem/cenario/gerar_porta_bloco.py`, `assets/modelagem/audio/gerar_efeitos_porta_bloco.py`, `assets/audio/efeitos/objetos/porta_bloco.wav`, as 14 cenas de salas de `cenas/salas/bloco_de_salas/`, `docs/mecanicas/movimentacao_e_terreno.md` e `assets/audio/README.md`.

## 2026-10-14 — Tela de item novo: na primeira vez que pega um item, o jogo mostra a imagem detalhada dele
**Decisão:** na **primeira vez** que um item entra no inventário (uma vez por `id`, por jogo novo), o jogo pausa e mostra uma tela no estilo do Resident Evil: a **imagem detalhada** do item, o nome e a descrição. `E` ou `Esc` fecham (só depois de 0,45 s, para não fechar sem querer). Item sem imagem detalhada mostra o ícone ampliado, então todos os itens passam pela tela e a arte entra aos poucos. Vários itens pegos juntos entram numa fila. Pegar outra unidade de item que empilha (pedra, clarão) não abre a tela de novo. A tela é um autoload (`ItemNovo`), por isso nenhuma cena de fase foi alterada. No **inventário**, `E` com um item escolhido abre a mesma tela em modo **"Examinar"** (fundo opaco, `E` volta ao inventário), para rever o item quando quiser.
A imagem detalhada é a arte de "capa" do item, feita à parte (gerador de imagem) e mostrada como está, com filtro suave. O ícone de 16 × 16, o sprite do chão e a lanterna do peito continuam em pixel art pequena, desenhados a partir dela. A **lanterna foi refeita** para combinar com a imagem: carcaça verde-oliva, placa de aço azulada, botão vermelho e lente âmbar. Depois entraram as imagens do rádio (que passou a ser verde-oliva com detalhes laranja), da cápsula de clarão, do notebook, das chaves da manutenção, da fita azul e do depósito, do molho de chaves e do alicate, cada um com ícone e sprite do chão redesenhados a partir dela. Com a imagem do disquete da Clarice e da pedra, **todos os itens têm imagem detalhada**. A sala de teste ganhou um exemplar de cada item.
**Por quê:** pedido do Davi. O jogador vê o item de perto, com a descrição, no momento em que o pega, em vez de só ler "Você pegou: ..." no canto da tela.
**Afeta:** `scripts/sistemas/inventario.gd` (`vistos` e sinal `item_novo`), `scripts/itens/item.gd` (campo `imagem_detalhe`), `scripts/interface/tela_item_novo.gd` e `cenas/interface/tela_item_novo.tscn`, `project.godot` (autoload `ItemNovo`), `dados/itens/lanterna.tres`, `assets/sprites/itens/lanterna_detalhe.png`, `assets/modelagem/itens/preparar_detalhe.py`, `assets/modelagem/interface/gerar_interface.py`, `gerar_objetos_biblioteca.py` e `gerar_objetos_bloco_de_salas.py` (ícones e sprites do chão), `dados/itens/*.tres`, `scripts/interface/tela_inventario.gd` e `cenas/interface/tela_inventario.tscn` (Examinar), `cenas/salas/sala_teste.tscn`, `docs/mecanicas/itens_e_inventario.md`.

## 2026-10-14 — A lanterna aparece presa ao peito do Gabriel e o feixe sai da lente
**Decisão:** com a lanterna equipada, aparece no **peito** do Gabriel uma lanterna pequena e escura (5 × 3 px, `lanterna_peito.png`), girada para a direção da mira e espelhada quando ele olha para a esquerda. Nas vistas de costas ela fica escondida pelo corpo. O cone e o brilho nascem na **lente** dela, e não mais de um ponto fixo na altura do tronco. A sombra continua calculada a partir de um ponto no chão (como em `docs/fases/labirinto.md`, seção 4), só a textura da luz é que sai da lente. A primeira versão pôs a lanterna na mão (7 × 4 px) e foi trocada pelo peito, a pedido do Davi, por ficar grande demais e chamar atenção.
**Por quê:** pedido do Davi. A luz parecia sair da cintura, porque não havia lanterna desenhada e o ponto de origem ficava fixo no corpo. No peito ela fica mais discreta e não depende do balanço do braço.
**Afeta:** `scripts/itens/lanterna.gd`, `cenas/itens/lanterna.tscn`, `scripts/personagens/gabriel.gd` (`PEITO_NO_QUADRO` e `posicao_do_peito()`), `assets/sprites/itens/lanterna_peito.png`, `assets/modelagem/interface/gerar_interface.py`, `docs/mecanicas/iluminacao_e_lanterna.md`. O ícone do inventário (`lanterna.png`) e a lanterna no chão (`lanterna_chao.png`) foram redesenhados como a mesma peça pequena, com a alça de prender ao peito, e o texto de `dados/itens/lanterna.tres` deixou de dizer "de mão". Se o sprite do Gabriel mudar, os pontos do peito precisam ser conferidos.

## 2026-10-14 — A terceira fase é o Labirinto, com a oficina do Zane
**Decisão:**
- **A fase depois do Bloco de salas é o Labirinto** (já jogável), no lugar do Centro de Convivência. A ordem fica **Biblioteca → Bloco de salas → Labirinto**. Isso substitui a entrada de 2026-10-11 ("A fase depois do Bloco de salas é o Centro de Convivência"); o Centro fica sem lugar na ordem. O projeto detalhado do Centro e a Diana no Posto de Manutenção (#101) foram desfeitos (#102).
- **O Zane fica numa oficina no canto de baixo à esquerda do Labirinto**, cheia de componentes eletrônicos, desorganizada, com telas holográficas. O Gabriel não começa dentro dela: nasce perto, do lado de fora, a poucos passos da porta (5 salinhas de caminho, uns 13 s), e segue pelo corredor até lá. O Zane pede ajuda e entrega o **notebook** dele: Gabriel invade **três nós de controle**, em três salões espalhados pelo labirinto, e **volta ao Zane**, que tem uma segunda conversa com ele e mostra a saída: um **alçapão escondido sob uma lona**, na própria oficina. Descer pelo alçapão termina a fase.
- **O Labirinto foi ampliado com os mesmos sprites:** de 12 × 8 para 18 × 11 salinhas (1760 × 1088 px), com **6 robôs** (4 Sentinelas e 2 Rastreadores; eram 3), 5 pilhas, 16 lampiões (14 nos cruzamentos e 2 nas salas) e 4 salas (a oficina e os 3 salões dos nós), cada uma com uma entrada só. Não há mais porta de saída no mapa: a saída é o alçapão da oficina, que o Zane só revela depois dos 3 nós.
- **Escolhas de implementação, a confirmar:** os nós são terminais da trava do sistema do subsolo, que só lê de dentro; nos nós o notebook **não gasta bateria** (para a fase não travar por falta de carga) e a dificuldade do hack sobe do fácil ao difícil; a oficina é **segura** (a patrulha dos robôs não entra nela, mas eles entram se estiverem perseguindo o Gabriel); a oficina e cada salão de nó têm um checkpoint; o alçapão leva, provisoriamente, à entrada do Bunker.

**Por quê:** pedido do Davi.
**Afeta:** `docs/historia/História_Completa.md` (seções 6, 8, 12.3 e 12.5), `docs/historia/personagens/zane.md`, `docs/fases/labirinto.md`, `bloco_de_salas.md`, `bunker.md` e `centro_de_convivencia.md`, `docs/mecanicas/hackeamento.md` e `vida_e_checkpoint.md`; `cenas/salas/labirinto.tscn`, `bloco_de_salas/fim_do_bloco.tscn` e `menu_principal.tscn` (fases renumeradas: `02_blocos_de_aula` e `03_labirinto`); scripts `labirinto.gd`, `mapa_labirinto.gd`, `grade_labirinto.gd`, `notebook.gd`, `caixa_dialogo.gd` e os novos `no_hackeavel.gd`, `rede_do_labirinto.gd`, `alcapao.gd` e `zane_oficina.gd`; cenas novas `no_hackeavel`, `zane_na_oficina`, `alcapao` e `holograma_*`; diálogos `zane_labirinto_*.json` e a transmissão `zane_labirinto_01`; geradores `gerar_labirinto.py` e `gerar_oficina.py`.

## 2026-10-14 — Mensagens do HUD quebram em linhas e ficam mais tempo na tela
**Decisão:** a mensagem do topo da tela (pegar item, porta trancada, bilhetes e placas) passa a **quebrar em várias linhas** dentro da largura da tela, com 8 px de margem de cada lado, em vez de ficar numa linha só. O tempo na tela continua 3,5 s para textos curtos e cresce com o tamanho: 0,05 s por caractere (`segundos_por_caractere` no `hud.gd`), então um texto de 100 caracteres fica 5 s.
**Por quê:** textos longos (o maior, o mapa de giz da sala 103, tem mais de 250 caracteres) passavam das laterais da tela e eram cortados, e nem dava tempo de ler os que cabiam por pouco.
**Afeta:** `cenas/interface/hud.tscn` (nó `Mensagem`), `scripts/interface/hud.gd`.

## 2026-10-12 — Melhorias de level design do Bloco de salas implementadas
**Decisão:** as propostas da seção 12 de `docs/fases/bloco_de_salas.md` (PR #96) entram no jogo: a brecha 101 ↔ 102 e a porta de serviço 203 ↔ 206 (com o trinco do lado do depósito), os três setores de piso dos corredores com o **fator de piso** no alcance do som (areia/mato 0,5, lajota/tapete 1,0, lajota solta 1,5), dois **nichos** por corredor onde o Gabriel parado e sem luz não é visto, a **fresta da barricada** da 103 para espiar o corredor antes de sair, o **mapa de giz** da Clarice na lousa da 103, os **estalos** do teto do térreo, a **pedra pelo buraco** da 204 que leva o Rastreador para dentro da 104 por 18 s, a queda **amortecida** por caixas na 104, e a sala **205** limpa, com luz fluorescente estável e zumbido de 60 Hz.
**Por quê:** pedido do Davi, depois de mesclar o #96.
**Afeta:** `docs/fases/bloco_de_salas.md` (seções 9 e 12.8), `docs/mecanicas/furtividade_e_esconderijos.md`, `docs/mecanicas/movimentacao_e_terreno.md`, `docs/computacao/ia_e_perseguicao.md`; os scripts `porta.gd` (`espiar()` e `trinco_deste_lado`), `robo.gd`, `gabriel.gd` (`esconder()`), `pedra_arremessada.gd` e os novos `zona_de_piso.gd`, `nicho_esconderijo.gd`, `estalo_do_teto.gd`, `buraco_no_chao.gd`, `robo_atraido_pelo_buraco.gd` e `fresta_da_barricada.gd`; as cenas do bloco (corredores e salas 101, 102, 103, 104, 203, 204, 205 e 206); peças novas do kit (`gerar_kit.py`), `caixas_queda.png` e quatro sons novos.

## 2026-10-11 — O despertar (seg_acordar) vira vídeo, com a Biblioteca tecnológica de 3026
**Decisão:**
- A animação provisória da `seg_acordar`, feita no Blender, foi descartada. A cutscene agora é um **vídeo de 6 s com som** (`assets/video/cutscenes/seg_acordar.ogv`), convertido de `animação_gabriel_acordando.mp4` para Ogg Theora em 1280×720.
- **História:** no vídeo, a cabine e a biblioteca em volta têm a **tecnologia de 3026** (painéis com luz ciano, holograma sobre o caderno, torres de equipamentos). Saem da descrição desta cena no Enredo a luz do sol pelo teto quebrado, a árvore e as estantes caídas e vazias. A árvore e o acampamento do Baltazar no salão continuam como estavam no Ato 1. A pendência "Cenários mais futuristas" anota que a cabine já aparece assim.

**Por quê:** decisão do Davi.
**Afeta:** `docs/historia/História_Completa.md` (Ato 1, seção 12.5 e a tabela de cutscenes), `docs/historia/roteiro/cutscenes/seg_acordar.md` e `README.md`, `cenas/cutscenes/seg_acordar.tscn`, `assets/video/cutscenes/seg_acordar.ogv` (novo). Saíram `assets/sprites/cutscenes/seg_acordar/` e `assets/modelagem/cutscenes/seg_acordar/` (`gerar_seg_acordar.py` e o `.blend`); comentários de `gerar_menu.py` e `gerar_biblioteca.py` e a lista de scripts em `docs/visao_geral/estilo_artistico.md` foram ajustados.

## 2026-10-11 — A fase depois do Bloco de salas é o Centro de Convivência
**Decisão:** a fase que vem depois do **Bloco de salas** é o **Centro de Convivência**. Ele ainda não foi feito: por enquanto só o nome e a posição estão decididos. A ordem fica **Biblioteca → Bloco de salas → Centro de Convivência**. Isso substitui a entrada anterior de que a saída do Bloco de salas levava ao Bunker: o Bunker continua sendo o Ato 3 da história, mas a posição dele na ordem das fases deixa de estar decidida.
- **No jogo nada muda por enquanto:** a porta corta-fogo do Bloco de salas continua abrindo a entrada do Bunker, de forma provisória, até o Centro de Convivência existir.
- **Fica pendente:** o que acontece no Centro de Convivência, quem Gabriel encontra nele e o que ele ensina (Enredo, seções 8 e 12.5). O texto antigo dele no GDD é da premissa anterior (Calouros) e precisa ser refeito.

**Por quê:** decisão do Davi.
**Afeta:** `docs/historia/História_Completa.md` (seções 8, 12.5), `docs/fases/bloco_de_salas.md`, `bunker.md` e `README.md`, e o documento novo `docs/fases/centro_de_convivencia.md` (só o que está decidido e as perguntas em aberto).

## 2026-10-11 — O começo da história: a Clarice é a voz do rádio, o Henrique chegou primeiro e ajuda por trás
**Decisão:**
- **A Clarice é a voz do rádio na Biblioteca.** Ela ajuda Gabriel na primeira fase pelo rádio, com o que o Henrique vê nas câmeras. O Henrique deixa de ser a voz que guia Gabriel: ele ajuda a Clarice e a Diana, e o primeiro contato dele com Gabriel é em pessoa, no bunker.
- **A Clarice vai para a 103 e acolhe a Diana.** Depois de chegar à Biblioteca, a Clarice foi para o Bloco de salas e ficou na 103. A Diana apareceu por lá depois, e a Clarice a acolheu. Desde então as duas tentam descobrir o que aconteceu, com a ajuda do Henrique pelo rádio.
- **O Baltazar** está escondido numa sala da Biblioteca desde que chegou. A última página do diário combina com isso: a luz nasce no chão da Biblioteca.
- **O Henrique foi o primeiro a chegar.** Ordem fechada, menos o Baltazar: Henrique primeiro, Zane antes da Clarice, Diana depois da Clarice, Gabriel por último.
- **O Henrique diz que está escondido no bunker, tentando entender tudo, e que, de alguma forma, estamos em 3026.** É ele quem diz o ano ao grupo. Se é verdade o que ele conta do lugar e do ano ficou como pergunta nova da "mentira do Henrique" (Enredo, seção 12.7).
- No jogo: as transmissões da Biblioteca passaram do Henrique para a Clarice (`henrique_01` e `henrique_02` viraram `clarice_biblioteca_01` e `clarice_biblioteca_02`, com os gatilhos `GatilhoRadio1` e `GatilhoRadio2`), e o aviso de ronda do Bloco de salas passou a ser dela (`henrique_03` virou `clarice_04`). As conversas da Clarice no Bloco e a do Henrique no bunker foram ajustadas.

**Por quê:** história contada pelo Davi.
**Afeta:** `docs/historia/História_Completa.md` (seções 4.1, 6, 6.1, 7.2, 8, 10, 12.3 e 12.7), as fichas de Clarice, Henrique, Diana e Baltazar, `resumo.md`, `docs/fases/biblioteca.md` e `bloco_de_salas.md`, `docs/mecanicas/registros_e_caderno.md` e `README.md`, `dados/transmissoes/clarice_*.tres`, `dados/dialogos/clarice_bloco_*.json` e `henrique_primeiro_encontro.json`, e as cenas `balcao.tscn`, `acervo.tscn`, `salao.tscn` e `corredor_primeiro_andar.tscn`.

## 2026-10-11 — Sai a pendência "Quanto tempo Gabriel tem"
**Decisão:** o jogo **não tem prazo para o Gabriel**: não há contagem de dias nem relógio que o jogador sinta. Sai do Enredo Principal (seção 12.1) a pendência "Quanto tempo Gabriel tem", e sai de `outras_ideias.md` a ideia 5 ("Os pulsos como relógio"), que só existia para resolvê-la. A seção 3 (como a fenda age) não muda.
**Por quê:** pedido do Davi: não existe esse prazo.
**Afeta:** `docs/historia/História_Completa.md` (seção 12.1) e `docs/historia/outras_ideias.md` (índice e ideia 5).

## 2026-10-11 — A Diana fica na 103 com a Clarice, e as duas falam com o Henrique
**Decisão:**
- A **Clarice** veio da Biblioteca, como todos, e está na **sala 103** do Bloco de salas **desde que chegou**, tentando descobrir o que é este lugar.
- A **Diana** fica com ela na 103 (sai do bunker). As duas estão em contato com o **Henrique** pelo rádio, e a Clarice conta isso a Gabriel.
- No jogo: a conversa da troca do molho (`clarice_bloco_devolve_chave.json`) ganhou as falas sobre a Diana e o Henrique, a conversa de depois (`clarice_bloco_de_novo.json`) ganhou a escolha "O que vocês já descobriram?", e a despedida (`clarice_03.tres`) cita a Diana. A Diana ainda não tem visual, então a cena da 103 mostra só a Clarice.
- As falas da Clarice no Bloco de salas e as do Henrique no bunker passam a ser **definitivas** (deixam de ser rascunho).

**Por quê:** pedido do Davi.
**Afeta:** `docs/historia/História_Completa.md` (seções 6, 6.1, 8, 12.3 e 12.4), as fichas de Clarice, Diana, Henrique e Zane, `resumo.md`, `docs/fases/bloco_de_salas.md` (passo 6 e sala 103) e `bunker.md`, os diálogos e a transmissão citados acima.

## 2026-10-11 — A eletricidade funciona, e o Bloco de salas leva ao Bunker
**Decisão:**
- **A eletricidade funciona normalmente** no campus de 3026. Sai do Enredo a regra "quase nada elétrico funciona; só os sistemas da Âncora", e sai junto a pendência sobre quais sistemas são da Âncora e quais do Carlos. Onde algo está apagado numa fase (a grade da Biblioteca antes dos disjuntores), é um circuito desligado ou quebrado.
- **A porta corta-fogo do Bloco de salas leva ao Bunker**, a próxima fase. A tela de fim do bloco ("Você saiu do bloco") agora abre a entrada do Bunker em vez de voltar ao menu. A ordem fica Biblioteca → Bloco de salas → Bunker; o Labirinto e as outras áreas continuam sem lugar.
- **Sai a pendência dos tracinhos:** quem riscou as lousas e deixou o bilhete da 203 não precisa de resposta. O puzzle continua igual (738).

**Por quê:** pedido do Davi.
**Afeta:** `docs/historia/História_Completa.md` (seções 2.2, 8, 12.5 e 12.6), `docs/gdd.md` (item Iluminar), `docs/fases/bloco_de_salas.md`, `docs/fases/bunker.md`, `cenas/salas/bloco_de_salas/fim_do_bloco.tscn`.

## 2026-10-11 — O Henrique no lugar da Clarice na sala de dados do bunker
**Decisão:** na cena do bunker (`central_dados`), o **Henrique** substitui a Clarice na estação de trabalho. Ele aparece em pé, de costas, olhando as câmeras (`henrique_na_estacao.tscn`), e tem conversa própria: `henrique_primeiro_encontro.json` e `henrique_de_novo.json` (rascunho, para o roteiro revisar; no jeito dele: pausado, se corrigindo, fala pouco, e fica nervoso quando o assunto é a Âncora). A estação ganhou um sprite próprio, sem ninguém sentado, com as três telas mostrando câmeras (`estacao_dados.png`). As portas lacradas do setor B passam a dizer "O Zane está tentando abrir". O **Zane** ainda não tem cena no bunker.
**Por quê:** a Clarice foi para o Bloco de salas (entrada acima) e o Henrique passou para a sala de dados, com acesso às câmeras. O sprite da Clarice tinha a estação desenhada junto, então foi preciso desenhar a estação separada.
**Afeta:** `cenas/salas/bunker/central_dados.tscn` e `corredor_b.tscn`, `cenas/personagens/henrique_na_estacao.tscn`, `dados/dialogos/henrique_*.json`, `assets/sprites/cenario/objetos/estacao_dados.png` e `assets/modelagem/cenario/gerar_estacao_dados.py`, `docs/fases/bunker.md`, as fichas de Henrique, Clarice e Zane, Enredo Principal (seção 12.4). A cena `clarice.tscn` e as conversas `clarice_primeiro_encontro.json` e `clarice_de_novo.json` ficam sem uso.

## 2026-10-11 — O Rafael sai da história, e a Clarice ocupa o lugar dele no Bloco de salas
**Decisão:**
- **Sai o Rafael.** A ficha dele foi retirada de `personagens/` e o personagem some do Enredo Principal e das fases. O grupo passa a ter **6 puxados** (Gabriel, Baltazar, Diana, Clarice, Henrique e Zane), dentro da meta de 5 ou 6 da pendência de diminuir o elenco.
- **A Clarice fica no lugar dele no Bloco de salas.** Ela está na **sala 103**, atrás da barricada, e é a pessoa que Gabriel encontra em pessoa pela primeira vez: fala com ele pelo rádio e o ajuda a sair do bloco. A mecânica da fase não muda: o molho de chaves, a chave da fita azul, a sala segura e a despedida são os mesmos. Muda a voz: ela troca o molho pela chave como uma **permuta** (ela não pede ajuda, é o defeito dela) e explica as rondas como o grafo que mapeou (a parte "conhece as rondas e sabe o que cada chave abre", que era do Rafael, passa para ela).
- **O Baltazar** continua escondido na Biblioteca, numa sala que o jogador **ainda não consegue abrir** (a sala de obras raras, barrada por dentro, é a candidata).
- **O Henrique** deixa o "posto de monitoramento" e fica na **sala de dados do bunker**, junto do Zane, com acesso às **câmeras** do campus. Continua sendo a voz do rádio que guia Gabriel desde a Biblioteca.
- No jogo: as quatro conversas do posto e as três transmissões do bloco passaram do Rafael para a Clarice (`rafael_*` → `clarice_bloco_*` e `clarice_01` a `clarice_03`), com as falas reescritas no jeito dela. O item `molho_rafael` virou `molho_de_chaves`. A cena do posto é `clarice_posto.tscn`.
- **A arte do Rafael fica guardada** (sprites, gerador, `rafael.tscn` e a instância dele na sala de teste), sem uso nas fases. Dá para apagar depois, se o grupo quiser.

**Por quê:** pedido do Davi, para diminuir o grupo de personagens (pendência de 2026-10-08, opção de tirar o Rafael).
**Afeta:** `docs/historia/História_Completa.md` (seções 3.1, 4.2, 6, 6.1, 7.1, 8 e 12.3 a 12.4), as fichas de Clarice, Henrique, Baltazar, Diana e Zane, `resumo.md` e a ficha do Rafael (retirada), `docs/fases/bloco_de_salas.md`, `bunker.md` e `biblioteca.md`, `docs/gdd.md`, `docs/README.md`, `template_documento.md`, `CLAUDE.md`, `.claude/agents/roteirista.md`, `dados/dialogos/clarice_bloco_*.json`, `dados/transmissoes/clarice_01.tres` a `clarice_03.tres`, `dados/itens/molho_de_chaves.tres` e `chave_grade.tres`, os ícones `assets/sprites/itens/molho_de_chaves*.png` (e `assets/modelagem/cenario/gerar_objetos_bloco_de_salas.py`), `cenas/personagens/clarice_posto.tscn`, as cenas `sala_102`, `sala_103`, `corredor_terreo` e `corredor_primeiro_andar` do Bloco de salas, e `assets/sprites/personagens/README.md` e `rafael/visual.md` (arte guardada).

## 2026-10-11 — Bloco de salas jogável: o posto do Rafael (103) e a saída pela porta corta-fogo
**Decisão:** o Bloco de salas ganha objetivos e puzzles no estilo da Biblioteca (*Resident Evil*), conforme [`fases/bloco_de_salas.md`](fases/bloco_de_salas.md). O **posto de guarda do Rafael é a sala 103**, que é também a sala segura do bloco. O Gabriel liga o teste de alarme na 104 (a sirene do fim do corredor atrai o Rastreador), devolve ao Rafael o molho de chaves perdido na 102 e recebe a **chave da fita azul** (grade da escada). Daí em diante, a parte do Rafael ("sabe o que cada chave abre") chega **pelo que ele fala**, em pessoa e pelo rádio: **não existe livro de ocorrências**, nem no jogo nem na ficha. No 1º andar, o código do claviculário da 203 é a contagem de tracinhos das lousas da 101, 201 e 205 (**738**), a chave do depósito abre a 206 e o alicate corta a corrente da **porta corta-fogo**, a saída do bloco. Pegar o alicate muda a ronda da Sentinela; o buraco da 204 desce para a 104 (atalho de mão única). Quem riscou os tracinhos e quem deixou o bilhete do quadro de avisos fica em aberto. Para onde a porta corta-fogo leva depende da ordem das fases (pendente); por enquanto ela termina a fase.
**Por quê:** pedido do Davi: estruturar a fase com portas fechadas, chaves e puzzles, e tirar o livro de ocorrências, de que ele não gostou.
**Afeta:** Enredo Principal (Ato 2 e pendências), ficha do Rafael, `docs/fases/bloco_de_salas.md`, as cenas de `cenas/salas/bloco_de_salas/`, `cenas/personagens/rafael_posto.tscn`, `cenas/sistemas/sirene.tscn` e `terminal_alarme.tscn`, os scripts `sirene.gd`, `terminal_alarme.gd`, `conversa_com_troca.gd` e pequenos campos novos em `porta.gd`, `painel_codigo.gd`, `item_no_chao.gd`, `visivel_com_marca.gd`, `gatilho_transmissao.gd`, `inventario.gd`, `robo.gd` e `saida_fase.gd`, os itens, transmissões e diálogos novos em `dados/`, e a arte e os sons gerados por `gerar_objetos_bloco_de_salas.py`, `gerar_efeitos_bloco_de_salas.py` e `gerar_kit.py` (lousas com contagem).

## 2026-10-11 — Animação de abrir porta, uma por mapa
**Decisão:** a porta ganha animação de abrir, e cada mapa terá a sua, feita a partir de um vídeo. A da Biblioteca é uma porta de correr de madeira com batente de aço (`cenas/cenario/biblioteca/parede_porta_animada.tscn`). A folha é uma peça de parede animada que a `Porta` encontra sozinha pela posição, então as salas só trocam a peça do vão. O som de abrir também é por mapa: a porta de correr da Biblioteca toca `porta_correr.wav` (rodinhas e batida no batente), em vez do `porta_abrir.wav` de porta de dobradiça.
**Por quê:** pedido do Davi, com os vídeos de cada mapa.
**Afeta:** `scripts/sistemas/porta.gd`, `scripts/sistemas/folha_porta.gd`, `cenas/cenario/biblioteca/`, `assets/sprites/cenario/biblioteca/porta/`, `assets/modelagem/cenario/gerar_porta_biblioteca.py`, as 8 salas de `cenas/salas/biblioteca/`, `docs/mecanicas/movimentacao_e_terreno.md`.

## 2026-10-11 — Legenda própria para cutscenes
**Decisão:** falas e pensamentos dentro de cutscenes usam a **legenda de cutscene** (`cenas/interface/legenda_cutscene.tscn`), e não a caixa de diálogo das salas: uma faixa escura em degradê no pé da tela, com o texto centralizado, sem retrato, sem nome e sem escolhas. O jogador continua avançando com `E`.
**Por quê:** a caixa das salas, com moldura e foto de perfil, pesava sobre as ilustrações. Pedido do Davi.
**Afeta:** `cenas/interface/legenda_cutscene.tscn`, `scripts/interface/legenda_cutscene.gd`, `cenas/cutscenes/seg_prologo.tscn`, `docs/historia/roteiro/cutscenes/README.md`, `docs/dialogos/README.md`.

## 2026-10-11 — Ilustrações de cutscene em resolução dobrada
**Decisão:** as ilustrações das cutscenes são feitas em **640×360** e mostradas com **escala 0,5**, como os sprites dos personagens humanos (entrada de 2026-09-30). Ocupam a tela de 320×180 do mesmo jeito, mas, como o stretch é `canvas_items`, são desenhadas na resolução da janela, com o dobro de detalhe. A paleta de cada ilustração é fechada em 96 cores.
**Por quê:** em 320×180 as ilustrações do prólogo perdiam detalhe demais (rostos e roupas viravam borrões). Pedido do Davi.
**Afeta:** `assets/sprites/cutscenes/seg_prologo/`, `assets/modelagem/cutscenes/seg_prologo/pixelar_seg_prologo.py`, `cenas/cutscenes/seg_prologo.tscn` (escala 0,5 e o shader de falha com as medidas dobradas), `docs/historia/roteiro/cutscenes/README.md` e `seg_prologo.md`.

## 2026-10-11 — O anel da avó fica no dedo do Gabriel
**Decisão:** o Gabriel usa o anel da avó **no dedo**, e não na mochila, como já dizia o Enredo Principal ("gasto no [dedo] de Gabriel", seção 5). No prólogo, ele põe o anel no dedo antes de sair de casa. O anel continua aparecendo no inventário desde o começo.
**Por quê:** decisão do Davi, para acabar com a diferença entre a ficha do Gabriel e o Enredo.
**Afeta:** `docs/historia/personagens/gabriel.md` (seção 1), `docs/historia/roteiro/cutscenes/seg_prologo.md` (cena 2).

## 2026-10-08 — Cutscene de prólogo e organização de cutscenes
**Decisão:** criado o documento de roteiro e storyboard para a cutscene inicial de prólogo (`docs/historia/roteiro/cutscenes/seg_prologo.md`), composta por 8 ilustrações sequenciais em pixel art retratando o dia a dia de Gabriel em 2026 (acordando, o anel da avó, trajeto até a Unifor, aula de cálculo com o caderno de equações e o adormecer na cabine da Biblioteca de madrugada, terminando no pulso da fenda). O despertar em 3026 continua sendo a cutscene `seg_acordar`, que vem logo depois. A pasta de cutscenes foi organizada com uma ficha detalhada por cena e especificações técnicas de produção.
**Por quê:** dar contexto narrativo ao jogador antes do despertar nas ruínas e estabelecer o contraste dramático entre a normalidade de 2026 e o colapso de 3026.
**Afeta:** `docs/historia/roteiro/cutscenes/seg_prologo.md` (novo), `docs/historia/roteiro/cutscenes/README.md`, `docs/historia/História_Completa.md` (Ato 1).

## 2026-10-08 — Sistema de fadiga e estamina do Gabriel
**Decisão:** implementado o sistema modular de fadiga (`scripts/sistemas/fadiga.gd` e `cenas/sistemas/fadiga.tscn`). Correr consome estamina de forma contínua (~8s de corrida total). Ao zerar a estamina, Gabriel entra em estado de exaustão por 3 segundos, ficando impossibilitado de correr, andando a 40% da velocidade normal e emitindo o sinal `ofegante` com efeito sonoro. A estamina se regenera gradualmente (mais rápido parado do que andando). O HUD exibe uma barra discreta no canto superior que surge apenas durante o consumo e esmaece quando cheia.
**Por quê:** implementação da dinâmica de estamina e fuga descrita no GDD e nas mecânicas de movimentação.
**Afeta:** `scripts/sistemas/fadiga.gd`, `cenas/sistemas/fadiga.tscn`, `scripts/personagens/gabriel.gd`, `cenas/personagens/gabriel.tscn`, `scripts/interface/hud.gd`, `assets/audio/efeitos/gabriel/gabriel_ofegante.wav`.

## 2026-10-08 — O Zane no computador do bunker, e a nova ordem de chegada
**Decisão:**
- O **Zane** troca de lugar com a **Clarice**: fica no **computador da central de dados do bunker** e faz a **comunicação de todos** (mantém a frequência de rádio do grupo e liga pelos telefones velhos). Divide o bunker com a Diana. Onde a Clarice fica passa a ser pendente.
- **Ordem de chegada:** o Zane chega antes da Clarice, e **Gabriel é o último**. O Zane deixa de ser o último a chegar, e a cena de Gabriel recebendo o Zane sai.
- Sai a ideia de que o jogador acha que a Clarice morreu: o bilhete dela não é mais uma "despedida".
- No jogo: a ligação do fim da Biblioteca passou a ser do Zane (`clarice_01.tres` → `zane_01.tres`, em `cenas/sistemas/telefone.tscn`), e a anotação do bilhete da Clarice não diz mais que "parece que não voltou". A arte da estação de trabalho e as conversas do bunker continuam da Clarice e precisam ser refeitas para o Zane.

**Por quê:** decisão do Davi.
**Afeta:** `docs/historia/História_Completa.md` (seções 4.1, 6, 6.1, 7.2, 8, 10, 12.3 e 12.4), as fichas de Zane, Clarice, Diana, Henrique, Rafael e Gabriel, `resumo.md`, `docs/fases/biblioteca.md` e `bunker.md`, `docs/mecanicas/registros_e_caderno.md`, `docs/gdd.md`, `docs/README.md`, `outras_ideias.md` (ideia 14), `dados/transmissoes/zane_01.tres`, `dados/documentos/bilhete_clarice.tres`, `cenas/sistemas/telefone.tscn`, os `visual.md` do Zane e do Rafael e um comentário de `gerar_rafael.py`.

## 2026-10-08 — Onde cada personagem fica, e a frequência de rádio do grupo
**Decisão:**
- **Esconderijos:** **bunker** com a Clarice e a Diana (depois o Zane); o **Baltazar** escondido numa sala da Biblioteca, com medo; o **Rafael** numa sala de aula do Bloco de salas, que virou o "posto de guarda" dele; o **Henrique** sozinho num **posto de monitoramento**, com as câmeras do campus; o **Carlos** sempre no laboratório do D-Tec.
- **Comunicação:** a **Clarice** montou uma **frequência de rádio** para o grupo e deixou um rádio sintonizado nela no balcão da Biblioteca. O **Henrique** é a **voz do rádio**: vê o campus pelas câmeras, dá as dicas de patrulha e guia Gabriel desde a primeira fase, mas fala pouco e fica distante. O **Baltazar** teve dificuldade com o rádio, se isolou e não está na frequência.
- No jogo, as duas transmissões da Biblioteca passaram do Rafael para o Henrique (`rafael_0X.tres` → `henrique_0X.tres`, gatilhos `GatilhoHenrique1` e `GatilhoHenrique2`), com as falas reescritas no jeito dele. (Na entrada seguinte, quem mantém a frequência passou a ser o Zane.)
- Resolve a pendência de como a voz do rádio "parece ver" Gabriel: pelas câmeras.

**Por quê:** decisão do Davi. A voz que ajuda Gabriel desde o começo ser justamente a de quem mente deixa "A virada" mais forte.
**Afeta:** `docs/historia/História_Completa.md` (seções 6, 6.1, 8, 10 e 12.3), as fichas de Rafael, Henrique, Diana, Clarice, Baltazar, Zane e Carlos, `resumo.md`, `docs/fases/biblioteca.md`, `docs/mecanicas/registros_e_caderno.md` e `README.md`, `dados/transmissoes/henrique_01.tres` e `henrique_02.tres`, `cenas/salas/biblioteca/salao.tscn`, `balcao.tscn` e `acervo.tscn`, comentários de `gerar_efeitos_registros.py` e `gerar_interface.py`, `assets/sprites/personagens/rafael/visual.md`.

## 2026-10-08 — Sala de teste: escolher o personagem
**Decisão:** na **sala de teste** (e só nela), a tecla **C** troca o personagem que o jogador controla, em ciclo: Gabriel, Clarice, Zane, Baltazar, Rafael, Henrique e Carlos. O HUD mostra o nome ("Personagem: Clarice   [C] trocar"). A troca só muda os sprites: velocidade, corrida, itens e o resto do jogador continuam os do Gabriel. Começa no Gabriel. Ao sair da sala de teste, o jogador volta a ser o Gabriel.
**Por quê:** pedido do Davi, para testar a caminhada e as animações de qualquer personagem.
**Afeta:** `scripts/salas/escolha_personagem.gd` (novo), `cenas/salas/sala_teste.tscn` (nó `EscolhaPersonagem`; saiu a troca fixa para os sprites da Clarice).

## 2026-10-08 — Clarice em pixel art desenhada: retratos, frente, costas, lado e 3/4 de costas
**Decisão:**
- Os **retratos** e as vistas **de frente, de costas, de lado e de 3/4 de costas** da Clarice (parada, andando e respirando) passam a sair de artes de referência em pixel art, como o Gabriel: `assets/modelagem/personagens/clarice_referencia/` (`expressoes.png`, `andar_frente.webp`, `andar_costas.webp`, `andar_lado.webp`, `andar_diagonal.webp`) e o script `pixelar_clarice.py`, que usa as ferramentas do `pixelar_gabriel.py`.
- **Cinco retratos:** `normal` (neutro), `seria` (raiva), `triste`, `envergonhada` (vergonha) e `sorrindo` (feliz). `normal`, `seria` e `sorrindo` mantêm os nomes que os diálogos já usam.
- **Caminhada de frente e de costas:** só as quatro poses da fileira de baixo de cada referência (pé esquerdo à frente, passagem, pé direito à frente, passagem), três quadros cada, nos 12 quadros de sempre. Na fileira de cima o pé direito fica à frente nas quatro poses: tocadas em sequência, metade da caminhada ficava parada. A fileira de cima só dá a pose parada.
- **Caminhada de lado: boneco recortado.** Nas poses desenhadas os dois passos são o mesmo desenho (a mesma perna à frente, os braços no mesmo lugar), e ela parecia andar com uma perna só; a fileira para a esquerda tem o mesmo problema e o tronco mais virado para a câmera. A caminhada de lado é um boneco, como a do Gabriel, com as peças da pose DIR 1 (tronco, braço do lado da câmera e perna da frente; o outro braço e a outra perna são cópias mais escuras): coxa 22° · sen φ, joelho até 30° só na perna que vem no ar, braços 20° ao contrário das pernas. Os 12 quadros são todos diferentes. Para a esquerda o Godot espelha o sprite.
- **3/4 de costas:** as três poses de 3/4 de costas de `andar_diagonal.webp`, espelhadas (vêm andando para a esquerda). A passagem é a mesma nos dois passos.
- **Mais quadros no 3/4 de costas:** entre cada passo aberto e a passagem entram dois quadros gerados, com as pernas girando no quadril até 65% e 30% da abertura (o tênis acompanha sem girar, e o corpo sobe e desce).
- **Barra da jaqueta de lado:** de lado e no 3/4 o fim da jaqueta é medido pelo começo do jeans (a barra roxa quase não aparece no meio do corpo, e a conta de frente pegava a faixa do peito ou uma munhequeira).
- **Consistência entre as poses:** a jaqueta tem a mesma largura nas dezesseis poses, mas cabeça, tronco e pernas variavam de tamanho (até ~8%). Cada trecho do corpo é esticado para a média, todas as vistas usam a mesma paleta de 40 cores, as poses são alinhadas pela cabeça (de lado, pela ponta do rosto) e a cabeça da pose parada vai para todos os quadros da mesma vista.
- **Altura:** 95 px do alto do coque ao pé, pé na linha 106 e centro na coluna 47 (como o Gabriel); a cena `clarice_em_pe.tscn` não muda.
- **Visual das referências:** muda alguns detalhes do visual antigo: jeans escuro (era calça preta), tênis cinza-claro (era branco de lona), munhequeiras roxas, argolas douradas, mangas compridas (eram arregaçadas) e sem o fone laranja à vista.
- O **3/4 de frente** e a **estação de trabalho** continuam saindo do `gerar_clarice.py` (Blender), com o visual antigo, até ganharem referência. A fileira "FR" de `andar_diagonal.webp` é a mesma imagem da vista de lado (de perfil), por isso não foi usada.
- **Sala de teste:** o jogador pode virar qualquer personagem, só na `sala_teste.tscn` (ver a entrada "Sala de teste: escolher o personagem").

**Por quê:** pedido do Davi, para a Clarice chegar no nível de qualidade das referências e combinar com o Gabriel novo.
**Afeta:** `assets/sprites/personagens/clarice/` (retratos, `clarice_frente`, `clarice_costas`, as vistas `frente`, `costas`, `lado` e `tres_quartos_costas` (parada, andando e respirando), `clarice_referencia`; dois retratos novos), `assets/modelagem/personagens/pixelar_clarice.py` e `clarice_referencia/` (novos), `gerar_clarice.py` (aviso no cabeçalho), `assets/sprites/personagens/clarice/visual.md`, `cenas/salas/sala_teste.tscn`. A ficha `docs/historia/personagens/clarice.md` ainda cita o fone de walkman laranja.

## 2026-10-08 — Resumo dos personagens
**Decisão:** a pasta `docs/historia/personagens/` ganha o `resumo.md`, com todos os personagens numa página (quem é, época, frase de essência, cor, esconderijo, parte para consertar a Âncora, relações e principais pendências). É a exceção à regra de "só as fichas" nessa pasta (entrada de 2026-10-07). O resumo não é lei: se ele e uma ficha discordarem, vale a ficha.
**Por quê:** pedido do Davi.
**Afeta:** `docs/historia/personagens/resumo.md` (novo), `docs/README.md`, `docs/historia/README.md`. Quem mudar uma ficha deve conferir se o resumo continua certo.

## 2026-10-08 — A Biblioteca implementada em várias salas
**Decisão:** o planejamento da Biblioteca (`docs/fases/biblioteca.md`) entrou no jogo. A cena única virou oito salas em `cenas/salas/biblioteca/`, e o jogo começa na cabine. Entraram: o autoload `Progresso` (as marcas da fase), portas com chave e com marca, a chave da manutenção, o quadro de energia (ordem 3, 1, 4, 2), as luzes de emergência que acendem e revelam o Gabriel para os robôs, o terminal com o disquete da Clarice (código 0394), o painel e a grade da ala leste, o telefone com a primeira ligação da Clarice, a porta barrada das obras raras e os robôs (Sentinela no salão, Rastreador no acervo) com rota fixa, rota nova depois da energia e bipe antes de virar.
**Por quê:** pedido do Davi: implementar tudo o que o planejamento descreve.
**Afeta:** `project.godot` (autoload `Progresso`), `scripts/sistemas/porta.gd`, `scripts/personagens/robo.gd`, `scripts/salas/sala.gd` (os limites automáticos também barram robôs), `scripts/itens/notebook.gd`, `scripts/menu_principal.gd`, `cenas/cutscenes/seg_acordar.tscn` e `dados/fases/01_biblioteca.tres` (começam na cabine). Os textos da ligação e do disquete são rascunho para o roteiro revisar.

## 2026-10-07 — Fase DTEC (laboratório), solta
**Decisão:** nova fase **DTEC**, o departamento de tecnologia: recepção, dois corredores e 8 salas (eletrônica, informática, servidores, química, robótica, controle e o Lab Central). No **meio do mapa**, o Lab Central tem uma **máquina grande e brilhante** (anel em pé com núcleo ciano que pulsa). Duas salas são **trancadas** e abrem com o hack do notebook (Servidores e Robótica); cinco portas ficam **lacradas** para depois. A fase é **solta**: não se chega a ela pelos mapas atuais, aparece só no menu Fases e **não tem lugar na história**. A máquina não tem nome nem papel (não é a Âncora). Sem robôs por enquanto.
**Por quê:** pedido do Davi: um mapa de laboratório grande e detalhado, com salas trancadas e uma máquina no centro.
**Afeta:** `cenas/salas/dtec/` e `cenas/cenario/dtec/` (novos), `assets/modelagem/cenario/gerar_dtec.py` e `assets/modelagem/salas/dtec/montar_dtec.py` (novos), `cenas/cenario/luzes/luz_maquina.tscn` e `scripts/cenario/luz_pulsante.gd` (novos), `dados/fases/09_dtec.tres` e `cenas/menu_principal.tscn` (menu Fases), `docs/fases/dtec.md`.

## 2026-10-07 — Gabriel em pixel art desenhada (a partir de referências)
**Decisão:**
- Os sprites do Gabriel deixam de sair do modelo 3D do Blender e passam a sair de **artes de referência em pixel art** (parado de frente e de costas, de lado e cinco expressões), guardadas em `assets/modelagem/personagens/gabriel_referencia/`. O script `pixelar_gabriel.py` (só Python, Pillow e NumPy) recorta, reduz para 99 px de altura, fecha a paleta em 40 cores e refaz o contorno.
- **Parado de frente e de costas:** saem de uma referência própria (`parado.png`). Os tons de cabelo e de calça do Gabriel parado de frente são o molde para repintar as outras poses.
- O que a referência não tem sai das vistas que ela tem: a **caminhada de lado** é um boneco recortado (braço, coxa, canela e pé girando nas juntas); a respiração sobe o peito e a cabeça.
- **Diagonal (3/4 e 3/4 de costas):** a cabeça, o tronco e os braços saem de uma referência própria do Gabriel dando um passo (`andar_diagonal.webp`); os braços giram no ombro. As **pernas são as mesmas peças da vista de lado** (coxa, canela e tênis), presas nos dois quadris da pose, com 60% do balanço de lado e o pé da frente 3 px mais baixo na tela (mais alto no 3/4 de costas): as pernas da pose vinham dobradas e, giradas, ficavam tortas e se cruzavam. A cabeça da pose também saiu grande e é encolhida para 87%, como a de lado. O 3/4 parado é esse boneco com os membros retos. Na referência o braço que vai à frente é o do mesmo lado da perna que avança; no jogo, cada braço balança ao contrário da sua perna. O cabelo da pose de frente saiu loiro e foi repintado com o castanho dele.
- **Cabeça de lado:** na referência de lado a cabeça saiu maior que na de frente (21 px do cabelo ao queixo, contra 18). O script encolhe a cabeça do perfil para 85%, presa no pescoço, e o corpo cresce um pouco para a altura total continuar 99 px.
- **Braços sempre mexendo:** em todas as caminhadas os braços balançam ao contrário das pernas.
- **Andando de frente e de costas:** saem de duas referências com quatro poses cada (`andar_frente.webp` e `andar_costas.webp`): pé no chão, passando, o outro pé no chão, passando. Cada pose dura 3 dos 12 quadros, centrada pelo peito, com o sobe e desce do desenho. Nas poses de frente a cabeça e o peito saíram maiores: o corpo estreita para 92% e a cabeça encolhe (85% na altura, 95% na largura). O cabelo (loiro nas poses de frente) e a calça (acinzentada nas de costas) são repintados com os tons do Gabriel parado, casando claro com claro.
- Mesmos nomes, tamanhos e quantidade de quadros de antes (96 × 112, 12 quadros andando, 8 respirando): a cena `gabriel.tscn` não muda.
- **Sem mochila**, como na referência: moletom vermelho de capuz, calça jeans e tênis cinza.
- **Retratos:** cinco em vez de três: `normal`, `preocupado` e `surpreso` (os nomes que os diálogos já usam) e os novos `bravo` e `envergonhado`.
- O `gerar_gabriel.py` e o `gabriel.blend` ficam como modelo 3D, mas **não devem ser rodados** para gerar os sprites do jogo: sobrescreveriam os novos.

**Por quê:** pedido do Davi, para o Gabriel chegar no nível de qualidade das referências.
**Afeta:** `assets/sprites/personagens/gabriel/` (todos os sprites e retratos, dois retratos novos), `assets/modelagem/personagens/pixelar_gabriel.py` e `gabriel_referencia/` (novos, com `andar_diagonal.webp`), `gerar_gabriel.py` (aviso no cabeçalho), `assets/sprites/personagens/gabriel/visual.md`. Os outros personagens continuam com os sprites do Blender, e ficam com um visual diferente do Gabriel até ganharem referências também.

## 2026-10-07 — Planejamento da Biblioteca no estilo Resident Evil
**Decisão:** a Biblioteca passa a ser planejada como uma fase de **salas ligadas por portas trancadas**, no estilo *Resident Evil*: cabine, salão principal (o centro), balcão, acervo sul, sala de manutenção (sala segura), sala de terminais, ala leste e uma sala de obras raras que só abre mais tarde. Para sair, o jogador busca a chave da manutenção no acervo, religa a energia, lê o código da grade no disquete da Clarice, abre a grade da ala leste e atende a primeira ligação da Clarice, que destranca a porta de saída. A Sentinela fica no salão e o Rastreador no acervo; com a energia, as luzes acendem e a rota da Sentinela muda. O mezanino, cogitado, foi descartado.
**Por quê:** pedido do Davi: uma fase com mais caminhos e cadeados, em vez de um salão só.
**Afeta:** `docs/fases/biblioteca.md` (reescrito). Para implementar: dividir `cenas/salas/biblioteca.tscn` em salas, chave como item, quadro de energia, painel de código e grade, luzes que acendem, telefone, disquete da Clarice e os dois robôs.

## 2026-10-07 — Visual do Henrique e do Carlos
**Decisão:**
- **Henrique:** camisa de flanela xadrez laranja-queimado aberta sobre camiseta cinza, jeans preto, tênis de lona, óculos redondos de aro fino, cabelo bagunçado na testa, o caderno sempre na mão e um lápis atrás da orelha. Postura fechada, cabeça baixa, passo curto. **Cor de identificação: laranja-queimado.**
- **Carlos**, o "cientista maluco": **mais velho que o grupo** (a idade exata continua pendente), careca no alto e cabelo grisalho arrepiado, jaleco sujo até o joelho e luvas pretas; por baixo, a roupa dos **anos 80** que ele idealiza (camiseta estampada colorida, jeans lavado, tênis branco de cano alto, relógio-calculadora, óculos grandes). Uma lupa com lente vermelha nos óculos e um controle com luz vermelha no cinto, o mesmo vermelho dos olhos dos robôs que ele controla. Postura curvada, cabeça esticada. **Cor de identificação: o branco do jaleco.** A aparência sai das pendências do Enredo (12.2); a idade exata fica.
- Os dois têm o mesmo conjunto de sprites do Gabriel (cinco vistas em 96 × 112, caminhada, respiração e três retratos) e estão na sala de teste, ao lado dos outros.

**Por quê:** pedido do Davi: os modelos do Henrique e do "cientista maluco que é o Carlos".
**Afeta:** `docs/historia/personagens/henrique.md` e `carlos.md` (direção de arte e arquivos), `docs/historia/História_Completa.md` (pendência 12.2), `assets/modelagem/personagens/` (`gerar_henrique.py`, `gerar_carlos.py`), `assets/sprites/personagens/henrique/` e `carlos/`, `cenas/personagens/henrique.tscn` e `carlos.tscn`, `cenas/salas/sala_teste.tscn`, `CLAUDE.md`.

## 2026-10-07 — O Carlos é o antagonista (ideia 23), o pesquisador é o Henrique
**Decisão:**
- **Ideia 23 aprovada, com partes ainda em aberto.** O antagonista é o **Carlos**, cientista de 3026 que criou a Âncora. Na época dele, a sociedade e o planeta estavam muito ruins, e o pouco que sobrou da humanidade foi para outro planeta. Ele ficou, por um objetivo egoísta: é obcecado pelos **anos 80** e quer usar a Âncora para ir viver lá. A Âncora é imprecisa: cada tentativa dele abre a fenda no chão da Biblioteca e puxa gente por acaso. Ele controla os robôs. A **Âncora** e o laboratório dele ficam no **D-Tec**, a parte de tecnologia da Unifor, no **Bloco M**. O **Bloco J foi descartado**.
- Em aberto, nas pendências do Enredo (12.2): como ele consegue o conhecimento (consciências roubadas, super IA ou as duas), se a IA continua existindo, por que os robôs caçam, e o resto da ficha dele.
- **Ideia 13 aprovada:** o pesquisador de 2019 se chama **Henrique**. A ficha virou `henrique.md`.
- **O Henrique engana o grupo**: esconde a ligação que tem com o Carlos (trabalha para ele ou foi enganado por ele, pendente). Quando o grupo descobre a mentira, todos vão atrás do Carlos. Isso resolve a pendência "Algum personagem atrapalha?" e entra no Enredo como "A virada", antes do Ato 4.
- **Ideias 20, 21 e 22 descartadas** (o pesquisador mentiu, o cientista que morreu, o drone).

**Por quê:** decisão do Davi.
**Afeta:** `docs/historia/História_Completa.md` (seções 1, 2, 3, 4, 6, 7, 8, 11 e 12), a ficha nova `docs/historia/personagens/carlos.md`, `pesquisador.md` → `henrique.md`, as fichas de Clarice, Zane, Gabriel e robôs, `docs/historia/outras_ideias.md`, `docs/historia/template_documento.md`, `docs/README.md`, `docs/gdd.md`, `CLAUDE.md` e o agente `roteirista`.

## 2026-10-07 — Visual do Baltazar e do Rafael, com os sprites do Gabriel
**Decisão:**
- **Baltazar:** tricórnio de feltro, cabelo comprido preso com fita, casaca **vinho** aberta até a coxa (gasta, com remendo) e canhões largos, colete marrom com botões de latão, camisa de linho, calções, meias e sapato de fivela; a **luneta** de latão numa bandoleira de couro e o **anel** de ouro na mão direita. **Cor de identificação: vinho**, o tom do pau-brasil, um eco escuro do vermelho do Gabriel (a mesma família). Postura cerimoniosa e curiosa, passo curto.
- **Rafael:** uniforme de vigilante de 2008 **grande para ele**: camisa de manga curta **azul-celeste** com dragonas e bolsos azul-marinho, emblema amarelo na manga e no boné, crachá, calça azul-marinho e coturno; bigodinho ralo para parecer mais velho; **rádio HT** e lanterna antiga no cinto. **Cor de identificação: azul-celeste.** Peito estufado, passo de ronda.
- Os dois têm o **mesmo conjunto de sprites do Gabriel**: cinco vistas em 96 × 112, caminhada (12 quadros) e respiração (8 quadros) em cada vista, e três retratos de 80 × 80 (Baltazar: normal, encantado, aflito; Rafael: normal, rindo, triste).
- O roteiro de um personagem em pé (renderizar, juntar a paleta e gravar) virou `comum.gerar_em_pe`. O Zane passou a usar e saiu idêntico.

**Por quê:** pedido do Davi. O visual segue a direção de arte das fichas: o Baltazar "rapaz do século XVIII, de sítio, roupa gasta, luneta e anel visíveis"; o Rafael "uniforme de 2008 um pouco largo, tentando parecer mais velho, rádio e lanterna no cinto".
**Afeta:** `assets/modelagem/personagens/` (`comum.py`, `gerar_zane.py`, `gerar_baltazar.py` e `gerar_rafael.py` novos), `assets/sprites/personagens/baltazar/` e `rafael/` (novos), as fichas `baltazar.md` e `rafael.md` (direção de arte e arquivos), `CLAUDE.md`. Ainda não há cena de nenhum dos dois.

## 2026-10-07 — Visual do Zane, e Clarice e Zane com os sprites do Gabriel
**Decisão:**
- **Visual do Zane:** braço direito de prótese de metal com linhas de luz ciano, olho direito de implante, placa na têmpora e porta na nuca; jaqueta técnica curta **amarelo-ácido** com painéis grafite, zíper na diagonal e gola alta, com a manga do braço de metal cortada no ombro; camiseta preta comprida, calça larga com tiras, botas de sola branca grossa com friso de luz; cabelo raspado dos lados com o topo descolorido num topete. Postura confiante: peito aberto, queixo erguido, passo largo. **Cor de identificação: amarelo-ácido** (Gabriel vermelho, Clarice verde-azulado). O ciano dos implantes é o mesmo da interface holográfica dos áudios dele.
- **Clarice e Zane têm o mesmo conjunto de sprites do Gabriel**, nos mesmos tamanhos: cinco vistas em pé (lado, frente, 3/4, costas, 3/4 de costas) em 96 × 112, a caminhada (12 quadros) e a respiração (8 quadros) em cada vista, e três retratos de 80 × 80. A Clarice continua com os sprites sentados na estação do bunker.
- A caminhada, a respiração e o retrato passaram para o `comum.py`, usados pelos três. Os sprites do Gabriel e os sprites antigos da Clarice saíram idênticos.

**Por quê:** pedido do Davi: os dois personagens com todas as dimensões do Gabriel. O visual do Zane segue a direção de arte da ficha dele (implantes visíveis, roupa de um futuro que ninguém reconhece, destoar de todos).
**Afeta:** `assets/modelagem/personagens/` (`comum.py`, `gerar_gabriel.py`, `gerar_clarice.py`, `gerar_zane.py` novo), `assets/sprites/personagens/clarice/` e `zane/` (novo), `docs/historia/personagens/zane.md` (direção de arte e arquivos). Ainda não há cena do Zane nem da Clarice andando no Godot.

## 2026-10-07 — Ideias 6, 7 e 15 aprovadas: o Zane fica, o Baltazar volta e os esconderijos
**Decisão:**
- **Ideia 6:** no fim, **o Zane escolhe ficar em 3026** para tentar domar a IA por dentro, em vez de voltar para 2123.
- **Ideia 7:** **o Baltazar quer ficar em 3026, mas precisa voltar**, ou a família de Gabriel não existe. Gabriel tem que convencê-lo.
- **Ideia 15, com ajustes do Davi:** o **bunker** fica com a Clarice e o pesquisador (e depois o Zane); o **posto de guarda** fica com o Rafael; o **Baltazar** tem um esconderijo **dentro da Biblioteca** (no lugar do terraço da ideia original); a **Diana** fica numa das **salas de aula do Bloco de salas** (no lugar do posto de guarda da ideia original).

**Por quê:** aprovação do Davi das ideias 6, 7 e 15 de `docs/historia/outras_ideias.md`.
**Afeta:** `docs/historia/História_Completa.md` (seções 5, 6, Atos 2 e 4 e pendências 12.1 e 12.3), as fichas de Baltazar, Zane, Gabriel, Clarice, pesquisador, Rafael e Diana, `docs/fases/bloco_de_salas.md`, e `docs/historia/outras_ideias.md` (as três ideias saíram).

## 2026-10-07 — A Âncora fica no Bloco J, e cada personagem tem a sua ficha completa
**Decisão:**
- A **Âncora** está no **Bloco J**, o bloco de tecnologia da Unifor. A fenda continua se abrindo no chão da Biblioteca.
- A descrição dos personagens (história, personalidade e relações) **saiu do Enredo Principal** e foi para as fichas em `docs/historia/personagens/`, **uma por personagem**. As fichas fazem parte do Enredo Principal e têm a mesma autoridade. O Enredo, na seção 4, ficou só com as regras do grupo, a lista de fichas e a IA.
- A pasta `personagens/` tem **só as fichas** (mais a dos robôs). O índice dela saiu, e o modelo de ficha foi para `docs/historia/template_personagem.md`.

**Por quê:** pedido do Davi.
**Afeta:** `docs/historia/História_Completa.md` (seções 1, 2.2, 3, 4 e 7.2), as fichas de `docs/historia/personagens/`, `docs/historia/template_personagem.md`, `CLAUDE.md`, `docs/README.md`, `docs/gdd.md`, `docs/historia/README.md`, `docs/historia/roteiro/README.md`, `docs/historia/template_documento.md`, `docs/dialogos/template_dialogo.md`, os agentes `roteirista` e `artista`, `clarice/visual.md` e `gerar_clarice.py`.

## 2026-10-07 — Personagens e roteiro dentro de `docs/historia/`, uma ficha por personagem
**Decisão:**
- As pastas `docs/personagens/` e `docs/roteiro/` passam a ficar dentro de `docs/historia/`, junto do Enredo Principal.
- `antecessores.md` (versão antiga, com loops e personagens mortos) foi apagado. No lugar, **uma ficha por personagem**: `gabriel.md`, `baltazar.md`, `diana.md`, `clarice.md`, `rafael.md`, `pesquisador.md` e `zane.md`, além de `robos.md`.
- As fichas **não repetem a personalidade**, que fica só no Enredo Principal (a lei do projeto). Guardam o que a produção precisa: onde o personagem aparece, como chega ao jogador, função no jogo, parte para consertar a Âncora, suporte dos registros, direção de arte, arquivos e pendências. O `template_personagem.md` segue esse formato.
- `revelacao_central.md` (a história antiga, com loops) foi **apagado**; o texto continua no histórico do git. O `docs/historia/README.md` virou um índice curto que manda começar pelo Enredo Principal, sem repetir nada dele. O `template_documento.md` foi refeito com os campos reais do recurso `Documento` (`id`, `titulo`, `autor`, `papel`, `paginas`, `anotacao`), o papel de cada época e os limites de texto.

**Por quê:** pedido do Davi: deixar as fichas de personagem congruentes com o Enredo Principal e perto dele.
**Afeta:** `docs/historia/personagens/` e `docs/historia/roteiro/` (movidos), todos os links para as pastas antigas (docs, agentes, `CLAUDE.md`, `CONTRIBUTING.md`, `README.md`, comentários dos geradores em `assets/modelagem/`), `assets/sprites/personagens/clarice/visual.md` (dias no bunker, sem loops), `docs/mecanicas/registros_e_caderno.md` (sem os bilhetes de "G."), `docs/historia/README.md`, `docs/historia/template_documento.md` e `docs/historia/revelacao_central.md` (apagado).

## 2026-10-07 — Menu principal com a arte nova (imagem única)
**Decisão:** o menu principal troca a cena renderizada no Blender (três camadas) por **uma imagem só**, a partir da imagem de referência enviada pelo Davi: estante com livros e papéis, relógio, monitor CRT bege com o bilhete, luminária apagada, teclado, pilha de livros e caneca de café. O texto que vinha pintado na tela do monitor foi apagado por `assets/modelagem/menu/preparar_menu.py`, e o Godot desenha o menu por cima, nas mesmas posições e cores da imagem: título "ANKHOR" em 16 com brilho, itens em 8 a cada 14 px, barra azul de seleção de ponta a ponta do vidro. As telas de Fases, Opções e Controles usam o mesmo vidro. A luminária da imagem está apagada, então a piscada da luminária saiu; ficaram a tremulação do brilho da tela, o efeito CRT (mais leve, porque a imagem já tem linhas) e a vinheta escura nas bordas.
**Por quê:** pedido do Davi: trocar completamente a tela de menu pela imagem de referência.
**Afeta:** `assets/sprites/menu/menu_cena.png` (novo; saíram `menu_fundo`, `menu_mesa` e `menu_frente`), `assets/modelagem/menu/preparar_menu.py` e `menu_referencia.webp` (novos), `cenas/menu_principal.tscn` (o nó `Mesa` virou `Monitor`), `scripts/menu_principal.gd`. O `gerar_menu.py` fica, porque a cutscene `seg_acordar` reaproveita a cabine.

## 2026-10-06 — Enredo Principal vira a lei do projeto, personalidades, Diana e Rafael
**Decisão:**
- O **Enredo Principal** (`docs/historia/História_Completa.md`) passa a ser a **lei do projeto** para história, mundo e personagens, acima de qualquer outro documento, inclusive deste registro. Em caso de dúvida em qualquer parte do jogo, vale o que ele diz. Mudanças de história entram no mesmo PR nele e aqui.
- **O policial de 1978 (Agostinho) vira mulher e se chama Diana**: recruta da polícia, dramática, ansiosa e impulsiva. **Valdir passa a se chamar Rafael** ("Seu Rafael").
- **Zane é homem**, e o defeito dele é confiar demais na tecnologia (a impulsividade ficou só com a Diana).
- **Gabriel é irônico**, de ironia seca, e é isso que combina com o sarcasmo da Clarice: os dois se provocam no mesmo tom.
- **Ordem de chegada:** o Zane é o último a chegar e Gabriel é o penúltimo. A fenda pulsa durante o jogo, e Gabriel recebe o Zane. A ordem dos outros cinco está pendente.
- Cada personagem ganhou uma **ficha de personalidade** (essência, traços, como fala, o que quer, o que teme, defeito e arco) e o grupo ganhou um quadro de relações entre eles.

**Por quê:** decisão do Davi: um documento único e profissional para consultar em caso de dúvida, e nomes e personalidades definidos antes de escrever falas e desenhar os personagens.
**Afeta:** `docs/historia/História_Completa.md`, `CLAUDE.md`, `docs/README.md`, `docs/gdd.md`, `docs/historia/README.md`, `docs/personagens/README.md`, os agentes `roteirista`, `artista` e `sistemas`. As transmissões do rádio viraram `dados/transmissoes/rafael_01.tres` e `rafael_02.tres` (com "Aqui é o Seu Rafael"), e os gatilhos em `cenas/salas/biblioteca.tscn` viraram `GatilhoRafael1` e `GatilhoRafael2`. Comentários dos geradores de áudio e interface, `assets/audio/README.md`, `docs/fases/biblioteca.md` e `docs/mecanicas/` também. `revelacao_central.md` e `antecessores.md` continuam com a versão antiga, marcados como fora de uso.

## 2026-10-06 — Nova linha da história: a fenda é um acaso
**Decisão:**
- **Saem** os loops, os bilhetes de "G.", a Clarice como "a única que lembra" e a revelação de que Gabriel é o paradoxo da Âncora. Também foi descartada a ideia de a fenda ser um teste.
- **A fenda é um acaso.** A Âncora é **só uma máquina**: abandonada, falhou em 3026 e abriu uma fenda no chão da Biblioteca que pulsa e puxa, a cada poucos dias, quem estiver no ponto em alguma época. Os personagens precisam descobrir o que aconteceu e como voltar, e cada um traz uma parte para consertar a Âncora.
- **3026:** a humanidade abandonou a Terra e uma **IA** dominou. A IA não tem rosto. Para ela, humanos são invasores, e por isso os robôs atacam. Ser pego dá game over e volta ao checkpoint.
- **Personagens:** todos com **cerca de 20 anos**, todos com ligação com a região da Unifor, todos **vivos**, puxados com dias de diferença. Gabriel encontra cada um ao longo do jogo. Cada um tem um esconderijo, e um lugar como o bunker pode abrigar 2 ou 3. O personagem de **2041 foi cortado**. O professor de 2019 vira um aluno de iniciação científica (nome em aberto). Agostinho vira recruta da polícia, e Valdir, um segurança jovem.
- **Família Magalhães:** Gabriel se chama **Gabriel Magalhães**, e o **Baltazar** é antepassado dele. Gabriel descobre isso jogando, por um **anel desgastado** da avó que está no inventário desde o começo, igual ao do Baltazar. Gabriel conta para o Baltazar.
- **Clarice:** a relação dela com Gabriel vai sendo desenvolvida ao longo do jogo. O final dos dois está em aberto.
- **Pendentes:** o objetivo da IA; quem criou a Âncora (talvez um descendente de Gabriel); Gabriel falhando na tela enquanto o Baltazar estiver fora de 1750; prazo da fenda; como cada um volta; se alguém escolhe ficar; se algum personagem atrapalha; o nome do pesquisador.

**Por quê:** decisão do Davi: uma história mais simples e humana, com personagens vivos para interagir ao longo do jogo.
**Afeta:** `docs/historia/História_Completa.md` (reescrito, com as pendências no fim). Ainda descrevem a versão antiga e precisam ser revistos: `docs/historia/revelacao_central.md`, `docs/personagens/antecessores.md`, `docs/mecanicas/sono_e_sonhos.md`, `docs/gdd.md`, `CLAUDE.md` (premissa) e as falas de loop em `dados/dialogos/clarice_primeiro_encontro.json`.

## 2026-10-06 — Menu principal mais claro, com a luminária acesa
**Decisão:** a cena do menu continua sendo a cabine de estudo da Biblioteca à noite, mas fica mais clara e legível: a **luminária de mesa está acesa** (luz quente no canto direito da mesa), tem uma caneca de café, uma pilha de livros maior à esquerda e a estante aparece melhor, com papéis largados nas prateleiras. O monitor está gasto: rachaduras na moldura, LED verde de ligado aceso, e teclas amareladas, afundadas ou faltando. A tela do monitor ganhou fundo com um leve clarão no centro, título com brilho, barra de seleção na largura toda da tela e, no efeito CRT, cantos arredondados e uma faixa clara que desce devagar. As bordas da cena escurecem com a mesma vinheta pixelada das salas, e a luz da luminária na mesa oscila de leve e de vez em quando falha por um instante, como lâmpada velha: na falha, a mesa fica mais escura que o normal. O cenário não se mexe mais com o mouse (a paralaxe saiu, e `scripts/camada_paralaxe.gd` foi apagado). O retângulo da tela não mudou (x 90–230, y 24–126).
**Por quê:** pedido do Davi, a partir de uma imagem de referência; o menu antigo era escuro demais e quase não se via a cena.
**Afeta:** `assets/modelagem/menu/gerar_menu.py` (e os PNGs de `assets/sprites/menu/`), `cenas/menu_principal.tscn`, `scripts/menu_principal.gd`, `shaders/tela_crt.gdshader`.

## 2026-10-02 — Trilha própria do Bunker
**Decisão:** o Bunker ganha uma trilha própria, mais escura que a da Biblioteca: Dó frígio, sem andamento, com o Dó grave "respirando", cordas graves, aço gemendo, um baque distante lá em cima e, na segunda metade, a fita da Clarice (quatro notas de piano elétrico gasto). Toca em todas as salas do bunker. O zumbido do bunker perdeu a ventilação que subia e descia: ficou só o transformador e um sopro grave constante.
**Por quê:** pedido do Davi: o som do bunker parecia mar (era a ventilação, um ruído largo pulsando a cada 2 s) e não combinava; pediu algo mais obscuro.
**Afeta:** `assets/modelagem/audio/gerar_trilha_bunker.py` e `assets/audio/musica/bunker/bunker_trilha.ogg` (novos), `cenas/sistemas/musica_bunker.tscn` (nova, usa `musica_fase.gd`), as 9 salas de `cenas/salas/bunker/`, `gerar_efeitos_bunker.py` e `bunker_zumbido.wav`, `assets/audio/README.md`, `docs/fases/bunker.md`.

## 2026-10-02 — Sem agachar
**Decisão:** o Gabriel não agacha mais. Saíram a ação `agachar` (`Ctrl` / `C`), a velocidade de 50%, o achatamento do sprite, a redução do alcance de visão dos robôs (×0,6) e o passo silencioso. Para não ser ouvido, o jogador agora anda em vez de correr; para não ser visto, apaga a lanterna e sai do cone.
**Por quê:** pedido do Davi.
**Afeta:** `project.godot` (ação `agachar`), `scripts/personagens/gabriel.gd` (o sinal `passo_dado` agora só leva `correndo`), `scripts/personagens/robo.gd`, `scripts/sistemas/passos.gd`, `cenas/menu_principal.tscn` (lista de controles), `docs/computacao/ia_e_perseguicao.md`, `docs/fases/labirinto.md`, `docs/mecanicas/movimentacao_e_terreno.md` (pisos alagados pedem andar devagar; as frestas que pediam agachar saíram), `docs/personagens/`, `docs/sugestao-melhoramento-futuro.md`.

## 2026-10-01 — Tela de pausa
**Decisão:** `Esc` (ou `P`, ou Start no controle) pausa o jogo em qualquer sala e abre a tela **PAUSADO**: Continuar, Opções (tela cheia e os três volumes, os mesmos do menu), **Voltar ao menu principal** (pede confirmação, porque o jogo ainda não salva e o progresso da fase se perde; o cursor começa em "Cancelar") e Sair do jogo. `Esc` dentro da pausa volta um passo. A pausa não abre por cima do inventário, de um documento, do diálogo ou da tela de morte (o `Esc` desses continua fechando eles), nem no menu e nas cutscenes. O jogo também pausa sozinho quando a janela perde o foco.
**Por quê:** pedido do Davi: poder voltar ao menu principal durante o jogo.
**Afeta:** `cenas/interface/tela_pausa.tscn` e `scripts/interface/tela_pausa.gd` (autoload `Pausa`), `project.godot` (autoload e ação `pausar`), `scripts/sistemas/configuracoes.gd` (as contas de volume saíram do menu e agora servem ao menu e à pausa), `scripts/menu_principal.gd`, `cenas/menu_principal.tscn` (lista de controles).

## 2026-10-05 — Hackeamento de portas vira minigame
**Decisão:** o notebook, ao hackear uma **porta trancada**, abre um minigame em tela cheia (o jogo pausa): **Sequência** (memorizar e repetir setas) ou **Sincronia** (parar o cursor na zona verde). Cada porta define a dificuldade (fácil, médio, difícil) e o minigame (ou sorteia). Robôs continuam com o hack por tempo, até o grupo decidir se também ganham minigame.
**Por quê:** dar ao hack um momento de tensão e habilidade, em vez de só esperar uma barra.
**Afeta:** `scripts/itens/notebook.gd`, `scripts/sistemas/porta.gd`, `scripts/sistemas/hackeamento.gd`, `scripts/interface/tela_hackeamento.gd` e `scripts/interface/hackeamento/`, `sala_teste.tscn` (seis portas de teste). Detalhes em `docs/mecanicas/hackeamento.md`.

## 2026-09-30 — Gabriel e Clarice em resolução dobrada
**Decisão:** o projeto passa a usar o stretch **`canvas_items`** (antes `viewport`): a lógica, as câmeras e a interface continuam em 320×180, mas a imagem é desenhada na resolução da janela. Com isso, **Gabriel e Clarice ganham sprites com o dobro de pixels** (Gabriel 96 × 112 por quadro, a estação da Clarice 160 × 128, retratos 80 × 80), mostrados com escala 0,5: no mesmo tamanho na tela, com o dobro de detalhe (rosto, óculos, texto nos monitores). O cenário, os objetos, os robôs e a interface continuam em 1×. **Efeito colateral:** as luzes (PointLight2D) também são calculadas na resolução da janela e ficaram mais suaves. O efeito CRT do menu foi ajustado para continuar com uma linha por pixel do jogo.
**Por quê:** pedido do Davi. Com 48 px de altura, polígono a mais quase não aparecia (testado: mais gomos e luz suave só mudavam a folha de referência). Uma imagem comparando as duas resoluções na mesma cena decidiu.
**Afeta:** `project.godot` (`window/stretch/mode`), `gerar_gabriel.py` e `gerar_clarice.py` (`RESOLUCAO = 2`), todos os sprites dos dois, `gabriel.tscn` e `clarice.tscn` (escala 0,5), `gabriel.gd` (agachar respeita a escala), `caixa_dialogo.tscn` (retrato 80 × 80 em 40 × 40), `shaders/tela_crt.gdshader`. Os robôs e o Vigia podem ir para 2× do mesmo jeito, se o grupo quiser.

## 2026-09-30 — Salas fundas e personagens com mais detalhe
**Decisão:** (1) as **salas** do Bloco de salas e do Bunker passam a ser **fundas, mais altas que largas** (400 × 480 a 640 × 720), em vez de faixas compridas que pareciam corredor. A parede do fundo guarda as peças que contam a sala, e o chão desce para a câmera com o conteúdo organizado como a sala seria de verdade (fileiras de carteiras, de beliches, de macas, corredores de servidores e de estantes). Os **corredores continuam compridos**. Para isso o kit ganhou as peças de **chão de fundo** (repetem para baixo) e a **parede lateral**. (2) **Gabriel e Clarice** com mais polígonos: `DETALHE = 3` (cones e esferas com o triplo de gomos, quinas arredondadas) e sombreamento suave nas curvas, mais detalhes pequenos (cordões do capuz, cadarço, zíper e fivelas da mochila, sobrancelhas; na Clarice, mais cachos, zíper, bolsos e um botton).
**Por quê:** pedido do Davi: mais definição nos personagens, e as salas pareciam corredores.
**Afeta:** `comum.py` (`DETALHE`, `SUAVE`, `achatar_sombra`; os robôs e o Vigia ficam como estavam até alguém rodar os scripts deles com outro valor), `gerar_gabriel.py` e `gerar_clarice.py` e todos os sprites dos dois, `gerar_kit.py` e `gerar_bunker.py` (peças de fundo e laterais), as 12 salas de aula e as 7 salas do bunker.

## 2026-09-30 — Nova fase: Bunker, e a Clarice em pessoa
**Decisão:** começou a fase **Bunker**: o bunker de pesquisa embaixo do núcleo da Âncora, com dois setores (A e B, ligados por escada), 9 salas abertas (entrada, dois corredores, dormitório, refeitório, enfermaria, central de dados, gerador e depósito) e **seis portas lacradas** para fazer depois (escotilha da superfície, elevador, arsenal, laboratório, arquivo e a comporta do núcleo). A **Clarice aparece em pessoa** na central de dados, sentada na estação de trabalho dela, fixa ali, e **conversa** com o Gabriel. Entrou junto o **sistema de diálogos** (JSON em `dados/dialogos/`, caixa com retrato, texto letra por letra e escolhas) e o design completo dela, modelado no Blender.
**Por quê:** pedido do Davi.
**Muda o que estava decidido:** a ficha da Clarice dizia que ela era **só voz** (ligações) e que os dois **só se viam no final** ("é a primeira vez que se veem", na cena final da revelação central). O bunker resolve o "em aberto" de **onde ela está escondida**, mas o grupo precisa decidir: (a) o bunker fica perto do fim e a cena final muda, ou (b) as ligações continuam e o bunker é o primeiro encontro, com a cena final reescrita. Os diálogos de exemplo funcionam nos dois casos.
**Afeta:** `cenas/salas/bunker/` (9 cenas), kit do bunker (`gerar_bunker.py`, `cenas/cenario/bunker/`), luzes `luz_tubo` e `luz_emergencia`, `cenas/personagens/clarice.tscn`, `gerar_clarice.py`, sistema de diálogos (`scripts/sistemas/dialogos.gd`, autoload `Dialogos`, `cenas/interface/caixa_dialogo.tscn` no `modelo_sala.tscn`, `conversa_npc.gd`), `scripts/sistemas/porta.gd` (portas bloqueadas e som próprio), `dados/fases/08_bunker.tres` e o menu Fases, `gerar_efeitos_bunker.py`, docs (`fases/bunker.md`, `dialogos/`, `antecessores.md`).

## 2026-09-30 — Nova fase: Bloco de salas
**Decisão:** começou a fase **Bloco de salas** (os "Blocos de aula" do GDD): um bloco de dois andares, cada andar um corredor com **6 salas de aula** (101 a 106 no térreo, 201 a 206 no 1º andar), ligados por uma escada. O térreo está meio enterrado na areia e escuro; o 1º andar tem o teto aberto, sol e mato. Cada sala tem uma ideia própria para não ficar repetitivo (sala comum, invadida pela duna, barricada, laboratório, sala escura com robô desmontado, árvore, auditório, sala dos professores, chão que cedeu, sala "intacta demais", depósito). As lousas têm os tracinhos contados do GDD. Entra no menu Fases no lugar de "Blocos de aula". **É noite:** céu escuro com estrelas, luar pelas janelas e buracos e poucos lampiões; corredores de 2560 px e salas de 800 a 1280 px. Uma lanterna fica no começo do corredor (item único que o Gabriel já tem não aparece de novo no chão).
**Por quê:** pedido do Davi.
**Afeta:** `cenas/salas/bloco_de_salas/` (14 cenas novas), kit de cenário (`gerar_kit.py`: lousa, quadro de avisos, escadas, carteiras), `dados/fases/03_blocos_de_aula.tres`, `docs/fases/bloco_de_salas.md`. **Em aberto:** objetivo e história, robôs, ligação com a porta de saída da Biblioteca.

## 2026-09-30 — Biblioteca mais larga: ala leste
**Decisão:** a Biblioteca cresceu para a direita, de 960 para **1440 px** (4,5 telas de largura; a altura continua 420). A parte nova, depois da coluna onde a sala terminava, é a **ala leste** (sala de periódicos): terceiro buraco no teto com uma árvore nova, mesas, cabines e um segundo acervo no fundo sul. A porta de saída para os Blocos de aula foi para o fim da ala leste.
**Por quê:** pedido do Davi: a Biblioteca precisa ser maior, e desta vez na horizontal.
**Afeta:** `gerar_biblioteca.py` (medidas, parede, chão, primeiro plano, buracos), as 4 imagens em `assets/sprites/salas/biblioteca/`, `cenas/salas/biblioteca.tscn` (tamanho, limites, câmera, objetos, luzes, raios de sol) e `docs/fases/biblioteca.md`.

## 2026-09-30 — Gadgets em teste: cápsula de clarão, pedra e notebook
**Decisão:** os três gadgets sugeridos foram implementados **só na sala de teste**, para o grupo jogar e decidir: cápsula de clarão (paralisa os robôs perto, no máximo 2), pedra (barulho que atrai robôs, no máximo 5) e notebook (hackeia porta trancada ou robô por trás, gasta bateria, deixa o Gabriel parado e visível). Robôs ganharam o estado `ATORDOADO`. Ainda **em aberto:** em que fase cada um aparece (sugestão: clarão e pedra cedo, notebook na fase 3 ou 4), se o notebook usa as mesmas pilhas da lanterna e se cada gadget vem de uma das pessoas que vieram antes do Gabriel.
**Por quê:** pedido do Davi, para testar as ideias antes de colocar numa fase.
**Afeta:** `scripts/personagens/robo.gd`, `scripts/sistemas/inventario.gd` (itens que empilham), `scripts/itens/item.gd`, gadgets em `cenas/itens/` e `dados/itens/`, `scripts/sistemas/porta.gd` (porta trancada e som), sala de teste. Detalhes em `docs/mecanicas/itens_e_inventario.md`.

## 2026-09-30 — Aviso de pegar item mostra só a tecla
**Decisão:** perto de um item no chão ou de uma pilha, o aviso mostra só `[E]`, sem "Pegar lanterna" ou "Trocar a pilha". O nome aparece na mensagem depois de pegar e a descrição fica no inventário. Documentos continuam com `[E] Ler...`.
**Por quê:** pedido do Davi. O texto entregava o que era o item antes de o jogador chegar nele; só a tecla deixa a tela mais limpa, como nos jogos de terror de referência.
**Afeta:** `scripts/interface/hud.gd`, `scripts/itens/item_no_chao.gd`, `scripts/itens/pilha_no_chao.gd`, `docs/mecanicas/itens_e_inventario.md`.

## 2026-09-30 — Tela de Opções no menu e canais de áudio
**Decisão:** o botão **Opções** do menu abre uma tela com tela cheia, efeito CRT, **volume geral**, **música** e **efeitos**, e um atalho para a lista de **Controles**. As escolhas ficam salvas em `user://configuracoes.cfg` pelo autoload `Configuracoes`. O áudio passa a ter dois canais (*buses*) além do Master: **Musica** (trilhas do menu, das fases e do labirinto) e **Efeitos** (todo o resto). Todo som novo precisa escolher um dos dois no Inspetor (`Bus`), senão ignora o volume da tela de Opções.
**Por quê:** pedido do Davi, para o jogador ajustar som e vídeo sem sair do jogo.
**Afeta:** `cenas/menu_principal.tscn`, `scripts/menu_principal.gd`, `scripts/sistemas/configuracoes.gd` (novo), `scripts/sistemas/tela.gd`, `default_bus_layout.tres` (novo), `project.godot` (autoload) e todas as cenas com `AudioStreamPlayer`.

## 2026-09-30 — Destaque nos coletáveis e anotações dentro do inventário
**Decisão:** todo item coletável no cenário (itens no chão e pilhas) ganha um **destaque**: uma luz fraca que pulsa em volta e um brilho de pixel que pisca em cima do desenho, visível no escuro. O **Caderno do Gabriel** deixa de ser uma tela separada e vira a aba **ANOTAÇÕES** do inventário, com um cabeçalho de abas **ITENS | ANOTAÇÕES**. `Tab`/`I` abrem em Itens, `N` abre em Anotações e `Q` troca de aba. As anotações ficam numa lista, com um ponto nas não lidas, e o texto da escolhida aparece ao lado, em páginas de 7 linhas.
**Por quê:** pedido do Davi: os itens sumiam no escuro, e ter itens e anotações numa tela só, organizada por abas, deixa tudo mais fácil de achar.
**Afeta:** `cenas/itens/` (novo `destaque_coletavel.tscn`), `cenas/interface/tela_inventario.tscn`, `cenas/interface/painel_anotacoes.tscn` (novo), `tela_caderno.tscn` (removida), as salas que tinham a tela do caderno, `project.godot` (ação `trocar_aba`), `docs/mecanicas/`.

## 2026-09-30 — Fonte Galmuri7 no tamanho 8
**Decisão:** a fonte do jogo passa a ser a **Galmuri7** (OFL), nos tamanhos 8 e 16, no lugar da Ark Pixel 10. Todo texto que era 10 vira 8, e todo título que era 20 vira 16. A altura da linha continua 14 px, então nenhuma caixa de texto mudou de tamanho.
**Por quê:** pedido do Davi. O texto em 10 estava grande, mas a Ark Pixel é desenhada para 10 px, e no tamanho 8 as letras deformavam e ficavam ruins de ler. A Galmuri7 é desenhada para 8 px: ocupa quase o mesmo espaço (uma frase de teste mede 164 px, contra 152 da Ark em 8 e 186 da Ark em 10), fica nítida e tem todos os acentos do português. A Fusion Pixel 8px também foi testada, mas perde o acento das maiúsculas (Ã, É, Ç).
**Afeta:** `assets/fontes/`, `cenas/interface/tema_jogo.tres`, `cenas/interface/fonte_jogo.tres` (novo), as cenas com `font_size` próprio (`botao_pular`, `espaco_item`, `hud`, `tela_inventario`, `tela_morte`, `menu_principal`, `saida_fase`), `CLAUDE.md` e `docs/personagens/antecessores.md`.

## 2026-09-29 — Fonte Ark Pixel e labirinto sem checkpoints
**Decisão:** a fonte do jogo passa a ser a **Ark Pixel 10** (OFL), nos tamanhos 10 e 20, no lugar da Tiny5, que era pequena demais para ler. As telas com texto foram ajustadas: os papéis dos bilhetes cresceram para 248 × 156 px com 8 linhas por página, a legenda do rádio ficou mais alta e a lista de Fases do menu passou a rolar. Os textos do diário, do bilhete e das anotações foram encurtados um pouco para caber. O **labirinto não tem mais checkpoints**: a fase é pequena, e morrer recomeça do início. O sistema de checkpoint continua pronto para fases maiores.
**Por quê:** pedido do Davi (a Tiny5 estava ruim de ler; a Ark Pixel foi a mais legível na comparação com Micro 5, Bytesized, Press Start 2P, Kenney Mini, Kenney Pixel e Fusion Pixel).
**Afeta:** `cenas/interface/tema_jogo.tres`, `assets/fontes/`, `CLAUDE.md`, todas as telas com texto, `gerar_interface.py` (papéis), `dados/documentos/`, `gerar_labirinto.py` e `dados/labirinto/mapa_labirinto.tres`.

## 2026-09-29 — Fim dos fungos: lanterna a pilha e luzes de emergência
**Decisão:** saem os fungos bioluminescentes (pote de fungos, colônias, fungos pintados no cenário). A luz passa a ser elétrica: o Gabriel usa uma **lanterna a pilha** (feixe em cone, bateria de 4 min, recarregada com **pilhas** achadas no mapa) e o cenário tem **luminárias de emergência** de parede e **lampiões** no chão, que tremem e piscam. As cápsulas de clarão continuam previstas, como flash descartável.
**Por quê:** pedido do Davi.
**Afeta:** `gerar_biblioteca.py`, `gerar_kit.py` e `gerar_interface.py` (arte refeita), `cenas/salas/biblioteca.tscn` e `sala_exemplo.tscn`, itens (`lanterna`, `pilha_no_chao`), `docs/mecanicas/iluminacao_e_lanterna.md` (antes `iluminacao_e_fungos.md`), GDD e docs que citavam fungos.

## 2026-09-29 — Vida, checkpoint, Labirinto, robôs e menu Fases
**Decisão:**
- **Vida:** 3 corações; toque de robô tira 1, com 1,5 s de invulnerabilidade; zerou, volta ao último **checkpoint** com vida cheia.
- **Checkpoint:** postos de emergência no mapa; passar por um salva a posição e recupera os corações.
- **Labirinto:** segunda fase jogável, um subsolo escuro com saída marcada. A ordem na história está a definir.
- **Robôs:** os dois primeiros tipos, a **Sentinela** (visão) e o **Rastreador** (audição), modelados no Blender e com IA: máquina de estados, cone de visão por produto escalar, audição por BFS, perseguição por A\* e patrulha por cadeia de Markov.
- **Trilha adaptativa** do labirinto em duas camadas.
- **Menu Fases**, com todas as fases previstas. As que ainda não existem aparecem apagadas.

**Por quê:** pedido do Davi. Cobre boa parte dos conteúdos de computação exigidos pela disciplina.
**Afeta:** `project.godot` (autoloads `Vida` e `Checkpoints`), `cenas/salas/labirinto.tscn` e `scripts/labirinto/`, `cenas/personagens/robo_*.tscn`, `scripts/personagens/robo.gd`, HUD, Gabriel, `sala.gd`, menu. Detalhes em `docs/mecanicas/vida_e_checkpoint.md`, `docs/fases/labirinto.md` e `docs/computacao/ia_e_perseguicao.md` (seção 5).

## 2026-09-29 — Leitura de documentos, Caderno do Gabriel e rádio do Valdir
**Decisão:**
- Os documentos dos antecessores abrem numa tela de leitura que **pausa o jogo**, com um papel diferente para cada época.
- O que for útil vira uma anotação no **Caderno do Gabriel**, aberto com a tecla **N**.
- O **rádio do Valdir** é um item comum. Com ele no inventário, gatilhos no mapa tocam transmissões, com legenda e chiado, **sem pausar o jogo**.
- Na Biblioteca entraram o acampamento e o diário do Baltazar, o robô desmontado, os riscos de estrelas na árvore, o terminal com o bilhete da Clarice e duas transmissões do Valdir.
**Por quê:** pedido do Davi (itens 1 a 3 do que faltava implementar dos antecessores).
**Afeta:** `project.godot` (autoloads `Caderno` e `Radio`, ação `caderno`), `cenas/salas/biblioteca.tscn`, `cenas/salas/modelo_sala.tscn`, HUD, inventário, menu. Detalhes em `docs/mecanicas/registros_e_caderno.md`.

## 2026-09-29 — Revelação central aprovada, Clarice viva e o final
**Decisão:**
- A **revelação central** está aprovada. Gabriel é o paradoxo da Âncora: ela nasce do caderno dele, esquecido na Biblioteca em 2026. A fenda não puxa por acaso, e sim quem esteve no chão da Biblioteca. Os sonhos são ciclos que falharam. A premissa "a fenda puxa pessoas aleatórias" passa a ser o que o jogador acredita até a revelação.
- **Clarice está viva.** O jogador acha que ela morreu, mas ela fala com Gabriel **por ligação**, pelos telefones velhos do campus, e é a única que lembra dos loops.
- **Um só final, por enquanto: o feliz.** Com a pesquisa do professor, Gabriel recalibra a Âncora, e os dois ficam juntos em 2026. Chegou a ser escrito um final triste (cada um volta ao seu tempo e os dois nunca mais se veem), que saiu por decisão do Davi. O texto dele está no histórico do PR #33, se o grupo quiser de volta.

**Por quê:** decisão do Davi. Dá uma relação central e emocional à história, e fecha o loop com os dois juntos.
**Afeta:** `docs/historia/revelacao_central.md`, `docs/personagens/antecessores.md`, `docs/historia/README.md`, `docs/gdd.md`, `docs/fases/biblioteca.md`. **Em aberto:** onde a Clarice está escondida; onde estão as partes da pesquisa do professor.

## 2026-09-29 — Personagens secundários: os antecessores
**Decisão:** entram na documentação as fichas das pessoas puxadas antes de Gabriel:
- **Mestre Baltazar** (~1750): some sem deixar corpo. Na Biblioteca fica o acampamento dele entre as raízes da árvore, com a luneta e o diário que mostra o ponto fraco dos sensores ópticos.
- **Inspetor Agostinho** (1978): deixa um mapa antigo com passagens secretas.
- **Clarice** (1994, a aluna já decidida): deixa disquetes e senhas.
- **Seu Valdir** (2008, o segurança já decidido): fala com Gabriel pelo rádio e dá dicas de patrulha. No fim se descobre que ele morreu há décadas e o rádio só repete as gravações dele.
- **O professor** (2019): a pesquisa dele virou a cadeira de Gabriel, e em 3026 ele apaga o nome do criador da Âncora.
- **Zane** (2123): deixa áudios que apontam para um usuário de 2026.

Todos foram puxados **no mesmo lugar**, o chão onde hoje fica a Biblioteca. Cada época tem um visual próprio de bilhete, e a Biblioteca só usa Baltazar, Clarice e Valdir. A revelação central que veio junto (Gabriel como paradoxo da Âncora, sonhos como loops, bilhetes de "G." dos ciclos anteriores) foi registrada como proposta; foi aprovada na entrada acima.
**Por quê:** proposta de personagens recebida pelo grupo, com os ajustes pedidos pelo Davi. Dá rosto aos bilhetes e liga cada pista a uma mecânica.
**Afeta:** `docs/personagens/antecessores.md` (novo), `docs/historia/revelacao_central.md` (novo), `docs/historia/README.md`, `docs/personagens/README.md`, `docs/gdd.md`, `docs/mecanicas/sono_e_sonhos.md`, `docs/fases/biblioteca.md`. **Em aberto:** se a pessoa de 2041 continua; como terminais e rádio funcionam se "nada elétrico funciona"; a revelação central.

## 2026-09-27 — Scripts GDScript sem comentários
**Decisão:** os scripts `.gd` não têm nenhum comentário (nem `#` nem `##`). O código se explica pelos nomes, em português. A explicação de algoritmos e da matemática fica em `docs/` (ex.: `docs/computacao/`). Geradores em Python (`assets/modelagem/`) e shaders continuam comentados. O guia de montar salas e as imagens de catálogo do kit (`docs/imagens/`) saíram; o catálogo do kit agora só é gerado com `CATALOGO=1`.
**Por quê:** decisão do Davi, para enxugar o código.
**Afeta:** todos os `scripts/*.gd`, `CLAUDE.md` (Convenções), `CONTRIBUTING.md`, agentes `artista`, `revisor` e `sistemas`, `assets/modelagem/cenario/gerar_kit.py`.

## 2026-09-27 — Biblioteca ainda maior ao sul, com o acervo
**Decisão:** a Biblioteca cresceu mais 120 px para o sul: passa de 300 para 420 px de altura, e a faixa onde o Gabriel anda vai de y 122 a 416. O fundo da parte sul é a área mais escura da sala (longe dos buracos do teto, iluminada só por fungos) e tem o **acervo**: duas fileiras de estantes em pé com corredores entre elas, para o Gabriel se esconder dos robôs. Dos lados, um canto desabado (esquerda) e um canto de leitura (direita). Tudo com objetos do kit de cenário.
**Por quê:** pedido do Davi: aumentar mais o mapa para a parte sul.
**Afeta:** `cenas/salas/biblioteca.tscn` (tamanho, limites, objetos e luzes novos), `gerar_biblioteca.py` (chão e primeiro plano), `docs/guia_montar_salas.md` e `docs/fases/biblioteca.md`.

## 2026-09-26 — Nome do jogo: Ankhor, e inimigos são robôs
**Decisão:** O jogo agora se chama oficialmente **Ankhor** (substitui o provisório "Projeto The Game"). Os inimigos que patrulham o campus passam a ser **robôs** (substitui o conceito anterior de Insones). As pessoas puxadas de outras épocas (aluna de 1994, segurança de 2008, professor de 2019 e a pessoa de 2041 a definir) deixaram **bilhetes** pelo campus explicando melhor os acontecimentos (textos a serem escritos pelo Davi).
**Por quê:** Decisão do Davi (definindo nome oficial, a natureza robótica dos inimigos e a forma de entrega de narrativa das pessoas de outras épocas).
**Afeta:** GDD, README, `decisoes.md`, `CLAUDE.md`, `project.godot`, `docs/personagens/` e `docs/mecanicas/`.

## 2026-09-26 — Premissa da Fenda Temporal e a Âncora (Ano 3026)
**Decisão:** Em 3026 (mil anos no futuro), a Unifor é um centro de pesquisa em física do tempo. A explosão de um aparelho chamado **Âncora** rasgou o tempo dentro do campus. A fenda encosta em momentos aleatórios do passado e puxa quem estiver perto — numa madrugada de 2026, puxou Gabriel da Biblioteca. A fenda está crescendo e, se não for fechada, vai engolir o passado do campus, incluindo o tempo de Gabriel. Gabriel não é o primeiro a ser puxado: antes dele vieram uma aluna de 1994, um segurança de 2008, um professor de 2019 e alguém de 2041, e ninguém conseguiu. A primeira fase do jogo é a Biblioteca.
**Por quê:** Definição da história principal e ponto de partida do jogo pelo Davi.
**Afeta:** `docs/gdd.md`, `docs/visao_geral/conceito.md`, `docs/historia/README.md`, `docs/fases/README.md`, `docs/fases/biblioteca.md` e `docs/personagens/gabriel.md`.

## 2026-09-26 — Tela cheia em Full HD (F11 alterna)
**Decisão:** o jogo abre em tela cheia e continua desenhado em 320 × 180, ampliado por número inteiro: 6× num monitor Full HD (1920 × 1080). `F11` alterna para janela de 1280 × 720 (4×) e volta.
**Por quê:** pedido do Davi (resolução Full HD). Mudar a resolução BASE para 1920 × 1080 exigiria refazer toda a arte e deixaria de ser pixel art; ampliar por inteiro mantém a arte e a fonte nítidas.
**Afeta:** `project.godot` (modo de janela, autoload `Tela`, ação `tela_cheia`) e `scripts/sistemas/tela.gd`. Ao rodar pelo editor (F5/F6), o jogo também abre em tela cheia: `F11` volta para a janela.

## 2026-09-26 — Sistema de itens, inventário e gadgets
**Decisão:** o Gabriel pega itens com `E`, guarda num inventário em grade de 3 × 4 (aberto com `Tab` ou `I`, pausa o jogo) e equipa até 3 gadgets, usados com as teclas `1`, `2` e `3`. O primeiro item é a lanterna, que é o **pote de fungos** do GDD: fica no chão da Biblioteca, perto de onde o Gabriel acorda. A carga dura 4,5 minutos destampado e recarrega nos fungos do cenário.
**Por quê:** pedido do Davi. Os 3 espaços correspondem às ferramentas equipáveis previstas (pote, cápsulas de clarão, arremesso), e a grade é o "inventário em grade (matriz)" do GDD, item 2.4.
**Afeta:** `project.godot` (autoload `Inventario` e ações `interagir`, `inventario`, `gadget_1` a `gadget_3`), `scripts/personagens/gabriel.gd`, `cenas/salas/modelo_sala.tscn` e `biblioteca.tscn` (HUD e inventário), `cenas/cenario/objetos/fungo.tscn` (colônia de recarga). Detalhes em `docs/mecanicas/itens_e_inventario.md`. **Em aberto:** `iluminacao_e_fungos.md` diz que a cápsula de clarão usa `Q`; com os espaços de gadget, ela usaria a tecla do espaço dela. O grupo decide qual fica.

## 2026-09-26 — Biblioteca maior, com a parte sul
**Decisão:** a Biblioteca cresceu para a frente (o "sul" da sala, na direção da câmera): passa de 180 para 300 px de altura, e a faixa onde o Gabriel anda vai de y 122 a 296. A câmera agora anda também na vertical. A parte sul foi mobiliada só com objetos do kit de cenário.
**Por quê:** pedido do Davi: a Biblioteca precisa ser maior.
**Afeta:** `scripts/salas/sala.gd` (novo campo `altura`, que qualquer sala pode usar), `scripts/salas/guias_sala.gd`, `cenas/salas/biblioteca.tscn`, `gerar_biblioteca.py` (chão e primeiro plano) e `docs/guia_montar_salas.md`.

## 2026-09-25 — Biblioteca e movimento 2.5D no estilo FNAF: Into the Pit
**Decisão:** a Biblioteca foi refeita do zero no estilo de *FNAF: Into the Pit*, e o jogador anda em todas as direções dentro da faixa de chão (esquerda/direita e fundo/frente da sala), passando na frente e atrás dos objetos (y-sort). W/S (e as setas ↑/↓) passam a ser mover para cima/baixo; agachar fica no Ctrl (e no C).
**Por quê:** pedido do Davi: a sala precisa ter profundidade de verdade, como em *Into the Pit*, e não só um corredor lateral.
**Afeta:** `project.godot` (ações `mover_cima`, `mover_baixo`, `agachar`), `scripts/personagens/gabriel.gd` (sem gravidade, colisão só nos pés), `cenas/salas/biblioteca.tscn`, arte em `assets/sprites/salas/biblioteca/` (gerada por `assets/modelagem/salas/biblioteca/gerar_biblioteca.py`) e `docs/mecanicas/movimentacao_e_terreno.md`. A "transição de planos" com W em portas e escadas (mecânicas, item 4) precisa de outra tecla ou de interação quando for implementada.

## 2026-09-24 — Nome do jogo: Projeto The Game
**Decisão:** o jogo se chama Projeto The Game (substitui o provisório "VIGÍLIA"). O estimulante da história continua se chamando VIGÍLIA-7.
**Por quê:** escolha do grupo.
**Afeta:** README, GDD, CLAUDE.md e `project.godot` — já atualizados.

## 2026-09-24 — Protagonista se chama Gabriel
**Decisão:** o nome do protagonista é Gabriel (substitui o provisório "Téo").
**Por quê:** escolha do grupo.
**Afeta:** GDD e roteiro — já atualizados em `docs/gdd.md`.

## 2026-09-24 — Roteiro e mecânicas definidos durante o projeto
**Decisão:** o GDD atual é ponto de partida. História e mecânicas vão sendo fechadas a cada sprint e registradas aqui.
**Por quê:** o grupo prefere descobrir o jogo fazendo, em vez de fechar tudo antes.
**Afeta:** tudo; conferir este arquivo antes de implementar algo grande.

## 2026-09-24 — Fluxo de trabalho com git
**Decisão:** GitHub Flow — `main` protegida, uma branch por tarefa, Pull Request com revisão obrigatória do Davi (e de outro integrante nos PRs do Davi).
**Por quê:** evita que uma mudança quebre o jogo de todo mundo e garante que alguém sempre revise.
**Afeta:** `CONTRIBUTING.md`.

## 2026-09-24 — Premissa: mil anos no futuro, na Unifor
**Decisão:** o jogo se passa na Unifor abandonada, mil anos depois; o protagonista acorda sem saber o que aconteceu e investiga. Estilo pixel art 2.5D lateral, inspirado em *FNAF: Into the Pit*.
**Por quê:** exigência de ambientação na Unifor, e o estilo 2D cabe no tamanho do grupo.
**Afeta:** GDD itens 1 a 4.
