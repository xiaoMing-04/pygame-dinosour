import pygame, sys, random

pygame.init()
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

GRAVITY = 0.4

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dinosaur")
icon = pygame.image.load(r"Assets/Dino/DinoStart.png").convert_alpha()
pygame.display.set_icon(icon)

CLOCK = pygame.time.Clock()

# set game track
track = pygame.image.load(r"Assets/Other/Track.png").convert_alpha()
track_pos = 0

# set dinosaur
dinosaur_run1 = pygame.image.load(r"assets/Dino/DinoRun1.png").convert_alpha()
dinosaur_run2 = pygame.image.load(r"assets/Dino/DinoRun2.png").convert_alpha()

dinosaur_jump = pygame.image.load(r"Assets/Dino/DinoJump.png").convert_alpha()

dinosaur_dead = pygame.image.load(r"Assets/Dino/DinoDead.png").convert_alpha()

dinosaur_state = [dinosaur_run1, dinosaur_run2]
index_dino = 0
dinosaur = dinosaur_state[index_dino]
dinosaur_rect = dinosaur.get_rect(center=(100, 480))

dinosaur_run = pygame.USEREVENT
pygame.time.set_timer(dinosaur_run, 90)

dinosaur_pos = 0

#  set game clouds
cloud = pygame.image.load(r"Assets/Other/Cloud.png").convert_alpha()
clouds = []

cloud_spawn= pygame.USEREVENT + 1
pygame.time.set_timer(cloud_spawn, 1200)

def get_cloud():
    cloud_height = random.choice([x for x in range(100, 300) if x % 10])
    return cloud.get_rect(center=(1200, cloud_height))

def display_cloud():
    for cloud_rect in clouds:
        SCREEN.blit(cloud, cloud_rect)
      
def update_clouds():
    new_clouds = []
    for cloud_rect in clouds:
        cloud_rect.right -= 1

        if cloud_rect.right > 0:
            new_clouds.append(cloud_rect)
    
    return new_clouds

game_speech = 3

# set game cactus
small_cactus1 = pygame.image.load(r"Assets/Cactus/SmallCactus1.png").convert_alpha()
small_cactus2 = pygame.image.load(r"Assets/Cactus/SmallCactus2.png").convert_alpha()
small_cactus3 = pygame.image.load(r"Assets/Cactus/SmallCactus3.png").convert_alpha()
large_cactus1 = pygame.image.load(r"Assets/Cactus/LargeCactus1.png").convert_alpha()
large_cactus2 = pygame.image.load(r"Assets/Cactus/SmallCactus2.png").convert_alpha()
large_cactus3 = pygame.image.load(r"Assets/Cactus/LargeCactus3.png").convert_alpha()

cactuses_spawn = [small_cactus1, small_cactus2, small_cactus3, large_cactus1, large_cactus2, large_cactus3]

cactus_index = 0
cactuses = []

def get_cactus():
    cactus_index = 0
    if game_speech <= 3:
        cactus_index = random.choice(range(2))
    elif game_speech <= 4:
        cactus_index = random.choice(range(3))
    else:
        cactus_index = random.choice(range(6))
        
    cactus_rect = cactuses_spawn[cactus_index].get_rect(midbottom=(1200, 520))
    return [cactuses_spawn[cactus_index], cactus_rect]

def display_cactus():
    for cactus in cactuses:
        SCREEN.blit(cactus[0], cactus[1])

def update_cactus():
    new_cactuses = []
    
    for cactus in cactuses:
        cactus[1].centerx -= game_speech
        
        if cactus[1].centerx > 0:
            new_cactuses.append(cactus)
    return new_cactuses

cactus_spawn = pygame.USEREVENT + 2
pygame.time.set_timer(cactus_spawn, 1500)


# set game bird
bird1 = pygame.image.load(r"Assets/Bird/Bird1.png").convert_alpha()
bird2 = pygame.image.load(r"Assets/Bird/Bird2.png").convert_alpha()

birds = [bird1, bird2]
bird_index = 0

bird = birds[bird_index]

bird_flap = pygame.USEREVENT + 3
pygame.time.set_timer(bird_flap, 300 - 10 * game_speech)

def get_bird():
    bird_rect = birds[0].get_rect(center=(1200, random.choice([300, 400])))
    return bird_rect

birds_rect = []
bird_spawn = pygame.USEREVENT + 4
pygame.time.set_timer(bird_spawn, 5000 - 100 * game_speech)

def display_bird(bird):
    for bird_rect in birds_rect:
        SCREEN.blit(bird, bird_rect)

def update_bird():
    new_birds_rect = []
    
    for bird_rect in birds_rect:
        bird_rect.centerx -= game_speech
        
        if bird_rect.centerx > 0:
            new_birds_rect.append(bird_rect)
    return new_birds_rect

# set game font
score = 0

def display_score(score):
    global font
    score_str = str(int(score))
    n = 5 - len(score_str)
    
    font = pygame.font.Font(r"04B_19.TTF", 40)
    font = font.render("0" * n + score_str, True, (128, 128, 128))
    font_rect = font.get_rect(center=(70, 40))
    
    SCREEN.blit(font, font_rect)

# set game over
game_over = pygame.image.load(r"Assets/Other/GameOver.png").convert_alpha()
game_over_rect = game_over.get_rect(center=(600, 200))
reset = pygame.image.load(r"Assets/Other/Reset.png").convert_alpha()
reset_rect = reset.get_rect(center=(600, 300))

# check collision
def check_collision(dino_rect):
    for cactus in cactuses:
        if dino_rect.colliderect(cactus[1]):
            return False
    for bird in birds_rect:
        if dino_rect.colliderect(bird):
            return False
    return True

# game logic variable
start_screen = pygame.image.load(r"Assets/Dino/DinoStart.png").convert_alpha()
start_screen_rect = start_screen.get_rect(center=(100, 480))

start = True
while start:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = False
                
    SCREEN.fill((255, 255, 255))
    SCREEN.blit(start_screen, start_screen_rect)
    
    CLOCK.tick(120)
    pygame.display.update()

# set game sound
hit_sound = pygame.mixer.Sound(r"sound/tick.wav")
collision_sound = pygame.mixer.Sound(r"sound/te.wav")
collision_sound_play = True

# set dinosaur duck
dino_duck1 = pygame.image.load(r"Assets/Dino/DinoDuck1.png").convert_alpha()
dino_duck2 = pygame.image.load(r"Assets/Dino/DinoDuck2.png").convert_alpha()

dino_rect = dino_duck1.get_rect(center=(100, 500))

dino_duck_list = [dino_duck1, dino_duck2]

# game hardcore mod
hardcore = {
    200 : 4,
    400: 5,
    700: 6,
    1200: 7
}

on_the_air = False
game_active = True
shift_hold = False
dino_bottom = 480
dino_rect_tmp = dinosaur_rect

duck = False

while True:
    tmp = int(score)
    if tmp in hardcore:
        game_speech = hardcore[tmp]
    
    game_active = check_collision(dino_rect_tmp)

    if game_active == False:
        if collision_sound_play:
            collision_sound.play()
            collision_sound_play = False
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and on_the_air == False:
                    hit_sound.play()
                    dinosaur_pos = -15
                    on_the_air = True
                    shift_hold = False
                    dino_bottom = 480
                    dino_rect_tmp = dinosaur_rect
                    dinosaur = dinosaur_state[index_dino]
    
            # dinosaur run
            if on_the_air == False:
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        shift_hold = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                        shift_hold = False
                
                if event.type == dinosaur_run:
                    if shift_hold == False:
                        dinosaur = dinosaur_state[index_dino]
                        dino_rect_tmp = dinosaur_rect
                        dino_bottom = 480
                    else:
                        dinosaur = dino_duck_list[index_dino]
                        dino_rect_tmp = dino_rect
                        dino_bottom = 500
                        
                    index_dino += 1
                    index_dino %= 2
            
            
            # clouds
            if event.type == cloud_spawn:
                if len(clouds) < 10:
                    clouds.append(get_cloud())
                
            # cactuses
            if event.type == cactus_spawn:
                cactus_tmp = get_cactus()
                if len(birds_rect) == 0 or cactus_tmp[1].centerx - birds_rect[-1].centerx >= 300:
                    cactuses.append(get_cactus())
                
            # birds
            if event.type == bird_flap:
                bird = birds[bird_index]
                bird_index += 1
                bird_index %= 2
                
            if event.type == bird_spawn:
                bird_tmp = get_bird()
                if len(cactuses) == 0 or bird_tmp.centerx - cactuses[-1][1].centerx >= 300:
                    birds_rect.append(get_bird())
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    track_pos = 0
                    score = 0
                    index_dino = 0
                    dinosaur_pos = 0
                    on_the_air = False
                    clouds.clear()
                    cactus_index = 0
                    cactuses.clear()
                    bird_index = 0
                    birds_rect.clear()
                    dino_bottom = 480
                    game_active = True
                    collision_sound_play = True
                    shift_hold = False
                    dino_rect_tmp.centery = 480
    
    SCREEN.fill((255, 255, 255)) 

    # cloud
    display_cloud()
    if game_active:
        clouds = update_clouds()
    
    # dinosaur
    if game_active:
        dino_rect_tmp.centery = min(dino_rect_tmp.centery + dinosaur_pos, dino_bottom)
    
        if on_the_air == False:
            SCREEN.blit(dinosaur, dino_rect_tmp)
        else:
            SCREEN.blit(dinosaur_jump, dino_rect_tmp)

        if dino_rect_tmp.centery == dino_bottom:
            on_the_air = False
            dinosaur_pos = 0
        else:
            dinosaur_pos += GRAVITY

    else:
        SCREEN.blit(dinosaur_dead, dinosaur_rect)
    
    # cactus
    display_cactus()
    if game_active:
        cactuses = update_cactus()
    
    # track
    SCREEN.blit(track, (track_pos, 500))
    SCREEN.blit(track, (track_pos + 2404, 500))
    if game_active:
        track_pos -= game_speech
        if track_pos < -2404:
            track_pos = 0
    
    # bird
    display_bird(bird)
    if game_active:
        birds_rect = update_bird()
    
    # font
    display_score(score)
    if game_active:
        score += 0.05
    
    # game over
    if game_active == False:
        SCREEN.blit(game_over, game_over_rect)
        SCREEN.blit(reset, reset_rect)
    
    CLOCK.tick(120)
    pygame.display.update()