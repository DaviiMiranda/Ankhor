# Fase — Bloco de salas

> **Status:** **jogável do começo ao fim** (2026-10-11): objetivos, puzzles, robôs, a Clarice no posto e a saída. As melhorias de level design da seção 12 foram implementadas em 2026-10-12 (resumo em 12.8).
> **Área:** um bloco de salas de aula da Unifor, dois andares (no GDD: "Blocos de aula").
> **Vem de:** a porta de saída da ala leste da Biblioteca ([`biblioteca.md`](biblioteca.md)).
> **História:** o que o Bloco de salas conta segue o [Enredo Principal](../historia/enredo_principal.md) (Ato 2), que é a lei do projeto. O plano foi aprovado pelo Davi em 2026-10-11 (registro em `docs/decisoes.md`).

---

## 1. Visão geral

- **Nome do local:** Bloco de salas de aula, em 3026.
- **Ambientação:** **é noite.** Dois corredores longos, um em cima do outro, com seis salas de aula em cada. Pouca luz: o luar azulado entrando pelas janelas e pelos buracos do teto (céu escuro com estrelas, `ceu_noite.png`) e alguns lampiões espalhados. A lanterna faz diferença. O **térreo** está parcialmente enterrado na areia das dunas. No **primeiro andar** o teto caiu em vários pontos: céu, mato no chão e duas árvores crescendo no corredor. Em quase toda sala a lousa ainda está presa na parede, coberta de **tracinhos contados** em grupos de cinco.
- **Ideia da fase:** a mesma dinâmica da Biblioteca, inspirada em *Resident Evil*: portas trancadas, chaves em lugares vigiados, um cadeado de segredo com a pista espalhada pelas salas, um atalho que se abre por dentro e um caminho que obriga a ir e voltar entre os dois andares. A diferença é a **Clarice**: pela primeira vez o Gabriel encontra alguém **em pessoa**, e precisa ganhar a confiança dela.
- **O que a fase ensina de novo:**
  - **barulho como ferramenta:** fazer um robô ir para onde você quer;
  - **luz natural como perigo:** no 1º andar, o luar dos buracos do teto revela o Gabriel;
  - **o chão importa:** areia abafa os passos, entulho denuncia;
  - **atalhos:** abrir uma porta por dentro encurta a volta.

### 1.1 No Godot (o que já existe)

Uma cena por corredor e uma por sala, em `cenas/salas/bloco_de_salas/`, montadas com o kit de cenário (herdando `modelo_sala.tscn`). No menu Fases: **Bloco de salas** (abre o corredor do térreo). A porta de saída da ala leste da Biblioteca já leva ao `corredor_terreo`.

Nos dois corredores as portas ficam na mesma ordem, do oeste (onde o Gabriel chega) para o leste: salas x01 (x = 281), x02 (601), x03 (921), x04 (1401), x05 (1721), x06 (2041) e a escada (2360).

| Cena | O que é | Piso |
|---|---|---|
| `corredor_terreo` | Corredor do térreo, 2560 px (8 telas), meio enterrado na areia | lajota e areia |
| `corredor_primeiro_andar` | Corredor do 1º andar, 2560 px, teto aberto | mato e lajota |
| `sala_101` | Sala de aula futurista: oito fileiras de cadeiras com óculos VR, lousa holográfica apagada com 7 tracinhos de luz e o professor robô desligado na doca de recarga | lajota |
| `sala_102` | Invadida pela duna: chão de areia, teto caído, cadeiras VR tombadas entre montes de entulho (3 pedras), a lousa holográfica meio soterrada e o professor robô caído de costas | areia |
| `sala_103` | Barricada: cadeiras VR tombadas, estantes e o professor robô caído atravessam a sala; atrás, um acampamento com lampiões (2 pilhas). A lousa é um painel apagado com o mapa a giz da Clarice | lajota e tapete |
| `sala_104` | Laboratório de informática e de imersão: fileiras de terminais antigos com telas verdes, cadeiras VR com muitas lentes acesas e dois painéis de óculos nas paredes | tapete e lajota |
| `sala_105` | Sem janela, a mais escura: cadeiras reviradas, painel trincado, a doca vazia, o professor robô desmontado no chão e dois robôs desmontados, um lampião (2 pilhas) | lajota |
| `sala_106` | Teto desabado, uma árvore no meio do chão e o luar caindo nela; o painel e um rack de óculos tomados de musgo, o professor robô caído sob as raízes | lajota, mato e areia |
| `sala_201` | Auditório: doze fileiras de cadeiras VR com dezenas de lentes acesas, dois painéis de ensino, um professor robô na doca ao lado do palco e dois painéis de óculos | tapete |
| `sala_202` | Duas árvores furando o chão, cadeiras VR em volta, luar por cima; um rack de óculos com musgo e um professor robô na doca com raízes | mato e lajota |
| `sala_203` | Sala dos professores: oito mesas com cadeiras VR de friso âmbar, um rack de óculos, a doca de um professor robô e o quadro de avisos | tapete e lajota |
| `sala_204` | O chão cedeu: monte de entulho no meio, cadeiras VR tombadas, óculos pelo chão e um professor robô sem a cabeça na doca (1 cápsula de clarão) | lajota e areia |
| `sala_205` | Intacta demais: seis fileiras perfeitamente alinhadas, todas as lentes acesas, sem entulho, a mais clara; o painel e a doca do professor robô sem uma marca de uso. Estranha | lajota |
| `sala_206` | Depósito: corredores de estantes (metade virou rack de óculos VR), cadeiras tombadas, peças do professor robô desmontado, um lampião (1 pilha) | lajota e areia |

---

## 2. Salas e conexões (plano)

### 2.1 Mapa

```
 1º ANDAR  ══[201]══[202]══[203]══[204]══[205]══[206]══[ESCADA]══[PORTA CORTA-FOGO]──► saída
 (teto aberto)                      │ buraco no chão       ║
                                    ▼ (só desce)           ║ grade com cadeado
 TÉRREO    ══[101]══[102]══[103]══[104]══[105]══[106]══[ESCADA]
 (areia)       ▲             │
               │       posto da Clarice (sala segura)
       vem da Biblioteca
```

- O **corredor** de cada andar é o centro, como o salão da Biblioteca: quase todo caminho passa por ele, e é ali que os robôs patrulham.
- A **escada** começa fechada por uma grade de aço de enrolar (como a da Biblioteca), presa no chão com um cadeado.
- O **buraco no chão da 204** dá na **104**, logo embaixo (as duas ficam no mesmo ponto dos corredores). Ele só serve para **descer**, e vira um atalho entre os andares (seção 5.5).
- A **saída** é a **porta corta-fogo** no fim do corredor do 1º andar, depois da escada. Ela está **acorrentada** e leva à próxima fase, o **Labirinto** ([`labirinto.md`](labirinto.md)), onde Gabriel encontra o Zane.
- **Rotas de flanqueamento e pequenos circuitos:** além da espinha central dos corredores, ver a seção 12 para o detalhamento de conexões entre salas (brecha 101 ↔ 102 e trinco interno 203 ↔ 206) que transformam a topologia em um grafo com ciclos para enriquecer a navegação furtiva.

### 2.2 As salas no plano

| Sala | Papel no plano | O que tem | Esconderijos | Ameaça |
|---|---|---|---|---|
| Corredor térreo | Chegada e eixo do andar de baixo | Três setores de piso: oeste de areia (passos abafados, ×0,5), centro de lajota e tapete (×1,0) e leste de lajota solta (passos barulhentos, ×1,5) | Atrás dos montes de areia e entulho | **Rastreador** (audição) |
| 101 | Pista do código | Lousa com tracinhos (1º número do cadeado) | Debaixo das carteiras | Nenhuma |
| 102 | Chave da escada | O **molho de chaves da Clarice**, caído na areia. 3 pedras | Atrás das carteiras tombadas | O Rastreador passa na porta |
| 103 | **Posto da Clarice e da Diana** e **sala segura** | A Clarice (a Diana ainda não tem visual), o acampamento, 2 pilhas | Não precisa: a barricada protege | Nenhuma |
| 104 | Distração e fim do atalho | Os terminais acesos. Um deles tem o **teste de alarme** do bloco, que dispara a **sirene do fim do corredor** (perto da escada). No teto, o buraco que vem da 204 | Debaixo das mesas | Nenhuma |
| 105 | Respiro | 2 robôs desmontados, 2 pilhas | Atrás dos robôs desmontados | Nenhuma (os robôs desmontados não ligam) |
| 106 | Respiro | A árvore e o luar | Atrás da árvore | Nenhuma |
| Corredor 1º andar | Eixo do andar de cima | Luar pelos buracos do teto: faixas de luz e de sombra no chão. Mato e areia no oeste (passos abafados, ×0,5), lajota solta no leste (×1,5) | Na sombra das árvores do corredor | **Sentinela** (visão) |
| 201 | Pista do código | Duas lousas; a da esquerda tem os tracinhos (2º número) | Entre as fileiras | Nenhuma |
| 202 | Respiro | As duas árvores. 1 pedra | Atrás das árvores | Nenhuma |
| 203 | Cadeado de segredo | O **claviculário** (armário de chaves) com cadeado de 3 números e o **quadro de avisos** com a pista | Debaixo das mesas | Nenhuma |
| 204 | Atalho | O buraco no chão (desce para a 104). 1 cápsula de clarão | Atrás do entulho | Nenhuma |
| 205 | Pista do código e mistério | Lousa com tracinhos (3º número). A sala "intacta demais" continua sem explicação (seção 8) | Entre as fileiras | Nenhuma |
| 206 | Ferramenta da saída | O **alicate corta-corrente**, 1 pilha. Porta trancada (chave do claviculário) | Os corredores entre as estantes | **Rastreador** (audição) |

---

## 3. Objetivos e progressão

**Objetivo:** encontrar a Clarice, ganhar a confiança dela e sair do Bloco de salas pela porta corta-fogo do 1º andar.

**O obstáculo:** a escada está fechada por uma grade com cadeado, e a porta corta-fogo está acorrentada. A Clarice sabe o que cada chave abre, mas está entrincheirada no posto dela e não abre a barricada para qualquer um (abrir faz barulho, e o Rastreador escuta).

### 3.1 Passo a passo

1. **A chegada (corredor térreo).** O Gabriel sai da Biblioteca no oeste do corredor. O **Rastreador** patrulha o corredor de ponta a ponta. No oeste, a areia abafa os passos (×0,5); no leste, a lajota solta faz barulho (×1,5).
   - *O que o jogador aprende:* o chão muda o barulho dos passos.
2. **A voz nova (rádio).** Na porta da 103, o rádio chia: é de novo a **Clarice**, a voz que o guiou na Biblioteca ("Ei, você aí no corredor. Devagar com o entulho, meu filho: o robô que ronda aí escuta até pensamento."). Ela está entrincheirada na 103 e não mexe na barricada com o robô rondando a porta dela (abrir faz um barulho dos infernos). Pede ao Gabriel que tire o robô dali: na 104 tem o teste de alarme, e a sirene fica no fim do corredor; o robô vai correndo ver o que é.
3. **A distração (sala 104).** Num dos terminais acesos, o Gabriel liga o **teste de alarme**. Quando ele volta ao corredor, a **sirene do fim do corredor está tocando** e o **Rastreador está lá, investigando** (por 20 s ele não ouve mais nada). O caminho até a 103 fica livre, e a barricada da 103 se abre.
   - *O que o jogador aprende:* barulho é ferramenta, não só perigo.
4. **O posto da Clarice (sala 103).** A Clarice abre uma fresta na barricada. É o primeiro encontro **em pessoa** do jogo. Ela desconfia ("mão onde eu possa ver") e diz que perdeu o **molho de chaves** na areia da 102, quando o robô a ouviu. Sem o molho, ninguém sobe: a grade da escada está no cadeado. "Você traz o molho, eu te digo qual chave abre o quê. Isso não é pedir ajuda, é permuta."
5. **O molho (sala 102).** O molho está na areia, entre carteiras tombadas e montes de entulho. O Rastreador volta à rotina e passa pela porta da 102. As **pedras** da sala servem para atraí-lo para longe.
6. **A confiança (sala 103).** O Gabriel devolve o molho. A Clarice confia nele, tira do molho a **chave da fita azul** e entrega: "Toma: a da fita azul é a da grade da escada. Fui eu que botei a fita." Daí em diante ela **guia o Gabriel pelo rádio**, do caderno de rondas dela: diz o que cada porta precisa e avisa por onde os robôs passam. **Esta é a parte da Clarice no bloco** (Enredo, seção 3.1: "mapeou as rondas dos robôs como um grafo e sabe o que cada chave abre"), mostrada pelo que ela fala, sem papel nem item. Ela conta que a saída do bloco é a **porta corta-fogo** lá em cima, acorrentada, e que a chave do **depósito (206)**, onde fica o alicate, está no **claviculário da sala dos professores (203)**, num cadeado de segredo que ela não abriu (são mil combinações, e o robô de cima enxerga longe). Ela também conta que está ali **desde que chegou**; que a **Diana** apareceu depois e ela a acolheu; e que as duas tentam descobrir o que aconteceu com a ajuda do **Henrique** pelo rádio (ele vê o campus pelas câmeras e disse que, de alguma forma, estão em 3026). A **103 vira a sala segura** (seção 6).
7. **Subir (escada).** A **chave da fita azul** abre o cadeado da grade da escada.
8. **O 1º andar (corredor).** Assim que o Gabriel sobe, a Clarice avisa pelo rádio como o robô de cima anda ("esse não escuta, esse enxerga longe. Ele para debaixo dos buracos do teto. Passa pelo escuro."). A **Sentinela** patrulha sob os buracos do teto. As faixas de luar no chão são onde ela vê de longe; nas sombras e no mato o Gabriel passa.
   - *O que o jogador aprende:* a luz do céu também denuncia, não só a lanterna.
9. **O cadeado (sala 203).** O claviculário tem um cadeado de **3 números**. No quadro de avisos, um papel: **"Conferir a contagem: 101 · 201 · 205"**. O Gabriel precisa **contar os tracinhos** das lousas dessas três salas. Duas estão no 1º andar; a **101 fica lá embaixo**, e é preciso descer de novo.
   - *O que o jogador aprende:* olhar o cenário com atenção; voltar faz parte.
10. **O depósito (sala 206).** O claviculário dá a **chave do depósito**. Lá dentro, entre corredores de estantes, um **Rastreador** escuta. No fundo, o **alicate corta-corrente**.
11. **A virada.** Quando o Gabriel pega o alicate, a **Clarice** avisa pelo rádio, com o que o **Henrique** vê pelas câmeras, que a máquina de cima "mudou de ronda". A **Sentinela passa a cobrir o trecho entre a 206 e a escada**, justamente o caminho de volta.
12. **O atalho (opcional, salas 204 e 104).** Pelo buraco no chão da 204, o Gabriel pode **descer direto para a 104**, longe da Sentinela e da escada. É mão única: só desce. Serve para voltar rápido ao posto da Clarice e salvar.
13. **Saída (porta corta-fogo).** No fim do corredor do 1º andar, o Gabriel corta a corrente com o alicate. Antes de sair, o rádio da Clarice se despede ("Então vai. Eu fico: ainda não fechei o mapa das rondas. Qualquer coisa, chama no rádio."). A Clarice **fica** no posto dela.

### 3.2 Grafo de dependências

```
rádio da Clarice → alarme da 104 → posto da Clarice → molho (102) → chave da fita azul → grade da escada
                                                                                              ↓
saída ← corrente cortada ← alicate (206) ← chave do depósito ← cadeado do claviculário ← tracinhos (101, 201, 205)
```

O atalho 204 → 104 é **opcional**: fica fora da cadeia principal.

Para a apresentação da disciplina, é o mesmo modelo da Biblioteca: salas são **vértices**, portas são **arestas**, cada cadeado é uma condição numa aresta e a ordem de solução é uma **ordenação topológica** do grafo de dependências. A novidade é a distração da 104: o teste de alarme é um evento sonoro que atravessa as salas (104 → corredor) e chega ao Rastreador, que vai investigar a sirene. Dentro de uma sala, o robô ouve passos e pedras pela **BFS** na grade (ver [`../computacao/grafos_e_navegacao.md`](../computacao/grafos_e_navegacao.md)).

### 3.3 Itens

| Item | Onde | Para quê |
|---|---|---|
| Molho de chaves | 102, na areia | Devolver à Clarice (confiança). O molho fica com ela |
| Chave da fita azul | 103, entregue pela Clarice | Abrir a grade da escada |
| Código do claviculário (**738**) | Tracinhos das lousas da 101 (7), 201 (3) e 205 (8) | Abrir o claviculário (203) |
| Chave do depósito | Claviculário (203) | Abrir a 206 |
| Alicate corta-corrente | 206 | Cortar a corrente da porta corta-fogo |
| Cápsula de clarão | 204 (já está lá) | Defesa |
| Pedras | 102 (3, já estão lá) e 202 (1) | Distração |
| Pilhas | 103 (2), 105 (2), 206 (1) | Lanterna |
| Rádio | Corredor do térreo, na chegada | Só aparece se o Gabriel ainda não tem (quem começa pelo menu Fases). Sem ele, as transmissões não tocam |

---

## 4. Robôs e ameaças

| Robô | Onde | Sentido forte | Rota |
|---|---|---|---|
| **Rastreador** | Corredor do térreo | Audição | Vai e volta pelo corredor inteiro. Depois do alarme (passo 3), fica 20 s investigando a sirene, no fim do corredor, sem ouvir mais nada, e depois volta à rota |
| **Sentinela** | Corredor do 1º andar | Visão | Antes do alicate: ronda entre a 202 e a 204, parando debaixo dos buracos do teto. Depois do alicate (passo 11): ronda entre a 203 e a porta corta-fogo, passando pela 206 e pela escada |
| **Rastreador** | Depósito (206) | Audição | Circula entre os corredores de estantes |

- **O chão:** nos corredores, no setor oeste de **areia** (ou **mato**) o alcance do som dos passos cai pela metade (×0,5), e no setor leste de **lajota solta** ele sobe a 150% (×1,5). Dentro das salas o fator é 1 (ver [`../mecanicas/movimentacao_e_terreno.md`](../mecanicas/movimentacao_e_terreno.md) e a seção 12.7).
- **O luar:** no 1º andar, as faixas de luz dos buracos do teto funcionam como as luzes de emergência da Biblioteca: quem está nelas é visto de mais longe.
- **Salas sem robôs:** todas as salas de aula, menos a 206. São os respiros entre os corredores.
- Ser pego dá game over e volta ao último checkpoint.

---

## 5. Puzzles

### 5.1 A distração (104)

- **Como funciona:** um terminal da 104 (com um LED vermelho piscando) tem o **teste de alarme**. Ligar arma a sirene do fim do corredor e marca `alarme_104`, que libera a barricada da 103.
- **Mecânica:** cada sala é uma cena, então o efeito é guardado até o Gabriel voltar ao corredor. Ao carregar, a `Sirene` toca por 20 s e chama `distrair()` nos robôs da sala: o Rastreador já está nela (correu para lá enquanto o Gabriel estava na 104) e fica investigando, ignorando outros barulhos. Dá para ligar o teste de novo quantas vezes precisar.
- **Solução:** ligar o alarme, voltar ao corredor e ir até a 103 enquanto a sirene toca.

### 5.2 O molho (102 e 103)

- **Como funciona:** busca de item numa sala por onde o robô passa, e troca de itens com um personagem.
- **Solução:** achar o molho, distrair o Rastreador com pedras se precisar, devolver o molho à Clarice, que entrega a chave da grade.

### 5.3 Os tracinhos (101, 201, 205 → 203)

- **Como funciona:** as lousas da 101, 201 (a da esquerda) e 205 têm poucos tracinhos, fáceis de contar: **7, 3 e 8**. Olhar a lousa também diz a contagem. O bilhete no quadro de avisos da 203 diz a ordem: **101 · 201 · 205**.
- **Mecânica:** o painel de código da Biblioteca (`painel_codigo.tscn`), sem precisar de energia, com o desenho do claviculário. Ao abrir, ele dá a chave do depósito.
- **Solução:** digitar **738**.
- As outras lousas do bloco continuam com os 25 tracinhos de antes.

### 5.4 A corrente (206 → porta corta-fogo)

- **Como funciona:** a porta de saída tem uma corrente com cadeado; o alicate é a "chave".
- **Mecânica:** porta com `chave` (o alicate é um item como a chave da manutenção). O primeiro uso só corta a corrente (som e aviso, e o rádio da Clarice se despede); o segundo atravessa a porta e termina a fase.

### 5.5 O atalho (204 → 104)

- **Como funciona:** o buraco no chão da 204 é uma passagem de mão única: o Gabriel desce e cai entre as mesas da 104, logo embaixo, com o som da queda. É uma `Porta` que leva a um ponto de chegada sem volta.
- **Para que serve:** encurtar a volta ao posto da Clarice (salvar) e fugir da Sentinela depois da virada.

---

## 6. Sala segura

- **Sala segura:** o **posto da Clarice (103)**. A barricada protege, e os robôs não entram. Tem um checkpoint ao lado da Clarice. Há outro na chegada do corredor do térreo.
- **Por que aqui:** fica no meio do térreo, perto da escada e do atalho, e é o lugar para onde o Gabriel volta depois de cada parte difícil.
- **O sonho:** o que os sonhos mostram está pendente no Enredo (seção 10.5).

---

## 7. Registros

| Registro | Onde | Quem | Arquivo |
|---|---|---|---|
| **1ª transmissão da Clarice** (pede para tirar o robô da porta) | Corredor térreo, perto da 103 | Clarice, pelo rádio | `dados/transmissoes/clarice_01.tres` |
| **Conversa no posto** (pede o molho) e o lembrete | 103 | Clarice, em pessoa | `dados/dialogos/clarice_bloco_pede_molho.json`, `clarice_bloco_pede_molho_de_novo.json` |
| **Troca** (devolve o molho, ganha a chave e as dicas) | 103 | Clarice, em pessoa | `dados/dialogos/clarice_bloco_devolve_chave.json` |
| **Conversa de depois** (claviculário, andar de cima) | 103 | Clarice, em pessoa | `dados/dialogos/clarice_bloco_de_novo.json` |
| **Como o robô de cima anda** | Topo da escada | Clarice, pelo rádio | `dados/transmissoes/clarice_02.tres` |
| **Bilhete do quadro de avisos** ("Conferir a contagem - 101 · 201 · 205") | 203 | Em aberto | na cena `sala_203` |
| **Aviso de ronda nova** | Porta da 206, depois do alicate | Clarice, pelo rádio (com o que o Henrique vê) | `dados/transmissoes/clarice_04.tres` |
| **Despedida** | Porta corta-fogo, ao cortar a corrente | Clarice, pelo rádio | `dados/transmissoes/clarice_03.tres` |

As falas são definitivas e seguem a ficha da Clarice (gírias dos anos 90, deboche, explica tudo como lógica, não pede ajuda; sem as falas de loop da versão antiga).

---

## 8. A sala 205

A sala "intacta demais" entra no puzzle só como uma das lousas. **Por que ela está intacta** fica sem explicação nesta fase, como a porta barrada das obras raras na Biblioteca: um gancho para depois. O motivo é decisão de história e não está no Enredo.

---

## 9. Como foi construído

| O quê | Como |
|---|---|
| Portas trancadas | `porta.gd`. Campos novos: `aviso_destrancada`, `marca_ao_destrancar`, `atravessa_ao_destrancar` (a grade e a corrente só destrancam no primeiro uso) e `som_destrancar` |
| Marcas da fase (autoload `Progresso`) | `alarme_104`, `molho_devolvido`, `escada_destrancada`, `claviculario_aberto`, `alicate`, `corrente_cortada` |
| Alarme da 104 | `cenas/sistemas/terminal_alarme.tscn` e `cenas/sistemas/sirene.tscn` (`terminal_alarme.gd`, `sirene.gd`). O robô ganhou `distrair(onde, segundos)` |
| Clarice na 103 | `cenas/personagens/clarice_posto.tscn`: a Clarice parada (`clarice_em_pe.tscn`) e a `ConversaComTroca` (`conversa_com_troca.gd`), que escolhe a conversa pelo progresso e, no fim da troca, tira o molho e dá a chave (`Inventario.remover`, novo) |
| Claviculário | `painel_codigo.tscn` com `marca_energia` vazia (sem energia), `texto_visor` e `item_ao_abrir` (campos novos) |
| Grade da escada | `grade_seguranca.tscn` com a textura `grade_escada.png`, que sobe com a marca `escada_destrancada` |
| Corrente da porta corta-fogo | `VisivelComMarca` com `some_com_marca` (novo): some quando a corrente é cortada |
| Luar que revela | `VisivelComMarca` com `marca` vazia (sempre acesa) e `revela_quem_passa`: quatro faixas de luz no chão do 1º andar |
| Alicate que muda a ronda | `item_no_chao.gd` com `marca_ao_pegar` (novo) = `alicate`, que é a `marca_da_rota` da Sentinela |
| Transmissões que esperam uma marca | `gatilho_transmissao.gd` com `marca_necessaria` (novo) |
| Fim da fase | `cenas/salas/bloco_de_salas/fim_do_bloco.tscn`: a `SaidaFase` com `sair_ao_carregar` (novo), que mostra "Você saiu do bloco" e leva ao Labirinto (`cenas/salas/labirinto.tscn`) |
| Itens novos | `dados/itens/molho_de_chaves.tres`, `chave_grade.tres`, `chave_deposito.tres`, `alicate.tres` |
| Arte nova | `assets/modelagem/cenario/gerar_objetos_bloco_de_salas.py` (ícones, claviculário, grade, corrente, buraco, sirene) e `gerar_kit.py` (lousas `parede_lousa_0`, `_3`, `_7`, `_8`) |
| Sons novos | `assets/modelagem/audio/gerar_efeitos_bloco_de_salas.py`: sirene (em loop), queda e corrente cortada |
| Melhorias da seção 12 | Ver a tabela da seção 12.8 |

---

## 10. Decidido e em aberto

Aprovado pelo Davi em 2026-10-11: o posto é a **103** e quem fica nele é a **Clarice** (o Rafael saiu da história no mesmo dia: ver `docs/decisoes.md`); a saída é a **porta corta-fogo** do 1º andar, que leva à próxima fase (na época o Centro de Convivência; desde 2026-10-14, o **Labirinto**); não existe livro de ocorrências; o notebook não entra nesta fase.

Continua em aberto (Enredo, pendências): por que a sala 205 está intacta.

---

## 11. Peças do kit criadas para este bloco

Em `assets/modelagem/cenario/gerar_kit.py` (servem para qualquer sala):

| Peça | Cena |
|---|---|
| Lousa com restos de giz e tracinhos | `cenas/cenario/paredes/parede_lousa.tscn` |
| Quadro de avisos de cortiça | `cenas/cenario/paredes/parede_mural.tscn` |
| Escada subindo (térreo) e descendo (1º andar) | `parede_escada_sobe.tscn`, `parede_escada_desce.tscn` |
| Carteira universitária, em pé e tombada | `cenas/cenario/objetos/carteira.tscn`, `carteira_caida.tscn` |

Os números das salas em cima das portas são `Label` com a fonte do jogo, dentro de `Paredes`.

---

## 12. Propostas e Sugestões de Melhorias de Design de Níveis

As propostas abaixo mantêm total fidelidade ao enredo já aprovado (a Clarice na 103 com a Diana, os 4 puzzles principais, a saída na porta corta-fogo e a chegada à fase seguinte, hoje o Labirinto), focando em refinar o **ritmo**, a **liberdade de escolha do jogador no espaço**, a **legibilidade sensorial (avisos antecipados)** e os **requisitos acadêmicos de computação gráfica e estruturas de dados**.

### 12.1 Diagnóstico do Design Atual

1. **Topologia em "Espinha de Peixe" (Árvore com ramos sem saída):** Quase todas as salas (com exceção do atalho vertical 204 → 104) são nós-folha com apenas uma entrada e saída voltadas para o mesmo corredor. Se o robô estiver patrulhando em frente à porta, o jogador fica encurralado na sala sem escolhas táticas além de esperar passivamente ou gastar recursos escassos (pedras).
2. **Monotonia Linear dos Corredores (2560 px / 8 telas):** Os corredores são retilíneos e extensos. Em um jogo 2.5D, uma perseguição em linha reta tão longa sem quebras arquitetônicas ou abrigos intermediários pode gerar frustração ou previsibilidade.
3. **Saída Cega da Sala Segura (103):** Ao abrir a barricada da sala segura para retornar ao corredor do térreo, o jogador não tem como espiar o corredor com antecedência. Se o Rastreador estiver passando bem na porta, pode ocorrer uma detecção punitiva imediata.
4. **Isolamento Sensorial Entre Pisos:** O térreo e o 1º andar operam como camadas quase desconectadas até o momento em que a grade da escada é aberta, sem antecipação tática do que está acima.

---

### 12.2 Proposta 1: Pequenos Circuitos e Rotas de Flanqueamento (Grafos com Ciclos)

Em jogos de terror e furtividade inspirados em *Resident Evil* e *Alien: Isolation*, a existência de pequenos caminhos circulares enriquece a tomada de decisão. Propõe-se criar duas conexões orgânicas entre salas:

```
 1º ANDAR  ══[201]══[202]══[203]════════[204]══[205]══[206]══[ESCADA]══[CORTA-FOGO]──► saída
                            │ (trinco interno)  │       │
                            └───────────────────┼───────┘ (desbloqueio após alicate)
                                                ▼ (queda 204→104)
 TÉRREO    ══[101]──────[102]══[103]══[104]══[105]══[106]══[ESCADA]
               └──(brecha)──┘
```

1. **Brecha na Alvenaria entre 101 e 102 (Flanqueamento da Duna):**
   - **Cenário:** O peso da duna de areia na sala 102 derrubou parte da parede divisória com a 101, deixando uma passagem baixa por baixo de uma lousa retorcida.
   - **Utilidade no Design de Níveis:** Na busca pelo molho de chaves da Clarice na 102, caso o Rastreador esteja rondando o corredor na altura da 102, o jogador pode entrar na 101, atravessar a brecha para a 102 em silêncio (chão de areia), recolher o molho e sair pela 101, contornando a rota do robô.
2. **Trinco Interno do Almoxarifado entre 203 e 206:**
   - **Cenário:** A sala dos professores (203) e o depósito (206) compartilham uma porta de armário/arquivo de serviço. Essa porta começa trancada pelo lado de dentro da 206 com uma alavanca metálica simples.
   - **Utilidade no Design de Níveis:** Quando Gabriel pega o alicate na 206 e a Sentinela muda sua rota para patrulhar agressivamente entre a 206 e a escada (a Virada), o jogador pode destravar o trinco da porta de serviço e escapar de volta para a 203. De lá, ele pode acessar o atalho da 204 sem se expor no corredor iluminado do 1º andar.

---

### 12.3 Proposta 2: Zoneamento dos Corredores e Nichos de Cobertura

Para quebrar a monotonia dos 2560 px de corredor e criar ritmo de tensão e alívio:

1. **Três Setores Arquitetônicos Claros:**
   - **Setor Oeste (Salas x01-x02) — "O Setor Soterrado":** Montes de areia e dunas invadindo o piso. Passos completamente abafados. Teto do 1º andar ruiu, com troncos de árvores e raízes que bloqueiam linhas de visão diretas.
   - **Setor Central (Salas x03-x04) — "O Ponto de Apoio":** Corredor intermediário com piso de lajota mista e tapetes desbotados. Onde se localizam o posto da Clarice e a porta do laboratório 104. Placas de salas legíveis e painéis informativos intactos.
   - **Setor Leste (Salas x05-x06 + Escada) — "A Ala Industrial e de Serviço":** Lajota limpa e ressonante. Cada passo descuidado ecoa pelo corredor. É a área de maior risco sonoro no térreo e de maior exposição visual no 1º andar.
2. **Nichos de Parede (Bebedouros e Armários Empilhados):**
   - Inserir 2 nichos reentrantes ao longo de cada corredor (espaços onde ficavam bebedouros ou armários de vestiário desativados).
   - O Gabriel pode recuar para a sombra do nicho e permanecer agachado enquanto um robô passa de costas pelo corredor, sem a necessidade de mudar de sala para se esconder.

---

### 12.4 Proposta 3: Dinâmica da Sala Segura (Posto da 103) e Fresta de Espiar

1. **Fresta de Observação da Barricada (`[E] Espiar Corredor`):**
   - Na barricada de carteiras da 103, há uma fresta entre as madeiras que permite ao Gabriel olhar o corredor do térreo antes de pedir para a Clarice abrir a passagem.
   - A câmera desliza suavemente para o corredor através da fresta, mostrando a iluminação e se o Rastreador está nas proximidades. Isso evita mortes injustas na saída.
2. **Mural Tático de Giz:**
   - Na lousa da 103, além do acampamento com lampiões, a Clarice desenhou um rascunho de giz da planta baixa do bloco com anotações lógicas ("escada trancada - grade", "sirene no leste", "depósito no 1º"). Serve como mapa visual, dentro do próprio cenário, para o jogador.

---

### 12.5 Proposta 4: Ritmo Vertical e Aviso Sensorial entre os Pisos

1. **Resposta Sonora e Visual do Andar Superior:**
   - Enquanto Gabriel explora o térreo, a movimentação da Sentinela ou de máquinas pesadas no 1º andar faz as lajes estalarem: poeira de gesso cai do teto em pontos específicos.
   - Esse aviso antecipado informa ao jogador que há perigo ativo no piso de cima antes mesmo de ele subir a escada.
2. **Interação Sonora no Buraco de Queda (204 → 104):**
   - **Arremesso de Distração:** Gabriel pode jogar uma pedra pelo buraco da 204 para que ela caia no chão da 104. O impacto do som da pedra atrai o Rastreador do térreo para dentro da 104, permitindo liberar o corredor de baixo antes da descida. Como cada sala é uma cena com a sua grade, o som da pedra é repassado à 104 por evento, como o da sirene (seção 5.1).
   - **Amortecimento por Mobiliário:** Na 104, Gabriel cai sobre uma pilha de caixas de papelão e cadeiras de espuma tombadas, gerando um som abafado característico em vez de um estalo estrondoso, recompensando o jogador pelo uso do atalho planejado.

---

### 12.6 Proposta 5: Atmosfera e Narrativa Ambiental da Sala 205

A sala 205 continua misteriosa conforme o Enredo Principal (sem explicação imediata), mas o projeto do nível pode amplificar o suspense:
- **Contraste de Iluminação e Som:** Ao entrar na 205, o ruído ambiente de vento e estalos de ruína cessa subitamente. A iluminação é estável e límpida, com uma lâmpada fluorescente que emite um zumbido limpo e contínuo de 60 Hz.
- **Geometria Impecável:** Todas as carteiras estão alinhadas a laser em grade ortogonal perfeita; a lousa está limpa sem manchas antigas de giz, contendo apenas os 8 tracinhos gravados de forma geométrica exata. Isso gera inquietação no jogador sem violar a pendência narrativa.

---

### 12.7 Formalização Acadêmica para a Disciplina de Computação Gráfica

Para a defesa técnica e os relatórios da disciplina, o Bloco de salas demonstra conceitos fundamentais de computação. O item 1 é o modelo de projeto, e os itens 2 a 4 estão no jogo desde 2026-10-12 (seção 12.8). Os números vêm de `scripts/personagens/robo.gd`, das cenas `robo_sentinela.tscn` e `robo_rastreador.tscn` e das `ZonaDePiso` dos dois corredores.

1. **Modelagem em grafo ponderado $G = (V, E, W)$ (modelo de projeto):**
   - **Vértices ($V$):** salas ($101 \dots 106, 201 \dots 206$), setores dos corredores ($C_{T1}, C_{T2}, C_{T3}$ no térreo; $C_{A1}, C_{A2}, C_{A3}$ no 1º andar) e nós de conexão especial (escada, porta corta-fogo).
   - **Arestas ($E$):** portas, atalho vertical direcionado ($204 \to 104$), brecha de flanqueamento ($101 \leftrightarrow 102$) e passagem de serviço ($203 \leftrightarrow 206$, que começa trancada e tem o trinco do lado da 206).
   - **Pesos ($W$):** a mesma fórmula do documento [`grafos_e_navegacao.md`](../computacao/grafos_e_navegacao.md):
     $$W(u, v) = \text{Distância}(u, v) \times \text{FatorPiso}(u, v)$$
   - **No código**, os robôs andam por A* em grade (heurística octile, diagonal só sem obstáculo), sem pesar o piso, e patrulham uma sequência de pontos fixos, que muda com a marca do alicate. O fator de piso da fórmula entra no jogo só no som, como o `fator_ruido` das `ZonaDePiso` (item 3). O grafo de salas é o modelo de projeto, e o grafo de dependências dos puzzles está na seção 3.2 (ordenação topológica).
2. **Campo de visão 2D por produto escalar (implementado):**
   - Gabriel não é percebido enquanto estiver escondido num nicho (parado por $0{,}4$ s e sem lanterna); a audição e o contato continuam valendo. Fora do nicho, ele é percebido se estiver a até $20$ px do robô (percepção por proximidade) ou se
     $$\lVert \vec{p}_{\text{gabriel}} - \vec{p}_{\text{robô}} \rVert \le R \quad \text{e} \quad \frac{(\vec{p}_{\text{gabriel}} - \vec{p}_{\text{robô}}) \cdot \vec{d}}{\lVert \vec{p}_{\text{gabriel}} - \vec{p}_{\text{robô}} \rVert} \ge \cos\left(\frac{\theta}{2}\right) \quad \text{e} \quad \text{LinhaLivre}(\vec{p}_{\text{robô}}, \vec{p}_{\text{gabriel}})$$
     onde $\vec{d}$ é a direção do olhar e `LinhaLivre` é um raio contra a camada de paredes.
   - $R$ e $\theta$ dependem do tipo de robô, e $R$ é multiplicado quando há luz:

     | Robô | $R$ | $\theta$ | $R$ com luz |
     |---|---|---|---|
     | Sentinela | 170 px | 60° | 289 px (×1,7) |
     | Rastreador | 80 px | 100° | 104 px (×1,3) |

   - "Há luz" quer dizer: a lanterna (ou o notebook) acesa, ou Gabriel a menos de 56 px de uma luz que revela (luar, luz de emergência).
3. **Propagação sonora por BFS e fator de piso (os dois implementados):**
   - **Base:** cada passo de Gabriel gera um evento com alcance-base $A_0$ de $5$ células andando e $14$ correndo (célula de $16$ px). O alcance de cada robô é
     $$A = \lfloor A_0 \cdot f_{\text{piso}} \cdot f_{\text{audição}} \rfloor$$
     com $f_{\text{audição}} = 0{,}5$ na Sentinela e $1{,}8$ no Rastreador. Uma busca em largura (BFS, vizinhança de 4) parte da célula do som, anda só por células livres e para depois de $A$ passos. O robô que estiver numa célula alcançada vai investigar. Os obstáculos da sala (paredes e móveis) bloqueiam o som por completo, e o corte é por número de passos, sem decaimento em dB.
   - **A grade é por sala:** cada sala é uma cena com a sua grade, então a BFS acontece dentro dela. O som que passa de uma sala para outra é repassado por evento, como descrito na seção 5.1: a sirene da 104 e a pedra pelo buraco da 204, que deixa o Rastreador do térreo $18$ s dentro da 104 (mais $4$ s para sair da sala).
   - **Fator de piso $f_{\text{piso}}$, por setor do corredor:** cada corredor (térreo e 1º andar) tem três faixas de chão, cada uma com uma `ZonaDePiso` de $90$ px de altura. Fora das zonas, dentro das salas, o fator é $1$.

     | Setor | Eixo x da cena | Piso (térreo / 1º andar) | $f_{\text{piso}}$ |
     |---|---|---|---|
     | Oeste (salas x01 e x02) | 0 a 768 px | areia / mato e areia | $0{,}5$ |
     | Centro (x03 e x04) | 768 a 1536 px | lajota e tapete | $1{,}0$ |
     | Leste (x05, x06 e escada) | 1536 a 2560 px | lajota solta | $1{,}5$ |

     Isso realiza a regra que o jogo anuncia: a areia abafa e o chão solto denuncia (`movimentacao_e_terreno.md`). No código, `ZonaDePiso.fator_em` devolve o fator da zona que contém o ponto (ou $1$), e `robo.gd` o multiplica pela base em `_ao_ouvir_passo`; `ouvir_barulho` aplica $f_{\text{audição}}$ e trunca para inteiro.
   - **Efeito**, em células ($16$ px cada), andando e correndo:

     | Robô | Oeste (×0,5) | Centro (×1,0) | Leste (×1,5) |
     |---|---|---|---|
     | Sentinela | 1 e 3 | 2 e 7 | 3 e 10 |
     | Rastreador | 4 e 12 | 9 e 25 | 13 e 37 |

   - **Limites:** o fator é por zona (um retângulo do corredor), não por peça de chão, e vale só nos corredores. As salas de chão de areia ou mato (102, 106, 202, 204 e 206) têm fator $1$.
4. **Ciclos fundamentais e conectividade (implementados):**
   - As duas arestas novas criam dois ciclos, $101$–$102$–corredor e $203$–$206$–corredor, e dão uma rota alternativa de fuga nesses pares de salas.
   - As demais salas ($103$, $105$, $106$, $201$, $202$, $205$) continuam com uma só porta, e a $104$ ganha apenas a entrada de descida ($204 \to 104$). É uma melhoria local: o grafo não passa a ter dois caminhos disjuntos para toda sala, e é assim que deve ser apresentada.

### 12.8 O que foi implementado (2026-10-12)

Todas as propostas acima entraram no jogo. Onde a implementação precisou de uma escolha que o texto não fazia, ela está na coluna "Como ficou".

| Proposta | Como ficou | Onde |
|---|---|---|
| Brecha 101 ↔ 102 | Uma brecha na parede lateral: a da direita da 101 e a da esquerda da 102, na mesma altura (y = 272). Apertar `E` passa para a outra sala, como numa porta | `parede_lateral_brecha.tscn` e a `Porta` "Brecha" nas duas salas |
| Porta de serviço 203 ↔ 206 | Uma porta de serviço nas paredes laterais (a direita da 203 e a esquerda da 206). Começa trancada; do lado do depósito há o trinco: o primeiro `E` na 206 destranca (marca `trinco_206`) sem atravessar, o segundo atravessa. Da 203, sem o trinco puxado, aparece "Trancada pelo outro lado" | `parede_lateral_porta.tscn` e a `Porta` "PortaDeServico", com o campo novo `trinco_deste_lado` |
| Três setores nos corredores | O chão dos dois corredores foi trocado por setor: oeste (salas x01 e x02) de **areia** no térreo e **mato** no 1º andar; centro (x03 e x04) de **lajota e tapete** alternados; leste (x05, x06 e a escada) de **lajota solta** | as peças `Chao1` a `Chao20` dos corredores |
| Fator de piso no som | Cada setor tem uma `ZonaDePiso` com o fator de ruído: oeste **0,5**, centro **1,0**, leste **1,5**. O alcance do passo é $A = \lfloor A_0 \cdot f_{\text{piso}} \cdot f_{\text{audição}} \rfloor$ (a tabela da seção 12.7). Fora das zonas (dentro das salas) o fator é 1 | `scripts/sistemas/zona_de_piso.gd`; `robo.gd` lê o fator em `_ao_ouvir_passo` |
| Nichos de cobertura | Dois nichos por corredor (um com bebedouro, outro com armários): no térreo nos x 1280 e 1920, no 1º andar nos mesmos x, longe das faixas de luar. Ficar **parado** no nicho, com a lanterna apagada, por 0,4 s esconde o Gabriel (ele fica azulado): os robôs não o veem. Andar, ou acender a lanterna, revela. Um robô que encoste nele ainda ataca | `parede_nicho_bebedouro.tscn`, `parede_nicho_armario.tscn`, `cenas/sistemas/nicho_esconderijo.tscn` (`nicho_esconderijo.gd`) e `Gabriel.esconder()` |
| Fresta da barricada (103) | Ao lado da porta da 103, "Espiar o corredor". O jogo abre o corredor com o Gabriel escondido atrás da porta (sem corpo e invisível para os robôs) e a câmera desliza para os dois lados. `E` (ou para baixo) sai para o corredor de verdade; para cima volta para a 103. O que se vê é o corredor que o jogador vai encontrar ao sair | `fresta_da_barricada.tscn` e `Porta.espiar()` |
| Mural de giz (103) | A lousa da 103 virou o mapa do bloco desenhado pela Clarice (`parede_lousa_mapa`), com as anotações no aviso "Olhar a lousa" | `sala_103.tscn` |
| Estalos no teto do térreo | Cinco pontos no corredor do térreo (x 600, 1000, 1300, 1800 e 2200) que, de tempos em tempos (12 a 28 s), estalam e soltam poeira de gesso, se o Gabriel estiver a menos de 280 px | `cenas/sistemas/estalo_do_teto.tscn` (`estalo_do_teto.gd`) e o som `estalo_laje.wav` |
| Pedra pelo buraco (204 → 104) | Uma pedra que cai no buraco da 204 faz barulho na 104: por 18 s o Rastreador do térreo fica **dentro** da 104, investigando onde ela caiu. No corredor ele some nesse tempo (e mais 4 s, o tempo de sair da sala) e depois volta pela porta da 104. Quem descer pelo buraco nesse tempo cai perto dele | `cenas/sistemas/buraco_no_chao.tscn` (`buraco_no_chao.gd`), `robo_atraido_pelo_buraco.gd` no corredor e na 104, e `pedra_arremessada.gd` |
| Queda amortecida | Embaixo do buraco, na 104, um monte de caixas de papelão e assentos de espuma; a descida toca um baque abafado | `caixas_queda.png` e `queda_abafada.wav` |
| Sala 205 | A lousa ficou limpa, com os oito tracinhos iguais e no mesmo espaçamento (`parede_lousa_8_limpa`); uma calha fluorescente acesa (`parede_fluorescente`) e duas luzes frias estáveis, sem tremer; as carteiras alinhadas em grade; e o zumbido de 60 Hz em loop (`zumbido_60hz.wav`). O mistério continua sem explicação | `sala_205.tscn` |

**Limites conhecidos:**
- O robô "dentro da 104" é contado em tempo real (`Time.get_ticks_msec`), não em tempo de jogo: se o jogador pausar, a janela de 18 s continua correndo.
- Os estalos do teto são sorteados: o 1º andar não roda enquanto o Gabriel está no térreo, então eles não seguem a posição real da Sentinela.
- O nicho esconde da visão, não do contato: se a rota do robô passar colada à parede, ele esbarra no Gabriel.

