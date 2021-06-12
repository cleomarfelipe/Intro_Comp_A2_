# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 18:21:22 2021
Autor: Breno Marques Azevedo

Aqui encontram-se as funções referentes aos elementos jogo (sprites).

As variáveis com nome em caixa alta não serão alteradas ao longo do programa.
"""

import pygame
import os

class Elemento_Sprite():
    # Carregando as imagens das naves inimigas;
    # ------------------------------------------
    # Nave vermelha;
    RED_SPACE_SHIP = pygame.image.load(os.path.join(
        "assets", "pixel_ship_red_small.png")).convert_alpha()
    
    # Nave verde;
    GREEN_SPACE_SHIP = pygame.image.load(os.path.join(
        "assets", "pixel_ship_green_small.png")).convert_alpha()
    
    # Nave azul;
    BLUE_SPACE_SHIP = pygame.image.load(os.path.join(
        "assets", "pixel_ship_blue_small.png")).convert_alpha()
    # ------------------------------------
    
    # Carregando imagem da nave do Jogador
    YELLOW_SPACE_player = pygame.image.load(os.path.join(
        "assets", "pixel_ship_yellow.png")).convert_alpha()
    # --------------------------------------

    # Lasers inimigos
    RED_LASERS = pygame.image.load(os.path.join(
        "assets", "pixel_laser_red.png")).convert_alpha()
    
    GREEN_LASERS = pygame.image.load(os.path.join(
        "assets", "pixel_laser_green.png")).convert_alpha()
    
    BLUE_LASERS = pygame.image.load(os.path.join(
        "assets", "pixel_laser_blue.png")).convert_alpha()
    # ----------------------------------------
    
    # Laser do  jogador
    YELLOW_LASERS = pygame.image.load(os.path.join(
        "assets", "pixel_laser_yellow.png")).convert_alpha()
    
        


