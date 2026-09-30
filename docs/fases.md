# Fases e Áreas — Visão Geral

Tudo que é específico de cada fase e área do **Ankhor** fica documentado na pasta [`fases/`](fases/): salas, puzzles, robôs presentes e eventos de sonho.

> [!NOTE]
> - **Primeira Fase (Confirmada):** [`fases/biblioteca.md`](fases/biblioteca.md).
> - Para entender o funcionamento do design de fases, consulte [`fases/README.md`](fases/README.md).
> - Para criar uma nova fase/área documentada, utilize o modelo [`fases/template_fase.md`](fases/template_fase.md).
> - **Sala de teste:** `cenas/salas/sala_teste.tscn`, uma sala vazia com os itens e gadgets prontos (lanterna, rádio, pilhas) para testar mecânicas novas. Aparece como **Teste** no menu Fases só quando o jogo roda pelo editor do Godot; no jogo exportado ela some. Gadget novo entra nela primeiro. A porta no fim da sala leva à **área dos robôs** (`cenas/salas/labirinto_teste.tscn`), um labirinto pequeno com um Sentinela e um Rastreador, montado pelo mapa `dados/labirinto/mapa_teste.tres` (mesmas letras do labirinto: `V` Sentinela, `R` Rastreador, `P` pilha, `C` checkpoint, `L` lâmpada).

---

## Diretrizes de Fase

- **Dono:** Papel 4 (Roteiro e fases). Mudanças passam por PR.
- Se algo aqui ou nos documentos de fases contradizer [`decisoes.md`](decisoes.md), vale [`decisoes.md`](decisoes.md).
