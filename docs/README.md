# Documentação — Ankhor

Bem-vindo ao repositório de documentação do **Ankhor**, jogo de terror atmosférico e sobrevivência em pixel art 2.5D desenvolvido para a disciplina de Computação Gráfica (Semestre 6) na Unifor.

---

## 📌 Fonte da Verdade e Hierarquia

Para manter a consistência entre o código, o design e o roteiro, adotamos a seguinte regra de precedência:

1. **[`docs/decisoes.md`](decisoes.md)** — **Autoridade máxima**. Toda decisão recente de design, história ou técnica registrada aqui sobrepõe qualquer outro documento.
2. **Documentos Específicos de Módulos** — Estruturações técnicas e mecânicas detalhadas em suas respectivas pastas.
3. **[`docs/gdd.md`](gdd.md)** — Sumário executivo e visão geral unificada (Game Design Document).

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
│   ├── iluminacao_e_fungos.md     # Pote de fungos, dilema luz/perigo e cápsulas de clarão
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
│   └── template_fase.md           # Modelo padronizado para documentação de novas fases/áreas
│
├── personagens/                   # Fichas técnicas e mecânica de personagens
│   ├── README.md                  # Arquitetura de personagens no Godot (Jogador vs Robôs)
│   ├── gabriel.md                 # Funcionamento mecânico do jogador (estados, estamina, inventário)
│   ├── robos.md                   # Funcionamento dos robôs de IA (sensores, FSM e patrulhas)
│   ├── antecessores.md            # Pessoas puxadas antes de Gabriel (Baltazar, Agostinho, Clarice, Valdir, Zane)
│   └── template_personagem.md     # Modelo padronizado para novas fichas de personagens
│
├── dialogos/                      # Sistema de conversação e falas
│   ├── README.md                  # Arquitetura técnica desacoplada via sinais no Godot 4.7
│   └── template_dialogo.md        # Modelo estrutural (JSON / GDScript) para criação de diálogos
│
├── historia/                      # Estrutura narrativa e narrativa ambiental
│   ├── README.md                  # Funcionamento das camadas narrativas (presente vs sonhos)
│   ├── revelacao_central.md       # Revelação central (Gabriel como paradoxo da Âncora) e o final
│   └── template_documento.md      # Modelo padronizado para documentos, bilhetes e relíquias
│
└── roteiro/                       # Roteirização cinematográfica e cutscenes
    ├── README.md                  # Diretrizes gerais de roteiro
    └── cutscenes/                 # Estrutura técnica e documentação de cutscenes
        ├── README.md              # Padrão de implementação de cutscenes no Godot
        └── seg_acordar.md         # Cutscene inicial do despertar de Gabriel
```
