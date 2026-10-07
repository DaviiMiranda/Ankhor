# Clarice (1994)

> **Status:** Em desenvolvimento. Já aparece em pessoa no Bunker, com diálogos.
> **Lei do projeto:** esta ficha faz parte do [Enredo Principal](../enredo_principal.md) e tem a mesma autoridade: quem a Clarice é vale como está escrito aqui. A história em volta dela (o acidente, a ordem dos acontecimentos, as pendências) está no Enredo.

---

## 1. Quem é

- **Época de origem:** 1994.
- **Quem é:** aluna de processamento de dados da Unifor, com cerca de 20 anos, que mora perto do campus.
- **História:** rodava um programa num terminal da Biblioteca de madrugada e foi puxada. Foi a primeira a notar que as rotas dos robôs formam um **grafo**. Deixou um bilhete no terminal que parece despedida ("Hoje à noite vou tentar entrar no sistema. Se der errado, foi mal."), e o jogador acha que ela morreu. Está viva, escondida no **bunker** embaixo do núcleo da Âncora, quebrando a senha do setor B "um disquete por vez". Liga para os telefones velhos do campus. A **relação dela com Gabriel vai sendo desenvolvida ao longo do jogo**.

## 2. Personalidade

- **Essência:** uma mente brilhante que usa o sarcasmo como armadura.
- **Traços:** rápida, independente, prática, engraçada, competitiva.
- **Como fala:** gírias dos anos 90 ("Isso é totalmente surreal", "meu filho", "Não confie nas luzes"), tom de deboche. Explica tudo como um problema de lógica.
- **O que quer:** resolver o problema grande, que é sair dali, e provar que consegue sozinha.
- **O que teme:** ser esquecida. Ficou dias sozinha antes de qualquer um aparecer.
- **Defeito:** não pede ajuda e quer controlar tudo.
- **Arco:** de quem resolve tudo sozinha a quem confia no grupo. A relação com Gabriel cresce nesse caminho.

## 3. Relações

| Com | Dinâmica |
|---|---|
| [Gabriel](gabriel.md) | Duelo de ironias: os dois se provocam o tempo todo no mesmo tom, e é assim que a relação cresce ao longo do jogo |
| [Diana](diana.md) | O drama contra o deboche: a Clarice não leva nada a sério e a Diana leva tudo a sério demais. Brigam o tempo todo e acabam amigas |

## 4. No jogo

- **Onde aparece:** na Biblioteca, pelo bilhete no terminal. No **Bunker**, em pessoa, sentada na estação de trabalho da central de dados.
- **Esconderijo:** o **bunker** embaixo do núcleo da Âncora. Divide com o pesquisador e, depois, com o Zane.
- **Como chega ao jogador:** bilhete, disquetes, **ligações** para os telefones velhos do campus e conversa em pessoa.
- **Função na jogabilidade:** senhas dos terminais e explicação das rotinas de patrulha (as rotas dos robôs formam um grafo). É a ponte para os conteúdos de computação. Quebra a senha do setor B do bunker "um disquete por vez".
- **Ideia de mecânica (não implementada):** o toque do telefone é um som no grafo (BFS). Se Gabriel demora a atender, os robôs ouvem.
- **Parte para consertar a Âncora:** código: faz os terminais da Âncora funcionarem.

## 5. Registros

- **Suporte:** folha de fichário com pautas azuis e adesivos coloridos (`papel = caderno_clarice`), disquete com etiqueta escrita à mão. Na ligação, só a voz e o chiado da linha.
- **Já escritos:** `dados/documentos/bilhete_clarice.tres`, `dados/dialogos/clarice_primeiro_encontro.json`, `dados/dialogos/clarice_de_novo.json`.

## 6. Direção de arte

- **Visual definido:** [`assets/sprites/personagens/clarice/visual.md`](../../../assets/sprites/personagens/clarice/visual.md). Jaqueta corta-vento em blocos de cor, cabelo cacheado preso com xuxinha magenta, óculos grandes, fone de walkman laranja.
- **Cor de identificação:** verde-azulado, o oposto do vermelho do Gabriel.
- Sprites em resolução dobrada (ver `CLAUDE.md`).

## 7. Arquivos

- **Cena:** `cenas/personagens/clarice.tscn`
- **Sprites:** `assets/sprites/personagens/clarice/`
- **Gerador:** `assets/modelagem/personagens/gerar_clarice.py`
- **Diálogos:** `dados/dialogos/clarice_*.json`

## 8. Pendências

- Três falas de `clarice_primeiro_encontro.json` ainda são da versão com loops ("Você sempre lê", "E sempre chega aqui com essa cara de quem viu assombração", "E você sempre repara") e precisam ser reescritas (Enredo Principal, seção 12.4).
- O final dela com Gabriel (seção 12.1).
