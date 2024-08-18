import pygame
import random
import time

def main():
    # Ask the user for their desired grid size
    grid_size = int(input("Enter the grid size (enter 5 for a 5x5 grid or 3 for a 3x3 grid, etc.): "))

    # Ask the user for the desired number of players
    total_players = int(input("Enter the number of players (2-4): "))
    if total_players < 2 or total_players > 4:
        print("Please enter a valid number of players (2-4).")
        return

    # Set up cell and window sizes
    cell = 60
    window = grid_size * cell

    background = (0, 0, 0)  # black
    character_colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)]  # Green, Red, Blue, Yellow
    statistics = (255, 255, 255)  # white

    # Initialize the game
    pygame.init()

    # Set up display
    game_screen = pygame.display.set_mode((window, window))
    pygame.display.set_caption("Wandering in the Woods")

    # Load sound and image
    pygame.mixer.music.load("C:\\Users\\13313\\Downloads\\game.mp3")
    collision_image = pygame.image.load("C:\\Users\\13313\\Downloads\\happy_graphics.jpg")

    # Ask the user for the initial positions of the characters
    def character_position(character_name):
        while True:
            try:
                row = int(input(f"Enter the starting row position for {character_name} (0 to {grid_size-1}): "))
                column = int(input(f"Enter the starting column position for {character_name} (0 to {grid_size-1}): "))
                if 0 <= row < grid_size and 0 <= column < grid_size:
                    return [row, column]
                else:
                    print("Invalid input. Please enter values within the grid size.")
            except ValueError:
                print("Invalid input. Please enter numeric values.")

    # Initialize positions, move counters, and groups for each character
    character_positions = []
    character_moves = [0] * total_players
    groups = [[i] for i in range(total_players)]  # Each player starts in their own group

    for i in range(total_players):
        position = character_position(f"Character {i+1} ({['Green', 'Red', 'Blue', 'Yellow'][i]})")
        character_positions.append(position)

    # Method to set up grid and characters
    def grid_creation():
        game_screen.fill(background)
        for row in range(grid_size):
            for column in range(grid_size):
                square = pygame.Rect(column * cell, row * cell, cell, cell)
                pygame.draw.rect(game_screen, (255, 255, 255), square, 1)

        # Draw the characters
        for group in groups:
            for i in group:
                pygame.draw.circle(game_screen, character_colors[i],
                                   (character_positions[i][1] * cell + cell // 2,
                                    character_positions[i][0] * cell + cell // 2), cell // 3)

        pygame.display.flip()

    # Method for random group movement
    def character_movement(group):
        character_direction = random.choice(['left', 'right', 'down', 'up'])
        character_position = character_positions[group[0]]

        if character_direction == 'up' and character_position[0] > 0:
            character_position[0] -= 1
        elif character_direction == 'down' and character_position[0] < grid_size - 1:
            character_position[0] += 1
        elif character_direction == 'left' and character_position[1] > 0:
            character_position[1] -= 1
        elif character_direction == 'right' and character_position[1] < grid_size - 1:
            character_position[1] += 1

        # Move all members of the group to the new position
        for character in group:
            character_positions[character] = character_position.copy()

    # Checks to see if any collision occurred
    def collision_occurred():
        collision_positions = set(map(tuple, character_positions))
        return len(collision_positions) < len(character_positions)

    # Checks and handles grouping upon collision
    def group_collision():
        position_to_groups = {}
        for index, pos in enumerate(character_positions):
            pos_array = tuple(pos)
            if pos_array in position_to_groups:
                # Merge groups if another character is at the same position
                group_one = position_to_groups[pos_array]
                group_two = groups[index]
                if group_one != group_two:
                    new_group = list(set(group_one + group_two))
                    for i in new_group:
                        groups[i] = new_group
            else:
                position_to_groups[pos_array] = groups[index]

    # Game loop
    game_running = True
    pygame.mixer.music.play(-1)  # starts the music

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        # Move the characters
        for group in groups:
            character_movement(group)
            for i in group:
                character_moves[i] += 1

        # Check for collisions and handle grouping
        if collision_occurred():
            group_collision()

        # Draw everything
        grid_creation()

        # Handles player collisions
        if len(groups[0]) == total_players:  # All players have collided
            pygame.mixer.music.stop()
            game_screen.blit(pygame.transform.scale(collision_image, (window, window)), (0, 0))
            collision_text = pygame.font.Font(None, 50)
            text = collision_text.render("ALL COLLISIONS HAVE OCCURRED!!!", True, (255, 0, 0))
            text_rect = text.get_rect(center=(window // 2, window // 2))
            game_screen.blit(text, text_rect)

            pygame.display.flip()

            time.sleep(2)  # Display the happy image for 2 seconds

            # Display the character move counts only after all have collided
            game_screen.fill(background)
            font = pygame.font.Font(None, 36)
            shortest_moves = min(character_moves)
            for i in range(total_players):
                text = font.render(f"Total Character {i+1} Moves: {character_moves[i]}", True, statistics)
                game_screen.blit(text, (10, 10 + 40 * i))
                if character_moves[i] == shortest_moves:
                    shortest_text = font.render(f"Character {i+1} had the shortest run with {shortest_moves} moves!", True, (255, 255, 0))
                    game_screen.blit(shortest_text, (10, 10 + 40 * total_players))

            pygame.display.flip()

            var = input('Do you want to play again? Enter Yes or No: ').strip().lower()
            if var == "yes":
                # Reset positions, counters, and groups after asking the user if they want to play again
                character_positions.clear()
                character_moves = [0] * total_players
                groups = [[i] for i in range(total_players)]  # Reset groups
                for i in range(total_players):
                    each_char_position = character_position(f"Character {i+1} ({['Green', 'Red', 'Blue', 'Yellow'][i]})")
                    character_positions.append(each_char_position)
                pygame.mixer.music.play(-1)  # Restart the music
            elif var == "no":
                game_running = False  # Exit the game loop

        pygame.time.delay(100)  # Slow down the movement

    # Quit the game
    pygame.quit()

if __name__ == "__main__":
    main_35()
