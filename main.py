# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 18:26:27 2021

Autores:
    Breno Marques Azevedo
    
    
Aqui encotram-se as classes e funções principais do jogo.
"""

import pygame
import os
import time
import random
from fundo import Fundo
from elementos import Elemento_Sprite

# Função que abilita o uso de diferentes fontes do pygame;
pygame.font.init() 

# Função que abilita os efeitos sonoros do pygame;
pygame.mixer.init()

"""
Várias como nome em caixa alta não serão alteradas ao londo do nosso programa.
"""

# # Tamanho da tela
# WIDTH, HEIGHT = 750, 750

"""
********************************************************
AQUI ENCONTRAM-SE AS VARIÁVEIS REFERENTES AOS EFEITOS SONOROS.
*********************************************************
"""

# Efeitos Sonoros - Música de fundo;
music = pygame.mixer.music.load('futurama_theme.mp3')

# O parâmento -1 da função play() faz com que a música toque em loop no jogo;
pygame.mixer.music.play(-1)

# Efeitos Sonoros - Som do laser;
# Esse som será usado na nave do jogador;
laser_sound = pygame.mixer.Sound('laser_wrath.wav')

# Volume do som do laser do jogador;
laser_sound.set_volume(0.1)

# Efeitos Sonoros - Larger explosion sound;
# Esse som será usado quando o jogador perder todas as vidas ou saúde;
larger_explosion_sound = pygame.mixer.Sound('larger_explosion.wav')

# Volume do som da explosão "maior" (larger)
larger_explosion_sound.set_volume(0.2)  

# Efeitos Sonoros - Smaller explosion sound
# Esse som será usado quando o jogador sofrer algum dano e perder saúde;
smaller_explosion_sound = pygame.mixer.Sound('smaller_explosion.wav')

# Volume do som da explosão "menor" (smaller)
smaller_explosion_sound.set_volume(0.2) 

"""

"""

class Jogo:
    def __init__(self,
                 main_font, 
                 lost_font,
                 run,
                 FPS,
                 level,
                 lives,
                 y,
                 WIN,
                 ):
        super().__init__(main_font, lost_font)
       # Determinando a fonte e seu tamanho
        self.main_font = pygame.font.SysFont("comicsans", 50)
        self.lost_font = pygame.font.SysFont("comicsans", 60)
        self.run = None
        self.FPS = None
        self.level = None
        self.lives = None
        self.y = None
        self.WIN = None
        
        
    def tela(self, run, F):
        # Variavel run determina se o jogo está rodando ou não;
        self.run = True
        # Quantidade de frames por segundo;
        self.FPS = 60
        # Nível inicial do jogador;
        self.level = 0
        # Número de vidas iniciais;
        self.lives = 5
        # Isso vai ser importante para criar o loop do fundo;
        self.y = 0
        
        # A variável WIN recebe o display do nosso jogo;
        self.WIN = pygame.display.set_mode((Fundo.WIDTH, Fundo.HEIGHT))
        
        # Determinando uma legenda para o jogo;
        pygame.display.set_caption("Space Shooter Tutorial")
        
    def redraw_window(self, main_font, lives, level, WIN, lives_label, level_label):
        #WIN.blit(BG, (0,0))
        
        # Escrever o texto
        '''
        Esses rótulos (label) armazenam os textos que exibirão as informações
        de número de vidas e o nível no qual o jogador se encontra.
        
        Respectivamente, temos o conteúdo, um valor inicial e a cor da fonte
        '''
        self.lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        self.level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        
        # Localização do texto
        WIN.blit(lives_label, (10, 10)) # 10p para a direita e 10p para baixo
        WIN.blit(level_label, (Fundo.WIDTH - level_label.get_width() - 10, 10)) 
        # A posição acima é em relação à posição anterior e ao tamanho da janela do jogo.
        
        for enemy in enemies:
            enemy.draw(WIN)
        
        player.draw(WIN)
        
        if lost:
            lost_label = lost_font.render("You Lost!", 1, (255, 255, 255))
            WIN.blit(lost_label, (Fundo.WIDTH / 2 - lost_label.get_width() / 2, 350))
        
        pygame.display.update()
   
