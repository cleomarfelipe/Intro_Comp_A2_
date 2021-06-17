'''
Neste módulo as imagens do plano de fundo são determinadas, bem como as dimensões
da tela do jogo.

'''
# Módulos importados
import pygame
import os


# Largura e altura da tela, respectivamente;
WIDTH, HEIGHT = 750, 750 

# WIN é como chamamos a janela (WINdow) que será aberta para rodar o nosso jogo;
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Determinando uma legenda ou título do nosso jogo
pygame.display.set_caption("Space Shooter")

"""
Imagens de fundo nas linhas abaixo.
Como o nosso jogo tem o tema de naves espaciais, todas as imagens do fundo são
do espaço sideral ou algo referente à galaxias.

A função convert_alpha() foi uma recomendação do professor a fim de otimizar o
funcionamento do jogo.
"""

# BG (BackGround) recebe a primeira imagem que será o plano de fundo do nosso jogo;
BG = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background-black.png")).convert_alpha(),
    (WIDTH, HEIGHT))

# BG_2 (BackGround) recebe a segunda imagem que será o plano de fundo do nosso jogo;

# Há mais de um plano de fundo, pois este irá se alterar a medida que o jogador atingir
# níveis mais elevados.
BG_2 = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background-black-artic.png")).convert_alpha(),
    (WIDTH, HEIGHT))

# BG_3 (BackGround) recebe a terceira imagem que será o plano de fundo do nosso jogo;
BG_3 = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background-stars.png")).convert_alpha(), 
    (WIDTH, HEIGHT))

# BG_4 (BackGround) recebe a quarta e última imagem que será o plano de fundo 
# do nosso jogo;
BG_4 = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "glitch-psychedelic.png")).convert_alpha(),
    (WIDTH, HEIGHT))

# No arquivo main.py há os códigos responsáveis pelo rolamento das imagens de 
# fundo, bem como da troca dos backgrounds;