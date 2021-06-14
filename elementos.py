import pygame
import os
from fundo import HEIGHT

pygame.display.set_mode()
pygame.mixer.init()

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

# Efeitos Sonoros - Música de fundo
music = pygame.mixer.music.load('futurama_theme.mp3')   # Música de Fundo
# Loop da Música de Fundo
pygame.mixer.music.play(-1)
# Volume da Música de Fundo
pygame.mixer_music.set_volume(0.3)

# Efeitos Sonoros - Laser sound
laser_sound = pygame.mixer.Sound('laser_wrath.wav')
laser_sound.set_volume(0.1)             # Determinando o volume do efeito sonoro

# Efeitos Sonoros - Larger explosion sound
larger_explosion_sound = pygame.mixer.Sound('larger_explosion.wav')
larger_explosion_sound.set_volume(0.2)  # Determinando o volume do efeito sonoro

# Efeitos Sonoros - Smaller explosion sound
smaller_explosion_sound = pygame.mixer.Sound('smaller_explosion.wav')
smaller_explosion_sound.set_volume(0.2) # Determinando o volume do efeito sonoro

# Efeitos Sonoros - Enemy laser sound
enemy_laser_sound = pygame.mixer.Sound('enemy_laser.wav')
enemy_laser_sound.set_volume(0.1)       # Determinando o volume do efeito sonoro


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel
            
    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)
        
    def collision(self, obj):
        return collide(self, obj)

class Ship:
    COOLDOWN = 30
    
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
    
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                smaller_explosion_sound.play()
                self.lasers.remove(laser)
        
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1  

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            laser_sound.play()
            self.lasers.append(laser)
            self.cool_down_counter = 1
            
    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()

# Classe do Jogador e sua nave
class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_player
        self.laser_img = YELLOW_LASERS
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

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
    
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
    
    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health), 10)) 
        
# Classe das naves inimigas
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
    
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
        
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
