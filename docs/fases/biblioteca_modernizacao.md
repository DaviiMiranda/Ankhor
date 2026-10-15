# Plano — Modernizar a Biblioteca

> **Status:** proposta de planejamento (2026-10-15). **Nada foi decidido nem implementado.** As seções 9 e 10 pedem decisão do Davi antes de qualquer arte.
> **Responde a:** a pendência "Cenários mais futuristas" do [Enredo Principal](../historia/enredo_principal.md) (seção 12.5), para a Fase 1.
> **Contexto:** o Bloco de salas ficou futurista no PR #113 ([`bloco_de_salas.md`](bloco_de_salas.md)). A Biblioteca, que vem antes dele, ficou para trás.
> **História:** este plano é só visual. Não muda fala, bilhete, personagem nem o Enredo. A fase continua a de [`biblioteca.md`](biblioteca.md).

---

## 1. Por que e o que "modernizar" quer dizer

**Três motivos:**

1. **O jogo contradiz o vídeo da abertura.** O `seg_acordar` mostra a cabine com painéis de luz ciano, um holograma aceso sobre o caderno e torres de equipamentos entre as estantes ([`seg_acordar.md`](../historia/roteiro/cutscenes/seg_acordar.md)). Quando o vídeo acaba, o jogo mostra uma ruína de madeira, com monitores de tubo e vidros esverdeados, na mesma sala.
2. **A progressão ficou ao contrário.** Hoje a Fase 1 parece mais antiga que a Fase 2.
3. **Pedido do Davi** (Enredo, seção 12.5): os cenários devem mostrar mais a tecnologia de 3026, misturada às ruínas e à vegetação.

**O que não é:** trocar a Biblioteca por um laboratório limpo. A árvore, o musgo, a luz entrando pelo teto quebrado e o acampamento do Baltazar são a identidade da fase e ficam.

**O que é:** uma **ruína de alta tecnologia**. A tecnologia de 3026 convive com a natureza e com as relíquias dos anos 80 do Carlos (monitores de tubo verdes, telefone, disquete, quadro de chaves).

### 1.1 Linguagem de cor (para o jogador ler o cenário sem texto)

| Cor | Quer dizer | Onde já existe |
|---|---|---|
| **Ciano** | tecnologia de 3026 funcionando | hologramas do Labirinto, lentes dos óculos do Bloco |
| **Âmbar** | alerta ou "sem carga" | indicadores das docas do Bloco |
| **Vermelho** | robô e perigo | olhos e farol dos robôs, luzes de emergência |
| **Verde-fósforo** | relíquia dos anos 80 (o mundo do Carlos) | monitores e terminais da Biblioteca |
| **Luz quente** | gente (lampião, lanterna do Gabriel) | lampiões do salão |

---

## 2. Como está hoje

Levantamento feito rodando as 8 cenas no Godot em 2026-10-15.

| Sala | Tamanho | Como é feita | O que tem de "antigo" | O que não pode quebrar |
|---|---|---|---|---|
| **Cabine** (`cabine`) | 320 | Peças do kit | Duas cabines de vidro verde com monitor de tubo, estantes de madeira, cadeira de madeira | A **lanterna** no chão (primeira coisa que o jogador pega) |
| **Salão** (`salao`) | 960 × 420 | **Arte pintada em 4 camadas** + objetos | Estantes de madeira (4 vazias, 4 quebradas, 3 caídas), mesas de leitura, 2 cabines com monitor, placas pintadas (BALCÃO, OBRAS RARAS, SERVIÇO, SILÊNCIO, ACERVO) | **Sentinela**, esconderijos atrás das estantes, acampamento e diário do Baltazar, painel do código, grade, telefone ao longe |
| **Balcão** (`balcao`) | 400 × 260 | Peças do kit | Bancada de madeira, quadro de chaves, placa SILÊNCIO | **Rádio**, quadro de chaves (gancho vazio), telefone, gatilho da 1ª transmissão |
| **Acervo sul** (`acervo`) | 560 × 420 | Peças do kit | 6 estantes vazias, 6 quebradas, 5 paredes de estante, carrinho | **Rastreador**, a **chave da manutenção** no carrinho, esconderijos nos corredores |
| **Corredor de serviço** (`corredor_servico`) | 480 | Peças do kit | Caixas, tambor, paredes rachadas e desabadas | Porta trancada pela chave |
| **Manutenção** (`manutencao`) | 400 × 240 | Peças do kit | Estante de metal, caixas, tambor | **Quadro de energia** (ordem 3, 1, 4, 2), papel do lado de dentro da porta, **sala segura** e checkpoint |
| **Terminais** (`terminais`) | 400 × 260 | Peças do kit | 3 terminais de tubo, mesas, mural, janela | **Terminal com energia**, bilhete da Clarice, disquete |
| **Ala leste** (`ala_leste`) | 480 × 420 | **Arte pintada em 4 camadas** + objetos | Cabines com monitor, estantes de madeira, árvore | **Grade**, porta de saída, toque do telefone ao longe |

As peças de arte da Biblioteca saem de `assets/modelagem/salas/biblioteca/gerar_biblioteca.py` (1340 linhas) e do kit de `assets/modelagem/cenario/gerar_kit.py`, que importa o primeiro. As do Bloco saem de `gerar_salas_futuristas.py`, que já tem a técnica das duas camadas (corpo e luz).

---

## 3. O que não pode quebrar

A modernização é só de aparência. Estas regras valem para todo PR deste plano:

1. **A cadeia da fase não muda:** lanterna → rádio → chave da manutenção → energia → terminal ligado → código da grade → grade aberta → telefone → porta de saída ([`biblioteca.md`](biblioteca.md), seção 3.2). Nenhum item, gatilho, marca do `Progresso` ou posição de interação muda de lugar.
2. **Troca 1:1 nos objetos com função.** Uma estante que vira rack de arquivo mantém a mesma pegada (64 × 8) e a mesma camada de colisão. Nas salas com robô, as estantes estão na camada 4 e cortam a visão; o nó `RobosDaSala` monta o mapa do chão com elas. Se a camada mudar, o robô passa a ver por dentro e o esconderijo deixa de funcionar.
3. **Luz decorativa não entrega o Gabriel.** Em `VisivelComMarca`, só as luzes dos nós com `revela_quem_passa = true` entram no grupo que faz o robô enxergar de longe. Painéis e hologramas ciano ficam com esse campo desligado: o único aviso de perigo continua sendo a luz de emergência.
4. **Os itens continuam legíveis no escuro:** a chave no carrinho, o papel dos disjuntores, o disquete e o painel do código não podem sumir no meio de arte nova.
5. **Os anos 80 do Carlos ficam.** Monitores de tubo verdes, telefone, disquete e quadro de chaves são relíquias, e são a pista de que há um Carlos. Eles continuam, agora cercados de tecnologia nova.
6. **Uma sala perfeita vale mais que cinco pela metade** (CLAUDE.md): um PR por sala ou par de salas.

---

## 4. Proposta por sala

Tamanho: **P** (poucas peças), **M**, **G** (muitas peças ou arte pintada). Risco é o de quebrar jogo, não o de ficar feio.

| Sala | O que muda | Peças novas | Tam. | Risco |
|---|---|---|---|---|
| **Cabine** | Igual ao vídeo: vidro das cabines com moldura ciano, monitor de tubo vira holograma sobre a mesa (o caderno), estantes de madeira viram **torres de equipamentos**, painéis ciano nas paredes, cadeira vira cadeira VR | `torre_equipamentos`, `cabine_vidro_ciano`, painel de parede | M | Baixo (sem robô nem puzzle) |
| **Balcão** | Bancada vira **balcão de atendimento** com painel e holograma; placa SILÊNCIO vira letreiro holográfico; o telefone e o quadro de chaves ficam como estão | `balcao_atendimento`, `letreiro_holografico` | M | Baixo |
| **Terminais** | Mesas com tampo holográfico, cadeiras VR; os terminais de tubo ficam (são o mundo do Carlos), cercados de telas novas | `mesa_holografica`, `monitor_plano` | M | Baixo a médio (puzzle do terminal) |
| **Corredor de serviço** | Conduítes e cabos ciano apagados nas paredes, caixas viram contêineres | `conduite_ciano`, `caixa_conteiner` | P | Baixo |
| **Manutenção** | Gerador e painel de distribuição ao lado do quadro de energia; conduítes que **pulsam em ciano quando a energia volta** | `gerador`, `painel_distribuicao` | M | Médio (puzzle da energia) |
| **Acervo sul** | Parte das estantes vira **rack de arquivo** (acervo digital), o resto fica quebrado ou vazio; um robô bibliotecário desligado, se o Davi quiser (seção 10) | `rack_arquivo`, `estante_oculos_vr` (do Bloco) | G | **Alto** (Rastreador, esconderijos, chave) |
| **Salão** | Placas pintadas viram **letreiros holográficos** (apagados até a energia voltar); parte das estantes vira rack; mesas com tampo holográfico; árvore, raízes, acampamento e musgo **ficam** | `letreiro_holografico`, `rack_arquivo`, `mesa_holografica`, `parede_servidores` | G | **Alto** (Sentinela, luz, grade, painel) |
| **Ala leste** | Mesma linguagem do salão; cabines com monitor viram cabines ciano; letreiro SAÍDA holográfico | as do salão | G | Médio (grade, porta, telefone) |

### 4.1 Peças novas (o kit da Biblioteca moderna)

| Peça | Para quê | Reaproveita |
|---|---|---|
| `torre_equipamentos` | A "torre de equipamentos entre as estantes" do vídeo | casco e vidro de `gerar_salas_futuristas.py` |
| `rack_arquivo` | Estante metálica de dados, no lugar de `estante_vazia` (mesma pegada) | `estante_oculos_vr` do Bloco |
| `parede_servidores` | Peça de parede com servidores acesos, no lugar de `parede_estante` | `parede_oculos_vr` do Bloco |
| `letreiro_holografico` | Substitui as placas pintadas e a `parede_placa` | camada de luz e varredura das lousas do Bloco |
| `mesa_holografica` | Mesa de leitura com tampo projetando | `mesa_leitura` |
| `balcao_atendimento` | Balcão do balcão, com painel | `mesa_leitura` |
| `monitor_plano`, `cabine_vidro_ciano` | Trocam o monitor de tubo e o vidro verde onde o puzzle não depende deles | `cabine` |
| `conduite_ciano`, `gerador`, `painel_distribuicao` | Serviço e manutenção | `quadro_energia` |
| `robo_bibliotecario` (opcional) | Par do professor robô: desligado na doca atrás do balcão | `parede_doca_professor` do Bloco |

Cadeira VR, óculos no chão e painel de óculos já existem (PR #113) e entram direto.

---

## 5. A tecnologia acorda com a energia

O que torna a modernização mais do que cenário: o `Progresso` já tem a marca `energia`, e o nó `VisivelComMarca` já faz coisas aparecerem, piscando, quando ela chega (as luzes de emergência do salão).

- **Antes da energia:** as peças novas aparecem **apagadas** (casco e vidro escuros). A Biblioteca parece ruína, como hoje.
- **Quando o Gabriel religa os disjuntores:** letreiros, painéis, hologramas e conduítes acendem em ciano, com as mesmas piscadas das luzes de emergência. O lugar muda diante do jogador, que é o que a fase quer ensinar ("um lugar conhecido pode mudar").
- **Exceção:** a **cabine** começa acesa, como no vídeo. Segundo o Enredo, nada fica apagado por falta de energia no mundo: é circuito desligado, e a cabine está num circuito que funciona.

Isso reaproveita a técnica das duas camadas: o corpo da peça fica sempre; a camada de luz é filha de um `VisivelComMarca`.

---

## 6. Como fazer

- **Gerador novo:** `assets/modelagem/cenario/gerar_biblioteca_moderna.py`, que importa as paletas e funções de `gerar_salas_futuristas.py` (casco, vidro, ciano, âmbar, `sobrepor`, `varredura`). Mantém o padrão: pixel art por código, determinística, comentada, sem alterar o que já existe.
- **Arte pintada (salão e ala leste):** `gerar_biblioteca.py` é importado pelo `gerar_kit.py`, então mexer nele muda o kit de todas as fases. A saída é **adicionar** funções `*_moderna` e novos arquivos (`biblioteca_fundo_moderna.png` etc.), trocar a textura nas duas cenas e **deixar os arquivos antigos até o Davi aprovar** a remoção.
- **Troca nas cenas por script**, com revisão do diff, como foi feito no Bloco: a troca de recurso e de nome de nó é mecânica; o que exige olho é a posição das peças novas.
- **Cada peça com função tem duas imagens** (corpo e luz) e o material "sem luz" na segunda.
- **Verificação em jogo:** importar o projeto pela linha de comando (`--headless --import`), carregar as 8 cenas, e capturar cada sala com e sem escuridão, como no Bloco.

---

## 7. Ordem de trabalho

Um PR por etapa, cada um mesclável sozinho:

| # | Etapa | Por que nessa ordem |
|---|---|---|
| 0 | **Decisões do Davi** (seção 10) e o guia de cor desta página | Sem isso a arte vai e volta |
| 1 | **Cabine** + as peças do kit usadas nela | É o primeiro contato, tem referência no vídeo e valida o kit sem risco |
| 2 | **Balcão** e **Terminais** | Sem robô; testam letreiro, mesa holográfica e o puzzle do terminal |
| 3 | **Corredor de serviço** e **Manutenção** | Testam a regra "acende com a energia" no puzzle mais importante |
| 4 | **Acervo sul** | Primeira sala com robô: testa a troca 1:1 e os esconderijos |
| 5 | **Salão** | A maior e a mais arriscada; só depois de o kit estar provado |
| 6 | **Ala leste** | Reusa tudo do salão |
| 7 | **Polimento**: luz geral, zumbido de servidores, tabelas desta fase, revisão pelos agentes `revisor` e `artista` | Fecha |

---

## 8. Como conferir cada PR

- [ ] As 8 cenas da Biblioteca carregam sem erro no Godot.
- [ ] A cadeia da seção 3 é jogável do começo ao fim (lanterna até a saída).
- [ ] Nas salas com robô: o robô patrulha a mesma rota e os esconderijos continuam cortando a visão.
- [ ] O que acende com a energia acende; o que não depende dela está acendido ou apagado como combinado.
- [ ] Nenhuma luz nova revela o Gabriel sem querer.
- [ ] Os itens e o papel dos disjuntores continuam legíveis na escuridão normal do jogo.
- [ ] `.import` e `.uid` novos incluídos; nada de `.godot/`.
- [ ] `docs/decisoes.md` e `docs/fases/biblioteca.md` atualizados no mesmo PR.

---

## 9. Riscos

| Risco | O que fazer |
|---|---|
| A Biblioteca ficar parecida demais com o Bloco | Manter a natureza em primeiro plano (árvore, raízes, musgo, luz do teto); o Bloco é fechado e noturno, a Biblioteca é aberta ao céu |
| Perder a leitura no escuro | Capturar cada sala e conferir os itens; subir só o contraste do que for interativo |
| Quebrar a visão dos robôs | Troca 1:1 de pegada e camada (seção 3); conferir com o `RobosDaSala` |
| Mexer em arte de outra pessoa | Pedir confirmação antes de tocar nos arquivos antigos; arquivos novos ao lado |
| Gastar o semestre só nisso | Etapas 1 a 3 já entregam a primeira impressão; 4 a 6 podem ficar para depois |

---

## 10. Decisões que preciso do Davi

| # | Pergunta | Recomendação |
|---|---|---|
| 1 | **Quanto de tecnologia?** (a) retoques: painéis e hologramas sobre a ruína, estantes de madeira ficam; (b) reforma: estantes viram racks, mais máquinas; (c) total | **(b)** nas salas fechadas (cabine, balcão, terminais, serviço, manutenção) e **(a) forte** no salão, acervo e ala leste, que são a imagem da fase |
| 2 | Os **anos 80 do Carlos** (monitores de tubo, telefone, disquete, quadro de chaves) ficam? | **Sim**, como contraponto |
| 3 | A tecnologia **acende com a energia** (seção 5)? | **Sim**, exceto a cabine |
| 4 | **Robô bibliotecário** desligado na doca atrás do balcão, par do professor? | **Sim**, uma peça, só cenário |
| 5 | Os letreiros continuam **em português** (BALCÃO, SERVIÇO, OBRAS RARAS...), agora holográficos? | **Sim** |
| 6 | **Por que a Biblioteca tem tecnologia?** O Enredo não responde (a cabine "já tem a tecnologia de 3026") | **Não escrever fala nem bilhete novo** até o Davi decidir; o plano é só visual |
| 7 | O vídeo `seg_acordar` é a **referência fixa** da cabine? | **Sim**: o jogo deve parecer a continuação do vídeo |

---

## 11. Fora do escopo

- Nova história, novos bilhetes, falas ou personagens.
- Mudar o mapa, a ordem das salas ou os puzzles da Biblioteca.
- Os outros prédios do campus (Centro de Convivência, Espaço Cultural, NAMI, Reitoria): ainda sem lugar na ordem das fases.
- A sala de obras raras (continua barrada).
- Áudio novo, além do zumbido de servidores do polimento.
