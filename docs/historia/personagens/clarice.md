# Clarice (1994)

> **Status:** Em desenvolvimento. Já aparece em pessoa no Bunker, com diálogos.
> **Lei do projeto:** história, personalidade e arco estão no [Enredo Principal](../enredo_principal.md), seção 4.3 ("Clarice"). Esta ficha guarda só o que a produção precisa.

---

## 1. Resumo

- **Época de origem:** 1994.
- **Em uma frase:** uma mente brilhante que usa o sarcasmo como armadura.
- **Quem é:** aluna de processamento de dados da Unifor, com cerca de 20 anos, que mora perto do campus. A relação dela com Gabriel cresce ao longo do jogo, num duelo de ironias.

## 2. No jogo

- **Onde aparece:** na Biblioteca, pelo bilhete no terminal. No **Bunker**, em pessoa, sentada na estação de trabalho da central de dados.
- **Esconderijo:** o **bunker** embaixo do núcleo da Âncora. Pode dividir com mais 1 ou 2 personagens (pendente).
- **Como chega ao jogador:** bilhete, disquetes, **ligações** para os telefones velhos do campus e conversa em pessoa.
- **Função na jogabilidade:** senhas dos terminais e explicação das rotinas de patrulha (as rotas dos robôs formam um grafo). É a ponte para os conteúdos de computação. Quebra a senha do setor B do bunker "um disquete por vez".
- **Ideia de mecânica (não implementada):** o toque do telefone é um som no grafo (BFS). Se Gabriel demora a atender, os robôs ouvem.
- **Parte para consertar a Âncora:** código: faz os terminais da Âncora funcionarem.

## 3. Registros

- **Suporte:** folha de caderno com pautas azuis e adesivos coloridos, disquete com etiqueta escrita à mão. Na ligação, só a voz e o chiado da linha.
- **Registros já escritos:** `dados/documentos/bilhete_clarice.tres`, `dados/dialogos/clarice_primeiro_encontro.json`, `dados/dialogos/clarice_de_novo.json`.

## 4. Direção de arte

- **Visual definido:** [`assets/sprites/personagens/clarice/visual.md`](../../../assets/sprites/personagens/clarice/visual.md). Jaqueta corta-vento em blocos de cor, cabelo cacheado preso com xuxinha magenta, óculos grandes, fone de walkman laranja. Cor de identificação: verde-azulado.
- Sprites em resolução dobrada (ver `CLAUDE.md`).

## 5. Arquivos

- **Cena Godot:** `cenas/personagens/clarice.tscn`
- **Sprites:** `assets/sprites/personagens/clarice/`
- **Gerador:** `assets/modelagem/personagens/gerar_clarice.py`
- **Diálogos:** `dados/dialogos/clarice_*.json`

## 6. Pendências

- Três falas de `clarice_primeiro_encontro.json` ainda são da versão com loops ("Você sempre lê", "E sempre chega aqui com essa cara de quem viu assombração", "E você sempre repara") e precisam ser reescritas (Enredo Principal, seção 12.4).
- O final dela com Gabriel (seção 12.1).
- Quem divide o bunker com ela (seção 12.3).
