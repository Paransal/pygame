import pygame
from game.constants import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.state = "main"  # main, pause, game_over
        self.options = {
            "main": ["Start Game", "Quit"],
            "pause": ["Resume", "Quit to Menu"],
            "game_over": ["Play Again", "Quit"]
        }
        self.selected = 0
        self.high_score = 0

    def draw(self, score=0):
        self.screen.fill(BLACK)
        if self.state == "game_over":
            self.draw_game_over(score)
        else:
            self.draw_menu_options()
        pygame.display.flip()

    def draw_menu_options(self):
        options = self.options[self.state]
        for i, option in enumerate(options):
            color = GREEN if i == self.selected else WHITE
            text = self.font.render(option, True, color)
            x = SCREEN_WIDTH // 2 - text.get_width() // 2
            y = SCREEN_HEIGHT // 2 - len(options) * 30 + i * 60
            self.screen.blit(text, (x, y))

    def draw_game_over(self, score):
        # Draw "Game Over" text
        game_over_text = self.font.render("Game Over!", True, RED)
        score_text = self.font.render(f"Score: {score}", True, WHITE)
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, WHITE)

        self.screen.blit(game_over_text, 
                        (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                         SCREEN_HEIGHT // 4))
        self.screen.blit(score_text,
                        (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                         SCREEN_HEIGHT // 3))
        self.screen.blit(high_score_text,
                        (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2,
                         SCREEN_HEIGHT // 2.5))
        self.draw_menu_options()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options[self.state])
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options[self.state])
            elif event.key == pygame.K_RETURN:
                return self.get_selected_option()
        return None

    def get_selected_option(self):
        return self.options[self.state][self.selected]

    def update_high_score(self, score):
        if score > self.high_score:
            self.high_score = score
