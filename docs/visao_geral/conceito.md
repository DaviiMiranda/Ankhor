# Visão Geral — Conceito e Pilares

## 1. Informações Básicas

- **Título do Jogo:** Ankhor
- **Gênero:** Terror atmosférico, sobrevivência, investigação e furtividade (*Stealth Horror*)
- **Plataforma:** PC (Windows)
- **Engine:** Godot Engine 4.7.x (GDScript)
- **Público-alvo:** Adolescentes e adultos (14+ anos). Foco em suspense psicológico, tensão e ambientação, sem apelo a violência gráfica ou gore gratuito. Conexão emocional especial para alunos e egressos da Unifor.

---

## 2. Resumo da Premissa

Gabriel, um estudante universitário, acorda **mil anos no futuro, em 3026**.

Ele descobre o que aconteceu com ele e com outras pessoas de outras épocas: em 3026, a Unifor é um centro de pesquisa em física do tempo, e a explosão de um aparelho chamado **Âncora** rasgou o tempo dentro do campus. A fenda temporal encosta em momentos aleatórios do passado e puxa quem estiver perto — numa madrugada de 2026, puxou Gabriel da Biblioteca.

A fenda está crescendo e, se não for fechada, vai engolir o passado do campus, incluindo o tempo de Gabriel. Gabriel não é o primeiro a ser puxado: antes dele vieram uma aluna de 1994, um segurança de 2008, um professor de 2019 e alguém de 2041, e ninguém conseguiu. Esses viajantes deixaram **bilhetes** pelo campus explicando melhor os acontecimentos. O campus em ruínas é patrulhado por **robôs**. Para sobreviver, impedir o colapso e salvar seu próprio tempo, Gabriel precisa investigar as ruínas do campus, evitar os robôs, entender o que ocorreu através dos bilhetes e fechar a fenda.

---

## 3. Pilares de Design (Core Pillars)

Todo sistema, diálogo e elemento visual do jogo deve apoiar estes quatro pilares:

### I. Estranhamento do Familiar (*The Uncanny Familiar*)
O choque não vem de monstros de outro planeta, mas de ver elementos triviais do cotidiano universitário — uma catraca eletrônica enferrujada, um bebedouro quebrado, uma grade de horários num quadro negro desbotado, a clássica cantina — fossilizados pelo tempo de mil anos. O contraste entre o campus vivo da memória e a ruína silenciosa do presente gera a atmosfera única do jogo.

### II. O Tempo como Relógio Mortal: Rotinas de Patrulha
Os robôs patrulham o campus seguindo rotinas e rondas estruturadas. O jogador que dominar os padrões de patrulha ganha a chave da segurança; quem os ignora entra desprevenido no campo de visão e detecção de um robô.

### III. Dormir é Salvar e é Lembrar
Em jogos tradicionais de sobrevivência, salvar é uma ação puramente técnica. Em *Ankhor*, dormir é salvar o jogo e é **a única maneira de acessar o passado**. Ao dormir em salas seguras, Gabriel é transportado em sonho para a última semana antes da catástrofe, onde o campus está iluminado, cheio e funcional. É nos sonhos que o jogador obtém senhas, lê os quadros de aviso originais e descobre a rotina dos robôs para usar no presente.

### IV. Vulnerabilidade e Defesa Restrita (*Stealth over Combat*)
Gabriel é um estudante comum, não um combatente. Fugir e se esconder é a regra absoluta; defender-se é uma exceção cara e desesperada. A luz revela caminhos mas atrai perigo; correr acelera o deslocamento mas reverbera sons pelas salas do campus. Cada recurso (fungos de iluminação e cápsulas de clarão) é escasso e precioso.

---

## 4. Escopo do Projeto

O jogo foi concebido sob a filosofia de **"o menor passo que funciona com excelência"**:
- **Ambiente Contínuo:** Campus da Unifor em ruínas, com áreas interligadas por portas, passagens e atalhos no grafo. A primeira fase definida é a **Biblioteca**.
- **Progressão Narrativa:** Avanço por resolução de puzzles, exploração e conhecimento adquirido nos sonhos e nas pistas deixadas por outras épocas.
- **Entrega Acadêmica:** Atendimento integral aos requisitos da disciplina de Computação Gráfica através de mecânicas jogáveis (Grafos, BFS, A*, Coloração, Markov, Visão 2D com Produto Escalar e Shaders).
