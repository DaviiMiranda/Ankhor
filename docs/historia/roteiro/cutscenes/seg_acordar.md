# seg_acordar

- **Quando:** início do jogo, logo depois do prólogo ([`seg_prologo`](seg_prologo.md)), que termina no pulso da fenda.
- **Onde:** Biblioteca, na cabine de estudo onde Gabriel pegou no sono, mil anos depois.
- **Personagens:** Gabriel.
- **Formato visual:** vídeo curto (6 s, com som).
- **O que acontece:** a cena abre no mesmo enquadramento da última ilustração do prólogo: Gabriel dormindo com a cabeça sobre os braços, a luminária, o caderno, o relógio e a mochila. Só que a cabine agora tem a tecnologia de 3026: painéis com luz ciano e um holograma aceso sobre o caderno. A câmera se afasta e mostra a biblioteca em volta, com estantes e torres de equipamentos. Gabriel se ergue, esfrega os olhos e olha em volta sem entender onde está.
- **Falas:** nenhuma.
- **O que o jogador descobre:** _a definir._
- **Status:** pronta

## Nota da cena

A cena `cenas/cutscenes/seg_acordar.tscn` toca o vídeo `assets/video/cutscenes/seg_acordar.ogv` num `VideoStreamPlayer` do tamanho da tela (640×360, com `expand`). Ela usa o script `scripts/cutscenes/cutscene.gd`: a animação `principal` dura o mesmo que o vídeo (6 s) e só faz a tela sair do preto no começo (0,6 s), continuando o preto em que o prólogo termina.

- **Formato do vídeo:** o Godot só toca vídeo em **Ogg Theora** (`.ogv`). O original (`animação_gabriel_acordando.mp4`, 1920×1080, 24 quadros por segundo) foi convertido para 1280×720 com o `ffmpeg`:
  ```
  ffmpeg -i animação_gabriel_acordando.mp4 -vf "scale=1280:720:flags=lanczos" -c:v libtheora -q:v 8 -c:a libvorbis -q:a 5 seg_acordar.ogv
  ```
  1280×720 é o tamanho padrão da janela do jogo: o vídeo aparece nítido e pesa menos para decodificar que o 1080p.
- **Som:** o som do vídeo toca no barramento `Efeitos`.
- **Trocar o vídeo:** converta o novo com o mesmo comando e substitua `seg_acordar.ogv`. Se a duração mudar, ajuste o `length` da animação `principal` para a duração nova.

O "Novo jogo" do menu abre o prólogo (`cenas/cutscenes/seg_prologo.tscn`), que ao terminar (ou ao apertar Esc) passa para esta cena. Ela, por sua vez, ao terminar (ou ao apertar Esc) passa para a primeira sala, a cabine de estudo da Biblioteca (`cenas/salas/biblioteca/cabine.tscn`).

Até 2026-10-11, esta cutscene era uma animação provisória feita no Blender (`gerar_seg_acordar.py`), com a Biblioteca em ruínas, raios de sol e paralaxe. Ela foi descartada e trocada pelo vídeo.
