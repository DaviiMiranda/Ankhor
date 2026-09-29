# Créditos de fontes

Toda fonte que não foi feita pelo grupo entra aqui.

| Arquivo | Autor | Fonte (link) | Licença |
|---|---|---|---|
| `ark_pixel_10.ttf` | TakWolf ([github.com/TakWolf/ark-pixel-font](https://github.com/TakWolf/ark-pixel-font)) | versão *10px proportional latin* | SIL Open Font License 1.1 (`OFL_ark_pixel.txt`) |
| `tiny5.ttf` (não usada) | The Tiny5 Project Authors ([github.com/Gissio/font_tiny5](https://github.com/Gissio/font_tiny5)) | [Google Fonts: Tiny5](https://fonts.google.com/specimen/Tiny5) | SIL Open Font License 1.1 (`OFL_tiny5.txt`) |

## Como usar a fonte do jogo

- A fonte do jogo é a **Ark Pixel 10** (desde 2026-09-29; antes era a Tiny5, que era pequena demais para ler). Ela é desenhada numa grade de 10 px: só fica nítida no tamanho **10** (ou múltiplos exatos: **20**, 30...). Use 10 para texto e 20 para títulos.
- Uma linha tem **14 px** de altura (11 acima da linha de base, com espaço para acentos, e 3 abaixo). O tema zera o espaço extra entre linhas (`Label/constants/line_spacing = 0`); um `LabelSettings` precisa de `line_spacing = 0` também.
- Ela já é a fonte padrão do jogo inteiro, pelo tema `cenas/interface/tema_jogo.tres` (Projeto > Configurações do Projeto > Interface > Tema). Um Label novo já sai com ela, no tamanho 10.
- A importação dela (aba Importar do Godot) está com **Antialiasing: Nenhum**, **Hinting: Nenhum** e **Subpixel Positioning: Desativado**. Suavização em fonte pixelada é o que deixa a letra borrada numa tela de 320 × 180 ampliada.
- A Tiny5 continua na pasta, sem uso, caso o grupo queira comparar ou voltar.
