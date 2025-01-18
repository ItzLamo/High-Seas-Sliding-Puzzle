# High Seas Sliding Puzzle

High Seas Sliding Puzzle is a fun and challenging sliding puzzle game built with Python and Pygame. Players navigate through levels, solving puzzles by rearranging tiles to complete an image.

## Features
- **Challenging Gameplay:** Solve sliding puzzles of varying difficulty.
- **Custom Levels:** Progress through multiple levels with unique images.
- **Hints:** Use hints to assist in solving the puzzle.
- **Scoring System:** Track your moves and time to aim for high scores.
- **Custom Fonts and Graphics:** Enhanced visuals for an immersive experience.

## Controls
- **Arrow Keys:** Move tiles up, down, left, or right.
- **R Key:** Reset the current puzzle.
- **H Key:** Get a hint for the next move.
- **Spacebar:** Proceed to the next level (when the puzzle is solved).

## How to Run the Game
1. Install Python 3.x and Pygame:
   ```bash
   pip install pygame
   ```
2. Clone or download the project files.
3. Ensure the following resources are available:
   - Custom font file (`font.otf`).
   - Puzzle images in the specified folder (`images/`).
   - Optional: Background image for added aesthetics.
4. Run the main game file:
   ```bash
   python main.py
   ```

## Game Resources
- **Font:** Ensure the custom font file is correctly located or the game will default to system fonts.
- **Images:** Add your own images to the `images/` folder to customize the puzzles.

## Scoring System
- Each level awards points based on performance:
  - Initial score starts at 1000 points.
  - 10 points deducted per move.
  - Minimum score per level: 100 points.

## System Requirements
- Python 3.7 or higher.
- Pygame library.
- PIL (Pillow) library for image processing.

## Future Enhancements
- Add more levels and image categories.
- Include a timer-based challenge mode.
- Improve hint functionality for smarter assistance.

## Credits
Developed by Hassan Ahmed.
Special thanks to the Hack Club High Seas project for inspiration.
