"""
Este módulo contém as funções principais responsáveis pelo funcionamento do jogo.
"""

# Módulos importados
import pygame 
import random
# Classes e variáveis específicas que precisaram ser importadas;
from elementos import (
    Player,
    Enemy,
    collide,
    larger_explosion_sound,
    smaller_explosion_sound
    )
# Classes e variáveis específicas que precisaram ser importadas;
from fundo import (BG, BG_2, BG_3, BG_4, WIDTH, HEIGHT, WIN)

# Preparando as fontes que serão usadas
pygame.font.init()

def main():   
    run = True                      # Determina que o jogo está rodando;
    FPS = 60                        # Frames por segundo;
    level = 0                       # Determina o nível em que o jogador está;
    lives = 5                       # Número de vidas do jogador;
    y = 0                           # Variável que será usada para rolar a tela;
        
    # Determinando a fonte e seu tamanho
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    
    # Aparição das naves inimigas
    enemies = []
    wave_length = 5                 # Número de inimigos acrescentados a cada onda;
    enemy_vel = 1
    
    # Determinando a velocidade do jogador
    player_vel = 5
    
    # Determinando a velocidade do laser
    laser_vel = 5
    
    # Criando a nave do jogador
    player = Player(300, 600)
    
    # Temporizador
    clock = pygame.time.Clock()     
    
    # Variável que recebe a(s) derrota(s);
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
        WIN.blit(lives_label, (10, 10)) # 10p para a direita e 10p para baixo;
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10)) 
        # A posição acima é em relação à posição anterior e ao tamanho da janela
        # do jogo.
        
        # Repetição responsável por gerar os inimigos;
        for enemy in enemies:
            enemy.draw(WIN)
        
        # Função que "desenha" o jogador;
        player.draw(WIN)
        
        # Tela de derrota;
        if lost:
            lost_label = lost_font.render("You Lost!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))
        
        pygame.display.update()
    
    # Variável que será usada para rolar a tela;
    y = 0
    while run:
        # A cada frame a tela será redesenhada;
        clock.tick(FPS)
        redraw_window()
        
        # Rolamento do plano de fundo durante o jogo;
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
        
        # Derrota do jogador;
        if lives <= 0 or player.health <= 0:
            larger_explosion_sound.play()
            lost = True
            lost_count += 1
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
            
        # Determinando o aumento das ordas de inimigos;
        # A cada nível mais cinco inimigos são acrescentados à orda;
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)
            
        # Determinando o "fechamento" do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        #  MOVIMENTOS DO JOGADOR 
        
        keys = pygame.key.get_pressed()
        
        # --------------------------------------------------------------------
        # Mover para a esquerda
        # player.x - player_vel > 0 impede que o jogador saia para fora da tela
        # pelo lado esquerdo.
        if keys[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
        # --------------------------------------------------------------------
        
        # Mover para a direita
        # player.x + player_vel + player.get_width() < WIDTH impede que o jogador
        # saia da tela pelo lado direito.
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        # --------------------------------------------------------------------
        
        # Mover para a cima
        # player.y - player_vel > 0 impede que o jogador saia para fora da tela
        # pelo por cima.
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
        # --------------------------------------------------------------------
        
        # Mover para a baixo
        # player.y + player_vel + player.get_height() + 15 impede que o jogador
        # saia para fora da tela pelo lado de baixo
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 50 < HEIGHT:
            player.y += player_vel
        # --------------------------------------------------------------------
        
        # Atirar lasers 
        if keys[pygame.K_SPACE]:
            player.shoot()
        # Botão de pause - Não funciona
        if keys[pygame.K_p]:
            paused()
            if keys[pygame.K_p]:
                not paused()
        
        # Repetição que determina o movimento dos lasers, bem como sua aparição;
        for enemy in enemies[:]:
            enemy.move(enemy_vel) 
            enemy.move_lasers(laser_vel, player)
            
            # Chance aleatória de um inimigo atirar;
            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()
            # Impedir que os inimigos saiam da tela do jogo;
            if enemy.x > WIDTH - 2 * enemy.ship_img.get_width():
                enemy.x -= enemy.ship_img.get_width()
            if enemy.x < 2 * enemy.ship_img.get_width():
                enemy.x += enemy.ship_img.get_width()
            # Colisão dos inimigos com o jogador;
            if collide(enemy, player):
                player.health -= 10
                smaller_explosion_sound.play()
                enemies.remove(enemy)
            # Redução de vidas do jogador;
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
        
        # Movimento do laser do jogador;
        # Como o eixo y do Python cresce para baixo, a velocidade do laser do 
        # jogador deve ser negativa. Senão, os lasers seriam disparados para 
        # baixo e não para cima, como se espera.
        player.move_lasers(-laser_vel, enemies)   

# Função que gera o menu principal;
# Nele é possível fechar o jogo;
def main_menu():
    # Funte do título
    title_font = pygame.font.SysFont("comicsans", 70)
    # Determina que o jogo está rodando
    run = True
    # Variável usada no rolamento da imagem fundo no eixo y;
    y = 0 
    while run:
        # Rolamento da imagem de fundo no eixo y;
        rel_y = y % BG.get_rect().height
        WIN.blit(BG, (0, rel_y - BG.get_rect().height))
        if rel_y < HEIGHT:
            WIN.blit(BG, (0, rel_y))
        y += 1
        
        # Título do jogo
        title_label = title_font.render("Press the mouse to begin...", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))
        
        # Update da janela do jogo;
        pygame.display.update()
        
        # Inicialização ou saída do jogo
        for event in pygame.event.get():
            # Para sair;
            if event.type == pygame.QUIT:
                run = False
            # Para iniciar o jogo;
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

# Função que pausa o jogo;
def paused():
    # Variável que determina que o jogo está pausado;
    pause = True
    
    # Mensagem que é exibida na tela;
    pause_font = pygame.font.SysFont("comicsans", 50)
    pause_label = pause_font.render("Paused, press any keybord key to resume", 1, (255, 255, 255))
    WIN.blit(pause_label, (WIDTH / 2 - pause_label.get_width() / 2, 350))
    
    # Atualiza a tela do pygame;
    pygame.display.flip()
    
    # Enquanto o jogo está pausado...
    while pause: 
        # Pressione qualquer tecla para fechar o pause;
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pygame.display.update()
                pause = False

# Chamando a função que inicia o jogo;
main_menu()