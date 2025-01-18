import pygame
import random
from PIL import Image
import time
import os
from pathlib import Path

# Initialize Pygame
pygame.init()

# Fixed screen dimensions (non-resizable)
WIDTH = 900
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("High Seas Sliding Puzzle")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
GOLD = (255, 215, 0)

# Load custom font
try:
    custom_font = pygame.font.Font(r"D:\Hack Club\Project 29\font.otf", 36)
    medium_font = pygame.font.Font(r"D:\Hack Club\Project 29\font.otf", 28)
    small_font = pygame.font.Font(r"D:\Hack Club\Project 29\font.otf", 24)
except:
    print("Custom font not found. Using default font.")
    custom_font = pygame.font.Font(None, 36)
    medium_font = pygame.font.Font(None, 28)
    small_font = pygame.font.Font(None, 24)

# Grid settings
GRID_SIZE = 3
PUZZLE_SIZE = 600  # Fixed puzzle size
TILE_SIZE = PUZZLE_SIZE // GRID_SIZE

# Load background
try:
    background_image = pygame.image.load(r"D:\Hack Club\Project 29\IMG_9361.JPEG")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except:
    background_image = None
    print("Background image not found")

# Define puzzle image paths
PUZZLE_IMAGES = [
    r"D:\Hack Club\Project 29\images\treasure7.png",
    r"D:\Hack Club\Project 29\images\treasure8.png",
    r"D:\Hack Club\Project 29\images\treasure9.png",
    r"D:\Hack Club\Project 29\images\treasure13.png",
    r"D:\Hack Club\Project 29\images\treasure14.png",
    r"D:\Hack Club\Project 29\images\treasure16.png",
    r"D:\Hack Club\Project 29\images\treasure18.png",
    r"D:\Hack Club\Project 29\images\treasure19.png"
]

class SlidingPuzzle:
    def __init__(self):
        self.move_count = 0
        self.start_time = time.time()
        self.game_solved = False
        self.current_level = 1
        self.total_score = 0
        self.load_random_image()
        self.reset_puzzle()

    def get_image_paths(self):
        return PUZZLE_IMAGES

    def load_random_image(self):
        try:
            image_paths = self.get_image_paths()
            if image_paths:
                image_path = random.choice(image_paths)
                print(f"Loading image: {image_path}")  # Debug print
                image = Image.open(image_path)
                image = image.resize((PUZZLE_SIZE, PUZZLE_SIZE))
                
                self.tiles = []
                for row in range(GRID_SIZE):
                    for col in range(GRID_SIZE):
                        left = col * TILE_SIZE
                        upper = row * TILE_SIZE
                        right = left + TILE_SIZE
                        lower = upper + TILE_SIZE
                        tile = image.crop((left, upper, right, lower))
                        pygame_tile = pygame.image.fromstring(
                            tile.tobytes(), tile.size, tile.mode)
                        self.tiles.append(pygame_tile)
                return True
            else:
                raise Exception("No image files found")
        except Exception as e:
            print(f"Error loading image: {e}")
            self.create_default_tiles()
            return False

    def create_default_tiles(self):
        self.tiles = []
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
                color = ((row * 85) % 255, (col * 85) % 255, ((row + col) * 85) % 255)
                surface.fill(color)
                self.tiles.append(surface)

    def reset_puzzle(self):
        self.move_count = 0
        self.start_time = time.time()
        self.game_solved = False
        
        tile_list = self.tiles[:-1] + [None]
        while True:
            random.shuffle(tile_list)
            self.grid = [tile_list[i:i + GRID_SIZE] 
                        for i in range(0, len(tile_list), GRID_SIZE)]
            if self.is_solvable() and not self.is_solved():
                break

    def next_level(self):
        self.current_level += 1
        self.total_score += max(1000 - self.move_count * 10, 100)
        self.load_random_image()
        self.reset_puzzle()

    def is_solvable(self):
        flat_grid = []
        for row in self.grid:
            flat_grid.extend(row)
        
        inversions = 0
        for i in range(len(flat_grid)):
            if flat_grid[i] is None:
                continue
            for j in range(i + 1, len(flat_grid)):
                if flat_grid[j] is None:
                    continue
                if flat_grid[i] != flat_grid[j]:
                    inversions += 1
        
        empty_row = 0
        for i in range(GRID_SIZE - 1, -1, -1):
            if None in self.grid[i]:
                empty_row = GRID_SIZE - i
                break
        
        if GRID_SIZE % 2 == 1:
            return inversions % 2 == 0
        else:
            return (inversions + empty_row) % 2 == 0

    def find_empty(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col] is None:
                    return row, col
        return None

    def is_solved(self):
        flat_current = []
        for row in self.grid:
            flat_current.extend(row)
        
        solved_tiles = self.tiles[:-1] + [None]
        return flat_current == solved_tiles

    def move_tile(self, direction):
        if self.game_solved:
            return False

        empty_row, empty_col = self.find_empty()
        new_row, new_col = empty_row, empty_col

        if direction == 'up' and empty_row < GRID_SIZE - 1:
            new_row = empty_row + 1
        elif direction == 'down' and empty_row > 0:
            new_row = empty_row - 1
        elif direction == 'left' and empty_col < GRID_SIZE - 1:
            new_col = empty_col + 1
        elif direction == 'right' and empty_col > 0:
            new_col = empty_col - 1
        else:
            return False

        self.grid[empty_row][empty_col] = self.grid[new_row][new_col]
        self.grid[new_row][new_col] = None
        self.move_count += 1
        
        if self.is_solved():
            self.game_solved = True
        
        return True

    def draw(self, screen):
        # Draw background
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill((30, 30, 50))

        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(100)
        screen.blit(overlay, (0, 0))

        # Game title with shadow
        title = "Sliding Puzzle Challenge"
        shadow_text = custom_font.render(title, True, BLACK)
        title_text = custom_font.render(title, True, GOLD)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 30))
        screen.blit(shadow_text, (title_rect.x + 2, title_rect.y + 2))
        screen.blit(title_text, title_rect)

        # Level and score
        level_text = medium_font.render(f"Level: {self.current_level}", True, WHITE)
        score_text = medium_font.render(f"Score: {self.total_score}", True, WHITE)
        screen.blit(level_text, (20, 20))
        screen.blit(score_text, (WIDTH - 200, 20))

        # Center the puzzle
        start_x = (WIDTH - PUZZLE_SIZE) // 2
        start_y = 100

        # Puzzle border
        pygame.draw.rect(screen, GOLD, 
                        (start_x - 5, start_y - 5, 
                         PUZZLE_SIZE + 10, PUZZLE_SIZE + 10), 3)

        # Draw tiles
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = start_x + (col * TILE_SIZE)
                y = start_y + (row * TILE_SIZE)
                tile = self.grid[row][col]
                
                if tile:
                    screen.blit(tile, (x, y))
                    pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE), 1)
                else:
                    pygame.draw.rect(screen, (40, 40, 60), 
                                   (x, y, TILE_SIZE, TILE_SIZE))

        # Stats
        stats_y = start_y + PUZZLE_SIZE + 20
        move_text = medium_font.render(f"Moves: {self.move_count}", True, WHITE)
        elapsed_time = int(time.time() - self.start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        time_text = medium_font.render(f"Time: {minutes:02d}:{seconds:02d}", 
                                     True, WHITE)
        screen.blit(move_text, (start_x, stats_y))
        screen.blit(time_text, (start_x + PUZZLE_SIZE - 150, stats_y))

        # Instructions
        instructions = small_font.render(
            "Arrow keys to move • R to reset • H for hint • Space for next level", 
            True, WHITE)
        instructions_rect = instructions.get_rect(
            center=(WIDTH // 2, HEIGHT - 40))
        screen.blit(instructions, instructions_rect)

        # Solved message
        if self.game_solved:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(150)
            screen.blit(overlay, (0, 0))
            
            solved_text = custom_font.render("Level Complete!", True, GOLD)
            text_rect = solved_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(solved_text, text_rect)
            
            press_space_text = medium_font.render(
                "Press SPACE for next level", True, WHITE)
            space_rect = press_space_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 50))
            screen.blit(press_space_text, space_rect)

    def get_hint(self):
        empty_row, empty_col = self.find_empty()
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col] == self.tiles[row * GRID_SIZE + col]:
                    continue
                if row == empty_row and abs(col - empty_col) == 1:
                    direction = 'left' if col > empty_col else 'right'
                    self.move_tile(direction)
                    return True
                if col == empty_col and abs(row - empty_row) == 1:
                    direction = 'up' if row > empty_row else 'down'
                    self.move_tile(direction)
                    return True
        return False

def main():
    game = SlidingPuzzle()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset_puzzle()
                elif event.key == pygame.K_SPACE and game.game_solved:
                    game.next_level()
                elif event.key == pygame.K_UP:
                    game.move_tile('up')
                elif event.key == pygame.K_DOWN:
                    game.move_tile('down')
                elif event.key == pygame.K_LEFT:
                    game.move_tile('left')
                elif event.key == pygame.K_RIGHT:
                    game.move_tile('right')
                elif event.key == pygame.K_h:
                    game.get_hint()

        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()