import pygame
from random import *

BLOCK_DEMENSIONS = 10
RED = 255, 0, 0
BLUE = 0, 0, 255


class Snake:
    def __init__(self, color, screen):
        self.color = color
        x = int(screen.get_width()/2)
        x = x - x % BLOCK_DEMENSIONS
        y = int(screen.get_height()/2)
        y = y - y % BLOCK_DEMENSIONS
        self.head_position = [x, y]
        self.previous_tail_position = [x, y]
        self.head_block = [x, y, BLOCK_DEMENSIONS, BLOCK_DEMENSIONS]
        self.body_blocks = []
        self.trail_blocks = []
        for i in range(5):
            self.trail_blocks.append(
                [x+(i+1)*BLOCK_DEMENSIONS, y, BLOCK_DEMENSIONS, BLOCK_DEMENSIONS])
        self.screen = screen
        self.direction = None
        self.draw_delay = 0
        self.change_stop = False

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.head_block)
        for block in self.body_blocks:
            pygame.draw.rect(self.screen, self.color, block)
        for block in self.trail_blocks:
            pygame.draw.rect(self.screen, RED, block)

    def move(self):
        if(self.draw_delay > 2):
            if(self.direction):
                if(self.direction == 'left'):
                    self.head_position[0] -= BLOCK_DEMENSIONS
                elif(self.direction == 'right'):
                    self.head_position[0] += BLOCK_DEMENSIONS
                elif(self.direction == 'up'):
                    self.head_position[1] -= BLOCK_DEMENSIONS
                elif(self.direction == 'down'):
                    self.head_position[1] += BLOCK_DEMENSIONS
                self.update_blocks()
            self.draw_delay = 0
            self.change_stop = False
        else:
            self.draw_delay += 1

    def update_block_position(self, position, block):
        block[0] = position[0]
        block[1] = position[1]

    def update_blocks(self):
        # move head
        next_trail_position = [self.head_block[0], self.head_block[1]]
        next_position = [self.head_block[0], self.head_block[1]]
        self.update_block_position(self.head_position, self.head_block)

        # move body
        if(self.body_blocks):
            block = self.body_blocks[-1]
            next_trail_position = [block[0], block[1]]
        for block in self.body_blocks:
            previous_position = [block[0], block[1]]
            self.update_block_position(next_position, block)
            next_position = previous_position

        # move trail blocks
        for block in self.trail_blocks:
            previous_position = [block[0], block[1]]
            self.update_block_position(next_trail_position, block)
            next_trail_position = previous_position

    def change_direction(self, event):
        if event.type == pygame.KEYDOWN:
            key_input = pygame.key.get_pressed()
            if(not self.change_stop):
                if key_input[pygame.K_LEFT]:
                    if(self.direction != 'right'):
                        self.direction = 'left'
                        self.change_stop = True
                elif key_input[pygame.K_UP]:
                    if(self.direction != 'down'):
                        self.direction = 'up'
                        self.change_stop = True
                elif key_input[pygame.K_RIGHT]:
                    if(self.direction != 'left'):
                        self.direction = 'right'
                        self.change_stop = True
                elif key_input[pygame.K_DOWN]:
                    if(self.direction != 'up'):
                        self.direction = 'down'
                        self.change_stop = True

    def eat_food(self, food_blocks):
        if self.draw_delay > 0:
            remaining_food = food_blocks
        else:
            remaining_food = []
            for food in food_blocks:
                if food.position == self.head_block:
                    self.add_body_block()
                else:
                    remaining_food.append(food)
            while len(remaining_food) < 10:
                remaining_food.append(
                    Food(BLUE, self.screen, self, remaining_food))
        return remaining_food

    def add_body_block(self):
        self.body_blocks.append(self.trail_blocks[0].copy())
        for i in range(len(self.trail_blocks) - 1):
            self.trail_blocks[i] = self.trail_blocks[i+1].copy()
        self.trail_blocks[-1] = self.trail_blocks[-2].copy()


class Food:
    def __init__(self, color, screen, snake, other_food):
        self.color = color
        self.screen = screen
        self.random_placement(snake, other_food)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.position)

    def random_placement(self, snake, other_food):
        x = randint(0, self.screen.get_width()-BLOCK_DEMENSIONS)
        x = x - x % BLOCK_DEMENSIONS
        y = randint(0, self.screen.get_height()-BLOCK_DEMENSIONS)
        y = y - y % BLOCK_DEMENSIONS
        while self.position_in_snake_or_food(snake, other_food, [x, y]):
            x = randint(0, self.screen.get_width())
            x = x - x % BLOCK_DEMENSIONS
            y = randint(0, self.screen.get_height())
            y = y - y % BLOCK_DEMENSIONS

        self.position = [x, y, BLOCK_DEMENSIONS, BLOCK_DEMENSIONS]

    def position_in_snake_or_food(self, snake, other_food, position):
        head_position = [snake.head_block[0], snake.head_block[1]]
        if(position == head_position):
            return True
        for block in snake.body_blocks:
            block_position = [block[0], block[1]]
            if(position == block_position):
                return True
        for food in other_food:
            block_position = [food.position[0], food.position[1]]
            if(position == block_position):
                return True

        return False
