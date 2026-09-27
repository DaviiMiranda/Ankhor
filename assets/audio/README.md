# Áudio

Todo som do jogo fica aqui. **Dono:** papel 4 (Roteiro e fases, que inclui o áudio). Qualquer um pode adicionar som por PR.

## Pastas

```
audio/
├── musica/              trilhas que tocam em loop
│   ├── menu/            menu principal
│   ├── gameplay/        exploração da Biblioteca (mistério, tocada de fundo)
│   ├── sonho/           o campus na última semana antes de tudo
│   ├── perseguicao/     quando um robô sai da patrulha e persegue
│   └── final/           o final no portão
├── ambiente/            som de fundo contínuo de cada área, presente e sonho
│   ├── biblioteca/
│   ├── blocos_aula/
│   ├── centro_convivencia/
│   ├── espaco_cultural/
│   ├── nami/
│   ├── reitoria/
│   └── areas_externas/  dunas e mato entre os prédios, rota do Vigia
├── efeitos/             sons curtos, tocados uma vez
│   ├── gabriel/         passos, corrida, respiração, esconder, dormir
│   ├── robos/           sons de cada tipo de robô
│   ├── objetos/         portas, entulho, estantes, objetos jogados, fungos, cápsula de clarão
│   └── interface/       botões do menu, inventário, avisos
└── vozes/               falas e murmúrios (ex.: a Pesquisadora)
```

## Sons gerados por código

Alguns sons são compostos por script, sem gravação (e sem problema de licença):

| Arquivo | Script | Como é |
|---|---|---|
| `musica/menu/menu_trilha.ogg` | `assets/modelagem/audio/gerar_trilha_menu.py` | 64 s em loop, ré menor, 60 BPM: pad escuro, drone grave, relógio e uma caixinha de música (canção de ninar) na segunda metade |
| `musica/gameplay/gameplay_trilha.ogg` | `assets/modelagem/audio/gerar_trilha_gameplay.py` | 70 s em loop, 48 BPM em 7/4, Mi menor sem resolução: pad escuro, pulso grave, sino de vidro com eco, gongo da Âncora, tom de Shepard descendo (a fenda) e goteiras. Toca pela cena `cenas/sistemas/musica_fase.tscn` |
| `efeitos/gabriel/gabriel_passo_ceramica_01.wav` … `_06.wav` | `assets/modelagem/audio/gerar_efeitos_gabriel.py` | 6 passos de tênis em cerâmica antiga com areia: baque do calcanhar, sola, grãos e um pouco do eco do salão. Tocados pela cena `cenas/sistemas/passos.tscn` (dentro do Gabriel), sorteando a variação |
| `efeitos/interface/inventario_abrir.wav` | `assets/modelagem/audio/gerar_efeitos_gabriel.py` | 0,55 s: zíper da mochila (acelera e freia), tecido e a aba caindo. Toca ao abrir o inventário |

Para mudar a música, edite o script (acordes, melodia, volumes estão no começo de cada função) e rode `python assets/modelagem/audio/gerar_trilha_menu.py` ou `gerar_trilha_gameplay.py` (precisa de numpy e ffmpeg). Os efeitos saem de `gerar_efeitos_gabriel.py` (só numpy).

## Nomes de arquivo

Formato: `onde_o_que_variacao.ext`, em `snake_case`, português, sem acento.

- Com variações, numere com dois dígitos: `gabriel_passo_areia_01.wav`, `gabriel_passo_areia_02.wav`.
- Em `ambiente/`, diga se é presente ou sonho: `biblioteca_presente.ogg`, `biblioteca_sonho.ogg`.
- Em `efeitos/robos/`, comece pelo tipo do robô (`docs/personagens/robos.md`): `sentinela_passos_01.wav`, `enxame_motor_01.wav`.
- Em `vozes/`, comece pelo personagem: `pesquisadora_murmurio_01.ogg`.

## Formato

| Tipo | Formato | Por quê |
|---|---|---|
| Música e ambiente | `.ogg` ou `.mp3` | arquivo pequeno, bom para sons longos em loop |
| Efeitos e interface | `.wav` | toca sem atraso, bom para sons curtos |
| Vozes | `.ogg` | falas longas ficam pequenas |

- Loop de música e ambiente se liga no Godot: selecione o arquivo, aba **Import**, marque **Loop** e clique em **Reimport**.
- Commite os arquivos `.import` que o Godot cria ao lado de cada som.
- Só sons livres (CC0 ou com licença que permita uso) ou gravados pelo grupo. Anote a origem de cada som de fora em `creditos.md`, nesta pasta.
