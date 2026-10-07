# Mecânicas — Registros dos antecessores e Caderno do Gabriel

Os antecessores (as pessoas puxadas pela fenda antes do Gabriel, [`../historia/personagens/`](../historia/personagens/)) contam a história por **registros**: documentos para ler (diários, bilhetes) e **transmissões de rádio**. Tudo o que for útil vai para o **Caderno do Gabriel**.

---

## 1. Como funciona no jogo

### Ler um documento
- Perto de um documento, aparece o aviso `[E] Ler...`. Apertar `E` abre a folha na tela e **pausa o jogo**.
- `E` vira a página; na última página, fecha. As setas folheiam para os dois lados. `Esc` fecha a qualquer momento.
- Cada época tem o seu papel (ver a seção "Registros" de cada ficha em [`../historia/personagens/`](../historia/personagens/)):

| Papel | Quem usa | Tinta |
|---|---|---|
| `pergaminho` | Baltazar (1750). Tem o esboço do robô no canto | marrom |
| `caderno_clarice` | Clarice (1994): folha de fichário, pautas azuis, estrela | azul de caneta |
| `caderno_gabriel` | O caderno do Gabriel | grafite |

- Ao fechar, a **anotação** do documento entra no caderno (uma vez só) e o HUD avisa: *"Nova anotação: Baltazar, 1750   [N] ver"*.

### Ouvir o rádio
- O rádio portátil do Rafael é um item comum (fica no inventário, não é gadget).
- Com o rádio no inventário, **gatilhos** espalhados pela sala tocam transmissões quando o Gabriel entra neles. Cada transmissão toca **uma vez só**.
- A transmissão **não pausa o jogo**: a fala aparece embaixo, letra por letra, com o chiado do rádio por baixo. Se duas forem pedidas juntas, a segunda espera a primeira acabar.
- No fim, a anotação da transmissão entra no caderno.

### Caderno (aba Anotações do inventário)
- As anotações ficam no **inventário**, na aba **ANOTAÇÕES**. `N` abre o inventário direto nela (e fecha, se ela já estiver aberta); `Q` troca entre Itens e Anotações. O jogo pausa enquanto está aberto.
- À esquerda, a **lista** das anotações, na ordem em que foram achadas. Ao abrir com `N`, a mais recente já vem escolhida. As não lidas têm um ponto na frente (`• Rafael, 2008`), e a aba também mostra o ponto enquanto houver alguma não lida.
- À direita, o **texto** da anotação escolhida: o título é quem deixou a pista, e o texto é o resumo do Gabriel, em tópicos quando for dica de jogo. Cabem 7 linhas; se passar disso, o texto vira páginas e o canto mostra `1/2`.
- Setas **cima/baixo** escolhem a anotação; **esquerda/direita** viram a página. Dá para clicar na lista com o mouse.

---

## 2. Na Biblioteca

| O quê | Posição (x, y) | Como dispara |
|---|---|---|
| Acampamento do Baltazar + diário (`DiarioBaltazar`) | (262, 148), entre as raízes da árvore | `E` perto |
| Riscos de estrelas na árvore | filho de `Arvore`, no tronco | só cenário |
| Robô desmontado | (280, 172) | só cenário |
| Rádio portátil | (628, 162), ao lado da mesa de leitura | `E` para pegar |
| Transmissão `rafael_01` (`GatilhoRafael1`) | círculo de 40 px em volta do rádio | toca ao pegar o rádio |
| Terminal + bilhete da Clarice (`BilheteClarice`) | (470, 236), na parte sul | `E` perto |
| Lampião do terminal | (492, 240) | ilumina o terminal |
| Transmissão `rafael_02` (`GatilhoRafael2`) | retângulo 270 × 110 no acervo, centro (548, 360) | toca ao entrar no acervo com o rádio |

---

## 3. Onde está no projeto

| O quê | Onde |
|---|---|
| Caderno (autoload `Caderno`): pedidos de leitura e anotações | `scripts/sistemas/caderno.gd` |
| Rádio (autoload `Radio`): pedidos de transmissão e quais já tocaram | `scripts/sistemas/radio.gd` |
| Tipo `Documento` (recurso) | `scripts/itens/documento.gd` |
| Tipo `Transmissao` (recurso) | `scripts/sistemas/transmissao.gd` |
| Os documentos e as transmissões | `dados/documentos/*.tres`, `dados/transmissoes/*.tres` |
| Documento no mapa (`E` para ler) | `cenas/itens/documento_no_mundo.tscn` |
| Gatilho de transmissão | `cenas/sistemas/gatilho_transmissao.tscn` |
| Tela de leitura | `cenas/interface/tela_documento.tscn` |
| Aba Anotações (dentro da tela do inventário) | `cenas/interface/painel_anotacoes.tscn` |
| Legenda do rádio | `cenas/interface/legenda_radio.tscn` |
| Papéis e ícone do rádio (gerados) | `assets/modelagem/interface/gerar_interface.py` |
| Acampamento, robô, riscos e terminal (gerados) | `assets/modelagem/cenario/gerar_antecessores.py` |
| Chiado, clique do rádio e folhear (gerados) | `assets/modelagem/audio/gerar_efeitos_registros.py` |

A tela de leitura, a legenda e o inventário (com a aba Anotações) já estão no `modelo_sala.tscn`: toda sala nova herda.

**Sinais:** quem está no mapa não conhece as telas. O documento chama `Caderno.ler(documento)`, que emite `leitura_pedida`, e a tela de leitura escuta. O gatilho chama `Radio.transmitir(transmissao)`, que emite `transmissao_pedida`, e a legenda escuta. Quando uma anotação entra, `Caderno` emite `anotado`, e o HUD mostra a mensagem. Quando ela é lida na aba, `Caderno.marcar_lida` emite `mudou`, e a aba apaga o ponto.

---

## 4. Como criar um documento novo

1. No Godot, botão direito em `dados/documentos/` → *Novo* → *Recurso...* → `Documento`.
2. Preencha `id` (único), `titulo` (vai no alto da folha), `autor` (vira o título da anotação no caderno, ex.: `Clarice, 1994`), `papel` e a `anotacao`.
3. Em `paginas`, **uma entrada por página**. Cada página tem no máximo **8 linhas** de ~45 caracteres (a linha em branco entre parágrafos conta). Se passar, o fim não aparece e o Godot mostra um aviso no painel de saída. Termine cada página no fim de um parágrafo.
4. A anotação também cabe em 8 linhas.
5. No mapa: arraste `cenas/itens/documento_no_mundo.tscn` para `Objetos`, na posição do objeto (a origem é o pé), escolha o `documento` e troque o `texto_acao` (ex.: `Ler o bilhete`). Se o objeto for alto, aumente `altura_aviso`.

**Papel novo:** desenhe a função em `gerar_interface.py` (248 × 156 px, as pautas nas medidas explicadas no topo do script), adicione em `PAPEIS` lá e em `PAPEIS` de `scripts/interface/tela_documento.gd` (textura e cor da tinta), e na lista do `@export_enum` de `documento.gd`.

## 5. Como criar uma transmissão nova

1. Botão direito em `dados/transmissoes/` → *Novo* → *Recurso...* → `Transmissao`.
2. `falante` aparece em cima da fala (ex.: `RAFAEL (rádio)`). Em `falas`, uma entrada por fala, com no máximo **2 linhas** (~85 caracteres).
3. `vozes` é opcional: um áudio por fala, na mesma ordem. Com voz gravada, a fala espera o áudio acabar. As gravações vão em `assets/audio/vozes/`.
4. No mapa: arraste `cenas/sistemas/gatilho_transmissao.tscn` para `Objetos`, escolha a `transmissao` e ajuste a forma da área (`Area`). O gatilho só toca com o item `item_necessario` (padrão: `radio`) no inventário.

---

## 6. Ainda não feito

- O caderno não guarda o texto completo dos documentos, só a anotação. Reler exige voltar ao lugar.
- Salvar caderno e transmissões ao dormir (depende do sistema de save).
- As ligações da Clarice pelos telefones (vão reaproveitar a legenda do rádio).
- As falas do Rafael ainda não têm voz gravada.
- O sistema de diálogos completo (escolhas, retratos) de [`../dialogos/README.md`](../dialogos/README.md): a legenda do rádio é só a parte de falas em sequência.
