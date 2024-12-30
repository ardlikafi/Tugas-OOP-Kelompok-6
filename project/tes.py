import pygame  # Mengimpor modul pygame untuk membuat game
import sys  # Mengimpor modul sys untuk interaksi dengan sistem
import time  # Mengimpor modul time untuk mengatur waktu
from collections import deque  # Mengimpor deque untuk implementasi antrian
from abc import ABC, abstractmethod  # Mengimpor ABC dan abstractmethod untuk membuat kelas abstrak

# Inisialisasi pygame
pygame.init()

# Konstanta untuk ukuran layar dan warna
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BUTTON_COLOR = (200, 200, 200)
BUTTON_TEXT_COLOR = BLACK

# Membuat layar game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Runner Arcade")  # Judul jendela
clock = pygame.time.Clock()  # Mengatur kecepatan frame

# Font untuk judul dan tombol
title_font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Kelas abstrak untuk entitas game
class GameEntity(ABC):
    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self):
        pass

# Kelas untuk karakter pemain
class Character(GameEntity):
    def __init__(self, x, y, speed):
        self._x = x  # Posisi x karakter
        self._y = y  # Posisi y karakter
        self._speed = speed  # Kecepatan karakter

    def draw(self):
        pass  # Metode untuk menggambar karakter (belum diimplementasikan)

    def move(self):
        pass  # Metode untuk menggerakkan karakter (belum diimplementasikan)

    def update(self):
        pass  # Metode untuk memperbarui status karakter (belum diimplementasikan)

# Kelas untuk labirin
class Maze(GameEntity):
    def __init__(self):
        # Layout labirin menggunakan 1 untuk dinding dan 0 untuk ruang kosong
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
        self.reset_stars()  # Memanggil metode untuk mereset status bintang
        # Posisi bintang yang harus dikumpulkan
        self._star_positions = [
            (9 * TILE_SIZE, 7 * TILE_SIZE), 
            (5 * TILE_SIZE, 3 * TILE_SIZE), 
            (15 * TILE_SIZE, 5 * TILE_SIZE) 
        ]
        self._stars_collected = [False, False, False]  # Status pengumpulan bintang
        # Memuat gambar dinding dan bintang
        self.wall_image = pygame.transform.scale(pygame.image.load('wall.jpg'), (TILE_SIZE, TILE_SIZE)) 
        self.star_image = pygame.transform.scale(pygame.image.load('star.png'), (TILE_SIZE, TILE_SIZE)) 

    def reset_stars(self):
        self._stars_collected = [False, False, False]  # Status pengumpulan bintang direset

    def draw(self):
        # Menggambar labirin
        for row_idx, row in enumerate(self._layout):
            for col_idx, tile in enumerate(row):
                if tile == 1:  # Jika tile adalah dinding
                    screen.blit(self.wall_image, (col_idx * TILE_SIZE, row_idx * TILE_SIZE)) 

        # Menggambar tujuan (kotak hijau)
        pygame.draw.rect(screen, GREEN, (19 * TILE_SIZE, 7 * TILE_SIZE, TILE_SIZE, TILE_SIZE))  

        # Menggambar bintang yang belum dikumpulkan
        for index, position in enumerate(self._star_positions):
            if not self._stars_collected[index]:
                screen.blit(self.star_image, position)

    def collect_star(self, player_position):
        # Mengumpulkan bintang jika pemain berada di posisi yang sama
        for index, position in enumerate(self._star_positions):
            if not self._stars_collected[index] and player_position == position:
                self._stars_collected[index] = True  # Tandai bintang sebagai terkumpul

    def update(self):
        pass  # Metode untuk memperbarui status labirin (belum diimplementasikan)

# Kelas untuk pemain
class Player(Character):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed)  # Memanggil konstruktor kelas induk
        self.player_images = []  # Daftar gambar untuk animasi pemain
        
        # Memuat gambar untuk animasi pemain
        for i in range(1, 5):
            self.player_images.append(pygame.transform.scale(pygame.image.load(f'imgp/{i}.png'), (TILE_SIZE, TILE_SIZE)))

        self.current_image = self.player_images[0]  # Gambar saat ini
        self.direction = 'right'  # Arah awal
        self.frame_index = 0  # Indeks frame untuk animasi
        self.animation_speed = 0.1  # Kecepatan animasi
        self.last_update_time = time.time()  # Waktu pembaruan terakhir

    def draw(self):
        screen.blit(self.current_image, (self._x, self._y))  # Menggambar pemain di posisi saat ini

    def update_animation(self):
        current_time = time.time()  # Mendapatkan waktu saat ini
        if current_time - self.last_update_time >= self.animation_speed:  # Memeriksa apakah sudah waktunya untuk memperbarui animasi
            self.frame_index = (self.frame_index + 1) % len(self.player_images)  # Mengupdate indeks frame
            self.current_image = self.player_images[self.frame_index]  # Mengatur gambar saat ini
            self.last_update_time = current_time  # Memperbarui waktu terakhir

    def move(self, keys, maze):
        new_x, new_y = self._x, self._y  # Menyimpan posisi baru
        moving = False  # Menandakan apakah pemain bergerak

        # Menggerakkan pemain berdasarkan input keyboard
        if keys[pygame.K_UP]:
            new_y -= self._speed
        if keys[pygame.K_DOWN]:
            new_y += self._speed
        if keys[pygame.K_LEFT]:
            new_x -= self._speed
            self.current_image = pygame.transform.flip(self.player_images[self.frame_index], True, False)  # Membalik gambar untuk arah kiri
            moving = True
        if keys[pygame.K_RIGHT]:
            new_x += self._speed
            self.current_image = self.player_images[self.frame_index]  # Mengatur gambar untuk arah kanan
            moving = True  

        if moving:
            self.update_animation()  # Memperbarui animasi jika bergerak

        # Membatasi gerakan pemain agar tidak keluar dari layar
        if new_x < 0:
            new_x = 0
        if new_x + TILE_SIZE > WIDTH:
            new_x = WIDTH - TILE_SIZE

        # Memeriksa apakah posisi baru valid dalam labirin
        top_left = (new_x // TILE_SIZE, new_y // TILE_SIZE)
        top_right = ((new_x + TILE_SIZE - 1) // TILE_SIZE, new_y // TILE_SIZE)
        bottom_left = (new_x // TILE_SIZE, (new_y + TILE_SIZE - 1) // TILE_SIZE)
        bottom_right = ((new_x + TILE_SIZE - 1) // TILE_SIZE, (new_y + TILE_SIZE - 1) // TILE_SIZE)

        if all(0 <= pos[0] < len(maze._layout[0]) and 0 <= pos[1] < len(maze._layout) for pos in [top_left, top_right, bottom_left, bottom_right]):
            if all(maze._layout[pos[1]][pos[0]] == 0 for pos in [top_left, top_right, bottom_left, bottom_right]):
                self._x, self._y = new_x, new_y  # Memperbarui posisi pemain

        # Mengumpulkan bintang jika pemain berada di posisi yang sama
        for index, position in enumerate(maze._star_positions):
            if not maze._stars_collected[index] and (self._x, self._y) == position:
                maze.collect_star((self._x, self._y))

        # Memeriksa apakah pemain telah mencapai tujuan
        if new_x + TILE_SIZE >= WIDTH:
            if all(maze._stars_collected):
                print("Selamat! Anda telah mencapai garis finish!")  # Pesan kemenangan
                game.finish_menu()  # Menampilkan menu akhir
            else:
                print("Anda harus mengumpulkan bintangnya terlebih dahulu!")  # Pesan jika belum mengumpulkan bintang

# Kelas untuk tombol
class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)  # Membuat rectangle untuk tombol
        self.text = text  # Teks tombol
        self.color = color  # Warna tombol
        self.text_color = text_color  # Warna teks tombol

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)  # Menggambar tombol
        text_surface = button_font.render(self.text, True, self.text_color)  # Membuat surface untuk teks
        text_rect = text_surface.get_rect(center=self.rect.center)  # Mengatur posisi teks di tengah tombol
        screen.blit(text_surface, text_rect)  # Menggambar teks di tombol

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)  # Memeriksa apakah tombol diklik

# Kelas untuk penjaga
class Guard(Character):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed) # Memanggil konstruktor kelas induk
        self.guard_images = []  # Daftar gambar untuk animasi penjaga
        
        # Memuat gambar untuk animasi penjaga
        for i in range(1, 5):
            self.guard_images.append(pygame.transform.scale(pygame.image.load(f'imgg/{i}.png'), (TILE_SIZE, TILE_SIZE)))

        self.current_image = self.guard_images[0]  # Gambar saat ini
        self.direction = 'right'  # Arah awal
        self.frame_index = 0  # Indeks frame untuk animasi
        self.animation_speed = 0.1  # Kecepatan animasi
        self.last_update_time = time.time()  # Waktu pembaruan terakhir
        self.slow_speed = speed  # Kecepatan penjaga

    def bfs(self, layout, start, goal):
        # Algoritma BFS untuk menemukan jalur dari penjaga ke pemain
        if not (isinstance(start, tuple) and isinstance(goal, tuple)):
            raise ValueError("Start and goal must be tuples.")  # Memastikan start dan goal adalah tuple
        
        start = (int(start[0]), int(start[1]))  # Mengonversi start ke tuple integer
        goal = (int(goal[0]), int(goal[1]))  # Mengonversi goal ke tuple integer

        queue = deque([start])  # Antrian untuk BFS
        visited = set()  # Set untuk menyimpan posisi yang sudah dikunjungi
        visited.add(start)  # Menandai posisi awal sebagai dikunjungi
        parent = {start: None}  # Menyimpan parent untuk membangun jalur

        while queue:
            current = queue.popleft()  # Mengambil posisi saat ini dari antrian
            if current == goal:  # Jika mencapai tujuan
                break

            # Memeriksa posisi tetangga
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  
                neighbor = (current[0] + dx, current[1] + dy)  # Menghitung posisi tetangga
                if (0 <= neighbor[0] < len(layout[0]) and
                    0 <= neighbor[1] < len(layout) and
                    layout[neighbor[1]][neighbor[0]] == 0 and
                    neighbor not in visited):  # Memeriksa validitas posisi tetangga
                    visited.add(neighbor)  # Menandai tetangga sebagai dikunjungi
                    parent[neighbor] = current  # Menyimpan parent
                    queue.append(neighbor)  # Menambahkan tetangga ke antrian

        path = []  # Jalur yang ditemukan
        while current is not None:
            path.append(current)  # Menambahkan posisi ke jalur
            current = parent[current]  # Mengambil parent
        path.reverse()  # Membalik jalur untuk mendapatkan urutan yang benar
        return path  # Mengembalikan jalur

    def draw(self):
        screen.blit(self.current_image, (self._x, self._y))  # Menggambar penjaga di posisi saat ini

    def update_animation(self):
        current_time = time.time()  # Mendapatkan waktu saat ini
        if current_time - self.last_update_time >= self.animation_speed:  # Memeriksa apakah sudah waktunya untuk memperbarui animasi
            self.frame_index = (self.frame_index + 1) % len(self.guard_images)  # Mengupdate indeks frame
            self.current_image = self.guard_images[self.frame_index]  # Mengatur gambar saat ini
            self.last_update_time = current_time  # Memperbarui waktu terakhir

    def move(self, player, maze):
        player_x, player_y = player._x, player._y  # Mendapatkan posisi pemain
        guard_x, guard_y = self._x, self._y  # Mendapatkan posisi penjaga
        
        possible_moves = []  # Daftar gerakan yang mungkin
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Arah gerakan
        for dx, dy in directions:
            new_x = guard_x + dx
            new_y = guard_y + dy
            
            # Memeriksa apakah gerakan valid
            if (0 <= new_x // TILE_SIZE < len(maze._layout[0]) and
                0 <= new_y // TILE_SIZE < len(maze._layout) and
                maze._layout[new_y // TILE_SIZE][new_x // TILE_SIZE] == 0): 
                possible_moves.append((new_x, new_y))  # Menambahkan gerakan yang valid ke daftar
        
        if possible_moves:
            self.update_animation()  # Memperbarui animasi jika ada gerakan
            if (guard_x // TILE_SIZE, guard_y // TILE_SIZE) in possible_moves:
                self._x, self._y = player_x, player_y  # Jika penjaga berada di posisi yang valid, ikuti pemain
            else:
                path = self.bfs(maze._layout, (guard_x // TILE_SIZE, guard_y // TILE_SIZE), (player_x // TILE_SIZE, player_y // TILE_SIZE))  # Mencari jalur ke pemain
                if len(path) > 1:  # Jika ada jalur yang ditemukan
                    next_move = path[1]  # Mengambil langkah berikutnya
                    if self._x < next_move[0] * TILE_SIZE:
                        self._x += self.slow_speed  # Menggerakkan penjaga ke kanan
                    elif self._x > next_move[0] * TILE_SIZE:
                        self._x -= self.slow_speed  # Menggerakkan penjaga ke kiri
                    if self._y < next_move[1] * TILE_SIZE:
                        self._y += self.slow_speed  # Menggerakkan penjaga ke bawah
                    elif self._y > next_move[1] * TILE_SIZE:
                        self._y -= self.slow_speed  # Menggerakkan penjaga ke atas
            
            # Memeriksa apakah pemain tertangkap
            if (abs(self._x - player_x) < TILE_SIZE / 2 and abs(self._y - player_y) < TILE_SIZE / 2) or \
            (abs(self._x - player_x) < TILE_SIZE and abs(self._y - player_y) < TILE_SIZE):
                print("Player caught by the guard!")  # Pesan jika pemain tertangkap
                game.lose_menu()  # Menampilkan menu kalah

            # Mengatur arah gambar penjaga berdasarkan posisi pemain
            if player_x < guard_x: 
                self.current_image = pygame.transform.flip(self.guard_images[self.frame_index], True, False)  # Membalik gambar untuk arah kiri
                self.direction = 'left'
            else:
                self.current_image = self.guard_images[self.frame_index]  # Mengatur gambar untuk arah kanan
                self.direction = 'right'

    def update(self):
        self.move(self.player, self.maze)  # Memperbarui posisi penjaga
        self.update_animation()  # Memperbarui animasi

# Kelas untuk game
class Game:
    def __init__(self):
        self.maze = Maze()  # Membuat objek labirin
        self.player = Player(0 * TILE_SIZE, 7 * TILE_SIZE, 5)  # Membuat objek pemain
        self.guards = []  # Daftar penjaga
        self.current_difficulty = None  # Menyimpan kesulitan saat ini, tidak diinisialisasi

    def main_menu(self):
        # Membuat tombol untuk memulai dan keluar dari game
        start_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 50, "Start Game", BUTTON_COLOR, BUTTON_TEXT_COLOR)
        quit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 50, "Quit Game", BUTTON_COLOR, BUTTON_TEXT_COLOR)

        running = True
        while running:
            screen.fill(BLACK)  # Mengisi layar dengan warna hitam

            # Menggambar judul game
            title_text = title_font.render("MAZE RUNNER ARCADE", True, YELLOW)
            title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            screen.blit(title_text, title_rect)

            start_button.draw()  # Menggambar tombol mulai
            quit_button.draw()  # Menggambar tombol keluar

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Menutup game
                    sys.exit()     
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.is_clicked(event.pos):
                        self.difficulty_menu()  # Menampilkan menu kesulitan
                    elif quit_button.is_clicked(event.pos):
                        pygame.quit()  # Menutup game
                        sys.exit()    

            pygame.display.flip()  # Memperbarui tampilan layar
            clock.tick(60)  # Mengatur frame rate

    def finish_menu(self):
        finish_text = title_font.render("Congratulations!", True, YELLOW)  # Teks kemenangan
        finish_rect = finish_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))

        back_button_text = "Back to Main Menu"
        back_button_surface = button_font.render(back_button_text, True, BUTTON_TEXT_COLOR)  # Membuat surface untuk tombol kembali
        back_button_width = back_button_surface.get_width() + 20  # Lebar tombol kembali
        back_button_height = back_button_surface.get_height() + 10  # Tinggi tombol kembali
        back_button = Button(WIDTH // 2 - back_button_width // 2, HEIGHT // 2 + 40, back_button_width, back_button_height, back_button_text, BUTTON_COLOR, BUTTON_TEXT_COLOR)  # Membuat tombol kembali

        quit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 110, 200, 50, "Quit Game", BUTTON_COLOR, BUTTON_TEXT_COLOR)  # Tombol keluar

        # Menentukan apakah tombol Next Level perlu ditampilkan
        next_level_button = None
        if self.current_difficulty == "easy":
            next_level_button = Button(WIDTH // 2 - 100, 270, 200, 50, "Next Level", BUTTON_COLOR, BUTTON_TEXT_COLOR)  # Tombol Next Level untuk Easy
        elif self.current_difficulty == "medium":
            next_level_button = Button(WIDTH // 2 - 100, 270, 200, 50, "Next Level", BUTTON_COLOR, BUTTON_TEXT_COLOR)  # Tombol Next Level untuk Medium

        running = True
        while running:
            screen.fill(BLACK)  # Mengisi layar dengan warna hitam

            screen.blit(finish_text, finish_rect)  # Menggambar teks kemenangan

            if next_level_button:  # Jika tombol Next Level ada, gambar tombol tersebut
                next_level_button.draw()

            back_button.draw()  # Menggambar tombol kembali
            quit_button.draw()  # Menggambar tombol keluar

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Menutup game
                    sys.exit()     
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_clicked(event.pos):
                        self.__init__()  # Menginisialisasi ulang game
                        self.main_menu()  # Kembali ke menu utama
                    elif quit_button.is_clicked(event.pos):
                        pygame.quit()  # Menutup game
                        sys.exit()
                    elif next_level_button and next_level_button.is_clicked(event.pos):
                        if self.current_difficulty == "easy":
                            self.start_game("medium")  # Melanjutkan ke level Medium
                        elif self.current_difficulty == "medium":
                            self.start_game("hard")  # Melanjutkan ke level Hard

            pygame.display.flip()  # Memperbarui tampilan layar
            clock.tick(60)  # Mengatur frame rate

    def start_game(self, difficulty):
        self.current_difficulty = difficulty  # Simpan kesulitan yang dipilih
        print(f" Starting game on {difficulty} difficulty...")  # Menampilkan tingkat kesulitan
        self.maze.reset_stars()  # Reset status bintang
        self.player = Player(0 * TILE_SIZE, 7 * TILE_SIZE, 5)  # Membuat objek pemain
        self.guards = []  # Mengosongkan daftar penjaga
        self.initialize_guards(difficulty)  # Menginisialisasi penjaga berdasarkan kesulitan
        self.play_game()  # Memulai permainan
    
    def initialize_guards(self, difficulty):
        # Menambahkan penjaga berdasarkan tingkat kesulitan
        if difficulty == "easy":
            self.guards.append(Guard(1 * TILE_SIZE, 1 * TILE_SIZE, 2))  # Satu penjaga untuk kesulitan mudah
        elif difficulty == "medium":
            self.guards.append(Guard(1 * TILE_SIZE, 1 * TILE_SIZE, 2))  # Dua penjaga untuk kesulitan sedang
            self.guards.append(Guard(18 * TILE_SIZE, 1 * TILE_SIZE, 2))
        elif difficulty == "hard":
            self.guards.append(Guard(1 * TILE_SIZE, 1 * TILE_SIZE, 2))  # Tiga penjaga untuk kesulitan sulit
            self.guards.append(Guard(18 * TILE_SIZE, 1 * TILE_SIZE, 2))  
            self.guards.append(Guard(1 * TILE_SIZE, 13 * TILE_SIZE, 2))  

    def play_game(self):
        running = True
        while running:
            screen.fill(BLACK)  # Mengisi layar dengan warna hitam

            self.maze.draw()  # Menggambar labirin
            self.player.draw()  # Menggambar pemain
            for guard in self.guards:
                guard.move(self.player, self.maze)  # Menggerakkan penjaga
                guard.draw()  # Menggambar penjaga

            keys = pygame.key.get_pressed()  # Mendapatkan input keyboard
            self.player.move(keys, self.maze)  # Menggerakkan pemain

            for guard in self.guards:
                if (self.player._x, self.player._y) == (guard._x, guard._y):  # Memeriksa apakah pemain tertangkap
                    self.lose_menu()  # Menampilkan menu kalah

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # Menghentikan permainan jika jendela ditutup

            pygame.display.flip()  # Memperbarui tampilan layar
            clock.tick(60)  # Mengatur frame rate

    def lose_menu(self):
        lose_text = title_font.render("You Lose!", True, YELLOW)  # Teks kalah
        lose_rect = lose_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        
        back_button_text = "Back to Main Menu" # Teks untuk tombol Kembali ke Main Menu
        back_button_surface = button_font.render(back_button_text , True, BUTTON_TEXT_COLOR)  # Membuat surface untuk tombol kembali
        back_button_width = back_button_surface.get_width() + 20  # Lebar tombol kembali
        back_button_height = back_button_surface.get_height() + 10  # Tinggi tombol kembali
        back_button = Button(WIDTH // 2 - back_button_width // 2, HEIGHT // 2 + 40, back_button_width, back_button_height, back_button_text, BUTTON_COLOR, BUTTON_TEXT_COLOR)  # Membuat tombol kembali

        retry_button_text = "Retry"  # Teks untuk tombol Retry
        retry_button_surface = button_font.render(retry_button_text, True, BUTTON_TEXT_COLOR)  # Membuat surface untuk tombol Retry
        retry_button_width = retry_button_surface.get_width() + 20  # Lebar tombol Retry
        retry_button_height = retry_button_surface.get_height() + 10  # Tinggi tombol Retry
        retry_button = Button(WIDTH // 2 - retry_button_width // 2, HEIGHT // 2 - 30, retry_button_width, retry_button_height, retry_button_text, BUTTON_COLOR, BUTTON_TEXT_COLOR)  # Membuat tombol Retry

        running = True
        while running:
            screen.fill(BLACK)  # Mengisi layar dengan warna hitam

            screen.blit(lose_text, lose_rect)  # Menggambar teks kalah

            retry_button.draw()  # Menggambar tombol Retry
            back_button.draw()  # Menggambar tombol kembali

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Menutup game
                    sys.exit()    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_clicked(event.pos):
                        self.__init__()  # Menginisialisasi ulang game
                        self.main_menu()  # Kembali ke menu utama
                    elif retry_button.is_clicked(event.pos):
                        if self.current_difficulty:  # Pastikan kesulitan sudah dipilih
                            self.start_game(self.current_difficulty)  # Mengulang permainan dengan kesulitan yang sama

            pygame.display.flip()  # Memperbarui tampilan layar
            clock.tick(60)  # Mengatur frame rate

    def difficulty_menu(self):
        # Membuat tombol untuk memilih tingkat kesulitan
        easy_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 50, "Easy", GREEN, BUTTON_TEXT_COLOR)
        medium_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 50, "Medium", (255, 165, 0), BUTTON_TEXT_COLOR)
        hard_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 110, 200, 50, "Hard", (255, 0, 0), BUTTON_TEXT_COLOR)
        back_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 180, 200, 50, "Back", BUTTON_COLOR, BUTTON_TEXT_COLOR)

        running = True
        while running:
            screen.fill(BLACK)  # Mengisi layar dengan warna hitam

            difficulty_text = title_font.render("Select Difficulty", True, YELLOW)  # Teks untuk memilih kesulitan
            difficulty_rect = difficulty_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            screen.blit(difficulty_text, difficulty_rect)  # Menggambar teks kesulitan

            easy_button.draw()  # Menggambar tombol mudah
            medium_button.draw()  # Menggambar tombol sedang
            hard_button.draw()  # Menggambar tombol sulit
            back_button.draw()  # Menggambar tombol kembali

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # Menghentikan permainan jika jendela ditutup
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_button.is_clicked(event.pos):
                        self.start_game("easy")  # Memulai permainan dengan kesulitan mudah
                    elif medium_button.is_clicked(event.pos):
                        self.start_game("medium")  # Memulai permainan dengan kesulitan sedang
                    elif hard_button.is_clicked(event.pos):
                        self.start_game("hard")  # Memulai permainan dengan kesulitan sulit
                    elif back_button.is_clicked(event.pos):
                        return  # Kembali ke menu sebelumnya

            pygame.display.flip()  # Memperbarui tampilan layar
            clock.tick(60)  # Mengatur frame rate

    def run(self):
        self.main_menu()  # Memulai game dengan menu utama

# Memulai game jika file ini dijalankan
if __name__ == "__main__":
    game = Game()  # Membuat objek game
    game.run()  # Menjalankan game