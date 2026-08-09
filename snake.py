import pygame
import random
import sys

# تنظیمات اولیه
pygame.init()
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
SPEED = 10

# رنگ‌ها
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 120, 255)

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.length = 3
        self.positions = [(WIDTH//2, HEIGHT//2)]
        self.direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        self.score = 0
        self.grow_to = 3
    
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
    
    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + (x * GRID_SIZE)) % WIDTH
        new_y = (head[1] + (y * GRID_SIZE)) % HEIGHT
        new_position = (new_x, new_y)
        
        if new_position in self.positions[1:]:
            self.reset()
            return False
        
        self.positions.insert(0, new_position)
        if len(self.positions) > self.grow_to:
            self.positions.pop()
        return True
    
    def draw(self, surface):
        for i, p in enumerate(self.positions):
            color = GREEN if i == 0 else BLUE
            rect = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, WHITE, rect, 1)
    
    def grow(self):
        self.grow_to += 1
        self.score += 10

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (
            random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
            random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        )
    
    def draw(self, surface):
        rect = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game - با پایتون")
    clock = pygame.time.Clock()
    
    snake = Snake()
    food = Food()
    font = pygame.font.SysFont('arial', 25)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.turn((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.turn((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.turn((1, 0))
        
        if not snake.move():
            # بازی ریست شده
            continue
        
        # بررسی برخورد با غذا
        if snake.get_head_position() == food.position:
            snake.grow()
            food.randomize_position()
            # اطمینان از اینکه غذا روی مار نباشد
            while food.position in snake.positions:
                food.randomize_position()
        
        # رسم
        screen.fill(BLACK)
        
        # رسم خطوط گرید
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))
        
        snake.draw(screen)
        food.draw(screen)
        
        # نمایش امتیاز
        score_text = font.render(f"امتیاز: {snake.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # نمایش راهنما
        help_text = font.render("از کلیدهای جهت‌دار استفاده کنید", True, WHITE)
        screen.blit(help_text, (WIDTH - help_text.get_width() - 10, 10))
        
        pygame.display.update()
        clock.tick(SPEED)

if __name__ == "__main__":
    main()