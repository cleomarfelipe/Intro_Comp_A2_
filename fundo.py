import pygame
import os

WIDTH, HEIGHT = 750, 750 

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Tutorial")

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
