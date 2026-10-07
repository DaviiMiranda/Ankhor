# Ankhor

Jogo de terror em pixel art 2.5D, feito em Godot 4.7 para a disciplina de Computação Gráfica — Unifor, Semestre 6.

> Em 3026, a Unifor é um centro de pesquisa em física do tempo, e a explosão de um aparelho chamado Âncora rasgou o tempo dentro do campus. A fenda puxa quem está por perto em momentos do passado: numa madrugada de 2026, puxou Gabriel da Biblioteca. Ela está crescendo, e ele não foi o primeiro. Robôs patrulham o campus.

## Documentos

| Arquivo | O que tem |
|---|---|
| [`docs/gdd.md`](docs/gdd.md) | Game Design Document (itens 1 a 4) |
| [`docs/fases.md`](docs/fases.md) | Cada fase em detalhe: salas, robôs, puzzles e sonho |
| [`docs/decisoes.md`](docs/decisoes.md) | Registro das decisões de design e de história, com data |
| [`docs/equipe.md`](docs/equipe.md) | Papéis e divisão de tarefas |
| [`docs/historia/`](docs/historia/) | Enredo Principal (a lei do projeto), personagens e roteiro |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | **Regras de git e de trabalho em equipe — leia antes de começar** |
| [`CLAUDE.md`](CLAUDE.md) | Contexto do projeto para o Claude |

## Primeira vez neste repositório

### 1. Instale

- **Git:** https://git-scm.com/download/win (pode aceitar as opções padrão da instalação)
- **Godot 4.7.x** (todos na mesma versão)

### 2. Configure seu nome no git (só uma vez por computador)

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu-email-do-github@exemplo.com"
```

### 3. Clone o repositório

**Não clone dentro do OneDrive, Google Drive ou Dropbox.** A sincronização dessas pastas briga com o git e corrompe o repositório. Use uma pasta local, como `C:\dev`.

```bash
cd C:\dev
git clone https://github.com/DaviiMiranda/Ankhor.git
cd Ankhor
```

> **Já tinha clonado quando o repositório se chamava `Projeto_thegame`?** O GitHub redireciona o endereço antigo, mas atualize uma vez, dentro da pasta do projeto:
> ```bash
> git remote set-url origin https://github.com/DaviiMiranda/Ankhor.git
> ```
> (Esse comando só troca o endereço que o git usa para `pull` e `push`; seus arquivos não mudam.) Renomear a pasta no seu computador para `Ankhor` é opcional: feche o Godot e o VS Code antes. Se você tiver pastas de tarefa abertas (`git worktree list` mostra quais), elas perdem a ligação com o repositório depois de renomear. Para consertar, rode dentro da pasta renomeada `git worktree repair ../<pasta-da-tarefa>`, uma vez para cada pasta.

### 4. Abra no Godot

No Godot, *Importar* → selecione o arquivo `project.godot` desta pasta.

### 5. Leia o `CONTRIBUTING.md` e comece sua primeira tarefa numa branch.

## Estrutura

```
cenas/          cenas do Godot (.tscn)
scripts/        GDScript (.gd)
shaders/        shaders
assets/         sprites, tiles, audio, fontes
docs/           documentação do projeto
.claude/        agentes do Claude para este projeto
.github/        modelo de PR e dono do código
```

## Equipe

[preencher]
