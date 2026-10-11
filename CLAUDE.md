# CLAUDE.md — contexto de Ankhor

Este arquivo dá contexto a qualquer sessão do Claude que trabalhe neste repositório. Leia antes de mexer em qualquer coisa.

## O projeto

**Ankhor** é o jogo do trabalho de Computação Gráfica (Semestre 6) de um grupo de 4 alunos da Unifor.

- **Premissa:** Em 3026 o pouco que sobrou da humanidade foi embora da Terra. Ficou o **Carlos**, um cientista obcecado pelos anos 80, que construiu a **Âncora** para ir viver lá. A máquina é imprecisa: a cada tentativa, abre uma **fenda** no tempo no chão da Biblioteca e puxa, por acaso, jovens de épocas diferentes que estavam naquele ponto. Um deles é **Gabriel Magalhães**, estudante de 2026. Ele precisa encontrar os outros, descobrir o que aconteceu e achar um jeito de todos voltarem. Os inimigos são **robôs** controlados pelo Carlos. A primeira fase é a Biblioteca.
- **Estilo:** pixel art em vista lateral 2.5D, inspirado em *Five Nights at Freddy's: Into the Pit*. Terror atmosférico, fuga e esconderijo, defesa limitada.
- **A lei do projeto para história, mundo e personagens é [`docs/historia/enredo_principal.md`](docs/historia/enredo_principal.md), junto com as fichas de [`docs/historia/personagens/`](docs/historia/personagens/)** (uma por personagem, com a mesma autoridade). Vale acima de qualquer outro documento (GDD, fichas, fases, `decisoes.md`). Em caso de dúvida em qualquer parte do jogo (uma fala, um bilhete, uma sala, um sprite), consulte o Enredo Principal. Se algo o contradiz, o erro está no outro lugar. O que ele ainda não decidiu está na seção "Pendências", no fim dele: não invente resposta para uma pendência, pergunte ao usuário.
- **Para o resto (mecânicas, técnica, arte),** a fonte da verdade é `docs/decisoes.md` + `docs/gdd.md`. Se os dois se contradizem, vale o registro de decisões (é o mais recente).

**Requisito obrigatório da disciplina:** o jogo precisa usar conteúdos de computação — grafos, estruturas de dados avançadas, matemática. Planejado: campus como grafo, BFS para propagação de som, A\* para perseguição, cadeia de Markov no movimento dos inimigos, coloração de grafos em rotinas de patrulha, máquina de estados, campo de visão por produto escalar. Detalhes em `docs/gdd.md`, item 2.4.

## Stack

- **Godot 4.7.x**, **GDScript**, 2D.
- Resolução base 320×180, escala inteira, filtro de textura *Nearest* (pixel art). O stretch é `canvas_items`: a lógica e a interface ficam em 320×180, mas a imagem é desenhada na resolução da janela. Por isso **os personagens humanos (Gabriel, Clarice, Zane, Baltazar, Rafael, Henrique, Carlos) têm sprites em resolução dobrada** (96 px de altura, mostrados com escala 0,5): no mesmo tamanho na tela, com o dobro de detalhe. O cenário continua em 1× (ver `docs/decisoes.md`).
- Fonte: **Galmuri7** (pixelada), padrão do jogo pelo tema `cenas/interface/tema_jogo.tres`. Só nos tamanhos **8** ou **16**: em outros tamanhos a letra deforma. Uma linha de texto tem 14 px de altura. Detalhes em `assets/fontes/creditos.md`.
- Sem assets pagos. Placeholders gerados no próprio Godot até a arte ficar pronta.

## Estrutura

```
cenas/          cenas do Godot (.tscn) — uma cena por sistema/sala/personagem
scripts/        GDScript (.gd)
dados/          recursos de dados (.tres), ex.: dados/itens/ — um arquivo por item
shaders/        shaders (.gdshader)
assets/         sprites, tiles, audio, fontes
docs/           gdd.md, equipe.md, decisoes.md
docs/historia/  enredo_principal.md (a lei do projeto), personagens/, roteiro/
.claude/agents/ agentes especializados deste projeto
```

## Convenções

- Arquivos, pastas, variáveis e funções em `snake_case`; `class_name` em `PascalCase`. Nomes em português, sem acento em nome de arquivo.
- **Scripts GDScript (`.gd`) sem nenhum comentário**: nem `#` nem `##`. O código se explica pelos nomes (em português, `snake_case`) e por funções curtas. O que precisa de explicação (algoritmo, matemática, como usar um sistema) vai para `docs/` (ex.: `docs/computacao/`, `docs/mecanicas/`). Os geradores em Python (`assets/modelagem/`) e os shaders (`.gdshader`) continuam comentados, explicando a matemática.
- Cada sistema, personagem e sala é uma **cena separada**. Não coloque vários sistemas numa cena só.
- Comunicação entre sistemas por **sinais** do Godot (ex.: `jogador_detectado`, `jogador_perdido`), não por referências diretas entre cenas de pessoas diferentes.
- Commite os arquivos `.import` e `.uid`. Nunca commite `.godot/`.

## Regras de git para o Claude

As regras completas estão em `CONTRIBUTING.md`. O essencial:

- **Nunca faça commit nem push na `main`.** Sempre trabalhe numa branch `tipo/descricao-curta`.
- **Nunca use `git push --force`.**
- Commits pequenos, mensagem no formato `tipo: o que mudou`, em português.
- Ao terminar uma tarefa, faça o push e **abra o PR** (título e descrição no modelo de `.github/pull_request_template.md`). **Só mescle quando o usuário pedir.** O revisor principal é o Davi.
- Não edite cenas (`.tscn`) ou arquivos de arte de outra pessoa sem que o usuário confirme que pode.

### Toda tarefa numa pasta separada (git worktree)

A **pasta principal** do projeto (onde o repositório foi clonado) é compartilhada. O nome dela muda de computador para computador (`Ankhor`, `Projeto_Ankhor`, ou `Projeto_thegame` num clone antigo). Confira com `git worktree list`: ela é a primeira linha. Abaixo, `<pasta>` é esse nome. Outras pessoas e outras sessões do Claude trabalham nela ao mesmo tempo. **Nunca troque de branch nem faça mudanças diretamente nela.** Trocar a branch ali muda os arquivos debaixo de quem está trabalhando, e o commit dessa pessoa acaba na branch errada.

Em vez disso, para cada tarefa:

1. **Crie uma pasta separada com a branch nova, a partir da `main` atualizada**, ao lado da pasta do projeto:
   ```bash
   git fetch origin
   git worktree add ../<pasta>-<tarefa> -b tipo/descricao-curta origin/main
   ```
   Ex.: `../Projeto_Ankhor-audio` com a branch `docs/estrutura-audio`. Se a tarefa depende de outra ainda não mesclada, crie a partir da branch dela e abra o PR apontando para ela.
2. **Faça todas as mudanças e commits dentro dessa pasta.** A pasta principal não é tocada.
3. **Push e PR** para a `main`: `git push -u origin <branch>` e `gh pr create`.
4. **Se a mudança precisa do Godot** (gerar `.import`, testar a cena), peça ao usuário para abrir o projeto nessa pasta, e commite os `.import` gerados.
5. **Mescle quando o usuário pedir**, com squash: `gh pr merge <número> --squash`.
6. **Limpe depois do merge**, a partir da pasta principal:
   ```bash
   git push origin --delete <branch>
   git worktree remove ../<pasta>-<tarefa>
   git branch -D <branch>
   ```
   Se o Windows não deixar apagar a pasta, algum programa está com ela aberta (Godot, Explorador ou o próprio terminal). Peça para fechar e tente de novo.

**Se a pasta principal for renomeada** com pastas separadas ainda abertas, o git perde a ligação com elas e responde `not a git repository` lá dentro. Para consertar, rode a partir da pasta principal `git worktree repair ../<pasta-da-tarefa>` (uma por pasta separada). Esse comando só refaz a ligação, sem mexer em nenhum arquivo.

A mesma regra vale para agentes do projeto: passe para eles o caminho da pasta separada e deixe claro que não devem mexer na pasta principal.

## Como ajudar este grupo

- O grupo nunca trabalhou com git em equipe. Quando um comando git for necessário, **explique o que ele faz** antes de sugerir.
- Prefira **o menor passo que funciona**. Escopo de trabalho de faculdade: uma sala perfeita vale mais que cinco pela metade.
- Mecânicas e história ainda mudam. Antes de implementar algo grande baseado no GDD, confira `docs/decisoes.md`, e, se tocar em história ou personagens, o Enredo Principal.
- Se uma mudança de design for decidida numa conversa, sugira registrá-la em `docs/decisoes.md`. Se for de **história**, ela entra **no mesmo PR** no Enredo Principal e em `docs/decisoes.md`.

## Agentes do projeto

Em `.claude/agents/`:

| Agente | Use para |
|---|---|
| `revisor` | revisar uma branch ou PR antes de pedir revisão humana: regras do `CONTRIBUTING.md`, bugs, cenas misturadas, arquivos que não deviam estar no commit |
| `roteirista` | escrever e revisar história, diálogos e textos, checando consistência com o que já foi decidido |
| `sistemas` | grafos, IA dos robôs, algoritmos — e explicar a matemática para a apresentação da disciplina |
| `artista` | guia de estilo, shaders, iluminação 2D, placeholders e listas de assets por sala; conferir se a arte conta o que o roteiro pede |
