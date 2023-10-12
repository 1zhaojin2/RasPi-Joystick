import RPi_I2C_driver

from time import *

import random

import lirc

sockid = lirc.init("main")
mylcd = RPi_I2C_driver.lcd()

snake_head_right = [0x00, 0x1E, 0x1E, 0x00]
snake_body_horizontal = [0x00, 0x1F, 0x1F, 0x00]
snake_head_left = [0x00, 0x0F, 0x0F, 0x00]
snake_head_down = [0x0E, 0x0E, 0x0E, 0x00]
snake_head_up = [0x00, 0x0E, 0x0E, 0x0E]
snake_body_vertical = [0x0E, 0x0E, 0x0E, 0x0E]
snake_left_down = [0x00, 0x1E, 0x1E, 0x0E]
snake_left_up = [0x0E, 0x1E, 0x1E, 0x00]
snake_right_down = [0x00, 0x0F, 0x0F, 0x0E]
snake_right_up = [0x0E, 0x0F, 0x0F, 0x00]
food = [0x1F, 0x1F, 0x1F, 0x1F]
empty = [0x00, 0x00, 0x00, 0x00]

print("finished initializing variables")

grid = [[0 for _ in range(16)] for _ in range(4)]
snake = [(1, 3), (1, 4), (1, 5)]
direction = "RIGHT"
food_pos = (random.randint(0, 3), random.randint(0, 15))
grid[food_pos[0]][food_pos[1]] = 1

grace_counter = 0
grace_threshold = 3

loaded_chars = {}
available_slots = list(range(8))


def combine_half_characters(top, bottom):
    if isinstance(top, int):
        top = [top]
    if top == [0]:
        top = [0,0,0,0]
    if isinstance(bottom, int):
        bottom = [bottom]
    if bottom == [0]:
        bottom = [0,0,0,0]
    print("characters combined")
    return top + bottom


def load_custom_char(character):
    if isinstance(character, int):
        character = [character]
    # Convert the list to a tuple to use as a key

    character_tuple = tuple(character)

    if character_tuple in loaded_chars:
        return loaded_chars[character_tuple]

    if not available_slots:
        char_to_remove = list(loaded_chars.keys())[0]
        slot = loaded_chars[char_to_remove]
        del loaded_chars[char_to_remove]
    else:
        slot = available_slots.pop(0)

    mylcd.lcd_load_custom_chars([character])
    loaded_chars[character_tuple] = slot

    print("loaded custom character")

    return slot


def end_game():
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Game Over!", 1)
    mylcd.lcd_display_string("Score: " + str(len(snake)), 2)
    sleep(5)
    mylcd.lcd_clear()


def determine_snake_pixel(prev_segment, current_segment, next_segment):
    dx = current_segment[1] - prev_segment[1] if prev_segment else 0
    dy = current_segment[0] - prev_segment[0] if prev_segment else 0

    if not next_segment:  # This is the head of the snake
        if dx == 1:
            print("finished determining snake pixel, returning snake head right")
            return snake_head_right
        elif dx == -1:
            print("finished determining snake pixel, returning snake head left")
            return snake_head_left
        elif dy == 1:
            print("finished determining snake pixel, returning snake head down")
            return snake_head_down
        elif dy == -1:
            print("finished determining snake pixel, returning snake head up")
            return snake_head_up
    else:  # This is a body segment or the tail
        next_dx = next_segment[1] - current_segment[1]
        next_dy = next_segment[0] - current_segment[0]

        # Check for straight horizontal movement
        if (dx == 1 and next_dx == 1) or (dx == -1 and next_dx == -1):
            print("finished determining snake pixel, returning snake body horizontal")
            return snake_body_horizontal
        # Check for straight vertical movement
        elif (dy == 1 and next_dy == 1) or (dy == -1 and next_dy == -1):
            print("finished determining snake pixel, returning snake body vertical")
            return snake_body_vertical
        # Check for turns
        elif dx == 1 and next_dy == 1:
            print("finished determining snake pixel, returning snake right down")
            return snake_right_down
        elif dx == 1 and next_dy == -1:
            print("finished determining snake pixel, returning snake right up")
            return snake_right_up
        elif dx == -1 and next_dy == 1:
            print("finished determining snake pixel, returning snake left down")
            return snake_left_down
        elif dx == -1 and next_dy == -1:
            print("finished determining snake pixel, returning snake left up")
            return snake_left_up
        elif dy == 1 and next_dx == 1:
            print("finished determining snake pixel, returning snake left up")
            return snake_left_up
        elif dy == 1 and next_dx == -1:
            print("finished determining snake pixel, returning snake right up")
            return snake_right_up
        elif dy == -1 and next_dx == 1:
            print("finished determining snake pixel, returning snake left down")
            return snake_left_down
        elif dy == -1 and next_dx == -1:
            print("finished determining snake pixel, returning snake right down")
            return snake_right_down

    print("finished determining snake pixel, returning empty")
    return empty  # Default case, should represent an empty segment

print("attempting to start game loop")

while True:
    print("looping")
    print("trying to get button")
    button = lirc.nextcode()
    if button:
        if button == ["vol_up"] and direction not in ["UP", "DOWN"]:
            direction = "UP"
        elif button == ["vol_down"] and direction not in ["UP", "DOWN"]:
            direction = "DOWN"
        elif button == ["previous"] and direction not in ["LEFT", "RIGHT"]:
            direction = "LEFT"
        elif button == ["next"] and direction not in ["LEFT", "RIGHT"]:
            direction = "RIGHT"
    
    print("button gotten")

    if direction == "RIGHT":
        new_head = (snake[0][0], snake[0][1] + 1)
    elif direction == "LEFT":
        new_head = (snake[0][0], snake[0][1] - 1)
    elif direction == "UP":
        new_head = (snake[0][0] - 1, snake[0][1])
    elif direction == "DOWN":
        new_head = (snake[0][0] + 1, snake[0][1])

    print("new head determined")

    snake.insert(0, new_head)

    print("new head inserted")

    if new_head == food_pos:
        # Generate new food
        while True:
            food_pos = (random.randint(0, 3), random.randint(0, 15))
            if grid[food_pos[0]][food_pos[1]] == 0:  # Check if position is empty
                break
        grid[food_pos[0]][food_pos[1]] = 1  # Place new food on the grid
    else:
        snake.pop()  # Remove tail

    print("food generated")

    if not (0 <= new_head[0] <= 3 and 0 <= new_head[1] <= 15):
        print("added to grace counter")
        grace_counter += 1

    elif new_head in snake[1:]:
        print("added to grace counter")
        grace_counter += 1

    else:
        print("reset grace counter")
        grace_counter = 0


    if grace_counter >= grace_threshold:
        print("grace counter exceeded threshold, ending game")
        end_game()
        break

    print("grace counter did not exceed threshold, continuing game")



    for i in range(len(snake)):
        prev_segment = snake[i - 1] if i - 1 >= 0 else None
        current_segment = snake[i]
        next_segment = snake[i + 1] if i + 1 < len(snake) else None

        pixel = determine_snake_pixel(prev_segment, current_segment, next_segment)
        grid[current_segment[0]][current_segment[1]] = pixel

    print("clearing LCD")

    mylcd.lcd_clear()
 
    print("starting rendering")

    for row in range(2):
        for col in range(16):
            upper_pixel = grid[row * 2][col]
            lower_pixel = grid[row * 2 + 1][col]

            combined_pixel = combine_half_characters(upper_pixel, lower_pixel)

            slot = load_custom_char(combined_pixel)

            mylcd.lcd_display_string_pos(chr(slot), row + 1, col)

    print("finished rendering, waiting 0.5 seconds to restart loop...")
    sleep(0.5)
