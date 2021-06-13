# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 18:21:22 2021
Autor: Breno Marques Azevedo

Aqui encontram-se as funções referentes aos elementos jogo (sprites).

As variáveis com nome em caixa alta não serão alteradas ao longo do programa.
"""

import pygame
import os
from fundo import Fundo

"""

********************************************************
AQUI ENCONTRAM-SE AS VARIÁVEIS REFERENTES AOS EFEITOS SONOROS.
*********************************************************

"""

# Função que abilita os efeitos sonoros do pygame;
pygame.mixer.init()

# Efeitos Sonoros - Som do laser;
# Esse som será usado na nave do jogador;
laser_sound = pygame.mixer.Sound('laser_wrath.wav')

# Volume do som do laser do jogador;
laser_sound.set_volume(0.1)

# Efeitos Sonoros - Smaller explosion sound
# Esse som será usado quando o jogador sofrer algum dano e perder saúde;
smaller_explosion_sound = pygame.mixer.Sound('smaller_explosion.wav')

# Volume do som da explosão "menor" (smaller)
smaller_explosion_sound.set_volume(0.2) 


"""

********************************************************
AQUI ENCONTRAM-SE AS VARIÁVEIS REFERENTES AOS SPRITES DO JOGO
*********************************************************

"""
# Carregando as imagens
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png")).convert_alpha()
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png")).convert_alpha()
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png")).convert_alpha()

# Nave do Jogador
YELLOW_SPACE_player = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png")).convert_alpha()

# Lasers
RED_LASERS = pygame.image.load(os.path.join("assets", "pixel_laser_red.png")).convert_alpha()
GREEN_LASERS = pygame.image.load(os.path.join("assets", "pixel_laser_green.png")).convert_alpha()
BLUE_LASERS = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png")).convert_alpha()
YELLOW_LASERS = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png")).convert_alpha()

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
    
    """
    Nesse caso, optei por criar criar classes internas na classe elementos.
    Assim posso tratar cada sprite indiviualmente.
    """
    # Aqui temos a classe que executará as funções relativas ao lasers;
    # Posição, movimentação e colisão de lases serão tratadas nessa classe;
    class Laser:
        #from Enemy import collide
        # Definindo as posições dos lasers;
        def __init__(self, x, y, img):
            # Posição no eixo x;
            self.x = x
            # Posição no eixo y;
            self.y = y
            # Imagem do laser para ser utilizada em outras funções;
            self.img = img
            # Região de contato da colisão do laser;
            self.mask = pygame.mask.from_surface(self.img)
            
            # Função que "desenha" o laser na tela;
            def draw(self, window):
                window.blit(self.img, (self.x, self.y))

            # Movimentação do laser;
            def move(self, vel):
                self.y += vel
            
            # Quando o laser sair da tela do jogo;
            def off_screen(self, height):
                return not (self.y <= height and self.y >= 0)
            
            # Colisões do laser; Vai fazer sentido no futuro;
            def collision(self, obj, collide):
                return collide(self, obj)

    # Aqui temos a classe que executa as funções referentes às naves em geral,
    # ou seja, as do jogador e as naves inimigas.
    # Posição, movimentação, disparos e dimensões são tratadas aqui;
    class Ship():
        # Cooldown do disparo do laser;
        COOLDOWN = 30
        
        # Definindo posição e saúde das naves;
        def __init__(self, x, y, health = 100):
            # Posição no eixo x;
            self.x = x
            # Posição no eixo y;
            self.y = y
            # Saúde da nave;
            self.health = health
            # Sprite relativo à nave;    
            self.ship_img = None
            # Sprite de laser relativo à nave;    
            self.laser_img = None
            # Lista dos lasers
            self.lasers = []
            # Contador do cooldown
            self.cool_down_counter = 0
            
            # Função que "desenha" o laser na tela;
            def draw(self, window):
                window.blit(self.ship_img, (self.x, self.y))
                for laser in self.lasers:
                    laser.draw(window)        
            
            # Função que faz a movimentação dos lasers (velocidade dos objetos);
            # vel = velocidade
            # obj = objeto
            def move_lasers(self, vel, obj):
                self.cooldown()
                for laser in self.lasers:
                    laser.move(vel)
                    if laser.off_screen(Fundo.HEIGHT):
                        self.lasers.remove(laser)
                    elif laser.collision(obj):
                        obj.health -= 10
                        smaller_explosion_sound.play()
                        self.lasers.remove(laser)        
            
            # Função que determina o tempo de cooldown do disparo da nave;
            def cooldown(self):
                if self.cool_down_counter >= self.COOLDOWN:
                    self.cool_down_counter = 0
                elif self.cool_down_counter > 0:
                    self.cool_down_counter += 1  

            # Função que determina o disparo do laser;
            # Chamei a classe laser nessa função, não sei se vai funcionar;
            def shoot(self, Laser):
                if self.cool_down_counter == 0:
                    laser = Laser(self.x, self.y, self.laser_img)
                    laser_sound.play()
                    self.lasers.append(laser)
                    self.cool_down_counter = 1
            
            # Os comandos a seguir serão úteis para determinar a região de dano
            # das naves;
            # Função que pega a largura da nave;
            def get_width(self):
                return self.ship_img.get_width()
    
            # Função que pega a altura da nave;
            def get_height(self):
                return self.ship_img.get_height()       

    # Aqui temos a classe que irá lidar com as funções referentes à nave do jogador;
    class Player(Ship):
        # Definindo posição e saúde do jogador;
        def __init__(self, x, y, health = 100):
            super().__init__(x, y, health)
            self.ship_img = YELLOW_SPACE_player
            self.laser_img = YELLOW_LASERS
            self.mask = pygame.mask.from_surface(self.ship_img)
            self.max_health = health

        # Função da movimentação dos disparos (lasers) do jogador;
        # vel = velocidade
        # obj = objeto
        def move_lasers(self, vel, objs):
            self.cooldown()
            for laser in self.lasers:
                laser.move(vel)
                if laser.off_screen(Fundo.HEIGHT):
                    self.lasers.remove(laser)
                else:
                    for obj in objs:
                        if laser.collision(obj):
                            objs.remove(obj)
                            if self in self.lasers:
                                self.lasers.remove(laser)
        
        # Função que "desenha" a barra de saúde na tela;
        def draw(self, window):
            super().draw(window)
            self.healthbar(window)
        
        # Função que determina a barra de saúde;
        def healthbar(self, window):
            pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
            pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health), 10)) 

    # Classe das naves inimigas
    # Aqui temos a classe que executará as funções relativas aos inimigos;
    # Posição, movimentação, colisão e disparos de inimigos serão tratadas 
    # nessa classe;
    class Enemy(Ship): 
        COLOR_MAP = {
                    "red": (RED_SPACE_SHIP, RED_LASERS),
                    "green": (GREEN_SPACE_SHIP, GREEN_LASERS),
                    "blue": (BLUE_SPACE_SHIP, BLUE_LASERS)
                    }
        
        def __init__(self, x, y, color, health = 100):
            super().__init__(x, y, health)
            self.ship_img, self.laser_img = self.COLOR_MAP[color]
            self.mask = pygame.mask.from_surface(self.ship_img)
    
        def move(self, vel):
            self.y += vel
        
        def shoot(self, Laser):
            if self.cool_down_counter == 0:
                laser = Laser(self.x - 20, self.y, self.laser_img)
                self.lasers.append(laser)
                self.cool_down_counter = 1
            
    def collide(obj1, obj2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
