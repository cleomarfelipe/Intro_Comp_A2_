# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 18:48:29 2021

Autores:
    Breno Marques Azevedo
    
Aqui encontram-se a classe e funções referentes ao fundo do nosso jogo.

Variaveis com nome em caixa alta não serão alteradas ao longo do programa.
"""

import pygame
import os

class Fundo:
    # Essa classe cria funções relacionadas ao fundo do jogo;
    
    """
    A intenção é que as imagens de fundo se movam em um loop enquanto o jogo roda.
    Por isso escolhi imagens genéricas que podem ser usadas dessa forma facilmente.
    
    Além disso, é interessante que as imagens de fundo mudem conforme o jogador 
    passe de nível. Por isso temos mais de uma imagem de fundo.
    """
    
    # Tamanho da tela
    # É mais cômodo determinar a largura e comprimento da tela dentro da classe Fundo.
    WIDTH, HEIGHT = 750, 750
    
    # Imagens de fundo
    # Convertendo as imagens de fundo para se adequarem às escalas da tela;
    BG = pygame.transform.scale(pygame.image.load(
        os.path.join("assets", "background-black.png")).convert_alpha(),
        (WIDTH, HEIGHT))
    
    BG_2 = pygame.transform.scale(pygame.image.load(
        os.path.join("assets", "background-black-artic.png")).convert_alpha(), 
        (WIDTH, HEIGHT))
    
    BG_3 = pygame.transform.scale(pygame.image.load(
        os.path.join("assets", "background-stars.png")).convert_alpha(), 
        (WIDTH, HEIGHT))
    
    BG_4 = pygame.transform.scale(pygame.image.load(
        os.path.join("assets", "glitch-psychedelic.png")).convert_alpha(), 
        (WIDTH, HEIGHT))

    pass

