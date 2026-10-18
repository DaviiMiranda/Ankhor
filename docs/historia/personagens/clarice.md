# Clarice (1994)

> **Status:** Em desenvolvimento. Guia Gabriel pelo rádio na Biblioteca e no Bloco de salas, e aparece em pessoa na sala 103.
> **Lei do projeto:** esta ficha faz parte do [Enredo Principal](../História_Completa.md) e tem a mesma autoridade: quem a Clarice é vale como está escrito aqui. A história em volta dela (o acidente, a ordem dos acontecimentos, as pendências) está no Enredo.

---

## 1. Quem é

- **Época de origem:** 1994.
- **Quem é:** aluna de processamento de dados da Unifor, com cerca de 20 anos, que mora perto do campus.
- **História:** rodava um programa num terminal da Biblioteca de madrugada e foi puxada. Foi a primeira a notar que as rotas dos robôs formam um **grafo**. Deixou num terminal da Biblioteca um bilhete pedindo que, se mais alguém chegasse, a procurasse no Bloco de salas, e disquetes com senhas. Chegou a 3026 **depois do Zane e antes de Gabriel**. Fala com o grupo pela frequência de rádio que o Zane mantém. Depois de chegar à Biblioteca, foi para o **Bloco de salas** e ficou na **sala 103**, atrás de uma barricada. A **Diana** apareceu por lá depois e ela a acolheu: desde então as duas tentam descobrir o que aconteceu, com a ajuda do **Henrique** pelo rádio (ele vê o campus pelas câmeras e diz que, de alguma forma, estão em 3026), e ela mapeia a ronda dos robôs pela fresta. **É a voz do rádio que ajuda Gabriel na Biblioteca**, com o que o Henrique vê, e a **primeira pessoa que Gabriel encontra em pessoa**, na 103, de onde o ajuda a sair do bloco. A **relação dela com Gabriel vai sendo desenvolvida ao longo do jogo**.

## 2. Personalidade

- **Essência:** uma mente brilhante que usa o sarcasmo como armadura.
- **Traços:** rápida, independente, prática, engraçada, competitiva.
- **Como fala:** gírias dos anos 90 ("Isso é totalmente surreal", "meu filho", "Não confie nas luzes"), tom de deboche. Explica tudo como um problema de lógica.
- **O que quer:** resolver o problema grande, que é sair dali, e provar que consegue sozinha.
- **O que teme:** ser esquecida. Ficou dias sozinha antes de achar os outros: é por causa dela que o Zane deixou um rádio no balcão da Biblioteca, para que o próximo não passasse pelo mesmo.
- **Defeito:** não pede ajuda e quer controlar tudo.
- **Arco:** de quem resolve tudo sozinha a quem confia no grupo. A relação com Gabriel cresce nesse caminho.

## 3. Relações

| Com | Dinâmica |
|---|---|
| [Gabriel](gabriel.md) | Duelo de ironias: os dois se provocam o tempo todo no mesmo tom, e é assim que a relação cresce ao longo do jogo |
| [Diana](diana.md) | O drama contra o deboche: a Clarice não leva nada a sério e a Diana leva tudo a sério demais. Dividem a 103 do Bloco de salas: a Clarice anota as rondas, a Diana desenha o mapa. Brigam o tempo todo e acabam amigas |
| [Henrique](henrique.md) | Falam pelo rádio: ele as ajuda com o que vê nas câmeras, e elas juntam isso com o que descobrem. É por ele que a Clarice sabe das rondas na Biblioteca e de que Gabriel acordou |

## 4. No jogo

- **Onde aparece:** na Biblioteca, pelo rádio (com o que o Henrique vê), pelo bilhete e pelo disquete no terminal. No **Bloco de salas**, pelo rádio e depois em pessoa, na sala 103.
- **Esconderijo:** a **sala 103** do Bloco de salas, atrás de uma barricada, que ela divide com a Diana. É a **sala segura** do bloco.
- **Como chega ao jogador:** bilhete, disquetes, a frequência de rádio do grupo e conversa em pessoa na 103.
- **Função na jogabilidade:** senhas dos terminais (o disquete com o código da grade da Biblioteca) e explicação das rotinas de patrulha (as rotas dos robôs formam um grafo). É a ponte para os conteúdos de computação.
- **Na Biblioteca:** guia Gabriel pelo rádio com as dicas de patrulha que o Henrique vê nas câmeras (o bipe do robô de um olho só, o robô do acervo que escuta).
- **No Bloco de salas:** troca o **molho de chaves** (que ela perdeu na areia da 102) pela chave da grade da escada, e daí em diante guia Gabriel pelo rádio: o que cada chave abre e por onde os robôs passam. Para ela é uma **permuta**, não um pedido de ajuda (ela não pede). Ver [`../../fases/bloco_de_salas.md`](../../fases/bloco_de_salas.md).
- **Ideia de mecânica (não implementada):** o toque do telefone é um som no grafo (BFS). Se Gabriel demora a atender, os robôs ouvem.
- **Parte para consertar a Âncora:** código: faz os terminais da Âncora funcionarem. Também mapeou as rondas dos robôs e sabe o que cada chave abre.

## 5. Registros

- **Suporte:** folha de fichário com pautas azuis e adesivos coloridos (`papel = caderno_clarice`), disquete com etiqueta escrita à mão. Na ligação, só a voz e o chiado da linha.
- **Já escritos:** `dados/documentos/bilhete_clarice.tres` (ainda com o texto antigo, "Hoje à noite vou tentar entrar no sistema": precisa virar o pedido para procurá-la no Bloco de salas: ver as [pendências de produção](../../pendencias_de_producao.md) e o disquete `dados/itens/disquete_clarice.tres`. Transmissões: `clarice_biblioteca_01.tres` e `clarice_biblioteca_02.tres` (Biblioteca, balcão e acervo) e `clarice_01.tres` a `clarice_04.tres` (Bloco de salas). Quatro conversas no Bloco de salas em `dados/dialogos/clarice_bloco_*.json`. As conversas `clarice_primeiro_encontro.json` e `clarice_de_novo.json` foram escritas para ela no computador do bunker e ficaram sem uso: ela não está lá, e a cena do bunker agora mostra o Henrique (ver as [pendências de produção](../../pendencias_de_producao.md)).

## 6. Direção de arte

- **Visual definido:** [`assets/sprites/personagens/clarice/visual.md`](../../../assets/sprites/personagens/clarice/visual.md). Jaqueta corta-vento em blocos de cor, cabelo cacheado preso com xuxinha magenta, óculos grandes, fone de walkman laranja.
- **Cor de identificação:** verde-azulado, o oposto do vermelho do Gabriel.
- Sprites em resolução dobrada (ver `CLAUDE.md`).

## 7. Arquivos

- **Cena:** `cenas/personagens/clarice_em_pe.tscn` (parada) e `clarice_posto.tscn` (na 103, com a conversa que troca o molho pela chave da grade). `clarice.tscn` é ela sentada na estação de trabalho do bunker, sem uso desde que o Henrique ocupou a estação.
- **Sprites:** `assets/sprites/personagens/clarice/`
- **Gerador:** `assets/modelagem/personagens/gerar_clarice.py`
- **Diálogos:** `dados/dialogos/clarice_*.json`
- **Transmissões:** gatilhos `GatilhoRadio1` (`cenas/salas/biblioteca/balcao.tscn`) e `GatilhoRadio2` (`acervo.tscn`) na Biblioteca; `GatilhoClarice1` a `GatilhoClarice4` nos corredores do Bloco de salas.
- **Som do rádio:** `assets/audio/efeitos/objetos/radio_chiado.wav` (gerado por `assets/modelagem/audio/gerar_efeitos_registros.py`).

## 8. Pendências

- Se ela e a Diana continuam na 103 até o fim ou se juntam ao grupo no bunker mais tarde, e quem fez as pichações assinadas "C." no bunker (Enredo Principal, seção 10.4).
- O final dela com Gabriel (seção 10.6).
