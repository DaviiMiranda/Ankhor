# Cutscenes

Uma ficha por cutscene nesta pasta.

## Nomes

`dia_o_que`, em `snake_case`, sem acento. O dia vem primeiro, como em `docs/fases.md`: `seg_`, `ter_`, `qua_`, `qui_`, `sex_`.
O mesmo nome é usado em todas as pastas da cutscene (ficha, cena, falas, sprites).

## Onde fica cada parte

| Parte | Pasta | Quem cuida |
|---|---|---|
| Ficha (o que acontece) | `docs/historia/roteiro/cutscenes/<nome>.md` | roteiro |
| Falas | `dialogos/<nome>.json` | roteiro |
| Cena do Godot | `cenas/cutscenes/<nome>.tscn` | arte e jogabilidade |
| Imagens | `assets/sprites/cutscenes/<nome>/` | arte |
| Modelos do Blender | `assets/modelagem/cutscenes/<nome>/` | arte |

Toda cena de cutscene usa o script `scripts/cutscenes/cutscene.gd`: ela toca a animação `principal` do seu `AnimationPlayer`, pode ser pulada com Esc e, ao terminar, avisa o jogo pelo sinal `cutscene_terminou` e troca para a `proxima_cena`.

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

Para cada cena/take ilustrado em pixel art (320×180):
- **Arquivo proposto:** caminho em `assets/sprites/cutscenes/<nome>/`.
- **Enquadramento:** composição, foco, planos (fechado, médio, aberto).
- **Paleta e iluminação:** atmosfera visual, tons e iluminação.
- **Áudio / SFX:** efeitos sonoros pontuais e trilha de fundo.
- **Texto:** narração, pensamento ou falas na caixa de diálogo.
- **Transição:** como passa para a cena seguinte (fade, corte, dissolve).

---

## Especificações Técnicas para Produção
Resoluções, camadas de paralaxe e conexão no Godot (`scripts/cutscenes/cutscene.gd`).
```

## Lista

| Cutscene | Descrição | Status |
|---|---|---|
| [`seg_prologo`](seg_prologo.md) | Prólogo em ilustrações: rotina de Gabriel em 2026, ida à faculdade, aula e o adormecer na cabine da Biblioteca | aprovada (roteiro fechado) |
| [`seg_acordar`](seg_acordar.md) | O despertar imediato de Gabriel dentro da cabine da Biblioteca nas ruínas de 3026 | aprovada (cena provisória no Godot) |
