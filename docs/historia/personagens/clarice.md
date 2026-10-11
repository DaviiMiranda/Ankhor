# Clarice (1994)

> **Status:** Em desenvolvimento. Aparece em pessoa no Bloco de salas (sala 103) e guia Gabriel pelo rádio lá. Falas em rascunho, para o roteiro revisar.
> **Lei do projeto:** esta ficha faz parte do [Enredo Principal](../enredo_principal.md) e tem a mesma autoridade: quem a Clarice é vale como está escrito aqui. A história em volta dela (o acidente, a ordem dos acontecimentos, as pendências) está no Enredo.

---

## 1. Quem é

- **Época de origem:** 1994.
- **Quem é:** aluna de processamento de dados da Unifor, com cerca de 20 anos, que mora perto do campus.
- **História:** rodava um programa num terminal da Biblioteca de madrugada e foi puxada. Foi a primeira a notar que as rotas dos robôs formam um **grafo**. Deixou um bilhete e disquetes com senhas num terminal da Biblioteca ("Hoje à noite vou tentar entrar no sistema. Se der errado, foi mal."). Chegou a 3026 **depois do Zane e antes de Gabriel**. Fala com o grupo pela frequência de rádio que o Zane mantém. Fica na **sala 103 do Bloco de salas**, atrás de uma barricada, de onde mapeia a ronda dos robôs pela fresta. É a **primeira pessoa que Gabriel encontra em pessoa** e quem o ajuda a sair do bloco. A **relação dela com Gabriel vai sendo desenvolvida ao longo do jogo**.

## 2. Personalidade

- **Essência:** uma mente brilhante que usa o sarcasmo como armadura.
- **Traços:** rápida, independente, prática, engraçada, competitiva.
- **Como fala:** gírias dos anos 90 ("Isso é totalmente surreal", "meu filho", "Não confie nas luzes"), tom de deboche. Explica tudo como um problema de lógica.
- **O que quer:** resolver o problema grande, que é sair dali, e provar que consegue sozinha.
- **O que teme:** ser esquecida. Ficou dias sozinha antes de achar os outros.
- **Defeito:** não pede ajuda e quer controlar tudo.
- **Arco:** de quem resolve tudo sozinha a quem confia no grupo. A relação com Gabriel cresce nesse caminho.

## 3. Relações

| Com | Dinâmica |
|---|---|
| [Gabriel](gabriel.md) | Duelo de ironias: os dois se provocam o tempo todo no mesmo tom, e é assim que a relação cresce ao longo do jogo |
| [Diana](diana.md) | O drama contra o deboche: a Clarice não leva nada a sério e a Diana leva tudo a sério demais. Brigam o tempo todo (pelo rádio: a Clarice fica no Bloco de salas e a Diana no bunker) e acabam amigas |

## 4. No jogo

- **Onde aparece:** na Biblioteca, pelo bilhete e pelo disquete no terminal. No **Bloco de salas**, pelo rádio e depois em pessoa, na sala 103.
- **Esconderijo:** a **sala 103** do Bloco de salas, atrás de uma barricada, onde fica sozinha. É a **sala segura** do bloco.
- **Como chega ao jogador:** bilhete, disquetes, a frequência de rádio do grupo e conversa em pessoa na 103.
- **Função na jogabilidade:** senhas dos terminais (o disquete com o código da grade da Biblioteca) e explicação das rotinas de patrulha (as rotas dos robôs formam um grafo). É a ponte para os conteúdos de computação.
- **No Bloco de salas:** troca o **molho de chaves** (que ela perdeu na areia da 102) pela chave da grade da escada, e daí em diante guia Gabriel pelo rádio: o que cada chave abre e por onde os robôs passam. Para ela é uma **permuta**, não um pedido de ajuda (ela não pede). Ver [`../../fases/bloco_de_salas.md`](../../fases/bloco_de_salas.md).
- **Ideia de mecânica (não implementada):** o toque do telefone é um som no grafo (BFS). Se Gabriel demora a atender, os robôs ouvem.
- **Parte para consertar a Âncora:** código: faz os terminais da Âncora funcionarem. Também mapeou as rondas dos robôs e sabe o que cada chave abre.

## 5. Registros

- **Suporte:** folha de fichário com pautas azuis e adesivos coloridos (`papel = caderno_clarice`), disquete com etiqueta escrita à mão. Na ligação, só a voz e o chiado da linha.
- **Já escritos:** `dados/documentos/bilhete_clarice.tres` e o disquete `dados/itens/disquete_clarice.tres`. No Bloco de salas (rascunho, para o roteiro revisar): três transmissões em `dados/transmissoes/clarice_01.tres` a `clarice_03.tres` e quatro conversas em `dados/dialogos/clarice_bloco_*.json`. As conversas `clarice_primeiro_encontro.json` e `clarice_de_novo.json` foram escritas para ela no computador do bunker e ficaram sem uso: ela não está lá, e a cena do bunker agora mostra o Henrique (Enredo Principal, seção 12.4).

## 6. Direção de arte

- **Visual definido:** [`assets/sprites/personagens/clarice/visual.md`](../../../assets/sprites/personagens/clarice/visual.md). Jaqueta corta-vento em blocos de cor, cabelo cacheado preso com xuxinha magenta, óculos grandes, fone de walkman laranja.
- **Cor de identificação:** verde-azulado, o oposto do vermelho do Gabriel.
- Sprites em resolução dobrada (ver `CLAUDE.md`).

## 7. Arquivos

- **Cena:** `cenas/personagens/clarice_em_pe.tscn` (parada) e `clarice_posto.tscn` (na 103, com a conversa que troca o molho pela chave da grade). `clarice.tscn` é ela sentada na estação de trabalho do bunker, sem uso desde que o Henrique ocupou a estação.
- **Sprites:** `assets/sprites/personagens/clarice/`
- **Gerador:** `assets/modelagem/personagens/gerar_clarice.py`
- **Diálogos:** `dados/dialogos/clarice_*.json`

## 8. Pendências

- Se ela continua na 103 até o fim ou se junta ao grupo no bunker mais tarde (Enredo Principal, seção 12.3).
- O final dela com Gabriel (seção 12.1).
