import pygame
import time
import random
pygame.init()

fps = 60
size = 16
ww = size * 32
wh = size * 48

game = pygame.display.set_mode((ww, wh))
clock = pygame.time.Clock()

class Snake:
    def __init__(self, size) -> None:
        self.size = size
        self.body = [[0, 0]]
        self.direction = "right"

    def move(self):
        head = self.body[-1]
        if self.direction == "left":
            self.body.append([head[0] - self.size, head[1]])
        elif self.direction == "right":
            self.body.append([head[0] + self.size, head[1]])
        elif self.direction == "up":
            self.body.append([head[0], head[1] - self.size])
        elif self.direction == "down":
            self.body.append([head[0], head[1] + self.size])

        del self.body[0]
        self.tail = self.body[0]

    def add_block(self):
        self.body.insert(0, [self.tail[0], self.tail[1]])
        ...

    def get_head(self):
        head = self.body[-1]
        return head

    def check_collision(self):
        head = self.get_head()
        if head[0] + self.size > ww \
            or head[0] < 0 \
            or head[1] - self.size > wh \
            or head[1] < 0:return True 
        
        for block in self.body[:-1]:           
            if block[0] == head[0] and block[1] == head[1]:return True

    def eat(self, apple_x, apple_y):
        head = self.get_head()
        if head[0] == apple_x and head[1] == apple_y:
            return True

    def draw(self):
        for block in self.body:
            draw_rect(block[0], block[1], self.size, color=(255, 255, 0))

class Apple:
    def __init__(self, size) -> None:
        self.size = size

    def create_coords(self):
        self.x = round(random.randrange(0, ww - self.size) / self.size) * self.size
        self.y = round(random.randrange(0, wh - self.size) / self.size) * self.size
        return self.x, self.y

    def draw(self):
        draw_rect(self.x, self.y, self.size, color=(255, 0, 0))

def draw_rect(x, y, size, game=game, color=(255, 255, 0)):
    pygame.draw.rect(game, color, (x, y, size, size))

def game_over():
    global snake
    snake.body = [[0, 0]]
    snake.direction = "right"

def draw_score(x, y, fz, score, game=game):
    my_font = pygame.font.SysFont('Montserrat', fz)
    text_surface = my_font.render(f'Score: {score}', False, (255, 255, 255))
    game.blit(text_surface, (x,y))

snake = Snake(size)
apple = Apple(size)
def main():
    run = True
    spawned_apple = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
        game.fill((0, 0, 0))
        draw_score(0, 0, 32, score=len(snake.body))
        if not spawned_apple:
            apple_x, apple_y = apple.create_coords()
            spawned_apple=True
        apple.draw()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and snake.direction != "right":
            snake.direction = "left"
        if keys[pygame.K_RIGHT] and snake.direction != "left":
            snake.direction = "right"
        if keys[pygame.K_UP] and snake.direction != "down":
            snake.direction = "up"
        if keys[pygame.K_DOWN] and snake.direction != "up":
            snake.direction = "down"

        snake.move()
        if snake.check_collision(): game_over()
        if snake.eat(apple_x, apple_y): spawned_apple=False; snake.add_block();
        snake.draw()
        pygame.display.flip()
        clock.tick(10)
    pygame.quit()
if __name__ == "__main__":
    main()