def main():
    import pygame
    import random
    import time

    # Initialize the game
    pygame.init()

    # Set up grid, cell, and window sizes
    grid = 10
    cell = 60
    window = grid * cell

    background = (0, 0, 0)  # black
    charater_one = (0, 255, 0)  # Green
    charater_two = (255, 0, 0)  # Red
    statistics = (255, 255, 255)  # white

    # Set up display
    game_screen = pygame.display.set_mode((window, window))
    pygame.display.set_caption("Wandering in the Woods")

    # Load sound and image
    pygame.mixer.music.load("C:\\Users\\13313\\Downloads\\game.mp3")
    collision_image = pygame.image.load("C:\\Users\\13313\\Downloads\\happy_graphics.jpg")

    # Character positions must start in opposite corners of each other
    charater_one_position = [0, 0]
    charater_two_position = [grid - 1, grid - 1]

    # counter the characters movement
    charater_one_moves = 0
    charater_two_moves = 0

    # method to set up grid and charaters
    def grid_creation():
        game_screen.fill(background)
        for row in range(grid):
            for column in range(grid):
                square = pygame.Rect(column * cell, row * cell, cell, cell)
                pygame.draw.rect(game_screen, (255, 255, 255), square, 1)


        # Draw the characters
        pygame.draw.circle(game_screen, charater_one,
                           (charater_one_position[1] * cell + cell // 2, charater_one_position[0] * cell + cell // 2), cell // 3)
        pygame.draw.circle(game_screen, charater_two,
                           (charater_two_position[1] * cell + cell // 2, charater_two_position[0] * cell + cell // 2), cell // 3)

        pygame.display.flip()

    # method for random character movement
    def person_movement(position):
        direction = random.choice(['left', 'right', 'down', 'up'])
        if direction == 'up' and position[0] > 0:
            position[0] -= 1
        elif direction == 'down' and position[0] < grid - 1:
            position[0] += 1
        elif direction == 'left' and position[1] > 0:
            position[1] -= 1
        elif direction == 'right' and position[1] < grid - 1:
            position[1] += 1

    # checks to see if a collision occurred
    def collision_occurred():
        return charater_one_position == charater_two_position

    # game loop
    game_running = True
    pygame.mixer.music.play(-1)  # starts the music

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        # Move the characters
        person_movement(charater_one_position)
        person_movement(charater_two_position)
        charater_one_moves += 1
        charater_two_moves += 1

        # Draw everything
        grid_creation()

        # method for checking collisions
        if collision_occurred():
            pygame.mixer.music.stop()
            game_screen.blit(pygame.transform.scale(collision_image, (window, window)), (0, 0))
            collision_text = pygame.font.Font(None, 50)
            text = collision_text.render("COLLISION OCCURRED!!!", True, (255, 0, 0))
            text_rect = text.get_rect(center=(window // 2, window // 2))
            game_screen.blit(text, text_rect)


            pygame.display.flip()

            time.sleep(2)  # Display the happy image for 2 seconds

            # Display the character move counts only after a collision has occurred
            game_screen.fill(background)
            font = pygame.font.Font(None, 36)
            text = font.render(f"Total Character One Moves: {charater_one_moves}", True, statistics)
            game_screen.blit(text, (10, 10))
            text = font.render(f"Total Character Two Moves: {charater_two_moves}", True, statistics)
            game_screen.blit(text, (10, 50))
            pygame.display.flip()

            var = str(input('Do you want to play again? Enter Yes or No: ')).strip().lower()
            if var == "yes":
                # Reset positions and counters after asking the user if they want to play again
                charater_one_position = [0, 0]
                charater_two_position = [grid - 1, grid - 1]
                charater_one_moves = 0
                charater_two_moves = 0
                pygame.mixer.music.play(-1)  # Restart the music
            elif var == "no":
                game_running = False  # Exit the game loop

        pygame.time.delay(100)  # Slow down the movement

    # Quit the game
    pygame.quit()


if __name__ == "__main__":
    main()
