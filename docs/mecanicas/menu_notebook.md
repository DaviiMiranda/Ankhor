# Menu na escrivaninha do Gabriel

Cena independente: `cenas/interface/menu_notebook.tscn`. Abra essa cena no Godot
4.7.x e use **F6**. Por escolha do Davi, o menu inicial atual continua
sendo a entrada do jogo e esta cena fica separada para avaliação.

O cenário usa a geometria da escrivaninha, do notebook, da luminária, da caneca,
dos livros, da janela, da cortina e do cacto do quarto VR. O enquadramento é
fixo, de frente para o notebook, com o pôr do sol do prólogo atrás dele. A
notebook tem escala uniforme de 1,6 e fica na frente do peitoril para dar
espaço à interface. Os arquivos originais do quarto não mudam.

## Arquivos de arte

- `assets/modelagem/menu/menu_notebook.blend`: modelo editável, com câmera,
  iluminação e textos de demonstração separados da geometria.
- `assets/modelos/menu_notebook.glb`: cenário exportado para o Godot, sem os
  textos de demonstração, sem câmera e sem luzes de prévia.
- `assets/modelagem/menu/menu_notebook_previa.png`: renderização do Blender.
- `assets/modelagem/menu/gerar_menu_notebook.py`: gerador reproduzível.

Para regenerar, na raiz da pasta de trabalho:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b --factory-startup --python assets/modelagem/menu/gerar_menu_notebook.py
```

O gerador lê as funções e os materiais de `gerar_sala_visor.py` pela árvore
sintática, sem executar o `main` dele. Assim reaproveita as mesmas peças sem
exportar novamente nem sobrescrever `sala_visor.glb`. No `.blend`, as texturas
ficam empacotadas para que o arquivo continue editável em outro computador.

## Interface e entrada

`tela_menu_notebook.tscn` contém a interface do menu, com o script
`tela_menu_notebook.gd` herdando de `menu_principal.gd`. As ações de campanha,
os seis espaços de salvamento, as fases, as configurações, os controles,
os créditos e os sons continuam usando a implementação existente.

A interface é desenhada em um `SubViewport` de 256 × 160. A textura dele
é o material da malha `TelaNotebook`: os botões ficam no aparelho em 3D.
A fonte continua Galmuri7 em tamanhos 8 e 16 e com filtro Nearest. A tela é
LCD; não recebe a máscara arredondada de CRT do antigo monitor.

O mouse é convertido com uma interseção entre seu raio e o plano da tela.
Se O é o canto superior esquerdo e U e V são os vetores das duas bordas,
um ponto P na tela tem coordenadas:

```text
u = produto_escalar(P - O, U) / comprimento_ao_quadrado(U)
v = produto_escalar(P - O, V) / comprimento_ao_quadrado(V)
pixel = (u, v) * tamanho_do_viewport
```

As coordenadas UV do GLB identificam os cantos. O cálculo acompanha a
resolução da janela, sem uma região de clique fixa na imagem.
O controlador encaminha os eventos ao viewport do notebook usando
[`Viewport.push_input`](https://docs.godotengine.org/en/stable/classes/class_viewport.html#class-viewport-method-push-input).
Mouse, roda, setas, WASD, Enter/E, Esc e controle usam esse mesmo caminho.

O cenário 3D é desenhado na resolução da janela, com MSAA 2×, como o quarto
VR. A interface externa continua na base 640 × 360. O enquadramento é fixo
para manter o texto e as regiões de clique estáveis.

## Validação

Conferido no Godot 4.7.2 com renderização OpenGL Compatibility:

- Foco inicial, cliques e projeção do mouse sobre os botões do notebook.
- Abrir Opções, Controles, Créditos e Fases; voltar com Esc.
- Mover a seleção com setas e confirmar com E.
- Projeção do mouse e resolução do 3D em 1280 × 720, 1920 × 1080 e 1024 × 768.
- Novo jogo abre `seg_prologo.tscn`.
- Importação final limpa e execução sem erros de script.

Captura do jogo: `assets/modelagem/menu/menu_notebook_godot.png`.
