'''
Neste módulo, estão presentes as classes e funções referentes aos elementos do
jogo, como os sprites das naves, disparos e os efeitos sonoros do jogo.

A função convert_alpha() foi uma recomendação do professor a fim de otimizar o
funcionamento do jogo.
'''

# Módulos importados
import pygame
import os
import random
from fundo import HEIGHT

# Carregando as imagens - NAVES INIMIGAS;
RED_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_red_small.png")).convert_alpha()

GREEN_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_green_small.png")).convert_alpha()

BLUE_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_blue_small.png")).convert_alpha()

# Nave do Jogador
YELLOW_SPACE_player = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png")).convert_alpha()

# Lasers
# Cada laser tem uma cor referente a um tipo específico de nave;
# Vermelho com vermelho, verde com verde...
RED_LASERS = pygame.image.load(
    os.path.join("assets", "pixel_laser_red.png")).convert_alpha()

GREEN_LASERS = pygame.image.load(
    os.path.join("assets", "pixel_laser_green.png")).convert_alpha()

BLUE_LASERS = pygame.image.load(
    os.path.join("assets", "pixel_laser_blue.png")).convert_alpha()

YELLOW_LASERS = pygame.image.load(
    os.path.join("assets", "pixel_laser_yellow.png")).convert_alpha()

# ----------------------------------------------------------------------------
# Função que habilita o uso de efeitos sonoros no pygame;
pygame.mixer.init()

# Efeitos Sonoros - Música de fundo
music = pygame.mixer.music.load('futurama_theme.mp3')   # Música de Fundo
# Loop da Música de Fundo
pygame.mixer.music.play(-1)
# Volume da Música de Fundo
pygame.mixer_music.set_volume(0.2)

# Efeitos Sonoros - Laser sound
laser_sound = pygame.mixer.Sound('laser_wrath.wav')
# Determinando o volume do efeito sonoro
laser_sound.set_volume(0.1)             

# Efeitos Sonoros - Larger explosion sound
larger_explosion_sound = pygame.mixer.Sound('larger_explosion.wav')
# Determinando o volume do efeito sonoro
larger_explosion_sound.set_volume(0.2)  

# Efeitos Sonoros - Smaller explosion sound
smaller_explosion_sound = pygame.mixer.Sound('smaller_explosion.wav')
# Determinando o volume do efeito sonoro
smaller_explosion_sound.set_volume(0.2) 

# ----------------------------------------------------------------------------
'''
Aqui encontram-se as classes e funções referentes aos sprites e seus respectivos
sons no jogo.

Há uma classe específica para os lasers, que determina funções como aparição, 
movimento e colisão.

Há uma classe específica para as naves, que tem funções que determinam a aparição,
colisão e movimentação das naves no geral.

Há classes para as naves inimigas e para a do jogador. Estas usam alguns elementos
presentes na classe geral das naves
'''

# Classe do laser
class Laser:
    # Variáveis que determinam a posição relativa aos eixos x e y;
    # Outra variável que recebe o respectivo sprite do laser;
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        # Aqui determinamos a superfície de contato do sprite. Será útil para
        # determinar a colisão dentro do jogo;
        self.mask = pygame.mask.from_surface(self.img)
        
    # Função que "desenha" o laser no jogo;
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    # Função que determina a movimentação;
    # Note que o laser só se move em relação ao eixo y;
    def move(self, vel):
        self.y += vel
    
    # Função que impede que o laser seja gerado fora da tela do jogo;
    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)
    
    # Colisão de ojbetos com o laser;    
    def collision(self, obj):
        return collide(self, obj)

# Classe geral das naves
class Ship:
    # Cooldown dos disparos
    COOLDOWN = 30
    
    # Variáveis que determinam a posição relativa aos eixos x e y;
    # Outra variável que recebe a saúde da nave;
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        # "Criando" o espaço em que serão armazenados sprites da nave e do laser;
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    # Função que "desenha" o laser da nave na mesma posição que ela;
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
    
    # Função que determina o movimento dos lasers;
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            # Removendo lasers que saem da tela;
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            # Colisão das naves com o laser;
            elif laser.collision(obj):
                obj.health -= 10
                smaller_explosion_sound.play()
                self.lasers.remove(laser)
    
    # Função que determina o cooldown dos disparos 
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1  

    # Função que gera o disparo do laser;
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            laser_sound.play()
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
    # As funções a seguir serão importantes para determinar a colição das naves;
    # Função que consegue a largura do sprite da nave;
    def get_width(self):
        return self.ship_img.get_width()
    
    # Função que consegue a altura do sprite da nave;
    def get_height(self):
        return self.ship_img.get_height()

# Classe do Jogador e sua nave
class Player(Ship):
    # Variáveis que determinam a posição relativa aos eixos x e y;
    # Outra variável que recebe a saúde da nave;
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        # A nave do jogador será a Nave amarela;
        self.ship_img = YELLOW_SPACE_player
        self.laser_img = YELLOW_LASERS
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    # Função que determina o movimento dos lasers disparados pelo jogador;
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if self in self.lasers:
                            self.lasers.remove(laser)
    
    # Aqui estão as funções referentes à barra de saúde do jogador;
    # Função que "desenha" a barra de saúde;
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
    
    # Função que determina a barra de saúde;
    # Aqui temos uma barra vermelha do tamanho da nave do jogador que está 
    # sobreposta por uma barra verde que diminui conforme o jogador leva dano.
    def healthbar(self, window):
        # Barra vermelha;
        pygame.draw.rect(window, 
                         (255, 0, 0), 
                         (self.x, self.y + self.ship_img.get_height() + 10, 
                          self.ship_img.get_width(), 10))
        # Barra verde;
        pygame.draw.rect(window, (0, 255, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10,
                          self.ship_img.get_width() * (self.health / self.max_health), 10)) 
        
# Classe das naves inimigas
class Enemy(Ship):
    # Aqui temos um dicionário que contém todos os sprites referentes às naves
    # inimigas;
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASERS),
                "green": (GREEN_SPACE_SHIP, GREEN_LASERS),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASERS)
                }
    
    def __init__(self, x, y, color, health = 100):
        # Variáveis que determinam a posição relativa aos eixos x e y;
        # Outras variaveis que recebem a cor e a saúde da nave;
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    # Função que determina o movimento das naves inimigas;
    def move(self, vel):
        # Os inimigos se movem para baixo de forma constante e para os lados 
        # de forma aleatória;
        self.y += vel
        self.x += random.randrange(-1, 1)
    
    # Função que determina o disparo dos lasers inimigos;
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

# Função que determina a colisão de dois objetos;
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
