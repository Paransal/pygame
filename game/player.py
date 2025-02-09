import pygame
from game.constants import *
from game.sprites import load_sprite

class Player:
    def __init__(self):
        self.sprite = load_sprite("assets/player.svg", PLAYER_WIDTH, PLAYER_HEIGHT)
        self.rect = pygame.Rect(100, SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2,
                              PLAYER_WIDTH, PLAYER_HEIGHT)
        self.hp = PLAYER_START_HP
        self.last_heal_time = 0
        self.animation_frame = 0
        self.animation_timer = 0
        self.speed = 10  # Increased vertical speed
        self.horizontal_speed = 8  # Increased horizontal speed
        self.target_enemy = None
        self.direction = 1  # 1 for right, -1 for left

    def track_enemies(self, enemies):
        if not enemies:
            self.return_to_default_position()
            return

        # Find the most threatening enemy (closest or passed by)
        nearest_enemy = None
        min_threat_score = float('inf')

        for enemy in enemies:
            if enemy.alive:
                # Calculate threat score based on distance and position
                dx = enemy.rect.centerx - self.rect.centerx
                dy = enemy.rect.centery - self.rect.centery
                distance = (dx ** 2 + dy ** 2) ** 0.5

                # Higher threat score for enemies that have passed
                passed_penalty = 0 if dx > 0 else 300
                threat_score = distance + passed_penalty

                if threat_score < min_threat_score:
                    min_threat_score = threat_score
                    nearest_enemy = enemy
                    self.target_enemy = enemy

        if nearest_enemy:
            self.move_to_target(nearest_enemy)
        else:
            self.return_to_default_position()

    def move_to_target(self, enemy):
        # Vertical movement with small buffer
        buffer_y = 5
        if abs(self.rect.centery - enemy.rect.centery) > buffer_y:
            if self.rect.centery < enemy.rect.centery:
                self.rect.y = min(SCREEN_HEIGHT - self.rect.height, 
                                self.rect.y + self.speed)
            else:
                self.rect.y = max(0, self.rect.y - self.speed)

        # Horizontal movement with dynamic buffer
        dx = enemy.rect.centerx - self.rect.centerx
        if dx > 0:  # Enemy is to the right
            self.direction = 1
            self.rect.x = min(enemy.rect.x - 20, 
                            self.rect.x + self.horizontal_speed)
        else:  # Enemy is to the left
            self.direction = -1
            self.rect.x = max(50, self.rect.x - self.horizontal_speed)

        # Keep player within screen bounds
        self.rect.x = max(50, min(SCREEN_WIDTH - self.rect.width, self.rect.x))

    def return_to_default_position(self):
        # Default vertical position
        center_y = SCREEN_HEIGHT // 2 - self.rect.height // 2
        if abs(self.rect.y - center_y) > self.speed:
            if self.rect.y > center_y:
                self.rect.y -= self.speed
            else:
                self.rect.y += self.speed

        # Default horizontal position with smooth movement
        default_x = 100
        if abs(self.rect.x - default_x) > self.horizontal_speed:
            if self.rect.x > default_x:
                self.rect.x -= self.horizontal_speed
            else:
                self.rect.x += self.horizontal_speed

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)
        # Draw HP bar
        hp_text = pygame.font.Font(None, FONT_SIZE).render(f"HP: {self.hp}", True, WHITE)
        screen.blit(hp_text, (self.rect.x, self.rect.y - 30))

    def heal(self, current_time):
        if current_time - self.last_heal_time >= PLAYER_HEAL_INTERVAL:
            self.hp = min(self.hp + PLAYER_HEAL_AMOUNT, PLAYER_START_HP)
            self.last_heal_time = current_time
            return True
        return False

    def update_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= 5:
            self.animation_frame = (self.animation_frame + 1) % 4
            self.animation_timer = 0