import pygame
import sys
import time
from collections import deque
from abc import ABC, abstractmethod

pygame.init()

WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BUTTON_COLOR = (200, 200, 200)
BUTTON_TEXT_COLOR = BLACK

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Runner Arcade")
clock = pygame.time.Clock()

title_font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

class GameEntity(ABC):
    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self):
        pass

class Character(GameEntity):
    def __init__(self, x, y, speed):
        self._x = x
        self._y = y
        self._speed = speed

    def draw(self):
        pass

    def move(self):
        pass

    def update(self):
        pass

class Maze(GameEntity):
    def __init__(self):
        self._layout = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
        self._star_positions = [
            (9 * TILE_SIZE, 7 * TILE_SIZE), 
            (5 * TILE_SIZE, 3 * TILE_SIZE), 
            (15 * TILE_SIZE, 5 * TILE_SIZE) 
        ]
        self._stars_collected = [False, False, False] 
        self.wall_image = pygame.transform.scale(pygame.image.load('wall.jpg'), (TILE_SIZE, TILE_SIZE)) 
        self.star_image = pygame.transform.scale(pygame.image.load('star.png'), (TILE_SIZE, TILE_SIZE)) 

    def draw(self):
        for row_idx, row in enumerate(self._layout):
            for col_idx, tile in enumerate(row):
                if tile == 1:
                    screen.blit(self.wall_image, (col_idx * TILE_SIZE, row_idx * TILE_SIZE)) 

        pygame.draw.rect(screen, GREEN, (19 * TILE_SIZE, 7 * TILE_SIZE, TILE_SIZE, TILE_SIZE))  

        for index, position in enumerate(self._star_positions):
            if not self._stars_collected[index]:
                screen.blit(self.star_image, position)

    def collect_star(self, player_position):
        for index, position in enumerate(self._star_positions):
            if not self._stars_collected[index] and player_position == position:
                self._stars_collected[index] = True 

    def update(self):
        pass 

class Player(Character):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed)
        self.player_images = []
        
        for i in range(1, 5):
            self.player_images.append(pygame.transform.scale(pygame.image.load(f'imgp/{i}.png'), (TILE_SIZE, TILE_SIZE)))

        self.current_image = self.player_images[0]  
        self.direction = 'right'  
        self.frame_index = 0 
        self.animation_speed = 0.1  
        self.last_update_time = time.time()

    def draw(self):
        screen.blit(self.current_image, (self._x, self._y)) 

    def update_animation(self):
        current_time = time.time()
        if current_time - self.last_update_time >= self.animation_speed:
            self.frame_index = (self.frame_index + 1) % len(self.player_images) 
            self.current_image = self.player_images[self.frame_index] 
            self.last_update_time = current_time 

    def move(self, keys, maze):
        new_x, new_y = self._x, self._y
        moving = False  

        if keys[pygame.K_UP]:
            new_y -= self._speed
        if keys[pygame.K_DOWN]:
            new_y += self._speed
        if keys[pygame.K_LEFT]:
            new_x -= self._speed
            self.current_image = pygame.transform.flip(self.player_images[self.frame_index], True, False) 
            moving = True 
        if keys[pygame.K_RIGHT]:
            new_x += self._speed
            self.current_image = self.player_images[self.frame_index] 
            moving = True  

        if moving:
            self.update_animation()

        if new_x < 0:
            new_x = 0

        if new_x + TILE_SIZE > WIDTH:
            new_x = WIDTH - TILE_SIZE

        top_left = (new_x // TILE_SIZE, new_y // TILE_SIZE)
        top_right = ((new_x + TILE_SIZE - 1) // TILE_SIZE, new_y // TILE_SIZE)
        bottom_left = (new_x // TILE_SIZE, (new_y + TILE_SIZE - 1) // TILE_SIZE)
        bottom_right = ((new_x + TILE_SIZE - 1) // TILE_SIZE, (new_y + TILE_SIZE - 1) // TILE_SIZE)

        if all(0 <= pos[0] < len(maze._layout[0]) and 0 <= pos[1] < len(maze._layout) for pos in [top_left, top_right, bottom_left, bottom_right]):
            if all(
                maze._layout[pos[1]][pos[0]] == 0
                for pos in [top_left, top_right, bottom_left, bottom_right]
            ):
                self._x, self._y = new_x, new_y

        for index, position in enumerate(maze._star_positions):
            if not maze._stars_collected[index] and (self._x, self._y) == position:
                maze.collect_star((self._x, self._y))

        if new_x + TILE_SIZE >= WIDTH:
            if all(maze._stars_collected):
                print("Selamat! Anda telah mencapai garis finish!")

                game.finish_menu()
            else:
                print("Anda harus mengumpulkan bintangnya terlebih dahulu!")

class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = button_font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class Guard(Character):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed)
        self.guard_images = []
        
        for i in range(1, 5):
            self.guard_images.append(pygame.transform.scale(pygame.image.load(f'imgg/{i}.png'), (TILE_SIZE, TILE_SIZE)))

        self.current_image = self.guard_images[0] 
        self.direction = 'right'  
        self.frame_index = 0  
        self.animation_speed = 0.1  
        self.last_update_time = time.time() 
        self.slow_speed = speed  

    def bfs(self, layout, start, goal):
        if not (isinstance(start, tuple) and isinstance(goal, tuple)):
            raise ValueError("Start and goal must be tuples.")
        
        start = (int(start[0]), int(start[1]))
        goal = (int(goal[0]), int(goal[1]))

        queue = deque([start])
        visited = set()
        visited.add(start)
        parent = {start: None}

        while queue:
            current = queue.popleft()
            if current == goal:
                break

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  
                neighbor = (current[0] + dx, current[1] + dy)
                if (0 <= neighbor[0] < len(layout[0]) and
                    0 <= neighbor[1] < len(layout) and
                    layout[neighbor[1]][neighbor[0]] == 0 and
                    neighbor not in visited):
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        path = []
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse() 
        return path

    def draw(self):
        screen.blit(self.current_image, (self._x, self._y)) 

    def update_animation(self):
        current_time = time.time()
        if current_time - self.last_update_time >= self.animation_speed:
            self.frame_index = (self.frame_index + 1) % len(self.guard_images) 
            self.current_image = self.guard_images[self.frame_index] 
            self.last_update_time = current_time  

    def move(self, player, maze):
        player_x, player_y = player._x, player._y  
        guard_x, guard_y = self._x, self._y  
       
        possible_moves = []
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] 
        for dx, dy in directions:
            new_x = guard_x + dx
            new_y = guard_y + dy
            
            if (0 <= new_x // TILE_SIZE < len(maze._layout[0]) and
                0 <= new_y // TILE_SIZE < len(maze._layout) and
                maze._layout[new_y // TILE_SIZE][new_x // TILE_SIZE] == 0): 
                possible_moves.append((new_x, new_y))
        
        if possible_moves:
            self.update_animation()
            if (guard_x // TILE_SIZE, guard_y // TILE_SIZE) in possible_moves:
                self._x, self._y = player_x, player_y
            else:
                path = self.bfs(maze._layout, (guard_x // TILE_SIZE, guard_y // TILE_SIZE), (player_x // TILE_SIZE, player_y // TILE_SIZE))
                if len(path) > 1: 
                    next_move = path[1] 
                    if self._x < next_move[0] * TILE_SIZE:
                        self._x += self.slow_speed
                    elif self._x > next_move[0] * TILE_SIZE:
                        self._x -= self.slow_speed
                    if self._y < next_move[1] * TILE_SIZE:
                        self._y += self.slow_speed
                    elif self._y > next_move[1] * TILE_SIZE:
                        self._y -= self.slow_speed
            
            if (abs(self._x - player_x) < TILE_SIZE / 2 and abs(self._y - player_y) < TILE_SIZE / 2) or \
            (abs(self._x - player_x) < TILE_SIZE and abs(self._y - player_y) < TILE_SIZE):
                print("Player caught by the guard!")
      
                game.lose_menu()

            if player_x < guard_x: 
                self.current_image = pygame.transform.flip(self.guard_images[self.frame_index], True, False)  
                self.direction = 'left'
            else:
                self.current_image = self.guard_images[self.frame_index] 
                self.direction = 'right'

    def update(self):
        self.move(self.player, self.maze) 
        self.update_animation() 

class Game:
    def __init__(self):
        self.maze = Maze()
        self.player = Player(0 * TILE_SIZE, 7 * TILE_SIZE, 5) 
        self.guards = [] 

    def main_menu(self):
        start_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 50, "Start Game", BUTTON_COLOR, BUTTON_TEXT_COLOR)
        quit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 50, "Quit Game", BUTTON_COLOR, BUTTON_TEXT_COLOR)

        running = True
        while running:
            screen.fill(BLACK)

            title_text = title_font.render("MAZE RUNNER ARCADE", True, YELLOW)
            title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            screen.blit(title_text, title_rect)

            start_button.draw()
            quit_button.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    sys.exit()     
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.is_clicked(event.pos):
                        self.difficulty_menu()
                    elif quit_button.is_clicked(event.pos):
                        pygame.quit()  
                        sys.exit()    

            pygame.display.flip()
            clock.tick(60)

    def finish_menu(self):
        back_button_text = "Back to Main Menu"
        back_button_surface = button_font.render(back_button_text, True, BUTTON_TEXT_COLOR)
        back_button_width = back_button_surface.get_width() + 20  
        back_button_height = back_button_surface.get_height() + 10  
        back_button = Button(WIDTH // 2 - back_button_width // 2, HEIGHT // 2 - back_button_height // 2, back_button_width, back_button_height, back_button_text, BUTTON_COLOR, BUTTON_TEXT_COLOR)

        quit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 50, "Quit Game", BUTTON_COLOR, BUTTON_TEXT_COLOR)

        running = True
        while running:
            screen.fill(BLACK)

            finish_text = title_font.render("Congratulations!", True, YELLOW)
            finish_rect = finish_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            screen.blit(finish_text, finish_rect)

            back_button.draw()
            quit_button.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    sys.exit()     
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_clicked(event.pos):
                        self.__init__()  
                        self.main_menu()  
                    elif quit_button.is_clicked(event.pos):
                        pygame.quit()  
                        sys.exit()    

            pygame.display.flip()
            clock.tick(60)

    def start_game(self, difficulty):
        print(f" Starting game on {difficulty} difficulty...")
        self.player = Player(0 * TILE_SIZE, 7 * TILE_SIZE, 5)  
        self.guards = []  
        self.initialize_guards(difficulty) 
        self.play_game()
    
    def initialize_guards(self, difficulty):
        if difficulty == "easy":
            self.guards.append(Guard(1 * TILE_SIZE, 1 * TILE_SIZE, 2))
        elif difficulty == "medium":
            self.guards.append(Guard(1 * TILE_SIZE, 1 * TILE_SIZE, 2))  
            self.guards.append(Guard(18 * TILE_SIZE, 1 * TILE_SIZE, 2))
        elif difficulty == "hard":
            self.guards.append(Guard(1 * TILE_SIZE, 1 * TILE_SIZE, 2))  
            self.guards.append(Guard(18 * TILE_SIZE, 1 * TILE_SIZE, 2))  
            self.guards.append(Guard(1 * TILE_SIZE, 13 * TILE_SIZE, 2))  

    def play_game(self):
        running = True
        while running:
            screen.fill(BLACK)

            self.maze.draw()
            self.player.draw()
            for guard in self.guards:
                guard.move(self.player, self.maze) 
                guard.draw()  

            keys = pygame.key.get_pressed()
            self.player.move(keys, self.maze)

            for guard in self.guards:
                if (self.player._x, self.player._y) == (guard._x, guard._y):
                    self.lose_menu() 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()
            clock.tick(60)

    def lose_menu(self):
        lose_text = title_font.render("You Lose!", True, YELLOW)
        lose_rect = lose_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        
        back_button_text = "Back to Main Menu"
        back_button_surface = button_font.render(back_button_text, True, BUTTON_TEXT_COLOR)
        back_button_width = back_button_surface.get_width() + 20  
        back_button_height = back_button_surface.get_height() + 10  
        back_button = Button(WIDTH // 2 - back_button_width // 2, HEIGHT // 2 - back_button_height // 2, back_button_width, back_button_height, back_button_text, BUTTON_COLOR, BUTTON_TEXT_COLOR)

        running = True
        while running:
            screen.fill(BLACK)

            screen.blit(lose_text, lose_rect)

            back_button.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  
                    sys.exit()    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_clicked(event.pos):
                        self.__init__()  
                        self.main_menu()  

            pygame.display.flip()
            clock.tick(60)

    def difficulty_menu(self):
        easy_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 50, "Easy", GREEN, BUTTON_TEXT_COLOR)
        medium_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 50, "Medium", (255, 165, 0), BUTTON_TEXT_COLOR)
        hard_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 110, 200, 50, "Hard", (255, 0, 0), BUTTON_TEXT_COLOR)
        back_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 180, 200, 50, "Back", BUTTON_COLOR, BUTTON_TEXT_COLOR)

        running = True
        while running:
            screen.fill(BLACK)

            difficulty_text = title_font.render("Select Difficulty", True, YELLOW)
            difficulty_rect = difficulty_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            screen.blit(difficulty_text, difficulty_rect)

            easy_button.draw()
            medium_button.draw()
            hard_button.draw()
            back_button.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_button.is_clicked(event.pos):
                        self.start_game("easy")
                    elif medium_button.is_clicked(event.pos):
                        self.start_game("medium")
                    elif hard_button.is_clicked(event.pos):
                        self.start_game("hard")
                    elif back_button.is_clicked(event.pos):
                        return

            pygame.display.flip()
            clock.tick(60)

    def run(self):
        self.main_menu()

if __name__ == "__main__":
    game = Game()
    game.run()