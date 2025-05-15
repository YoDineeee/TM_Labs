
import pygame
import math
import numpy as np

class Player:
    def __init__(self):
        """Initialize the player."""
        # Position and orientation
        self.x = 5.0
        self.y = 5.0
        self.angle = 0.0  # Angle in radians
        self.height = 0.5  # Player height (for rendering)
        
        # Movement attributes
        self.move_speed = 0.05
        self.rotation_speed = 0.03
        self.moving_forward = False
        self.moving_backward = False
        self.turning_left = False
        self.turning_right = False
        self.strafing_left = False
        self.strafing_right = False
        
        # Combat attributes
        self.health = 100
        self.max_health = 100
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_power = 10
        
        # Field of view and raycasting parameters
        self.fov = math.pi / 3  # 60 degrees
        self.half_fov = self.fov / 2
        self.num_rays = 320  # Number of rays to cast
        self.max_depth = 20  # Maximum ray distance
        
        # Initialize raycasting result buffers
        self.ray_angles = np.linspace(self.angle - self.half_fov, 
                                      self.angle + self.half_fov,
                                      self.num_rays)
        self.wall_heights = np.zeros(self.num_rays)
        self.wall_colors = np.zeros((self.num_rays, 3))
        
    def update(self):
        """Update player state each frame."""
        # Handle player rotation
        if self.turning_left:
            self.angle -= self.rotation_speed
        if self.turning_right:
            self.angle += self.rotation_speed
        
        # Normalize angle to [0, 2π)
        self.angle = self.angle % (2 * math.pi)
        
        # Handle player movement
        move_x = 0
        move_y = 0
        
        if self.moving_forward:
            move_x += math.cos(self.angle) * self.move_speed
            move_y += math.sin(self.angle) * self.move_speed
        if self.moving_backward:
            move_x -= math.cos(self.angle) * self.move_speed
            move_y -= math.sin(self.angle) * self.move_speed
        if self.strafing_left:
            move_x += math.cos(self.angle - math.pi/2) * self.move_speed
            move_y += math.sin(self.angle - math.pi/2) * self.move_speed
        if self.strafing_right:
            move_x += math.cos(self.angle + math.pi/2) * self.move_speed
            move_y += math.sin(self.angle + math.pi/2) * self.move_speed
        
        # Apply movement (collision will be checked in a real implementation)
        # Here we would check for collisions with walls, etc.
        self.x += move_x
        self.y += move_y
        
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # Update raycasting angles based on new player angle
        self.ray_angles = np.linspace(self.angle - self.half_fov, 
                                     self.angle + self.half_fov,
                                     self.num_rays)
    
    def handle_input(self, event):
        """Handle input events specific to the player."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.moving_forward = True
            elif event.key == pygame.K_s:
                self.moving_backward = True
            elif event.key == pygame.K_a:
                self.strafing_left = True
            elif event.key == pygame.K_d:
                self.strafing_right = True
            elif event.key == pygame.K_LEFT:
                self.turning_left = True
            elif event.key == pygame.K_RIGHT:
                self.turning_right = True
            elif event.key == pygame.K_SPACE:
                self.attack()
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.moving_forward = False
            elif event.key == pygame.K_s:
                self.moving_backward = False
            elif event.key == pygame.K_a:
                self.strafing_left = False
            elif event.key == pygame.K_d:
                self.strafing_right = False
            elif event.key == pygame.K_LEFT:
                self.turning_left = False
            elif event.key == pygame.K_RIGHT:
                self.turning_right = False
        
        # Handle mouse for looking around
        elif event.type == pygame.MOUSEMOTION:
            # Mouse sensitivity can be adjusted
            mouse_sensitivity = 0.002
            dx, dy = event.rel
            self.angle += dx * mouse_sensitivity
    
    def attack(self):
        """Perform a melee attack."""
        if self.attack_cooldown <= 0:
            self.is_attacking = True
            self.attack_cooldown = 30  # 0.5 seconds at 60 FPS
            print("Player attacked!")
            # Actual attack logic will be implemented in combat system
            return True
        return False
    
    def take_damage(self, amount):
        """Take damage from enemies or environment."""
        self.health = max(0, self.health - amount)
        if self.health <= 0:
            self.die()
        return self.health
    
    def heal(self, amount):
        """Heal the player."""
        self.health = min(self.max_health, self.health + amount)
        return self.health
    
    def die(self):
        """Handle player death."""
        print("Player died!")
        # Will implement death logic later
    
    def cast_rays(self, world_map):
        """Cast rays from player position to detect walls."""
        # Sample implementation - in a real game, this would interact with the level
        # For now, just setting some placeholder values
        for i, angle in enumerate(self.ray_angles):
            # Calculate ray direction
            ray_x = math.cos(angle)
            ray_y = math.sin(angle)
            
            # Simple distance calculation (in a real game, this would be DDA or similar)
            # This is just a placeholder for demonstration
            distance = np.random.uniform(0.5, self.max_depth)
            
            # Calculate wall height based on distance (perspective correction)
            distance_corrected = distance * math.cos(angle - self.angle)  # Fish-eye correction
            wall_height = min(2.0 / distance_corrected, 2.0)  # Capped at 2.0
            
            self.wall_heights[i] = wall_height
            
            # Determine wall color based on direction or texture (simplified)
            # In a real game, this would involve texture mapping
            self.wall_colors[i] = [
                max(0, min(255, 255 / distance)),
                max(0, min(255, 200 / distance)),
                max(0, min(255, 150 / distance))
            ]
    
    def render(self, screen):
        """Render the player's view using raycasting."""
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # For demonstration, we'll draw vertical strips based on ray distances
        # In a real game, this would involve proper texture mapping
        
        # Fill the screen with a gradient for sky and floor
        pygame.draw.rect(screen, (25, 25, 50), (0, 0, screen_width, screen_height // 2))  # Sky
        pygame.draw.rect(screen, (50, 50, 50), (0, screen_height // 2, screen_width, screen_height // 2))  # Floor
        
        # Cast rays to determine wall heights
        # In a real implementation, this would take the actual world map
        self.cast_rays(None)
        
        # Render walls
        strip_width = screen_width // self.num_rays
        for i in range(self.num_rays):
            # Calculate wall height on screen
            wall_height_pixels = int(self.wall_heights[i] * screen_height)
            
            # Calculate wall position
            wall_top = (screen_height - wall_height_pixels) // 2
            wall_bottom = wall_top + wall_height_pixels
            
            # Draw the wall strip
            color = self.wall_colors[i]
            pygame.draw.rect(
                screen, 
                color, 
                (i * strip_width, wall_top, strip_width + 1, wall_height_pixels)
            )
        
        # Render crosshair
        crosshair_size = 10
        crosshair_color = (255, 255, 255)
        center_x, center_y = screen_width // 2, screen_height // 2
        pygame.draw.line(screen, crosshair_color, 
                        (center_x - crosshair_size, center_y), 
                        (center_x + crosshair_size, center_y), 2)
        pygame.draw.line(screen, crosshair_color, 
                        (center_x, center_y - crosshair_size), 
                        (center_x, center_y + crosshair_size), 2)
        
        # Render attack animation if attacking
        if self.is_attacking:
            # Simple punch animation
            punch_color = (200, 100, 100)
            pygame.draw.rect(screen, punch_color, 
                            (center_x - 50, screen_height - 150, 100, 100))
            
            # Reset attack flag after animation
            if self.attack_cooldown < 25:  # 5 frames of animation
                self.is_attacking = False
