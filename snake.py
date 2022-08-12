import random

import pygame
from pygame.locals import *
import time

size = 27
OVER_COLOR = (255,255,255)
x_final_value = 36
y_final_value = 18

class Apple:
    def __init__(self,parent_screen):
        self.img = pygame.image.load('image/block.jpg').convert()
        self.parent_screen = parent_screen
        self.x = size * 3
        self.y = size * 3

    def draw(self):
        self.parent_screen.blit(self.img, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0,x_final_value)*size
        self.y = random.randint(0,y_final_value)*size

class snake:
    def __init__(self,parent_screen,length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load('image/target.png').convert()
        self.block_x = [size]*length
        self.block_y = [size]*length
        self.direction = 'down'
        self.counter_direction = 'up'
        self.length = length

    def draw(self):
        #self.parent_screen.fill((0, 230, 0))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.block_x[i], self.block_y[i]))
        pygame.display.flip()

    def move_up(self):
        self.direction = 'up'
        self.counter_direction = 'down'

    def move_down(self):
        self.direction = 'down'
        self.counter_direction = 'up'

    def move_left(self):
        self.direction = 'left'
        self.counter_direction = 'right'

    def move_right(self):
        self.direction = 'right'
        self.counter_direction = 'left'

    def walk(self):

        for i in range(self.length-1,0,-1):
            self.block_x[i] = self.block_x[i-1]
            self.block_y[i] = self.block_y[i-1]

        if self.direction == 'up':
            self.block_y[0] -= size
        if self.direction == 'down':
            self.block_y[0] += size
        if self.direction == 'left':
            self.block_x[0] -= size
        if self.direction == 'right':
            self.block_x[0] += size

        self.draw()

    def increase_length(self):
        self.length += 1
        self.block_x.append(-1)
        self.block_y.append(-1)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.game_mode = True
        self.count = 0

        self.surface = pygame.display.set_mode((999, 513))
        self.choose_game_mode()
        self.play_background_music()
        #self.surface.fill((0, 230, 0))
        self.background()

        self.snake = snake(self.surface,1)
        self.snake.draw()

        self.apple = Apple(self.surface)
        self.apple.draw()

    def choose_game_mode(self):
        self.surface.fill((OVER_COLOR))

        font = pygame.font.SysFont('airel', 50)
        line_1 = font.render(f'CHOOSE GAME MODE', True, (0, 0, 255))
        self.surface.blit(line_1, (300, 100))
        line_2 = font.render(f'BORDER MODE     LOOP MODE', True, (0, 0, 0))
        self.surface.blit(line_2, (250, 300))
        line_3 = font.render(f'  PRESS 1                    PRESS 2', True, (0, 0, 0))
        self.surface.blit(line_3, (250, 400))
        pygame.display.flip()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_1:
                        self.game_mode = True
                        #print("YUP WORKED")
                        running = False
                    elif event.key == K_2:
                        self.game_mode = False
                        running = False
                    elif event.key == K_ESCAPE:
                        exit(0)

    def reset(self):
        self.snake = snake(self.surface, 1)

        self.apple = Apple(self.surface)

    def collision(self,x1,y1,x2,y2):
        #if x2 <= x1 <= x2 + size:
         #   if y2 <= y1 <= y2 + size:
          #      if x1 <= x2 <= x1 + size:
           #         if y1 <= y2 <= y1 + size:
            #            return True
        if x2 <= x1 <= x2 + (size//2):
            if y2 <= y1 <= y2 + (size//2):
                return True
        return False

    def background(self):
        back = pygame.image.load('image/depositphotos_57986157-stock-photo-grass-texture-seamless.jpg')
        self.surface.blit(back,(0,0))

    def play_background_music(self):
        pygame.mixer.music.load('mp3/bg_music_1.mp3')
        pygame.mixer.music.play()

    def play_sound(self,sound):
        sound = pygame.mixer.Sound(f'mp3/{sound}')
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.background()
        self.snake.walk()
        self.apple.draw()
        self.score()
        pygame.display.flip()

        if self.collision(self.snake.block_x[0],self.snake.block_y[0],self.apple.x,self.apple.y):
            #print("COLLISON")
            self.play_sound('1_snake_game_resources_ding.mp3')
            self.apple.move()
            self.snake.increase_length()

        #collode with snake
        for i in range(3,self.snake.length):
            if self.collision(self.snake.block_x[0],self.snake.block_y[0],self.snake.block_x[i],self.snake.block_y[i]):
                #print('GAME OVER')
                self.play_sound('mixkit-player-losing-or-failing-2042.wav')
                raise "Game Over"

        #collide with boundries
        if self.game_mode:
            if not (0 <= self.snake.block_x[0] <= 999 and 0 <= self.snake.block_y[0] <= 513):
                self.play_sound('1_snake_game_resources_crash.mp3')
                raise "Hit the BOUNDARY"
        else:
            if self.snake.block_x[0] < 0:
                self.loop(1)
            elif self.snake.block_x[0] > 999:
                self.loop(2)
            elif self.snake.block_y[0] < 0:
                self.loop(3)
            elif self.snake.block_y[0] > 513:
                self.loop(4)

    def loop(self,value):
        if value == 1:
            self.snake.block_x[0] = size * (x_final_value + 1)
        elif value == 2:
            self.snake.block_x[0] = 0 - size
        elif value == 3:
            self.snake.block_y[0] = size * (y_final_value + 1)
        elif value == 4:
            self.snake.block_y[0] = 0 - size

    def score(self):
        font = pygame.font.SysFont('airel',30)
        score = font.render(f'score:{self.snake.length}',True,(255,255,255))
        self.surface.blit(score,(800,10))

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        self.choose_game_mode()
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:
                        if event.key == K_UP and self.snake.counter_direction != 'up':
                            self.snake.move_up()
                        if event.key == K_DOWN and self.snake.counter_direction != 'down':
                            self.snake.move_down()
                        if event.key == K_LEFT and self.snake.counter_direction != 'left':
                            self.snake.move_left()
                        if event.key == K_RIGHT and self.snake.counter_direction != 'right':
                            self.snake.move_right()
                    # pass
                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.2)

    def show_game_over(self):
        self.surface.fill(OVER_COLOR)
        #self.background()
        font = pygame.font.SysFont('airel',50)
        over = font.render(f'GAME OVER SCORE :{self.snake.length}',True,(0,0,255))
        self.surface.blit(over,(100,100))
        menu = font.render('To play again ENTER,To exit press ESC',True,(255,0,0))
        self.surface.blit(menu,(100,200))
        pygame.display.flip()

        pygame.mixer.music.pause()


if __name__ =='__main__':

    game = Game()
    game.choose_game_mode()
    game.run()












