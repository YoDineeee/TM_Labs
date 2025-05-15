"""
Game class - manages the main game loop and state transitions
"""

import pygame
import sys
import os
import math
from player import Player
from stage_controller import StageController
from ui import UI

class Game:
    def __init__(self, screen):
        """Initialize the game with the primary screen surface."""
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.fps = 60
        
        # Initialize game components
        self.player = Player()
        self.stage_controller = StageController(self)
        self.ui = UI(self)
        
        # Game state variables
        self.current_stage = 1  # Start with stage 1
        self.power_level = 0  # Player's power level (0-100)
        self.has_overkill = False  # Whether player has unlocked OverKill ability
        
        # Initialize resources
        self._load_resources()
        
    def _load_resources(self):
        """Load all necessary game resources."""
        # Set up resource paths
        self.asset_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
        self.image_dir = os.path.join(self.asset_dir, 'images')
        self.audio_dir = os.path.join(self.asset_dir, 'audio')
        self.font_dir = os.path.join(self.asset_dir, 'fonts')
        
        # Load basic font
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        
        # TODO: Load common images, sounds, etc.
        
    def run(self):
        """Run the main game loop."""
        while self.running:
            self._handle_events()
            
            if not self.paused:
                self._update()
            
            self._render()
            
            # Cap the frame rate
            self.clock.tick(self.fps)
    
    def _handle_events(self):
        """Process all input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Handle keyboard events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
            
            # Delegate event handling to current stage
            self.stage_controller.handle_event(event)
    
    def _update(self):
        """Update game state."""
        # Update player
        self.player.update()
        
        # Update current stage
        self.stage_controller.update()
        
        # Update UI
        self.ui.update()
    
    def _render(self):
        """Render the game."""
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        # Render current stage
        self.stage_controller.render(self.screen)
        
        # Render player view
        self.player.render(self.screen)
        
        # Render UI
        self.ui.render(self.screen)
        
        # Display pause screen if paused
        if self.paused:
            self._render_pause_screen()
        
        # Update display
        pygame.display.flip()
    
    def _render_pause_screen(self):
        """Render the pause screen overlay."""
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Display pause text
        pause_text = self.font.render("PAUSED", True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(pause_text, text_rect)
    
    def change_stage(self, stage_number):
        """Change to a different game stage."""
        if 1 <= stage_number <= 4:
            self.current_stage = stage_number
            self.stage_controller.load_stage(stage_number)
            print(f"Changed to Stage {stage_number}")
        else:
            print(f"Invalid stage number: {stage_number}")
    
    def increase_power(self, amount):
        """Increase player's power level."""
        self.power_level = min(100, self.power_level + amount)
        if self.power_level >= 100 and not self.has_overkill:
            self.unlock_overkill()
    
    def unlock_overkill(self):
        """Unlock the OverKill ability."""
        self.has_overkill = True
        print("OverKill ability unlocked!")
        # TODO: Add special effects, sound, etc.
