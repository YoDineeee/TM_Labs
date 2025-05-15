

import os
import sys
import pygame
from game import Game

def main():
    """Main entry point for the game."""
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Configure display
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("OverKill: Awakening")
    
    # Create game instance
    game = Game(screen)
    
    # Start game
    game.run()
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
