import pygame
import time
from game.constants import *
from game.player import Player
from game.enemy import EnemyManager
from game.audio import AudioManager
from game.menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Enhanced 2D RPG Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "menu"  # menu, playing, paused, game_over

        self.player = Player()
        self.enemy_manager = EnemyManager()
        self.audio_manager = AudioManager()
        self.menu = Menu(self.screen)
        self.score = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.game_state in ["menu", "paused", "game_over"]:
                option = self.menu.handle_input(event)
                if option:
                    self.handle_menu_option(option)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = "paused"
                    self.menu.state = "pause"

    def handle_menu_option(self, option):
        if option == "Start Game" or option == "Play Again":
            self.reset_game()
            self.game_state = "playing"
            self.audio_manager.play_music()
        elif option == "Resume":
            self.game_state = "playing"
        elif option == "Quit to Menu":
            self.game_state = "menu"
            self.menu.state = "main"
        elif option == "Quit":
            self.running = False

    def reset_game(self):
        self.player = Player()
        self.enemy_manager = EnemyManager()
        self.score = 0

    def update(self):
        if self.game_state != "playing":
            return

        current_time = time.time()

        # Update player
        self.player.track_enemies(self.enemy_manager.enemies)  # Autonomous movement
        if self.player.heal(current_time):
            self.audio_manager.play_sound('heal')
        self.player.update_animation()

        # Update enemies
        self.enemy_manager.update(current_time, self.player)

        # Check collisions with increased damage
        for enemy in self.enemy_manager.enemies:
            if enemy.alive and enemy.rect.colliderect(self.player.rect):
                enemy.hp -= 2.5  # Halved from 5 to 2.5
                self.audio_manager.play_sound('attack')
                if enemy.hp <= 0:
                    enemy.alive = False
                    enemy.death_time = current_time
                    self.score += 10

        # Remove dead enemies
        self.enemy_manager.remove_dead(current_time)

        # Check game over
        if self.player.hp <= 0:
            self.game_state = "game_over"
            self.menu.state = "game_over"
            self.menu.update_high_score(self.score)
            self.audio_manager.stop_music()

    def draw(self):
        self.screen.fill(BLACK)

        if self.game_state == "playing":
            self.player.draw(self.screen)
            self.enemy_manager.draw(self.screen)

            # Draw score
            score_text = pygame.font.Font(None, FONT_SIZE).render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))
        else:
            self.menu.draw(self.score)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()