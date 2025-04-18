import pygame
import random

class Grid:
    def __init__(self, width, height, cell_size):
        self.rows = height // cell_size
        self.columns = width // cell_size
        self.cell_size = cell_size
        self.cells = [[0 for _ in range(self.columns)] for _ in range(self.rows)]

    def draw(self, window, is_running=False):
        for row in range(self.rows):
            for column in range(self.columns):
                cell_value = self.cells[row][column]
                
                # Default color (empty space)
                color = (7, 7, 56)
                
                if cell_value == 1:
                    if is_running:
                        # Show dying/living colors only when simulation is running
                        alive_neighbors = self.count_neighbors(row, column, 1)
                        
                        if alive_neighbors < 2 or (not self.is_in_green_zone(row, column) and alive_neighbors > 3) or \
                        (self.is_in_green_zone(row, column) and alive_neighbors > 6):
                            color = (255, 60, 60)  # Dying cells (red)
                        else:
                            color = (60, 255, 60)  # Healthy cells (green)
                    else:
                        color = (255, 255, 255)  # White when not running
                elif cell_value == 2:
                    color = (160, 160, 160)  # Asteroid (gray)
                    
                pygame.draw.rect(
                    window, color,
                    (column * self.cell_size, row * self.cell_size,
                    self.cell_size - 1, self.cell_size - 1)
                )

    def fill_random(self):
        for row in range(self.rows):
            for column in range(self.columns):
                self.cells[row][column] = random.choice([1, 0, 0, 0])

    def clear(self):
        for row in range(self.rows):
            for column in range(self.columns):
                self.cells[row][column] = 0

    def toggle_cell(self, row, column):
        if 0 <= row < self.rows and 0 <= column < self.columns:
            self.cells[row][column] = 0 if self.cells[row][column] != 0 else 1

    def is_in_red_zone(self, row, column):
        return (
            row > 0 and row < self.rows // 4 and
            column >= self.columns * 3 // 4 and column < self.columns - 1
        )

    def is_in_green_zone(self, row, column):
        return (
            row > self.rows * 3 // 4 and row < self.rows - 1 and
            column > 0 and column < self.columns // 4
        )
    
    # Inside your Grid class
    def set_cell(self, row, col, value):
        if 0 <= row < self.rows and 0 <= col < self.columns:
            self.cells[row][col] = value  # Assuming self.cells is your 2D list

    def count_neighbors(self, row, column, kind=1):
        count = 0
        neighbor_offsets = [(-1, -1), (-1, 0), (-1, 1),
                        (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for offset in neighbor_offsets:
            new_row = (row + offset[0]) % self.rows
            new_col = (column + offset[1]) % self.columns
            if self.cells[new_row][new_col] == kind:
                count += 1
        return count

    def draw_zone_overlay(self, window):
        zone_surface = pygame.Surface((self.columns * self.cell_size, self.rows * self.cell_size), pygame.SRCALPHA)

        glow_fill = (0, 255, 255, 30)     # Soft neon interior
        glow_border = (0, 255, 255, 120)  # Strong neon edge

        # === RED ZONE (Top Right) ===
        red_x = self.columns * 3 // 4 * self.cell_size
        red_y = self.cell_size
        red_w = (self.columns // 4 - 1) * self.cell_size
        red_h = (self.rows // 4 - 1) * self.cell_size
        red_rect = pygame.Rect(red_x, red_y, red_w, red_h)

        pygame.draw.rect(zone_surface, glow_fill, red_rect)
        pygame.draw.rect(zone_surface, glow_border, red_rect, width=2)

        # === GREEN ZONE (Bottom Left) ===
        green_x = self.cell_size
        green_y = self.rows * 3 // 4 * self.cell_size
        green_w = (self.columns // 4 - 1) * self.cell_size
        green_h = (self.rows // 4 - 1) * self.cell_size
        green_rect = pygame.Rect(green_x, green_y, green_w, green_h)

        pygame.draw.rect(zone_surface, glow_fill, green_rect)
        pygame.draw.rect(zone_surface, glow_border, green_rect, width=2)

        window.blit(zone_surface, (0, 0))