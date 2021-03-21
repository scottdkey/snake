import sys
import pygame
import time
import actors

BLACK = 0, 0, 0
RED = 255, 0, 0
BLUE = 0, 0, 255
WHITE = 255, 255, 255


def main():
    pygame.init()
    screen = setup_screen()
    game_state = init_game_state()
    game_loop(screen, game_state)


def init_game_state():
    game_state = {}
    game_state['game_over'] = False
    game_state['clock'] = pygame.time.Clock()
    return game_state


def setup_screen():
    size = 320, 240
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Snake')
    return screen


def handle_events(game_state, snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        else:
            snake.change_direction(event)


def paint_screen(screen, snake, food_blocks):
    screen.fill(BLACK)
    snake.draw()
    for food in food_blocks:
        food.draw()
    pygame.display.flip()


def check_game_over(screen, snake, game_state):
    if(snake.head_position[0] > screen.get_width() - actors.BLOCK_DEMENSIONS or
            snake.head_position[0] < 0):
        game_state['game_over'] = True
    elif(snake.head_position[1] > screen.get_height() - actors.BLOCK_DEMENSIONS or
            snake.head_position[1] < 0):
        game_state['game_over'] = True

    head_position = snake.head_position
    for block in snake.body_blocks:
        block_position = [block[0], block[1]]
        if(head_position == block_position):
            game_state['game_over'] = True


def game_loop(screen, game_state):
    food_blocks = []
    snake = actors.Snake(WHITE, screen)
    while not game_state['game_over']:
        handle_events(game_state, snake)
        snake.move()
        if snake.direction:
            food_blocks = snake.eat_food(food_blocks)
        check_game_over(screen, snake, game_state)
        paint_screen(screen, snake, food_blocks)
        game_state['clock'].tick(60)


if __name__ == '__main__':
    main()
