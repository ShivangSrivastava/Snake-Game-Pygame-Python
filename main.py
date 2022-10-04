import pygame
import random
import os

pygame.mixer.init()

pygame.init()



# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

#Background Image
#bgimg = pygame.image.load("snake.jpg")
#bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()


# Game Title
pygame.display.set_caption("Snake Game By Shivang")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233,210,229))
        text_screen("Welcome to Snakes", black, 260, 250)
        text_screen("Press Space Bar To Play", black, 232, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()

        pygame.display.update()
        clock.tick(60)


# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_color = black
    food_color = red
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    # Check if high_score file exists
    if(not os.path.exists("high_score.txt")):
        with open("high_score.txt", "w") as f:
            f.write("0")

    with open("high_score.txt", "r") as f:
        high_score = f.read()

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    init_velocity = 1
    temp_vx, temp_vy = 0, 0
    snake_size = 30
    fps = 60
    while not exit_game:
        if game_over:
            with open("high_score.txt", "w") as f:
                f.write(str(high_score))
            gameWindow.fill(white)
            text_screen("Game Over! Press Enter To Continue", red, 100, 250)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score += 10

                    if event.key == pygame.K_w:
                        if score > 10:
                            score -= 10

                    if event.key == pygame.K_a:
                        init_velocity += 1

                    if event.key == pygame.K_s:
                        if init_velocity > 1:
                            init_velocity -= 1
                    
                    if event.key == pygame.K_z:
                        snk_length += 5
                    
                    if event.key == pygame.K_x:
                        if snk_length > 20:
                            snk_length -= 5
                    if event.key == pygame.K_p:
                        temp_vx, temp_vy = velocity_x, velocity_y 
                        velocity_x, velocity_y = 0, 0

                    if event.key == pygame.K_o:
                        velocity_x, velocity_y = temp_vx, temp_vy
                    
                    if event.key == pygame.K_l:
                        food_color = random.randrange(256),random.randrange(256),random.randrange(256)

                    if event.key == pygame.K_k:
                        snake_color = random.randrange(256), random.randrange(
                            256), random.randrange(256)


            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<15 and abs(snake_y - food_y)<15:
                pygame.mixer.music.load('eat.mp3')
                pygame.mixer.music.play()
                score +=10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 20
                if score>int(high_score):
                    high_score = score

            gameWindow.fill(white)
            #gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score) + "  High score: "+str(high_score), red, 5, 5)
            pygame.draw.rect(gameWindow, food_color, [food_x, food_y, snake_size, snake_size])


            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('over.mp3')
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('over.mp3')
                pygame.mixer.music.play()
            plot_snake(gameWindow, snake_color, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()


welcome()
