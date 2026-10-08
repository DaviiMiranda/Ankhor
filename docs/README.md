# Documentação — Ankhor

Bem-vindo ao repositório de documentação do **Ankhor**, jogo de terror atmosférico e sobrevivência em pixel art 2.5D desenvolvido para a disciplina de Computação Gráfica (Semestre 6) na Unifor.

---

## 📌 Fonte da Verdade e Hierarquia

Para manter a consistência entre o código, o design e o roteiro, adotamos a seguinte regra de precedência:

1. **[`docs/historia/enredo_principal.md`](historia/enredo_principal.md)** — **Lei do projeto para história, mundo e personagens**, junto com as fichas de [`docs/historia/personagens/`](historia/personagens/) (uma por personagem). Vale acima de qualquer outro documento, inclusive do registro de decisões. Em caso de dúvida em qualquer parte do jogo, consulte-o primeiro. O que ele ainda não decidiu está na seção "Pendências", no fim dele.
2. **[`docs/decisoes.md`](decisoes.md)** — Autoridade máxima para design, mecânicas e técnica, e histórico de todas as mudanças (inclusive as de história, que entram no mesmo PR aqui e no Enredo Principal).
3. **Documentos Específicos de Módulos** — Estruturações técnicas e mecânicas detalhadas em suas respectivas pastas.
4. **[`docs/gdd.md`](gdd.md)** — Sumário executivo e visão geral unificada (Game Design Document).

---

## 🗺️ Mapa de Navegação da Documentação

A documentação é organizada de forma modular, servindo como guia de funcionamento de cada sistema e fornecendo templates padronizados para preenchimento:

```
docs/
├── README.md                      # Este mapa de navegação e índice mestre
├── decisoes.md                    # Registro cronológico de decisões (ADRs)
├── equipe.md                      # Papéis da equipe e entregas acadêmicas
├── fases.md                       # Ponto de entrada para o design de fases
├── gdd.md                         # GDD executivo integrado
├── sugestao-melhoramento-futuro.md # Backlog de melhorias secundárias, polimento e QoL
│
├── visao_geral/                   # Pilares conceituais, escopo e identidade
│   ├── conceito.md                # Premissa, público-alvo, escopo e pilares de design
│   └── estilo_artistico.md        # Identidade visual 2.5D, iluminação e pipeline Blender->Sprites
│
├── mecanicas/                     # Regras de jogo e funcionamento dos sistemas
│   ├── README.md                  # Diagrama do Core Loop de gameplay
│   ├── movimentacao_e_terreno.md  # Andar, correr, estamina, ruído e tipos de superfícies
│   ├── furtividade_e_esconderijos.md # Esconderijos, microgames de tensão e distrações
│   ├── iluminacao_e_lanterna.md   # Lanterna a pilha, dilema luz/perigo, luzes de emergência
│   ├── vida_e_checkpoint.md       # 3 corações, dano, tela de morte e checkpoints
│   ├── registros_e_caderno.md     # Documentos dos antecessores, rádio e o Caderno do Gabriel
│   └── sono_e_sonhos.md           # Salas seguras, mecânica de save e investigação no passado
│
├── computacao/                    # Requisitos da disciplina de Computação Gráfica / CC
│   ├── README.md                  # Matriz de algoritmos aplicados ao jogo
│   ├── grafos_e_navegacao.md      # Campus modelado como grafo ponderado dinâmico
│   ├── grade_e_coloracao.md       # Algoritmo de coloração de grafos para horários de patrulha
│   ├── ia_e_perseguicao.md        # BFS (som), A* (perseguição), Cadeia de Markov e FSM
│   └── geometria_e_shaders.md     # Visão 2D por produto escalar, raycasting e shaders
│
├── fases/                         # Design de fases e áreas
│   ├── README.md                  # Estrutura e funcionamento do level design no campus
│   ├── biblioteca.md              # Fase 1 (Confirmada): O despertar na Biblioteca Central
│   ├── labirinto.md               # Labirinto escuro com robôs (jogável pelo menu Fases)
│   └── template_fase.md           # Modelo padronizado para documentação de novas fases/áreas
│
├── dialogos/                      # Sistema de conversação e falas
│   ├── README.md                  # Arquitetura técnica desacoplada via sinais no Godot 4.7
│   └── template_dialogo.md        # Modelo estrutural (JSON / GDScript) para criação de diálogos
│
└── historia/                      # História, personagens e roteiro
    ├── enredo_principal.md        # A LEI DO PROJETO: história, mundo, personagens e pendências
    ├── README.md                  # Índice da pasta: comece pelo Enredo Principal
    ├── template_documento.md      # Modelo para escrever bilhetes, diários e relatórios
    ├── template_personagem.md     # Modelo de ficha para um personagem novo
    ├── outras_ideias.md           # Ideias ainda não decididas (não é lei)
    ├── personagens/               # Uma ficha por personagem (parte do Enredo Principal)
    │   ├── resumo.md              # Resumo de todos os personagens, para consulta rápida
    │   ├── gabriel.md             # O protagonista: estados, estamina, inventário
    │   ├── baltazar.md            # ~1750, antepassado de Gabriel
    │   ├── diana.md               # 1978, recruta da polícia
    │   ├── clarice.md             # 1994, aluna de processamento de dados
    │   ├── rafael.md              # 2008, segurança noturno
    │   ├── henrique.md            # 2019, o pesquisador
    │   ├── carlos.md              # 3026, o antagonista
    │   ├── zane.md                # 2123, o último a chegar
    │   └── robos.md               # Os robôs inimigos: sensores, FSM e patrulhas
    └── roteiro/                   # Roteirização cinematográfica e cutscenes
        ├── README.md              # Diretrizes gerais de roteiro
        └── cutscenes/             # Estrutura técnica e documentação de cutscenes
            ├── README.md          # Padrão de implementação de cutscenes no Godot
            └── seg_acordar.md     # Cutscene inicial do despertar de Gabriel
```
