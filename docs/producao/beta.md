# Versões beta (builds de teste)

Como gerar o `.exe` de teste do Ankhor, de onde vem o número da versão e o que fazer antes de mandar para alguém. A primeira beta é a **0.1.0-beta.1**.

---

## 1. O número da versão

- **Formato:** `MAIOR.MENOR.CORREÇÃO-beta.N`, por exemplo `0.1.0-beta.1`. O `0` do começo quer dizer "ainda não é o jogo final". O `beta.N` conta quantas betas já saíram dessa versão: a seguinte é `0.1.0-beta.2`, e quando entrar muita coisa nova (uma fase, uma mecânica) sobe o do meio: `0.2.0-beta.1`.
- **Onde ela vive:** em um lugar só, `application/config/version` em `project.godot`. O resto sai dela:
  - o canto de baixo do **menu principal** (`cenas/interface/rotulo_versao.tscn`), para o testador dizer qual versão estava jogando;
  - o nome da pasta e do `.zip` (`Ankhor_0.1.0-beta.1`);
  - a versão que o Windows mostra nas propriedades do `.exe` (`0.1.0.1`, em `export_presets.cfg`, campos `file_version` e `product_version`).
- **Ao subir a versão,** mude **os dois lugares**: `config/version` em `project.godot` e os dois campos em `export_presets.cfg` (`0.1.0-beta.2` vira `0.1.0.2`). O `ferramentas/gerar_beta.py` confere e para se estiverem diferentes.

## 2. O ícone

O ícone do jogo é `assets/icone/ankhor_icone.png` (512 × 512, com cantos transparentes), feito a partir da arte do "A" que o Davi mandou. O `assets/icone/ankhor_icone.ico` tem os tamanhos de 16 a 256 px. O `.png` é o ícone do projeto (`config/icon`), o `.ico` vai para o `.exe` (campo `application/icon` do preset) e para a janela no Windows (`config/windows_native_icon`).

## 3. Preparar o computador (uma vez só)

O Godot precisa dos **modelos de exportação** da mesma versão do editor (4.7.2). No editor: **Editor → Gerenciar modelos de exportação → Baixar e instalar** (são mais de 1 GB). Se preferir baixar o arquivo `.tpz` à mão, ele está nas versões oficiais do Godot (`Godot_v4.7.2-stable_export_templates.tpz`). Para o preset do jogo só os arquivos `windows_release_x86_64*.exe` fazem falta, na pasta `%APPDATA%\Godot\export_templates\4.7.2.stable\`.

O preset **Windows Desktop** já está em `export_presets.cfg` (não tem senha nem segredo, por isso entra no git). Ele junta o jogo num `.exe` só (**Embed PCK**), deixa de fora `docs/`, `assets/modelagem/` e `ferramentas/` e inclui os `.json` dos diálogos.

## 4. Gerar a beta

1. **Parta da `main` atualizada,** com tudo o que vai na beta já mesclado, e do jogo **sem mudanças por commitar**: a beta tem que sair de um commit conhecido, e não da pasta de trabalho de alguém.
2. Suba o número da versão (seção 1), se for uma beta nova.
3. Rode, a partir da pasta do projeto:

   ```bash
   python ferramentas/gerar_beta.py --godot "C:/caminho/Godot_v4.7.2-stable_win64_console.exe"
   ```

   Se guardar o caminho na variável de ambiente `GODOT`, o `--godot` não precisa.
4. Sai em `exports/` (pasta que o git ignora):

   | Arquivo | O que é |
   |---|---|
   | `exports/Ankhor_<versão>/Ankhor.exe` | o jogo, num arquivo só (uns 130 MB, a maior parte é o motor do Godot) |
   | `exports/Ankhor_<versão>/LEIAME.txt` | as instruções do testador (modelo em `ferramentas/leiame_beta.txt`) |
   | `exports/Ankhor_<versão>.zip` | os dois arquivos juntos, para enviar (uns 55 MB) |

5. **Teste de fumaça** antes de enviar (numa pasta limpa, de preferência em **outro computador sem o Godot**): abrir, ver a versão no canto do menu, **Novo jogo**, andar, pegar um item, abrir o inventário, pausar, **Fases** e entrar em uma fase por cada uma das seis, salvar e **Continuar**, sair. O Windows pode mostrar "O Windows protegeu o computador": **Mais informações → Executar assim mesmo**.
6. **Marque o commit** (depois do PR da versão mesclado), para saber para sempre o que foi para os testadores:

   ```bash
   git tag -a v0.1.0-beta.1 -m "Primeira beta"
   git push origin v0.1.0-beta.1
   ```

## 5. Mandar para os testadores

- **Como:** o `.zip` num link do Drive, ou num *release* do GitHub. A pessoa descompacta e abre o `Ankhor.exe`, sem instalar nada.
- **Junto do jogo,** o `LEIAME.txt` já diz como jogar, o aviso do Windows, o que já se sabe que falta e como mandar o retorno. **Atualize a lista de "o que ainda não está pronto"** em `ferramentas/leiame_beta.txt` antes de cada beta.
- **O retorno** vem com a versão (canto do menu), onde a pessoa estava, o que fez e, se travou, o arquivo `godot.log`, que o jogo grava sozinho em `%APPDATA%\Godot\app_userdata\Ankhor\logs\`. Junte os relatos numa lista única e passe cada erro para o Trello ou para uma *issue*.

## 6. Limites desta beta

- **Só Windows 64 bits.** Outras plataformas pedem outro preset e outros modelos de exportação.
- **O `.exe` não tem assinatura digital** (certificado pago, que não vale para trabalho de faculdade), então o Windows e alguns antivírus desconfiam. Avise os testadores.
- **O jogo abre em tela cheia** (F11 alterna), e o menu **Fases** deixa abrir qualquer fase direto, o que é útil para testar. Numa versão final, esse menu sairia.
- **A autoria e a licença da trilha sonora** ainda estão como "(preencher)" em `assets/audio/creditos.md`: resolva antes de divulgar o jogo para fora do grupo e da turma.
- **Build é de release:** os erros não aparecem numa janela de console. Para investigar um problema, abra o projeto no editor.
