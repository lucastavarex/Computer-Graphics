# Computer-Graphics
Trabalhos desenvolvidos para a disciplina de Computação Gráfica, no primeiro semestre de 2023 @UFRJ 

## trab1
O primeiro trabalho consiste em implementar um editor simples de formas geométricas 2D.

Neste trabalho, construiremos um editor simples de formas. O trabalho final implementará 5 funcionalidades: 

- Criar retângulos por clique e arraste
- Criar círculos por clique e arraste
- Aplicar translações por clique e arraste
- Aplicar rotações por clique e arraste
- Aplicar escalas ao longo de um eixo (não alinhado com o sistema de coordenadas) por clique e arraste.

Instalações
```
pip install numpy
pip install pyrr
```

## trab2
Neste trabalho faremos um "clone" do jogo "tap away 3d". O programa envolve o conhecimento de 3 técnicas discutidas em sala de aula:

- O uso de texturas
- Especificação interativa de rotações usando arcball
- Picking

## trab3
A tarefa é implementar uma demonstração de curvas B-Spline seguindo as linhas gerais do notebook B-splines mostrado em aula. Em particular, você deve desenhar B-splines uniformes de grau entre 0 e 5. Use o mouse para movimentar 6 pontos de controle numa tela bi-dimensional. Use o teclado para aumentar o diminuir o grau: tecla "d" diminui o grau e tecla "D" aumenta o grau. O código do notebook pode ser usado como referência, mas sua implementação deve usar OpenGL. 

Dicas:

- Use os seguintes comandos OpenGL para obter pontos "redondos":
- glPointSize(tamanho)
- glEnable (GL_POINT_SMOOTH)
- glEnable (GL_BLEND) 
- glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

Use glutBitmapCharacter() para desenhar as legendas dos pontos de controle.
O código do notebook é um tanto ineficiente. Você pode fazer melhor! Em particular, nem todas as funções de base precisam ser computadas para todos os pontos plotados. 
