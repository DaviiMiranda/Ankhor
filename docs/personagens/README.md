# Personagens — Estrutura e Funcionamento

Este documento define como os personagens e inimigos são arquitetados e funcionam mecanicamente em **Ankhor**.

---

## 🎭 Arquitetura de Personagens no Godot 4.7

Conforme as regras do projeto, cada personagem e inimigo é uma **cena isolada** (`.tscn`) com seu respectivo script (`.gd`):

1. **O Jogador (Gabriel):**
   - Controlado pelo usuário através de inputs (`CharacterBody2D`).
   - Possui máquina de estados de locomoção (Parado, Andando, Correndo, Agachado, Escondido, Exausto).
   - Detalhes mecânicos em [`gabriel.md`](gabriel.md).

2. **Os Robôs (Inimigos de IA):**
   - Controlados por inteligência artificial autônoma (`CharacterBody2D`).
   - Operam sob uma Máquina de Estados Finita (Rotina, Investigando, Caçando, Atordoado, Retornando).
   - Possuem sensores de percepção (visão por produto escalar e raycast, audição conectada ao grafo BFS, fotossensibilidade).
   - Detalhes de funcionamento em [`robos.md`](robos.md).

3. **NPCs dos Sonhos (Interações Passivas):**
   - Cenas leves focadas em interação de diálogo e passagem de informações investigativas.

4. **Os Antecessores (pessoas puxadas antes de Gabriel):**
   - Baltazar (~1750), Agostinho (1978), Clarice (1994), Valdir (2008), o professor (2019) e Zane (2123).
   - Aparecem como bilhetes, diários, áudios, NPCs de sonho e, no caso de Valdir, uma voz no rádio.
   - Fichas em [`antecessores.md`](antecessores.md).

---

## 📋 Como Criar uma Nova Ficha de Personagem

Para documentar um novo personagem quando o grupo decidir seu papel narrativo e mecânico:
👉 Utilize o modelo padronizado em **[`template_personagem.md`](template_personagem.md)**.
