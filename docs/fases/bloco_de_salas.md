# Fase — Bloco de salas

> **Status:** cenário e portas jogáveis. **Planejamento de objetivos e puzzles proposto em 2026-10-11, aguardando aprovação do Davi** (seções 3 a 9). Depois de aprovado, é implementado.
> **Área:** um bloco de salas de aula da Unifor, dois andares (no GDD: "Blocos de aula").
> **Vem de:** a porta de saída da ala leste da Biblioteca ([`biblioteca.md`](biblioteca.md)).
> **História:** o que o Bloco de salas conta segue o [Enredo Principal](../historia/enredo_principal.md) (Ato 2), que é a lei do projeto. O objetivo desta fase era uma pendência do Enredo (seção 12.5); o que está aqui é uma **proposta**.

---

## 1. Visão geral

- **Nome do local:** Bloco de salas de aula, em 3026.
- **Ambientação:** **é noite.** Dois corredores longos, um em cima do outro, com seis salas de aula em cada. Pouca luz: o luar azulado entrando pelas janelas e pelos buracos do teto (céu escuro com estrelas, `ceu_noite.png`) e alguns lampiões espalhados. A lanterna faz diferença. O **térreo** está parcialmente enterrado na areia das dunas. No **primeiro andar** o teto caiu em vários pontos: céu, mato no chão e duas árvores crescendo no corredor. Em quase toda sala a lousa ainda está presa na parede, coberta de **tracinhos contados** em grupos de cinco.
- **Ideia da fase:** a mesma dinâmica da Biblioteca, inspirada em *Resident Evil*: portas trancadas, chaves em lugares vigiados, um cadeado de segredo com a pista espalhada pelas salas, um atalho que se abre por dentro e um caminho que obriga a ir e voltar entre os dois andares. A diferença é o **Rafael**: pela primeira vez o Gabriel encontra alguém **em pessoa**, e precisa ganhar a confiança dele.
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
| `sala_101` | Sala de aula comum: oito fileiras de carteiras, lousa, mesa do professor | lajota |
| `sala_102` | Invadida pela duna: chão de areia, teto caído, carteiras tombadas entre montes de entulho (3 pedras) | areia |
| `sala_103` | Barricada: carteiras tombadas e estantes atravessam a sala; atrás, um acampamento com lampiões (2 pilhas) | lajota e tapete |
| `sala_104` | Laboratório de informática: fileiras de terminais; telas ainda acesas, verdes | tapete e lajota |
| `sala_105` | Sem janela, a mais escura: carteiras reviradas, dois robôs desmontados, um lampião (2 pilhas) | lajota |
| `sala_106` | Teto desabado, uma árvore no meio do chão e o luar caindo nela | lajota, mato e areia |
| `sala_201` | Auditório: doze fileiras de carteiras, duas lousas | tapete |
| `sala_202` | Duas árvores furando o chão, carteiras em volta, luar por cima | mato e lajota |
| `sala_203` | Sala dos professores: oito mesas, estantes, quadro de avisos | tapete e lajota |
| `sala_204` | O chão cedeu: monte de entulho no meio, carteiras tombadas (1 cápsula de clarão) | lajota e areia |
| `sala_205` | Intacta demais: seis fileiras perfeitamente alinhadas, sem entulho, a mais clara. Estranha | lajota |
| `sala_206` | Depósito: corredores de estantes, carteiras empilhadas, um lampião (1 pilha) | lajota e areia |

---

## 2. Salas e conexões (plano)

### 2.1 Mapa

```
 1º ANDAR  ══[201]══[202]══[203]══[204]══[205]══[206]══[ESCADA]══[PORTA CORTA-FOGO]──► saída
 (teto aberto)                      │ buraco no chão       ║
                                    ▼ (só desce)           ║ grade com cadeado
 TÉRREO    ══[101]══[102]══[103]══[104]══[105]══[106]══[ESCADA]
 (areia)       ▲             │
               │       posto do Rafael (sala segura)
       vem da Biblioteca
```

- O **corredor** de cada andar é o centro, como o salão da Biblioteca: quase todo caminho passa por ele, e é ali que os robôs patrulham.
- A **escada** começa fechada por uma grade sanfonada com cadeado.
- O **buraco no chão da 204** dá na **104**, logo embaixo (as duas ficam no mesmo ponto dos corredores). Ele só serve para **descer**, e vira um atalho entre os andares (seção 5.5).
- A **saída** é a **porta corta-fogo** no fim do corredor do 1º andar, depois da escada. Ela está **acorrentada**. Para onde ela leva depende da ordem das fases, que ainda está pendente (Enredo, seção 12.5).

### 2.2 As salas no plano

| Sala | Papel no plano | O que tem | Esconderijos | Ameaça |
|---|---|---|---|---|
| Corredor térreo | Chegada e eixo do andar de baixo | Areia em parte do chão (passos abafados), entulho perto da 102 (passos barulhentos) | Atrás dos montes de areia e entulho | **Rastreador** (audição) |
| 101 | Pista do código | Lousa com tracinhos (1º número do cadeado) | Debaixo das carteiras | Nenhuma |
| 102 | Chave da escada | O **molho de chaves do Rafael**, caído na areia. 3 pedras | Atrás das carteiras tombadas | O Rastreador passa na porta |
| 103 | **Posto de guarda do Rafael** (proposta) e **sala segura** | O Rafael, o acampamento, 2 pilhas | Não precisa: a barricada protege | Nenhuma |
| 104 | Distração e fim do atalho | Os terminais acesos. Um deles tem o **teste de alarme** do laboratório. No teto, o buraco que vem da 204 | Debaixo das mesas | Nenhuma (o Rastreador vem quando o alarme toca) |
| 105 | Respiro | 2 robôs desmontados, 2 pilhas | Atrás dos robôs desmontados | Nenhuma (os robôs desmontados não ligam) |
| 106 | Respiro | A árvore e o luar. 1 pilha a mais (opcional) | Atrás da árvore | Nenhuma |
| Corredor 1º andar | Eixo do andar de cima | Luar pelos buracos do teto: faixas de luz e de sombra no chão. Mato (passos abafados) | Na sombra das árvores do corredor | **Sentinela** (visão) |
| 201 | Pista do código | Duas lousas; a da esquerda tem os tracinhos (2º número) | Entre as fileiras | Nenhuma |
| 202 | Respiro | As duas árvores. 1 pedra | Atrás das árvores | Nenhuma |
| 203 | Cadeado de segredo | O **claviculário** (armário de chaves) com cadeado de 3 números e o **quadro de avisos** com a pista | Debaixo das mesas | Nenhuma |
| 204 | Atalho | O buraco no chão (desce para a 104). 1 cápsula de clarão | Atrás do entulho | Nenhuma |
| 205 | Pista do código e mistério | Lousa com tracinhos (3º número). A sala "intacta demais" continua sem explicação (seção 8) | Entre as fileiras | Nenhuma |
| 206 | Ferramenta da saída | O **alicate corta-corrente**, 1 pilha. Porta trancada (chave do claviculário) | Os corredores entre as estantes | **Rastreador** (audição) |

---

## 3. Objetivos e progressão

**Objetivo:** encontrar o Rafael, ganhar a confiança dele e sair do Bloco de salas pela porta corta-fogo do 1º andar.

**O obstáculo:** a escada está fechada por uma grade com cadeado, e a porta corta-fogo está acorrentada. O Rafael sabe o que cada chave abre, mas está entrincheirado no posto dele e não abre a barricada para qualquer um.

### 3.1 Passo a passo

1. **A chegada (corredor térreo).** O Gabriel sai da Biblioteca no oeste do corredor. O **Rastreador** patrulha o corredor de ponta a ponta. A areia abafa os passos; o entulho perto da 102 faz barulho.
   - *O que o jogador aprende:* o chão muda o barulho dos passos.
2. **A voz nova (rádio).** Na porta da 103, o rádio chia: é o **Rafael**, pela primeira vez ("Rapaz, quem tá aí no corredor? Aqui é o Seu Rafael, da segurança. Câmbio."). Ele está entrincheirado na 103 e não mexe na barricada com "a máquina da obra" rondando a porta dele. Pede ao Gabriel que tire o robô dali: "Lá na 104 tem um teste de alarme. Liga aquilo que ela vai atrás. Câmbio." *(Falas são rascunho, para o roteiro: o Rafael chama os robôs de "máquinas da obra" porque acha que é tudo reforma, como diz a ficha dele.)*
3. **A distração (sala 104).** Num dos terminais acesos, o Gabriel liga o **teste de alarme**. O barulho se espalha pelo bloco. Quando ele volta ao corredor, o **Rastreador está parado na porta da 104, investigando**, e o caminho até a 103 fica livre por alguns segundos.
   - *O que o jogador aprende:* barulho é ferramenta, não só perigo.
4. **O posto do Rafael (sala 103).** O Rafael abre uma fresta na barricada. É o primeiro encontro **em pessoa** do jogo. Ele desconfia ("estudante a essa hora no bloco fechado?") e diz que perdeu o **molho de chaves** na areia da 102, quando a máquina o surpreendeu. Sem o molho, ninguém sobe: a grade da escada está no cadeado. "Traz o meu molho que eu te digo qual chave abre o quê."
5. **O molho (sala 102).** O molho está na areia, entre carteiras tombadas e montes de entulho. O Rastreador volta à rotina e passa pela porta da 102. As **pedras** da sala servem para atraí-lo para longe.
6. **A confiança (sala 103).** O Gabriel devolve o molho. O Rafael confia nele, tira do molho a **chave da fita azul** e entrega: "Essa aqui é a da grade da escada." Daí em diante ele **guia o Gabriel pelo rádio**, de cabeça: diz o que cada porta precisa e avisa por onde as máquinas passam. **Esta é a parte do Rafael** (Enredo, seção 3.1: "conhece o campus e as rondas, e sabe o que cada chave abre"), mostrada pelo que ele fala, sem papel nem item. Ele conta que a saída do bloco é a **porta corta-fogo** lá em cima, acorrentada, e que a chave do **depósito (206)**, onde fica o alicate, está no **claviculário da sala dos professores (203)**, num cadeado de segredo que ele nunca conseguiu abrir. A **103 vira a sala segura** (seção 6).
7. **Subir (escada).** A **chave da fita azul** abre o cadeado da grade da escada.
8. **O 1º andar (corredor).** Assim que o Gabriel sobe, o Rafael avisa pelo rádio como a máquina de cima anda ("ela para debaixo dos buracos do teto, macho. Passa pelo escuro. Câmbio."). A **Sentinela** patrulha sob os buracos do teto. As faixas de luar no chão são onde ela vê de longe; nas sombras e no mato o Gabriel passa.
   - *O que o jogador aprende:* a luz do céu também denuncia, não só a lanterna.
9. **O cadeado (sala 203).** O claviculário tem um cadeado de **3 números**. No quadro de avisos, um papel: **"Conferir a contagem: 101 · 201 · 205"**. O Gabriel precisa **contar os tracinhos** das lousas dessas três salas. Duas estão no 1º andar; a **101 fica lá embaixo**, e é preciso descer de novo.
   - *O que o jogador aprende:* olhar o cenário com atenção; voltar faz parte.
10. **O depósito (sala 206).** O claviculário dá a **chave do depósito**. Lá dentro, entre corredores de estantes, um **Rastreador** escuta. No fundo, o **alicate corta-corrente**.
11. **A virada.** Quando o Gabriel pega o alicate, o rádio do **Henrique** avisa que a máquina de cima "mudou de ronda" (ele vê pelas câmeras). A **Sentinela passa a cobrir o trecho entre a 206 e a escada**, justamente o caminho de volta.
12. **O atalho (opcional, salas 204 e 104).** Pelo buraco no chão da 204, o Gabriel pode **descer direto para a 104**, longe da Sentinela e da escada. É mão única: só desce. Serve para voltar rápido ao posto do Rafael e salvar.
13. **Saída (porta corta-fogo).** No fim do corredor do 1º andar, o Gabriel corta a corrente com o alicate. Antes de sair, o rádio do Rafael se despede ("Vai com Deus, macho. Qualquer coisa, chama no rádio. Câmbio."). O Rafael **fica** no posto dele.

### 3.2 Grafo de dependências

```
rádio do Rafael → alarme da 104 → posto do Rafael → molho (102) → chave da fita azul → grade da escada
                                                                                            ↓
saída ← corrente cortada ← alicate (206) ← chave do depósito ← cadeado do claviculário ← tracinhos (101, 201, 205)
```

O atalho 204 → 104 é **opcional**: fica fora da cadeia principal.

Para a apresentação da disciplina, é o mesmo modelo da Biblioteca: salas são **vértices**, portas são **arestas**, cada cadeado é uma condição numa aresta e a ordem de solução é uma **ordenação topológica** do grafo de dependências. A novidade é a distração da 104: o alarme é um **evento sonoro propagado por BFS** pelo grafo das salas (ver [`../computacao/grafos_e_navegacao.md`](../computacao/grafos_e_navegacao.md)).

### 3.3 Itens

| Item | Onde | Para quê |
|---|---|---|
| Molho de chaves do Rafael | 102, na areia | Devolver ao Rafael (confiança). O molho fica com ele |
| Chave da fita azul | 103, entregue pelo Rafael | Abrir a grade da escada |
| Código do claviculário | Tracinhos das lousas da 101, 201 e 205 | Abrir o claviculário (203) |
| Chave do depósito | Claviculário (203) | Abrir a 206 |
| Alicate corta-corrente | 206 | Cortar a corrente da porta corta-fogo |
| Cápsula de clarão | 204 (já está lá) | Defesa |
| Pedras | 102 (3, já estão lá) e 202 (1) | Distração |
| Pilhas | 103 (2), 105 (2), 206 (1), 106 (1) | Lanterna |

---

## 4. Robôs e ameaças

| Robô | Onde | Sentido forte | Rota |
|---|---|---|---|
| **Rastreador** | Corredor do térreo | Audição | Vai e volta pelo corredor inteiro. Depois do alarme (passo 3), fica um tempo parado na porta da 104, investigando, e depois volta à rota |
| **Sentinela** | Corredor do 1º andar | Visão | Antes do alicate: ronda curta entre a 201 e a 204. Depois do alicate (passo 11): cobre também o trecho entre a 206 e a escada |
| **Rastreador** | Depósito (206) | Audição | Circula entre os corredores de estantes |

- **O chão:** na **areia** e no **mato**, os passos quase não fazem barulho. No **entulho**, até andando faz (ver [`../mecanicas/movimentacao_e_terreno.md`](../mecanicas/movimentacao_e_terreno.md)).
- **O luar:** no 1º andar, as faixas de luz dos buracos do teto funcionam como as luzes de emergência da Biblioteca: quem está nelas é visto de mais longe.
- **Salas sem robôs:** todas as salas de aula, menos a 206. São os respiros entre os corredores.
- Ser pego dá game over e volta ao último checkpoint.

---

## 5. Puzzles

### 5.1 A distração (104)

- **Como funciona:** um terminal da 104 tem o **teste de alarme**. Ligar faz um barulho alto que se propaga pelo bloco.
- **Mecânica:** evento sonoro (BFS). Como cada sala é uma cena, o efeito fica guardado como uma marca (`alarme_104`). Ao voltar ao corredor, o Rastreador começa **parado na porta da 104**, investigando, por um tempo, e depois retoma a rota.
- **Solução:** ligar o alarme, voltar ao corredor e chegar à 103 antes de o Rastreador terminar de investigar.

### 5.2 O molho (102 e 103)

- **Como funciona:** busca de item numa sala por onde o robô passa, e troca de itens com um personagem.
- **Solução:** achar o molho, distrair o Rastreador com pedras se precisar, devolver o molho ao Rafael, que entrega a chave da grade.

### 5.3 Os tracinhos (101, 201, 205 → 203)

- **Como funciona:** cada lousa tem um número de tracinhos. O papel no quadro de avisos da 203 diz em que ordem contar.
- **Mecânica:** o painel de código da Biblioteca (`painel_codigo.tscn`), com 3 números.
- **Solução:** contar os tracinhos das três lousas e digitar na ordem 101, 201, 205.
- **Os tracinhos na história (sugestão, não decisão):** podem ser as **noites que o Rafael riscou** em cada sala da ronda, esperando a "reforma" acabar. Combina com a ficha dele (continua fazendo a ronda, nega a realidade). Se o grupo aprovar, o papel do quadro de avisos é dele.

### 5.4 A corrente (206 → porta corta-fogo)

- **Como funciona:** a porta de saída tem uma corrente com cadeado; o alicate é a "chave".
- **Mecânica:** porta com `chave` (o alicate é um item como a chave da manutenção).

### 5.5 O atalho (204 → 104)

- **Como funciona:** o buraco no chão da 204 é uma passagem de mão única: o Gabriel desce e cai entre as mesas da 104, logo embaixo. Cair faz barulho (o Rastreador do corredor pode ouvir).
- **Para que serve:** encurtar a volta ao posto do Rafael (salvar) e fugir da Sentinela depois da virada.

---

## 6. Sala segura

- **Sala segura:** o **posto de guarda do Rafael (103)**. A barricada protege, e os robôs não entram. O Gabriel pode dormir e salvar aqui (a ficha do Rafael já sugere: "pode servir de sala segura").
- **Por que aqui:** fica no meio do térreo, perto da escada e do atalho, e é o lugar para onde o Gabriel volta depois de cada parte difícil.
- **O sonho:** o que os sonhos mostram está pendente no Enredo (seção 12.4).

---

## 7. Registros

| Registro | Onde | Quem |
|---|---|---|
| **1ª transmissão do Rafael** (pede para tirar a máquina da porta) | Corredor térreo, perto da 103 | Rafael, pelo rádio |
| **Conversa no posto** (pede o molho; depois entrega a chave da grade) | 103 | Rafael, em pessoa (diálogo) |
| **Como a máquina de cima anda** | Topo da escada, ao chegar no 1º andar | Rafael, pelo rádio |
| **Papel do quadro de avisos** ("Conferir a contagem: 101 · 201 · 205") | 203 | A definir (sugestão: do Rafael) |
| **Aviso de ronda nova** | Corredor 1º andar, depois do alicate | Henrique, pelo rádio |
| **Despedida** | Porta corta-fogo | Rafael, pelo rádio |

Todas as falas aqui são rascunho de intenção. O texto final é do roteiro (agente `roteirista`), seguindo a ficha do Rafael (jeito cearense, "câmbio", "Seu Rafael", nega que é 3026).

---

## 8. A sala 205

A sala "intacta demais" entra no puzzle só como uma das lousas. **Por que ela está intacta** fica sem explicação nesta fase, como a porta barrada das obras raras na Biblioteca: um gancho para depois. O motivo é decisão de história e não está no Enredo.

---

## 9. O que precisa ser construído

A maior parte já existe e foi usada na Biblioteca:

| O quê | Já existe? | Como |
|---|---|---|
| Portas com chave e com marca | Sim (`porta.gd`: `chave`, `liberada_por`, `marca_ao_tentar`) | Grade da escada, 206, porta corta-fogo |
| Marcas da fase | Sim (autoload `Progresso`) | Novas: `alarme_104`, `molho_devolvido`, `claviculario_aberto`, `alicate` |
| Painel de código | Sim (`painel_codigo.tscn`) | Claviculário com 3 números |
| Robôs com rota e troca de rota por marca | Sim (Sentinela e Rastreador, `RobosDaSala`) | Três robôs (seção 4) |
| Transmissões de rádio | Sim (`GatilhoTransmissao`, `dados/transmissoes/`) | Rafael e Henrique |
| Diálogo em pessoa | Sim (`ConversaNpc` + JSON) | Rafael no posto |
| Itens | Sim (`dados/itens/`) | Novos: molho, chave da fita azul, chave do depósito, alicate |
| **Alarme da 104** | **Não** | Terminal que, ao ligar, marca `alarme_104`. No corredor, o Rastreador começa investigando a porta da 104 |
| **Buraco de mão única** | **Não** | Interagível na 204 que leva à 104 (como uma porta sem volta), com um barulho de queda |
| **Lousas com tracinhos contáveis** | Em parte (`parede_lousa.tscn`) | Variante com um número fixo e legível de tracinhos nas lousas da 101, 201 e 205 |
| **Luar que revela** | Em parte (as luzes de emergência da Biblioteca já revelam) | Mesmo efeito nas faixas de luar do 1º andar |
| **Rafael na 103** | Em parte (`rafael.tscn` existe, parado) | Colocar na 103 com a conversa |

---

## 10. Para aprovar

Decisões que dependem do Davi antes de implementar:

1. **O posto do Rafael é a sala 103** (a da barricada com acampamento)? O Enredo deixa a sala pendente (seção 12.3).
2. **A saída é a porta corta-fogo do 1º andar.** Para onde ela leva depende da ordem das fases (pendente).
3. **Os tracinhos são as noites de ronda do Rafael?** (seção 5.3). Se não, o papel do quadro de avisos fica sem autor.
4. **Energia:** a 104 tem terminais acesos e o alarme funciona. Isso depende de como fica a regra de eletricidade de 3026 no Enredo (seção 2.2), que precisa ser corrigida.
5. O **notebook** (hackeamento) **não** entra aqui, porque ele está no D-Tec e a ordem das fases não está decidida.

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
