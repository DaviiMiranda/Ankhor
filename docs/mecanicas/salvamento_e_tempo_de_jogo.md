# Mecânicas — Espaços de save e tempo de jogo

Como no *Resident Evil*: o jogo conta quanto tempo a campanha levou, sem contar a pausa, e guarda até **seis saves** separados. Ao salvar, o jogador escolhe se grava num espaço livre ou por cima de um antigo.

## 1. Tempo de jogo

- O relógio começa do zero no **Novo jogo** (e ao escolher uma fase na lista **Fases**) e continua do tempo do save ao **carregar**.
- Ele **para** só na tela **PAUSADO** (Esc) e no menu principal. Todo o resto conta: salas, cutscenes, inventário, documentos, diálogos, tela de morte e o quarto do visor. É o tempo que o jogador passou jogando, como no *Resident Evil*.
- Morrer não volta o relógio: o Gabriel volta ao checkpoint, mas o tempo segue.
- O relógio mede **tempo real** (`Time.get_ticks_usec`), não o `delta` dos quadros, então não muda se o jogo ficar lento.
- **Onde aparece:**
  - na tela **PAUSADO**, embaixo do título: *Tempo de jogo: 01:12:01* (some nas Opções e na confirmação);
  - em cada espaço de save, na TV do quarto e na lista **CARREGAR** do menu principal.
- Formato `HH:MM:SS` (`TempoDeJogo.formatar`).
- Saves feitos antes do relógio existir aparecem com `00:00:00` e contam a partir daí.

## 2. Espaços de save

- São **6 espaços**, cada um num arquivo: `user://salvamento_1.cfg` a `user://salvamento_6.cfg`. O que cada arquivo guarda está em [`sala_segura.md`](sala_segura.md), seção 3.
- Cada espaço aparece numa linha: `3  01:02:05  Biblioteca` (número, tempo de jogo, fase), ou `3  Vazio`. A data e a hora ficam numa linha embaixo da lista, para o espaço que está com o cursor.
- O nome da fase vem dos recursos de `dados/fases/` (`Fase.nome_da_cena`): a sala salva pertence à fase cuja pasta de salas é a mesma (`cenas/salas/biblioteca/...` é a Biblioteca; o Labirinto, cuja cena fica direto em `cenas/salas/`, usa a pasta `cenas/salas/labirinto/`).
- **Salvar** (na TV do quarto do visor, ver [`visor_3d.md`](visor_3d.md)): espaço vazio grava direto; espaço ocupado pergunta antes de gravar por cima. O cursor começa no espaço do último save feito ou carregado nesta sessão; num jogo novo, no primeiro vazio.
- **Carregar** (botão **Continuar** do menu principal): abre a lista **CARREGAR** com o cursor no save **mais recente** (pelo instante gravado em `jogo/momento`). Os espaços vazios ficam apagados.
- **Save antigo:** quem tinha o `user://salvamento.cfg` de antes ganha esse save no espaço 1, automaticamente, na primeira vez que abrir o jogo.

## 3. Onde está

| O quê | Onde |
|---|---|
| Relógio da campanha (autoload `TempoDeJogo`) | `scripts/sistemas/tempo_de_jogo.gd` |
| Espaços, gravar e carregar (autoload `Salvamento`) | `scripts/sistemas/salvamento.gd` |
| Nome da fase de uma sala | `scripts/sistemas/fase.gd` (`nome_da_cena`) |
| Lista da TV, com a pergunta de gravar por cima | `cenas/visor/menu_visor.tscn`, `scripts/visor/menu_visor.gd` |
| Lista CARREGAR do menu principal | painel `Monitor/Carregar` em `cenas/menu_principal.tscn`, `scripts/menu_principal.gd` |
| Tempo na pausa | `Janela/TempoDeJogo` em `cenas/interface/tela_pausa.tscn`, `scripts/interface/tela_pausa.gd` |

Para mudar o número de espaços, mude `QUANTIDADE_DE_ESPACOS` em `salvamento.gd`. A TV tem lugar para 6 linhas; com mais, a lista da TV precisa de rolagem (a do menu principal já tem).
