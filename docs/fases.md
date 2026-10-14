# Fases e Áreas — Visão Geral

Tudo que é específico de cada fase e área do **Ankhor** fica documentado na pasta [`fases/`](fases/): salas, puzzles, robôs presentes e eventos de sonho.

> [!NOTE]
> - **Primeira Fase (Confirmada):** [`fases/biblioteca.md`](fases/biblioteca.md).
> - **Bunker** (em desenvolvimento): [`fases/bunker.md`](fases/bunker.md). Dois setores, 9 salas, a Clarice e seis portas lacradas para depois.
> - **Bloco de salas** (em desenvolvimento): [`fases/bloco_de_salas.md`](fases/bloco_de_salas.md). Dois corredores e 12 salas de aula.
> - **DTEC** (mapa pronto, fase solta): [`fases/dtec.md`](fases/dtec.md). O departamento de tecnologia: dois corredores, 8 salas (2 trancadas para hackear, 5 portas lacradas) e, no meio, o salão de uma máquina grande e brilhante. Sem lugar na história ainda.
> - Para entender o funcionamento do design de fases, consulte [`fases/README.md`](fases/README.md).
> - Para criar uma nova fase/área documentada, utilize o modelo [`fases/template_fase.md`](fases/template_fase.md).
> - **Sala de teste:** `cenas/salas/sala_teste.tscn`, uma sala vazia com os itens e gadgets prontos (lanterna, rádio, pilhas, cápsulas de clarão, pedras e notebook) para testar mecânicas novas. Aparece como **Teste**, em primeiro, no menu Fases só quando o jogo roda pelo editor do Godot; no jogo exportado ela some. Gadget novo entra nela primeiro. A porta no fim da sala leva à **área dos robôs** (`cenas/salas/labirinto_teste.tscn`), um labirinto pequeno com um Sentinela e um Rastreador, montado pelo mapa `dados/labirinto/mapa_teste.tres` (mesmas letras do labirinto: `V` Sentinela, `R` Rastreador, `P` pilha, `C` checkpoint, `L` lâmpada). Na área dos robôs há uma segunda porta, **trancada**, para testar o hack do notebook; ela também volta para a sala de teste.

---

## Diretrizes de Fase

- **Dono:** Papel 4 (Roteiro e fases). Mudanças passam por PR.
- Se algo aqui ou nos documentos de fases contradizer [`decisoes.md`](decisoes.md), vale [`decisoes.md`](decisoes.md).
