import pygame


class Snake:
    def __init__(self, color, screen):
        self.color = color
        x = int(screen.get_width()/2)
        x = x - x % 10
        y = int(screen.get_height()/2)
        y = y - y % 10
        self.head_position = [x, y]
        self.previous_tail_position = [x, y]
        self.head_block = [x, y, 10, 10]
        self.body_blocks = []
        self.screen = screen
        self.direction = None
        self.draw_delay = 0

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.head_block)

    def move(self):
        if(self.draw_delay > 2):
            if(self.direction):
                if(self.direction == 'left'):
                    self.head_position[0] -= 10
                elif(self.direction == 'right'):
                    self.head_position[0] += 10
                elif(self.direction == 'up'):
                    self.head_position[1] -= 10
                elif(self.direction == 'down'):
                    self.head_position[1] += 10
                self.update_blocks()
            print(self.direction)
            self.draw_delay = 0
        else:
            self.draw_delay += 1

    def update_block_position(self, position, block):
        block[0] = position[0]
        block[1] = position[1]

    def update_blocks(self):
        next_block_position = [self.head_block[0], self.head_block[1]]
        self.update_block_position(self.head_position, self.head_block)
        for block in self.body_blocks:
            previous_block_position = [block[0], block[1]]
            self.update_block_position(next_block_position, block)
            next_block_position = previous_block_position

    def change_direction(self, event):
        if event.type == pygame.KEYDOWN:
            key_input = pygame.key.get_pressed()
            if key_input[pygame.K_LEFT]:
                if(self.direction != 'right'):
                    self.direction = 'left'
            elif key_input[pygame.K_UP]:
                if(self.direction != 'down'):
                    self.direction = 'up'
            elif key_input[pygame.K_RIGHT]:
                if(self.direction != 'left'):
                    self.direction = 'right'
            elif key_input[pygame.K_DOWN]:
                if(self.direction != 'up'):
                    self.direction = 'down'
