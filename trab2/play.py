#   Rio de Janeiro, June 10, 2023   @UFRJ - Computer Graphics
#   Professor: Cláudio Esperança
#   Subject: Tap Away 3D Game
#   Author: Lucas Tavares Da Silva Ferreira
#   DRE: 120152739


import sys
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import random
import numpy as np
from math import degrees

from PIL  import Image
from arcball import ArcBall

# As seguintes variáveis são usadas para armazenar informações sobre o estado do jogo,
# como o cubo selecionado (selected), os cubos removidos (removed), o tamanho do cubo (n), 
# a largura e altura da janela (width e height), e as animações de clique e remoção dos cubos 
# (animacao_click e animacao_remocao).

# Selected object
selected = [];

# Set of removed objects
removed = set();

# size of cube array
n = 3;

animacao_click = dict();
animacao_remocao = dict();
distancia_remocao = 10;
distancia_click = 0.2 * 1/n;

# Esse código tem como objetivo encontrar as coordenadas de um cubo tridimensional a partir de um número fornecido.
def encontra_coordenada_cubo(nome):
    x = nome // n**2 ;
    resto = nome % n**2;
    y = resto // n ;
    z = resto % n ;
    return x,y,z ;

# Função que retorna o nome do cubo com base nas coordenadas (x, y, z)
def acha_nome_do_cubo(x,y,z):
    return x * n**2 + y * n + z ;

# Função que gera direções aleatórias para os cubos
def gera_direcoes_aleatorias():
    direcoes = [] ; # Cria uma lista vazia para armazenar as direções aleatórias
    for nome in range(n**3): # Itera sobre os números de 0 a (n**3) - 1
        direcao_aleatoria = random.randint(1, 6) ; # Gera um número aleatório entre 1 e 6 para representar uma direção
        direcoes += [direcao_aleatoria] ; # Adiciona a direção aleatória à lista de direções
    return direcoes # Retorna a lista de direções aleatórias

# Função que valida as direções dos cubos para garantir que todos os cubos são acessíveis
def valida_direcoes(direcoes):
    direcoes_disponiveis = [1, 2, 3, 4, 5, 6]  # Lista das direções disponíveis (1 a 6)
    cubos_removidos = set()  # Conjunto para armazenar os cubos que foram removidos
    while (len(cubos_removidos) < n**3 - 1):  # Enquanto ainda houver cubos não removidos
        qntd_removidos = 0  # Variável para contar a quantidade de cubos removidos em cada iteração
        for x in range(n):  # Percorre as coordenadas x do cubo (0 a n-1)
            for y in range(n):  # Percorre as coordenadas y do cubo (0 a n-1)
                for z in range(n):  # Percorre as coordenadas z do cubo (0 a n-1)
                    cubo_atual = x, y, z  # Coordenadas do cubo atual
                    nome_do_cubo = acha_nome_do_cubo(*cubo_atual)  # Encontra o nome do cubo com base nas coordenadas
                    if cubo_atual in cubos_removidos:  # Se o cubo atual já foi removido, continua para o próximo
                        continue
                    else:
                        proximo_cubo = pega_proximo_cubo(cubo_atual, direcoes[nome_do_cubo])  # Obtém o próximo cubo com base na direção atual
                        while proximo_cubo in cubos_removidos:  # Enquanto o próximo cubo já tiver sido removido, busca o próximo
                            proximo_cubo = pega_proximo_cubo(proximo_cubo, direcoes[nome_do_cubo])
                        if proximo_cubo is None:  # Se não houver próximo cubo, significa que o cubo atual foi removido
                            cubos_removidos.add(cubo_atual)  # Adiciona o cubo atual ao conjunto de cubos removidos
                            qntd_removidos += 1  # Incrementa a quantidade de cubos removidos
        if (qntd_removidos > 0):  # Se houver cubos removidos nesta iteração, continua para a próxima iteração
            continue
        else:  # Se nenhum cubo foi removido nesta iteração
            for cubo in range(n**3):  # Percorre todos os cubos
                if encontra_coordenada_cubo(cubo) not in cubos_removidos:  # Se o cubo não estiver removido
                    direcao_atual = direcoes[cubo]  # Obtém a direção atual do cubo
                    direcoes[cubo] = random.choice([x for x in direcoes_disponiveis if x != direcao_atual])  # Escolhe aleatoriamente uma nova direção diferente da atual
    return direcoes  # Retorna as direções válidas

def pega_proximo_cubo(cubo, direcao):
    x, y, z = cubo  # Extrai as coordenadas do cubo atual
    if direcao == 1:  
        if z == n - 1:  # Se o cubo está na borda direita do eixo z, não há próximo cubo nessa direção
            return None
        return x, y, z + 1  # Retorna as coordenadas do próximo cubo na direção 1 (z + 1)
    elif direcao == 2:  
        if z == 0:  # Se o cubo está na borda esquerda do eixo z, não há próximo cubo nessa direção
            return None
        return x, y, z - 1  # Retorna as coordenadas do próximo cubo na direção 2 (z - 1)
    elif direcao == 3:  
        if y == n - 1:  # Se o cubo está na borda superior do eixo y, não há próximo cubo nessa direção
            return None
        return x, y + 1, z  # Retorna as coordenadas do próximo cubo na direção 3 (y + 1)
    elif direcao == 4:  
        if y == 0:  # Se o cubo está na borda inferior do eixo y, não há próximo cubo nessa direção
            return None
        return x, y - 1, z  # Retorna as coordenadas do próximo cubo na direção 4 (y - 1)
    elif direcao == 5:  
        if x == n - 1:  # Se o cubo está na borda superior do eixo x, não há próximo cubo nessa direção
            return None
        return x + 1, y, z  # Retorna as coordenadas do próximo cubo na direção 5 (x + 1)
    elif direcao == 6:  
        if x == 0:  # Se o cubo está na borda inferior do eixo i, não há próximo cubo nessa direção
            return None
        return x - 1, y, z  # Retorna as coordenadas do próximo cubo na direção 6 (x - 1)

directions = valida_direcoes(gera_direcoes_aleatorias())  # Obtém as direções válidas após a validação

def loadTexture(filename):
    "Loads an image from a file as a texture"

    # Read file and pega pixels
    imagefile = Image.open(filename);
    sx,sy = imagefile.size[0:2];
    global pixels;
    pixels = imagefile.convert("RGBA").tobytes("raw", "RGBA", 0, -1);

    # Create an OpenGL texture name and load image into it
    image = glGenTextures(1);
    glBindTexture(GL_TEXTURE_2D, image);  
    glPixelStorei(GL_UNPACK_ALIGNMENT,1);
    glTexImage2D(GL_TEXTURE_2D, 0, 3, sx, sy, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels);
    
    # Set other texture mapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
    
    # Return texture name (an integer)
    return image

# Essa estrutura coordenadas_textura armazena as coordenadas de textura para cada face dos cubos. 
# Cada entrada da estrutura corresponde a um tamanho de cubo (1, 2 ou 3). 
# Por exemplo, coordenadas_textura[1] contém as coordenadas de textura para um cubo de tamanho 1, 
# coordenadas_textura[2] para um cubo de tamanho 2 e assim por diante...

coordenadas_textura = {
   
    6: [[(0.0, 1.0),(0.0, 0.0),(1.0, 0.0),(1.0, 1.0)], 
        [(1.0, 0.0),(1.0, 1.0),(0.0, 1.0),(0.0, 0.0)], 
        [(0.0, 1.0),(0.0, 0.0),(1.0, 0.0),(1.0, 1.0)], 
        [(1.0, 0.0),(1.0, 1.0),(0.0, 1.0),(0.0, 0.0)], 
        [(0.0, 0.0),(1.0, 0.0),(1.0, 0.2),(0.0, 0.2)], 
        [(0.0, 0.8),(1.0, 0.8),(1.0, 1.0),(0.0, 1.0)]],
  
    5: [[(1.0, 0.0),(1.0, 1.0),(0.0, 1.0),(0.0, 0.0)], 
        [(0.0, 1.0),(0.0, 0.0),(1.0, 0.0),(1.0, 1.0)], 
        [(1.0, 0.0),(1.0, 1.0),(0.0, 1.0),(0.0, 0.0)], 
        [(0.0, 1.0),(0.0, 0.0),(1.0, 0.0),(1.0, 1.0)], 
        [(0.0, 0.8),(1.0, 0.8),(1.0, 1.0),(0.0, 1.0)],
        [(0.0, 0.0),(1.0, 0.0),(1.0, 0.2),(0.0, 0.2)]], 
    
    4: [[(1.0, 1.0),(0.0, 1.0),(0.0, 0.0),(1.0, 0.0)], 
        [(1.0, 1.0),(0.0, 1.0),(0.0, 0.0),(1.0, 0.0)], 
        [(0.0, 0.0),(1.0, 0.0),(1.0, 0.2),(0.0, 0.2)], 
        [(0.0, 0.8),(1.0, 0.8),(1.0, 1.0),(0.0, 1.0)], 
        [(1.0, 1.0),(0.0, 1.0),(0.0, 0.0),(1.0, 0.0)], 
        [(1.0, 1.0),(0.0, 1.0),(0.0, 0.0),(1.0, 0.0)]], 
    
    3: [[(0.0, 0.0),(1.0, 0.0),(1.0, 1.0),(0.0, 1.0)], 
        [(0.0, 0.0),(1.0, 0.0),(1.0, 1.0),(0.0, 1.0)], 
        [(0.0, 0.8),(1.0, 0.8),(1.0, 1.0),(0.0, 1.0)],
        [(0.0, 0.0),(1.0, 0.0),(1.0, 0.2),(0.0, 0.2)], 
        [(0.0, 0.0),(1.0, 0.0),(1.0, 1.0),(0.0, 1.0)], 
        [(0.0, 0.0),(1.0, 0.0),(1.0, 1.0),(0.0, 1.0)]], 

    2: [[(0.0, 0.0),(1.0, 0.0),(1.0, 0.2),(0.0, 0.2)], 
        [(0.0, 0.8),(1.0, 0.8),(1.0, 1.0),(0.0, 1.0)], 
        [(0.0, 0.0),(1.0, 0.0),(1.0, 1.0),(0.0, 1.0)], 
        [(0.0, 0.0),(1.0, 0.0),(1.0, 1.0),(0.0, 1.0)], 
        [(1.0, 0.0),(1.0, 1.0),(0.0, 1.0),(0.0, 0.0)], 
        [(0.0, 1.0),(0.0, 0.0),(1.0, 0.0),(1.0, 1.0)]], 

    1: [[(0.0, 0.8),(1.0, 0.8),(1.0, 1.0),(0.0, 1.0)], 
        [(0.0, 0.0),(1.0, 0.0),(1.0, 0.2),(0.0, 0.2)], 
        [(1.0, 1.0),(0.0, 1.0),(0.0, 0.0),(1.0, 0.0)], 
        [(1.0, 1.0),(0.0, 1.0),(0.0, 0.0),(1.0, 0.0)], 
        [(0.0, 1.0),(0.0, 0.0),(1.0, 0.0),(1.0, 1.0)], 
        [(1.0, 0.0),(1.0, 1.0),(0.0, 1.0),(0.0, 0.0)]]  
}

def draw_cube(flatColors = False):
    global n, directions, animacao_remocao, animacao_click, textureId_arrow, matrix ;
    glClearColor(0.0, 1.0, 0.0, 1.0) ; # Define a cor para verde
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) ;  # Limpa os buffers de cor e profundidade
    glMatrixMode(GL_MODELVIEW) ;  # Define o modo de visualização da matriz de modelo
    glLoadIdentity() ; # Carrega a matriz de identidade
    glTranslatef(0, 0, -3) ; # Translada a cena em relação ao eixo Z para trás
    glRotatef(-80, 1, 0, 0) ;  # Rotaciona a cena em relação ao eixo X
    glMultMatrixd (matrix) ; # Multiplica a matriz atual pela matriz fornecida
    size = 1 / n ; # Calcula o tamanho de cada cubo com base no número de cubos em cada dimensão
     # Loop pelos cubos em cada dimensão
    for i in range(n):
        x = i - (n - 1) / 2 ;
        for j in range(n):
            y = j - (n - 1) / 2 ;
            for k in range(n):
                z = k - (n - 1) / 2 ;
                name = (i * n + j) * n + k ;  
                if flatColors:
                    glColor3f((i+1)/n, (j+1)/n, (k+1)/n) ;
                if name in removed:
                    continue
                glLoadName(name) ;
                glPushMatrix() ;
                glTranslatef(x * size, y * size, z * size) ;

                if name in animacao_remocao:
                    removal_direction = animacao_remocao.get(name)[0] ;
                    removal_step = animacao_remocao.get(name)[1] ;

                    if removal_direction == 1:  
                        glTranslatef(0, 0, removal_step) ;
                    elif removal_direction == 2:  
                        glTranslatef(0, 0, -removal_step) ;
                    elif removal_direction == 3:  
                        glTranslatef(0, removal_step, 0) ;
                    elif removal_direction == 4:  
                        glTranslatef(0, -removal_step, 0) ;
                    elif removal_direction == 5:  
                        glTranslatef(removal_step, 0, 0) ;
                    elif removal_direction == 6:  
                        glTranslatef(-removal_step, 0, 0) ;
                
                elif name in animacao_click:
                    click_direction = animacao_click.get(name)[0] ;
                    click_step = animacao_click.get(name)[1] ;

                    if click_direction == 1:  
                        glTranslatef(0, 0, click_step) ;
                    elif click_direction == 2:  
                        glTranslatef(0, 0, -click_step) ;
                    elif click_direction == 3:  
                        glTranslatef(0, click_step, 0) ;
                    elif click_direction == 4:  
                        glTranslatef(0, -click_step, 0) ;
                    elif click_direction == 5:  
                        glTranslatef(click_step, 0, 0) ;
                    elif click_direction == 6:  
                        glTranslatef(-click_step, 0, 0) ;

                if flatColors:
                    glutSolidCube(size*0.8) ;
                else:
                    glEnable(GL_TEXTURE_2D) ;
                    glBindTexture(GL_TEXTURE_2D, textureId_arrow) ;
                    glBegin(GL_QUADS) ;
                    
                    dir = directions[name] ;
                    
                    # Front Face (note that the texture's corners have to match the quad's corners)
                    glNormal3f(0, 0, 1) ;
                    glTexCoord2f(*coordenadas_textura[dir][0][0]) ;
                    glVertex3f(-size*0.8/2, -size*0.8/2, size*0.8/2) ;
                    glTexCoord2f(*coordenadas_textura[dir][0][1]) ;
                    glVertex3f(size*0.8/2, -size*0.8/2, size*0.8/2) ;  
                    glTexCoord2f(*coordenadas_textura[dir][0][2]) ;
                    glVertex3f(size*0.8/2, size*0.8/2, size*0.8/2) ;
                    glTexCoord2f(*coordenadas_textura[dir][0][3]) ;
                    glVertex3f(-size*0.8/2, size*0.8/2, size*0.8/2) ;
                    # Back Face
                    glNormal3f(0,0,-1) ;
                    glTexCoord2f(*coordenadas_textura[dir][1][0]) ;
                    glVertex3f(size*0.8/2, -size*0.8/2, -size*0.8/2) ;
                    glTexCoord2f(*coordenadas_textura[dir][1][1]) ;
                    glVertex3f(-size*0.8/2, -size*0.8/2, -size*0.8/2) ;
                    glTexCoord2f(*coordenadas_textura[dir][1][2]) ;
                    glVertex3f(-size*0.8/2, size*0.8/2, -size*0.8/2) ;
                    glTexCoord2f(*coordenadas_textura[dir][1][3]) ;
                    glVertex3f(size*0.8/2, size*0.8/2, -size*0.8/2) ;
                    # Top Face
                    glNormal3f(0,1,0) ;
                    glTexCoord2f(*coordenadas_textura[dir][2][0]) ;
                    glVertex3f(-size*0.8/2, size*0.8/2, size*0.8/2)  ;
                    glTexCoord2f(*coordenadas_textura[dir][2][1]) ;
                    glVertex3f(size*0.8/2, size*0.8/2, size*0.8/2) ;
                    glTexCoord2f(*coordenadas_textura[dir][2][2]) ;
                    glVertex3f(size*0.8/2, size*0.8/2, -size*0.8/2) ;
                    glTexCoord2f(*coordenadas_textura[dir][2][3]) ;
                    glVertex3f(-size*0.8/2, size*0.8/2, -size*0.8/2) ;
                    # Bottom Face
                    glNormal3f(0,-1,0) ;
                    glTexCoord2f(*coordenadas_textura[dir][3][0]) ;
                    glVertex3f(size*0.8/2, -size*0.8/2, size*0.8/2) ;
                    glTexCoord2f(*coordenadas_textura[dir][3][1]) ;
                    glVertex3f(-size*0.8/2, -size*0.8/2, size*0.8/2) ;
                    glTexCoord2f(*coordenadas_textura[dir][3][2]) ;
                    glVertex3f(-size*0.8/2, -size*0.8/2, -size*0.8/2) ;
                    glTexCoord2f(*coordenadas_textura[dir][3][3]) ;
                    glVertex3f(size*0.8/2, -size*0.8/2, -size*0.8/2) ;
                    # Right face
                    glNormal3f(1,0,0) ;
                    glTexCoord2f(*coordenadas_textura[dir][4][0]) ;
                    glVertex3f(size*0.8/2, -size*0.8/2, size*0.8/2) ;
                    glTexCoord2f(*coordenadas_textura[dir][4][1]) ;
                    glVertex3f(size*0.8/2, -size*0.8/2, -size*0.8/2) ;
                    glTexCoord2f(*coordenadas_textura[dir][4][2]) ;
                    glVertex3f(size*0.8/2, size*0.8/2, -size*0.8/2) ;
                    glTexCoord2f(*coordenadas_textura[dir][4][3]) ;
                    glVertex3f(size*0.8/2, size*0.8/2, size*0.8/2) ; 
                    # Left Face
                    glNormal3f(-1,0,0) ;
                    glTexCoord2f(*coordenadas_textura[dir][5][0]) ;
                    glVertex3f(-size*0.8/2, -size*0.8/2, -size*0.8/2) ;
                    glTexCoord2f(*coordenadas_textura[dir][5][1]) ;
                    glVertex3f(-size*0.8/2, -size*0.8/2, size*0.8/2) ;
                    glTexCoord2f(*coordenadas_textura[dir][5][2]) ;
                    glVertex3f(-size*0.8/2, size*0.8/2, size*0.8/2) ;
                    glTexCoord2f(*coordenadas_textura[dir][5][3]) ;
                    glVertex3f(-size*0.8/2, size*0.8/2, -size*0.8/2) ;

                    glEnd() ;
                    glDisable(GL_TEXTURE_2D) ;

                glPopMatrix() ;

# Dimensions
width  = 650;
height = 650;

def draw_you_win():
    global textureId_win ;
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) ;
    glMatrixMode(GL_PROJECTION) ;
    glLoadIdentity() ;
    gluOrtho2D(0, width, 0, height) ;
    glMatrixMode(GL_MODELVIEW) ;
    glLoadIdentity() ;
    glBindTexture(GL_TEXTURE_2D, textureId_win) ;
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL) ;
    glEnable(GL_TEXTURE_2D) ;

    glBegin(GL_QUADS) ;
    glTexCoord2f(0.0, 0.0) ;
    glVertex2f(0, 0) ;          
    glTexCoord2f(1.0, 0.0) ;
    glVertex2f(width, 0) ;      
    glTexCoord2f(1.0, 1.0) ;
    glVertex2f(width, height) ;
    glTexCoord2f(0.0, 1.0) ;
    glVertex2f(0, height) ;     
    glEnd() ;
    
    glDisable(GL_TEXTURE_2D) ;


def display():
    if (len(removed) < n ** 3):
        draw_cube() ;
    else:
        draw_you_win() ;
    glutSwapBuffers() ;


def animacao_atualiza_remocao():
    global distancia_remocao, removed, selected, animacao_remocao;
    if animacao_remocao: 
        for name in animacao_remocao.copy():
            animation_info = animacao_remocao.get(name);
            animation_info[1] += 0.07 ;
            if animation_info[1] >= distancia_remocao:
                removed.add(name);
                del animacao_remocao[name] ;

def animacao_click_atualiza():
    global distancia_click, removed, selected, animacao_click;
    if animacao_click:
        for name in animacao_click.copy():
            animation_info = animacao_click.get(name);
            if animation_info[2] == True:
                animation_info[1] += 0.01 ;
                if animation_info[1] >= distancia_click: 
                    animation_info[2] = False ;
            if animation_info[2] == False: 
                animation_info[1] -= 0.01 ;
                if animation_info[1] <= 0.0:
                    del animacao_click[name] ;


def init():
    """Initialize state"""
    global textureId_arrow, textureId_win, matrix ;
    glClearColor(0.0, 0.0, 0.0, 1.0) ;
    glEnable(GL_DEPTH_TEST) ;
    glEnable(GL_LIGHTING) ;
    glLight(GL_LIGHT0, GL_POSITION, [.0,.2,0.5,0]) ;
    glMaterial(GL_FRONT_AND_BACK, GL_EMISSION, [0.2,0.2,0.2,1]) ;
    glEnable(GL_LIGHT0) ;
    glEnable(GL_NORMALIZE) ;
    # Helps with antialiasing
    glEnable(GL_MULTISAMPLE) ;
    
    matrix = glGetDoublev(GL_MODELVIEW_MATRIX) ;
    textureId_arrow = loadTexture("arrow.jpg") ;
    textureId_win = loadTexture("youwin.png") ;


def reshape(w, h):
    """Reshape Callback"""
    global width, height ;
    global projectionArgs, windowSize ;
    windowSize = width,height ;
    width, height = w, h ;
    glMatrixMode (GL_PROJECTION) ;
    glLoadIdentity() ;
    projectionArgs = 50, width/height, 0.1,20 ;
    gluPerspective (*projectionArgs) ;
    glViewport (0,0,width,height) ;


def pick2(x,y):
    glDisable(GL_LIGHTING) ;
    draw_cube(True) ;
    glFlush() ;
    glEnable (GL_LIGHTING) ;
    buf = glReadPixels (x,windowSize[1]-y,1,1,GL_RGB,GL_FLOAT) ;
    pixel = buf[0][0] ;
    r,g,b = pixel ;
    i,j,k = int(r*n-1),int(g*n-1),int(b*n-1) ;
    if i >= 0: return (i*n + j) * n + k ;
    return -1 

def mousePressed(button, state, x, y):
    global selected,startx,starty ;
    if state == GLUT_DOWN:
        startx, starty = x, y ;
        selected = pick2(x,y) ;
        if selected >= 0:
            animacao_click[selected] = [directions[selected], 0.0, True] ;

        global arcball ;
        global prevx, prevy ;
        arcball = ArcBall ((width/2,height/2,0), width/2) ;
        prevx, prevy = startx, starty ;
        glutMotionFunc (callback_rotacao) ;

    elif state == GLUT_UP:
        glutMotionFunc (None) ;
        if (x,y) == (startx,starty): 
            if selected >= 0:
                cube_free = pode_remover_bool(selected) ;
                if cube_free:
                    animacao_remocao[selected] = [directions[selected], 0.0] ;
                selected = None ;
    glutPostRedisplay() ;


def callback_rotacao (x, y):
    global prevx,prevy,matrix,arcball ;
    angle, axis = arcball.rot (prevx, height - prevy, x, height - y) ;
    glLoadIdentity () ;
    glRotatef (degrees(angle),*axis) ;
    glMultMatrixd (matrix) ;
    matrix = glGetDoublev(GL_MODELVIEW_MATRIX) ;
    prevx, prevy = x, y ;
    glutPostRedisplay() ;


def pode_remover_bool(cube):
    global n, directions, removed, animacao_remocao ;
    cube_coord = encontra_coordenada_cubo(cube) ;
    proximo_cubo_coord = pega_proximo_cubo(cube_coord, directions[cube]) ;
    while True:
        if proximo_cubo_coord == None: 
            return True 
        else:
            if acha_nome_do_cubo(*proximo_cubo_coord) in removed or acha_nome_do_cubo(*proximo_cubo_coord) in animacao_remocao:
                proximo_cubo_coord = pega_proximo_cubo(proximo_cubo_coord,directions[cube]);
            else: 
                return False

def idle():
    """Idle callback. Rotate and redraw the scene"""
    animacao_atualiza_remocao();
    animacao_click_atualiza();
    glutPostRedisplay();


def main():
    glutInit(sys.argv);
    glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE);
    glutInitWindowSize (650, 650);
    glutInitWindowPosition (250, 250);
    glutCreateWindow ("Tapa way 3D");
    init ();
    glutReshapeFunc(reshape);
    glutDisplayFunc(display);
    glutMouseFunc(mousePressed);
    glutIdleFunc(idle);
    glutMainLoop();


main()
