import datetime
import os
import random
import threading
import pygame
import os

pygame.init()

# Global Constants

SCREEN_HEIGHT = 480
SCREEN_WIDTH = 1050
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background_image = pygame.image.load('assets\CityBG.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Chrome Dino Runner")

Ico = pygame.image.load(os.path.join("assets/Duke", "Duke_1.png"))
pygame.display.set_icon(Ico)

RUNNING = [
    pygame.image.load(os.path.join("assets/Duke", "Duke_1.png")),
    pygame.image.load(os.path.join("assets/Duke", "Duke_2.png")),
    pygame.image.load(os.path.join("assets/Duke", "Duke_3.png")),
    pygame.image.load(os.path.join("assets/Duke", "Duke_4.png")),
    pygame.image.load(os.path.join("assets/Duke", "Duke_5.png")),
    pygame.image.load(os.path.join("assets/Duke", "Duke_6.png")),
    pygame.image.load(os.path.join("assets/Duke", "Duke_7.png")),
    pygame.image.load(os.path.join("assets/Duke", "Duke_8.png")),
    pygame.image.load(os.path.join("assets/Duke", "Duke_9.png")),
    pygame.image.load(os.path.join("assets/Duke", "Duke_10.png")),
    pygame.image.load(os.path.join("assets/Duke", "Duke_11.png")),
    pygame.image.load(os.path.join("assets/Duke", "Duke_12.png")),
]
JUMPING = pygame.image.load(os.path.join("assets/Duke", "Duke_9.png"))

DUCKING = [
    pygame.image.load(os.path.join("assets/Duke", "Duke_10.png")),
    pygame.image.load(os.path.join("assets/Duke", "Duke_10.png"))
]

SMALL_CACTUS = [
    pygame.image.load(os.path.join("assets/Pines", "SpikeUpR.png")),
    pygame.image.load(os.path.join("assets/Pines", "SpikeUpR.png")),
    pygame.image.load(os.path.join("assets/Pines", "SpikeUpR.png")),
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join("assets/Pines", "SpikeUpR.png")),
    pygame.image.load(os.path.join("assets/Pines", "SpikeUpR.png")),
    pygame.image.load(os.path.join("assets/Pines", "SpikeUpR.png")),
]

BIRD = [
    pygame.image.load(os.path.join("assets/Pines", "SpikeLeftR.png")),
    pygame.image.load(os.path.join("assets/Pines", "SpikeLeftR.png")),
]

CLOUD = pygame.image.load(os.path.join("assets/Other", "Cloud_3.png"))

BG = pygame.image.load(os.path.join("assets/Other", "Track_4.png"))

FONT_COLOR=(255,255,255)

class Dinosaur:

    X_POS = 80 # Main Character Position
    Y_POS = 390
    Y_POS_DUCK = 325
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 12:
            self.step_index = 0

        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 6]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 1]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(70, 120)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(800, 1200)
            self.y = random.randint(70, 120)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 345


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 345

class Bird(Obstacle):
    BIRD_HEIGHTS = [245, 320]

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1
        
        os.system('cls')

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    clouds = [Cloud() for _ in range(3)]
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 450
    points = 0
    font = pygame.font.Font("C:/Windows/WinSxS/amd64_microsoft-windows-f..ruetype-comicsansms_31bf3856ad364e35_10.0.22621.1_none_3deaef772e20c404/comic.ttf", 20)
    obstacles = []
    death_count = 0
    pause = False

    def score():
        global points, game_speed, highscore  # Adicione highscore como global para acessá-lo diretamente
        points += 1
        if points % 100 == 0:
            game_speed += 1

        highscore = 0  # Inicializa o highscore

        # Verifique se o arquivo score.txt existe e não está vazio
        if os.path.exists("score.txt") and os.path.getsize("score.txt") > 0:
            with open("score.txt", "r") as f:
                score_ints = [int(x) for x in f.read().split() if x.isdigit()]
                if score_ints:
                    highscore = max(score_ints)

        # Renderiza o texto do highscore na tela
        text = font.render("High Score: " + str(highscore) + "  Points: " + str(points), True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (900, 40)
        SCREEN.blit(text, textRect)



    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    def unpause():
        nonlocal pause, run
        pause = False
        run = True

    def paused():
        nonlocal pause
        pause = True
        font = pygame.font.Font("C:/Windows/WinSxS/amd64_microsoft-windows-f..ruetype-comicsansms_31bf3856ad364e35_10.0.22621.1_none_3deaef772e20c404/comic.ttf", 30)
        text = font.render("Game Paused, Press 'u' to Unpause", True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT  // 3)
        SCREEN.blit(text, textRect)
        pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    unpause()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                run = False
                paused()

        current_time = datetime.datetime.now().hour
        if 7 < current_time < 19:
            FONT_COLOR=(255,255,255)
            SCREEN.blit(background_image, (0, 0)) 
        else:
            FONT_COLOR=(255,255,255)
            SCREEN.blit(background_image, (0, 0))  # Tela durante o jogo.
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                death_count += 1
                menu(death_count)

        background()
        
        for cloud in clouds:
            cloud.draw(SCREEN)
            cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points, highscore
    run = True
    
    def save_highscore(highscore):
        if os.path.exists("score.txt"):
            with open("score.txt", "r") as f:
                scores = f.readlines()
                if any(str(highscore) in score for score in scores):
                    return
        with open("score.txt", "a") as f:
            f.write(str(highscore) + "\n")
    
    while run:
        SCREEN.fill((44,7,53))  # Tela de morte.
        pygame.display.flip()
        font = pygame.font.Font("C:/Windows/WinSxS/amd64_microsoft-windows-f..ruetype-comicsansms_31bf3856ad364e35_10.0.22621.1_none_3deaef772e20c404/comic.ttf", 20)
                
        if death_count == 0:
            text = font.render("Press any Key to Start", True, (255,255,255))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (255,255,255))
            score = font.render("Your Score: " + str(points), True, (255,255,255))    
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
            
            save_highscore(highscore)
            hs_score_text = font.render(
                "High Score : " + str(highscore), True, FONT_COLOR
            )
            hs_score_rect = hs_score_text.get_rect()
            hs_score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            SCREEN.blit(hs_score_text, hs_score_rect)
            
            os.system('cls')
            
            if points > highscore:
                highscore = points
                initials = input("Novo recorde! Insira suas iniciais (3 letras): ")[:3].upper()
                with open("TopLeader.txt", 'r') as file:
                    conteudo_existente = file.read() 
                with open("TopLeader.txt", "w") as f:
                    f.write(f"{initials}: {highscore}\n{conteudo_existente}")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    main()
            
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        
        os.system('cls')
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()
                
        os.system('cls')
t1 = threading.Thread(target=menu(death_count=0), daemon=True)
t1.start()
