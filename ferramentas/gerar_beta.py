# gerar_beta.py — gera a versão BETA do Ankhor para Windows: exporta o jogo com
# o Godot (sem abrir a janela do editor), confere o resultado e monta o .zip que
# vai para os testadores. Passo a passo e regras da versão em docs/producao/beta.md.
#
# Como rodar (Python 3, a partir da pasta do projeto, com o jogo SEM mudanças
# por commitar):
#
#   python ferramentas/gerar_beta.py --godot "C:/caminho/Godot_v4.7.2-stable_win64_console.exe"
#
# (ou guarde o caminho na variável de ambiente GODOT). Precisa dos modelos de
# exportação do Godot 4.7.2 instalados (Editor > Gerenciar modelos de
# exportação) e do preset "Windows Desktop" que está em export_presets.cfg.
#
# O que sai (em exports/, que o .gitignore não deixa ir para o git):
#   exports/Ankhor_<versao>/Ankhor.exe     o jogo, num arquivo só (o PCK vai dentro)
#   exports/Ankhor_<versao>/LEIAME.txt     as instruções para o testador
#   exports/Ankhor_<versao>.zip            os dois arquivos acima, para enviar
#
# A versão vem de application/config/version, em project.godot: é a única fonte.
# Ela aparece no canto do menu principal, no nome da pasta e do .zip e no
# arquivo do jogo, então o testador sempre sabe qual versão está jogando.

import argparse
import os
import re
import subprocess
import sys
import zipfile

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PRESET = "Windows Desktop"
LEIAME_MODELO = os.path.join(RAIZ, "ferramentas", "leiame_beta.txt")


def ler_versao():
    with open(os.path.join(RAIZ, "project.godot"), encoding="utf-8") as arquivo:
        achado = re.search(r'^config/version="([^"]+)"', arquivo.read(), re.MULTILINE)
    if not achado:
        sys.exit("Não achei config/version em project.godot.")
    return achado.group(1)


def versao_do_preset(versao):
    """O preset guarda a versão do arquivo .exe como quatro números (0.1.0.1).
    Confere se bate com a versão do projeto, senão o .exe mostraria outra."""
    numeros = re.match(r"(\d+)\.(\d+)\.(\d+)-beta\.(\d+)", versao)
    if not numeros:
        sys.exit(f"A versão {versao} não segue o formato 0.1.0-beta.1.")
    esperado = ".".join(numeros.groups())
    with open(os.path.join(RAIZ, "export_presets.cfg"), encoding="utf-8") as arquivo:
        texto = arquivo.read()
    for chave in ("file_version", "product_version"):
        achado = re.search(rf'application/{chave}="([^"]+)"', texto)
        if not achado or achado.group(1) != esperado:
            sys.exit(f"export_presets.cfg: application/{chave} deveria ser \"{esperado}\" (a versão é {versao}).")


def exportar(godot, destino):
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    comando = [godot, "--headless", "--path", RAIZ, "--export-release", PRESET, destino]
    print("Exportando:", " ".join(comando))
    resultado = subprocess.run(comando, capture_output=True, text=True, encoding="utf-8", errors="replace")
    saida = resultado.stdout + resultado.stderr
    erros = [linha for linha in saida.splitlines() if "ERROR" in linha and "ObjectDB" not in linha and "resources still in use" not in linha]
    if resultado.returncode != 0 or not os.path.exists(destino) or erros:
        print(saida)
        sys.exit("A exportação falhou (veja as mensagens acima).")
    print(f"  ok: {os.path.relpath(destino, RAIZ)} ({os.path.getsize(destino) / 1e6:.1f} MB)")


def montar_zip(versao, pasta, exe):
    with open(LEIAME_MODELO, encoding="utf-8") as arquivo:
        leiame = arquivo.read().replace("{versao}", versao)
    caminho_leiame = os.path.join(pasta, "LEIAME.txt")
    with open(caminho_leiame, "w", encoding="utf-8", newline="\r\n") as arquivo:
        arquivo.write(leiame)
    caminho_zip = os.path.join(os.path.dirname(pasta), f"Ankhor_{versao}.zip")
    with zipfile.ZipFile(caminho_zip, "w", zipfile.ZIP_DEFLATED) as zipado:
        zipado.write(exe, f"Ankhor_{versao}/Ankhor.exe")
        zipado.write(caminho_leiame, f"Ankhor_{versao}/LEIAME.txt")
    print(f"  ok: {os.path.relpath(caminho_zip, RAIZ)} ({os.path.getsize(caminho_zip) / 1e6:.1f} MB)")
    return caminho_zip


def main():
    analise = argparse.ArgumentParser(description="Gera a versão beta do Ankhor para Windows.")
    analise.add_argument("--godot", default=os.environ.get("GODOT", ""), help="caminho do Godot 4.7.2 (de preferência o _console.exe)")
    argumentos = analise.parse_args()
    if not argumentos.godot or not os.path.exists(argumentos.godot):
        sys.exit("Diga onde está o Godot: --godot \"C:/.../Godot_v4.7.2-stable_win64_console.exe\" (ou a variável GODOT).")
    versao = ler_versao()
    versao_do_preset(versao)
    print(f"Versão: {versao}")
    pasta = os.path.join(RAIZ, "exports", f"Ankhor_{versao}")
    exe = os.path.join(pasta, "Ankhor.exe")
    exportar(argumentos.godot, exe)
    montar_zip(versao, pasta, exe)


if __name__ == "__main__":
    main()
