import pygame
import os
import random
from elementos import (
    Player,
    Enemy,
    collide,
    larger_explosion_sound,
    smaller_explosion_sound
    )

from fundo import (BG, BG_2, BG_3, BG_4, WIDTH, HEIGHT, WIN)

# Preparando as fontes que serão usadas
pygame.font.init()


# Tamanho da tela
#WIDTH, HEIGHT = 750, 750
#WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption("Space Shooter Tutorial")
'''
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
'''
# Imagem de fundo
# BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")).convert_alpha(), (WIDTH, HEIGHT))
# BG_2 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black-artic.png")).convert_alpha(), (WIDTH, HEIGHT))
# BG_3 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-stars.png")).convert_alpha(), (WIDTH, HEIGHT))
# BG_4 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "glitch-psychedelic.png")).convert_alpha(), (WIDTH, HEIGHT))
'''
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
'''


def main():   
    run = True                      # Determina que o jogo está rodando
    FPS = 60                        # Frames por segundo
    level = 0
    lives = 5
    y = 0 
        
    # Determinando a fonte e seu tamanho
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    
    # Aparição das naves inimigas
    enemies = []
    wave_length = 5
    enemy_vel = 1
    
    # Determinando a velocidade do jogador
    player_vel = 5
    
    # Determinando a velocidade do laser
    laser_vel = 5
    
    # Criando a nave do jogador
    player = Player(300, 600)
    
    clock = pygame.time.Clock()     
    
    lost = False
    lost_count = 0
    
    '''
    A função abaixo irá adicionar a imagem de ao pygame. Se não me engano ela 
    irá se atualizar constantemente.
    '''
    def redraw_window():
        '''
        Escrever o texto
        
        Esses rótulos (label) armazenam os textos que exibirão as informações
        de número de vidas e o nível no qual o jogador se encontra.
        
        Respectivamente, temos o conteúdo, um valor inicial e a cor da fonte
        '''
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        
        # Localização do texto
        WIN.blit(lives_label, (10, 10)) # 10p para a direita e 10p para baixo
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10)) 
        # A posição acima é em relação à posição anterior e ao tamanho da janela do jogo.
        
        for enemy in enemies:
            enemy.draw(WIN)
        
        player.draw(WIN)
        
        if lost:
            lost_label = lost_font.render("You Lost!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))
        
        pygame.display.update()
    
    y = 0
    while run:
        clock.tick(FPS)
        redraw_window()
        
        if level < 2:
            rel_y = y % BG.get_rect().height
            WIN.blit(BG, (0, rel_y - BG.get_rect().height))
            if rel_y < HEIGHT:
                WIN.blit(BG, (0, rel_y))
            y += 3
        if level >= 2:
            rel_y = y % BG.get_rect().height
            WIN.blit(BG_2, (0, rel_y - BG.get_rect().height))
            if rel_y < HEIGHT:
                WIN.blit(BG_2, (0, rel_y))
            y += 3
        if level >= 5:
            rel_y = y % BG.get_rect().height
            WIN.blit(BG_3, (0, rel_y - BG.get_rect().height))
            if rel_y < HEIGHT:
                WIN.blit(BG_3, (0, rel_y))
            y += 1
        if level >= 7:
            rel_y = y % BG.get_rect().height
            WIN.blit(BG_4, (0, rel_y - BG.get_rect().height))
            if rel_y < HEIGHT:
                WIN.blit(BG_4, (0, rel_y))
            y += 3
        
        if lives <= 0 or player.health <= 0:
            larger_explosion_sound.play()
            lost = True
            lost_count += 1
        
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)
            
        # Determinando o "fechamento" do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #quit()
                run = False
                #pygame.quit()
         
        keys = pygame.key.get_pressed()
        # Mover para a esquerda
        # ----------------------------------------------------
        # player.x - player_vel > 0 impede que o jogador saia para fora da tela
        # pelo lado esquerdo.
        if keys[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
        # Mover para a direita
        # --------------------------------------------------
        # player.x + player_vel + player.get_width() < WIDTH impede que o jogador
        # saia da tela pelo lado direito.
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        # Mover para a cima
        # ---------------------------------------------------
        # player.y - player_vel > 0 impede que o jogador saia para fora da tela
        # pelo por cima.
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
        # Mover para a baixo
        # ----------------------------------------------------
        # player.y + player_vel + player.get_height() + 15 impede que o jogador
        # saia para fora da tela pelo lado de baixo
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 50 < HEIGHT:
            player.y += player_vel
        # Atirar lasers 
        if keys[pygame.K_SPACE]:
            player.shoot()
            
        if keys[pygame.K_p]:
            main_menu()
            
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            
            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()
            if collide(enemy, player):
                player.health -= 10
                smaller_explosion_sound.play()
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
                
        player.move_lasers(-laser_vel, enemies)

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    y = 0 
    while run:
        rel_y = y % BG.get_rect().height
        WIN.blit(BG, (0, rel_y - BG.get_rect().height))
        if rel_y < HEIGHT:
            WIN.blit(BG, (0, rel_y))
        y += 1
        # WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()
    
main_menu()