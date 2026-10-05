# Áudio

Todo som do jogo fica aqui. **Dono:** papel 4 (Roteiro e fases, que inclui o áudio). Qualquer um pode adicionar som por PR.

## Pastas

```
audio/
├── musica/              trilhas que tocam em loop
│   ├── menu/            menu principal
│   ├── gameplay/        exploração da Biblioteca (mistério, tocada de fundo)
│   ├── bunker/          o bunker da Clarice (peso, enterrado)
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
| `musica/bunker/bunker_trilha.ogg` | `assets/modelagem/audio/gerar_trilha_bunker.py` | 64 s em loop, sem andamento marcado, Dó frígio (Dó m, Ré♭/Dó, Sol♭, Dó m♭9): Dó grave com batimento, cordas graves, aço gemendo, baque distante lá em cima, a fita da Clarice (piano elétrico gasto) e um fio agudo dissonante. Toca pela cena `cenas/sistemas/musica_bunker.tscn` em todas as salas do bunker |
| `efeitos/gabriel/gabriel_passo_ceramica_01.wav` … `_06.wav` | `assets/modelagem/audio/gerar_efeitos_gabriel.py` | 6 passos de tênis em cerâmica antiga com areia: baque do calcanhar, sola, grãos e um pouco do eco do salão. Tocados pela cena `cenas/sistemas/passos.tscn` (dentro do Gabriel), sorteando a variação |
| `efeitos/interface/inventario_abrir.wav` | `assets/modelagem/audio/gerar_efeitos_gabriel.py` | 0,55 s: zíper da mochila (acelera e freia), tecido e a aba caindo. Toca ao abrir o inventário |
| `efeitos/interface/inventario_fechar.wav` | `assets/modelagem/audio/gerar_efeitos_gabriel.py` | 0,45 s: a aba empurrada, o zíper mais rápido e o "tec" do cursor no fim. Toca ao fechar o inventário |
| `efeitos/objetos/radio_chiado.wav` | `assets/modelagem/audio/gerar_efeitos_registros.py` | 2 s em loop sem emenda: estática de rádio portátil, com o sinal indo e voltando. Toca por baixo das falas do Valdir (`cenas/interface/legenda_radio.tscn`) |
| `efeitos/objetos/radio_clique.wav` | `assets/modelagem/audio/gerar_efeitos_registros.py` | 0,3 s: o clique do botão de falar e o chiado do canal abrindo. Toca no começo e no fim de cada transmissão |
| `musica/perseguicao/labirinto_tensao.ogg` | `assets/modelagem/audio/gerar_trilha_labirinto.py` | 38,4 s em loop, 100 BPM, Ré frígio: drone, coração, metal arrastado, máquinas ao longe, cordas agudas. Camada que toca sempre no labirinto |
| `musica/perseguicao/labirinto_perseguicao.ogg` | `assets/modelagem/audio/gerar_trilha_labirinto.py` | Mesma duração e andamento: tambores, baixo em ostinato, golpes de metal, Shepard subindo, alarme. Sobe quando um robô vê o Gabriel (`cenas/sistemas/musica_labirinto.tscn`) |
| `efeitos/robos/sentinela_passo.wav`, `rastreador_passo.wav` | `assets/modelagem/audio/gerar_efeitos_labirinto.py` | Pisada pesada de metal; garras correndo no concreto |
| `efeitos/robos/robo_zumbido.wav` | `assets/modelagem/audio/gerar_efeitos_labirinto.py` | 2 s em loop: o motor do robô ligado (60 Hz, engrenagem, ventoinha) |
| `efeitos/robos/robo_alerta.wav` | `assets/modelagem/audio/gerar_efeitos_labirinto.py` | O guincho de quando o robô vê o Gabriel |
| `efeitos/gabriel/gabriel_dano.wav`, `efeitos/interface/morte.wav`, `efeitos/interface/checkpoint.wav` | `assets/modelagem/audio/gerar_efeitos_labirinto.py` | Pancada ao levar dano; tela de morte; posto de checkpoint acendendo |
| `efeitos/objetos/lanterna_clique.wav`, `pilha_troca.wav` | `assets/modelagem/audio/gerar_efeitos_labirinto.py` | Botão da lanterna; troca de pilha |
| `efeitos/interface/menu_passar.wav`, `menu_clique.wav` | `assets/modelagem/audio/gerar_efeitos_menu.py` | Bipe de computador velho ao passar por uma opção do menu; clique do mouse com bipe de confirmação ao escolher |
| `efeitos/objetos/porta_abrir.wav` | `assets/modelagem/audio/gerar_efeitos_gadgets.py` | 1,4 s: trinco, dobradiça rangendo e a porta batendo. Toca ao atravessar uma porta (`cenas/sistemas/porta.tscn`) |
| `efeitos/objetos/clarao_disparo.wav`, `pedra_impacto.wav`, `notebook_hack.wav` | `assets/modelagem/audio/gerar_efeitos_gadgets.py` | Estalo do flash com o capacitor recarregando; pedra batendo e quicando; 2,5 s de bipes de dados com o "ok" no fim |
| `ambiente/bunker/bunker_zumbido.wav`, `bunker_goteiras.wav` | `assets/modelagem/audio/gerar_efeitos_bunker.py` | Loops do bunker: transformador de 60 Hz com o ar parado do duto, grave e constante (em toda sala do bunker; mais grave e alto no gerador) e pingos d'água no setor B |
| `efeitos/objetos/porta_blindada.wav`, `porta_emperrada.wav` | `assets/modelagem/audio/gerar_efeitos_bunker.py` | Porta de aço de correr (trava, pistão, batida) e a maçaneta de uma porta lacrada |
| `efeitos/objetos/teclado.wav` | `assets/modelagem/audio/gerar_efeitos_bunker.py` | 3 s em loop: a Clarice digitando |
| `efeitos/interface/dialogo_bip.wav` | `assets/modelagem/audio/gerar_efeitos_bunker.py` | O bipe das letras na caixa de diálogo (o tom muda com quem fala) |
| `efeitos/interface/papel_folhear.wav` | `assets/modelagem/audio/gerar_efeitos_registros.py` | 0,35 s: uma folha virando. Toca ao abrir, folhear e fechar documentos e o caderno |

Para mudar a música, edite o script (acordes, melodia, volumes estão no começo de cada função) e rode `python assets/modelagem/audio/gerar_trilha_menu.py` , `gerar_trilha_gameplay.py` ou `gerar_trilha_bunker.py` (precisa de numpy e ffmpeg). Os efeitos saem de `gerar_efeitos_gabriel.py` (só numpy).

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
