# Créditos de fontes

Toda fonte que não foi feita pelo grupo entra aqui.

| Arquivo | Autor | Fonte (link) | Licença |
|---|---|---|---|
| `galmuri_7.ttf` | Lee Minseo ([github.com/quiple/galmuri](https://github.com/quiple/galmuri)) | Galmuri7 v2.40.4, cortada só para o alfabeto latino (acentos, pontuação e símbolos) | SIL Open Font License 1.1 (`OFL_galmuri.txt`) |
| `ark_pixel_10.ttf` (não usada) | TakWolf ([github.com/TakWolf/ark-pixel-font](https://github.com/TakWolf/ark-pixel-font)) | versão *10px proportional latin* | SIL Open Font License 1.1 (`OFL_ark_pixel.txt`) |
| `tiny5.ttf` (não usada) | The Tiny5 Project Authors ([github.com/Gissio/font_tiny5](https://github.com/Gissio/font_tiny5)) | [Google Fonts: Tiny5](https://fonts.google.com/specimen/Tiny5) | SIL Open Font License 1.1 (`OFL_tiny5.txt`) |

## Como usar a fonte do jogo

- A fonte do jogo é a **Galmuri7** (desde 2026-09-30). Antes foram a Tiny5 (pequena demais para ler) e a Ark Pixel 10 (nítida só no tamanho 10, grande demais; no tamanho 8 as letras deformavam).
- Ela é desenhada numa grade de 8 px: só fica nítida no tamanho **8** (ou múltiplos exatos: **16**, 24...). Use 8 para texto e 16 para títulos. Em qualquer outro tamanho a letra perde ou repete fileiras de pixels.
- As letras têm 7 px de altura nas maiúsculas e 5 px nas minúsculas; os acentos sobem até 9 px e as pernas (g, j, p, ç) descem 2 px.
- O jogo não usa o arquivo `.ttf` direto, e sim `cenas/interface/fonte_jogo.tres` (uma *FontVariation*), que soma 3 px acima e 2 px abaixo da linha. Assim uma linha tem **14 px** de altura, com a linha de base a 11 px do topo, igual à fonte anterior: todas as caixas de texto do jogo continuam do mesmo tamanho. Para linhas mais juntas, diminua `spacing_top` e `spacing_bottom` nesse arquivo (o mínimo sem os acentos encostarem é 12 px: 2 e 1).
- O tema zera o espaço extra entre linhas (`Label/constants/line_spacing = 0`); um `LabelSettings` precisa de `line_spacing = 0` também.
- Ela já é a fonte padrão do jogo inteiro, pelo tema `cenas/interface/tema_jogo.tres` (Projeto > Configurações do Projeto > Interface > Tema). Um Label novo já sai com ela, no tamanho 8.
- A importação dela (aba Importar do Godot) está com **Antialiasing: Nenhum**, **Hinting: Nenhum** e **Subpixel Positioning: Desativado**. Suavização em fonte pixelada é o que deixa a letra borrada numa tela de 320 × 180 ampliada.
- A Tiny5 e a Ark Pixel 10 continuam na pasta, sem uso, caso o grupo queira comparar ou voltar.
