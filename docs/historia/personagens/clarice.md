# Clarice (1994)

> **Status:** Em desenvolvimento. Já aparece em pessoa no Bunker, com diálogos.
> **Lei do projeto:** esta ficha faz parte do [Enredo Principal](../enredo_principal.md) e tem a mesma autoridade: quem a Clarice é vale como está escrito aqui. A história em volta dela (o acidente, a ordem dos acontecimentos, as pendências) está no Enredo.

---

## 1. Quem é

- **Época de origem:** 1994.
- **Quem é:** aluna de processamento de dados da Unifor, com cerca de 20 anos, que mora perto do campus.
- **História:** rodava um programa num terminal da Biblioteca de madrugada e foi puxada. Foi a primeira a notar que as rotas dos robôs formam um **grafo**. Deixou um bilhete e disquetes com senhas num terminal da Biblioteca ("Hoje à noite vou tentar entrar no sistema. Se der errado, foi mal."). Chegou a 3026 **depois do Zane e antes de Gabriel**. Fala com o grupo pela frequência de rádio que o Zane mantém. Onde ela fica está pendente. A **relação dela com Gabriel vai sendo desenvolvida ao longo do jogo**.

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
| [Diana](diana.md) | O drama contra o deboche: a Clarice não leva nada a sério e a Diana leva tudo a sério demais. Brigam o tempo todo e acabam amigas |

## 4. No jogo

- **Onde aparece:** na Biblioteca, pelo bilhete e pelo disquete no terminal. Em pessoa: pendente.
- **Esconderijo:** pendente.
- **Como chega ao jogador:** bilhete, disquetes, a frequência de rádio do grupo e conversa em pessoa.
- **Função na jogabilidade:** senhas dos terminais (o disquete com o código da grade da Biblioteca) e explicação das rotinas de patrulha (as rotas dos robôs formam um grafo). É a ponte para os conteúdos de computação.
- **Ideia de mecânica (não implementada):** o toque do telefone é um som no grafo (BFS). Se Gabriel demora a atender, os robôs ouvem.
- **Parte para consertar a Âncora:** código: faz os terminais da Âncora funcionarem.

## 5. Registros

- **Suporte:** folha de fichário com pautas azuis e adesivos coloridos (`papel = caderno_clarice`), disquete com etiqueta escrita à mão. Na ligação, só a voz e o chiado da linha.
- **Já escritos:** `dados/documentos/bilhete_clarice.tres` e o disquete `dados/itens/disquete_clarice.tres`. As conversas `dados/dialogos/clarice_primeiro_encontro.json` e `clarice_de_novo.json` foram escritas para ela no computador do bunker e precisam ser refeitas para o Zane.

## 6. Direção de arte

- **Visual definido:** [`assets/sprites/personagens/clarice/visual.md`](../../../assets/sprites/personagens/clarice/visual.md). Jaqueta corta-vento em blocos de cor, cabelo cacheado preso com xuxinha magenta, óculos grandes, fone de walkman laranja.
- **Cor de identificação:** verde-azulado, o oposto do vermelho do Gabriel.
- Sprites em resolução dobrada (ver `CLAUDE.md`).

## 7. Arquivos

- **Cena:** `cenas/personagens/clarice.tscn` (ela sentada na estação de trabalho do bunker, que agora é do Zane) e `clarice_em_pe.tscn`
- **Sprites:** `assets/sprites/personagens/clarice/`
- **Gerador:** `assets/modelagem/personagens/gerar_clarice.py`
- **Diálogos:** `dados/dialogos/clarice_*.json`

## 8. Pendências

- Onde ela fica e onde Gabriel a encontra em pessoa (Enredo Principal, seção 12.3).
- O final dela com Gabriel (seção 12.1).
