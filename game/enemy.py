import pygame
import random
from game.constants import *
from game.sprites import load_sprite

class Enemy:
    def __init__(self):
        self.sprite = load_sprite("assets/enemy.svg", ENEMY_WIDTH, ENEMY_HEIGHT)
        self.rect = pygame.Rect(SCREEN_WIDTH, 
                              random.randint(50, SCREEN_HEIGHT - 150),
                              ENEMY_WIDTH, ENEMY_HEIGHT)
        self.hp = random.randint(30, 50)  
        self.damage = random.randint(1, 3)
        self.attack_timer = 0
        self.alive = True
        self.death_time = 0
        self.animation_frame = 0

    def draw(self, screen):
        if self.alive:
            screen.blit(self.sprite, self.rect)
            hp_text = pygame.font.Font(None, FONT_SIZE).render(f"HP: {self.hp}", True, WHITE)
            screen.blit(hp_text, (self.rect.x, self.rect.y - 30))

    def move(self):
        if self.alive:
            self.rect.x -= ENEMY_SPEED

    def update_animation(self):
        if self.alive:
            self.animation_frame = (self.animation_frame + 1) % 4

class EnemyManager:
    def __init__(self):
        self.enemies = []
        self.spawn_timer = 0

    def spawn_enemy(self, current_time):
        if len(self.enemies) < MAX_ENEMIES and current_time - self.spawn_timer >= ENEMY_SPAWN_INTERVAL:
            self.enemies.append(Enemy())
            self.spawn_timer = current_time

    def update(self, current_time, player):
        self.spawn_enemy(current_time)
        for enemy in self.enemies:
            enemy.move()
            enemy.update_animation()
            if enemy.alive and current_time - enemy.attack_timer >= ENEMY_ATTACK_INTERVAL:
                if enemy.rect.colliderect(player.rect):
                    player.hp -= enemy.damage
                    enemy.attack_timer = current_time

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)

    def remove_dead(self, current_time):
        self.enemies = [enemy for enemy in self.enemies 
                       if enemy.alive or current_time - enemy.death_time < 3]