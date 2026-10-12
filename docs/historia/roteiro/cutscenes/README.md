# Cutscenes

Uma ficha por cutscene nesta pasta.

## Nomes

`dia_o_que`, em `snake_case`, sem acento. O dia vem primeiro, como em `docs/fases.md`: `seg_`, `ter_`, `qua_`, `qui_`, `sex_`.
O mesmo nome é usado em todas as pastas da cutscene (ficha, cena, falas, sprites).

## Onde fica cada parte

| Parte | Pasta | Quem cuida |
|---|---|---|
| Ficha (o que acontece) | `docs/historia/roteiro/cutscenes/<nome>.md` | roteiro |
| Falas | `dados/dialogos/<nome>/` (um JSON por momento de fala) | roteiro |
| Cena do Godot | `cenas/cutscenes/<nome>.tscn` | arte e jogabilidade |
| Imagens | `assets/sprites/cutscenes/<nome>/` | arte |
| Vídeo (quando a cutscene é um vídeo) | `assets/video/cutscenes/<nome>.ogv` (Ogg Theora, o único formato que o Godot toca) | arte |
| Modelos do Blender | `assets/modelagem/cutscenes/<nome>/` | arte |

Toda cena de cutscene usa o script `scripts/cutscenes/cutscene.gd`: ela toca a animação `principal` do seu `AnimationPlayer`, pode ser pulada com Esc e, ao terminar, avisa o jogo pelo sinal `cutscene_terminou` e troca para a `proxima_cena`.

### Falas e pensamentos no meio da cutscene

Uma cutscene com texto (como a `seg_prologo`) usa um script próprio que herda de `Cutscene` e tem a função `pensar(caminho_dialogo)`. Na animação `principal`, uma trilha de **chamada de método** chama `pensar` no momento em que o texto deve aparecer, passando o JSON da fala. A partir daí:

1. `pensar` abre o diálogo pelo autoload `Dialogos`, que **pausa o jogo** e mostra o texto na **legenda de cutscene** (`cenas/interface/legenda_cutscene.tscn`, instanciada dentro da cena da cutscene).
2. O `AnimationPlayer` está em modo `PAUSABLE`, então a animação para junto e espera o jogador ler. O jogador avança com `E` (ou `Enter`).
3. Quando a fala termina, o `Dialogos` despausa o jogo e a animação continua de onde parou.

A legenda de cutscene é mais discreta que a caixa de diálogo das salas: uma faixa escura em degradê no pé da tela, com o texto centralizado (até 3 linhas) e com sombra, **sem retrato e sem nome**. Ela aparece e some com um fade curto, escreve letra por letra com um bipe mais baixo e pisca um `E` embaixo do texto quando a fala termina. Usa os mesmos JSONs de `dados/dialogos/`, só que sem escolhas: o campo `retrato` é ignorado.

A raiz da cutscene fica em modo `ALWAYS`, para o Esc e o botão "Pular" funcionarem mesmo com uma fala aberta. Ao pular, o script fecha a fala antes de trocar de cena, para o jogo não ficar pausado.

## Ficha e Organização

Cada cutscene possui um documento dedicado nesta pasta seguindo a estrutura:

```markdown
# nome_da_cutscene

- **Quando:** momento exato no fluxo do jogo em que é disparada.
- **Onde:** localização no espaço/tempo.
- **Personagens:** quem participa ou aparece.
- **Formato visual:** ilustrações estáticas com paralaxe / animação in-engine / plano fixo.
- **Objetivo dramático:** o que a cena transmite e constrói para o jogador.
- **Status:** ideia / aprovada / em produção / pronta.

---

## Roteiro Ilustração por Ilustração (quando aplicável)

Para cada cena/take ilustrado em pixel art (tela de 320×180; ilustrações em resolução dobrada, 640×360, mostradas com escala 0,5):
- **Arquivo proposto:** caminho em `assets/sprites/cutscenes/<nome>/`.
- **Enquadramento:** composição, foco, planos (fechado, médio, aberto).
- **Paleta e iluminação:** atmosfera visual, tons e iluminação.
- **Áudio / SFX:** efeitos sonoros pontuais e trilha de fundo.
- **Texto:** narração, pensamento ou falas na legenda de cutscene.
- **Transição:** como passa para a cena seguinte (fade, corte, dissolve).

---

## Especificações Técnicas para Produção
Resoluções, camadas de paralaxe e conexão no Godot (`scripts/cutscenes/cutscene.gd`).
```

## Lista

| Cutscene | Descrição | Status |
|---|---|---|
| [`seg_prologo`](seg_prologo.md) | Prólogo em ilustrações: rotina de Gabriel em 2026, ida à faculdade, aula e o adormecer na cabine da Biblioteca | em produção (cena montada no Godot; faltam os sons) |
| [`seg_acordar`](seg_acordar.md) | Vídeo: Gabriel acorda na cabine da Biblioteca, mil anos depois, cercado pela tecnologia de 3026 | pronta |
