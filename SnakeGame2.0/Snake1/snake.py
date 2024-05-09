class Snake:
    counter = 0

    def __init__(self, initial_length, initial_position):
        self.length = initial_length
        self.body = [initial_position]
        self.direction = 'RIGHT'

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == 'UP':
            new_head = (head_x, head_y - 1)
        elif self.direction == 'DOWN':
            new_head = (head_x, head_y + 1)
        elif self.direction == 'LEFT':
            new_head = (head_x - 1, head_y)
        elif self.direction == 'RIGHT':
            new_head = (head_x + 1, head_y)
        self.body.insert(0, new_head)
        self.body.pop()

    def change_direction(self, new_direction):
        if new_direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            if (self.direction == 'UP' and new_direction != 'DOWN') or \
               (self.direction == 'DOWN' and new_direction != 'UP') or \
               (self.direction == 'LEFT' and new_direction != 'RIGHT') or \
               (self.direction == 'RIGHT' and new_direction != 'LEFT'):
                self.direction = new_direction

    def grow(self):
        self.length += 1
        tail_x, tail_y = self.body[-1]
        if self.direction == 'UP':
            new_segment = (tail_x, tail_y + 1)
        elif self.direction == 'DOWN':
            new_segment = (tail_x, tail_y - 1)
        elif self.direction == 'LEFT':
            new_segment = (tail_x + 1, tail_y)
        elif self.direction == 'RIGHT':
            new_segment = (tail_x - 1, tail_y) 
        self.body.append(new_segment)

    def check_collision(self, board_width, board_height):
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= board_width or head_y < 0 or head_y >= board_height:
            return True
        if self.body[0] in self.body[1:]:
            return True
        return False