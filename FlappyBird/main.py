import random
from sys import exit
import pygame
try:
    pygame.mixer.init()
    bg_music=pygame.mixer.Sound("gallery/audio/bg.mp3")
    bg_music.play(loops=-1)
except Exception:
    pass

pygame.init()
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("gallery/sprites/bird.png").convert_alpha()
        self.rect = self.image.get_rect(center=(50, 250))
        self.velocity = 0
        self.gravity = 0.4
        self.max_velocity = 10  # Maximum velocity limit
        self.jumping = False
        try:
            self.jump_sound=pygame.mixer.Sound("gallery/audio/wing.wav")
            self.jump_sound.set_volume(0.3)
        except Exception:
            pass        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.top >= 0 and not self.jumping:
            self.velocity = -8  # Set velocity directly to control jump
            try:
                self.jump_sound.play()
            except Exception:
                pass
            self.jumping = True
        elif not keys[pygame.K_SPACE]:
            self.jumping = False
    def apply_gravity(self):
        self.velocity += self.gravity
        if self.velocity > self.max_velocity:  # Limit maximum velocity
            self.velocity = self.max_velocity
        if self.rect.bottom >= 511:  # Check if bird reaches the bottom of the screen
            global game_active
            game_active=False
        if self.rect.top <= 0:  # Check if bird reaches the top of the screen
            self.rect.top = 0
    def update(self):
        self.rect.y += self.velocity
    def update_0(self):
        self.apply_gravity()
        self.update()
        self.player_input()
class Pipe(pygame.sprite.Sprite):
    def __init__(self):
   
        super().__init__()
        self.image_bottom=pygame.image.load("gallery/sprites/pipe.png").convert_alpha()
        self.image_top = pygame.transform.rotate(self.image_bottom, 180)
        self.rect_bottom=self.image_bottom.get_rect(midbottom=(500, 600))
        self.rect_top=self.image_top.get_rect(midtop=(500, -200))
        self.passed=True
        self.height_change=0
    def movement(self):
        self.rect_bottom.x-=4
        self.rect_top.x-=4    
        if self.rect_top.x<=-50:
            self.reset()
            self.newheight()
            global score
            score+=1
            
            
    def newheight(self):
        heightchange = random.randint(-100, 100)
        self.rect_bottom.y = 300 + heightchange
        self.rect_top.y = self.rect_bottom.y - self.rect_top.height - 150


    def update(self):
        self.movement()
        self.destroy()
        
    def reset(self):
        self.rect_top.x = 500
        self.rect_bottom.x = 500
        self.passed=False
    def destroy(self):
        if self.rect_top.right < 0:
            self.kill()       
def display_score(score):
    
    score_surface = test_font.render(str(score), False, "#ccffff")
    score_surface_rect = score_surface.get_rect(center=(150, 100))
    display_screen.blit(score_surface, score_surface_rect)
def collision_sprite():

    
    for pipe in pipe_group:
        if bird.rect.colliderect(pipe.rect_bottom) or bird.rect.colliderect(pipe.rect_top):
            return False
       
    if bird.rect.y>=500:
        return False
    
    return True
def highscore(score):
    with open ("highscore.txt") as e:
        a=int(e.read())
        
        int(score)
        if a>=score:
            return a
        else:
            with open ("highscore.txt","w") as e:
                e.write(str(score))
            return score
display_screen = pygame.display.set_mode((289, 511))
gameoverscreen = pygame.image.load("gallery/sprites/gameover.png").convert()
background = pygame.image.load("gallery/sprites/background.png").convert()
score = 0
game_active = True
change_height = False
bird = Bird()
bird_group = pygame.sprite.GroupSingle(bird)
pipe=Pipe()
pipe_group=pygame.sprite.Group(pipe)
test_font = pygame.font.Font("font/Pixel.ttf", 50)
test_font_2 = pygame.font.Font("font/Pixel.ttf", 25)
pygame.display.set_caption("FlappyBird")
pygame.display.set_icon(bird.image)
clock = pygame.time.Clock()
while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_w or event.key==pygame.K_UP:
                    bird.velocity= -8
            if not game_active:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_active = True
                    
                    score = 0
                    bird.rect.center = (50, 250)
                    pipe.reset()
                    bird.velocity = 0


        if game_active:
            bird.update_0()
            display_screen.blit(background, (0, 0))
            bird_group.draw(display_screen)
            display_screen.blit(pipe.image_bottom, pipe.rect_bottom)
            display_screen.blit(pipe.image_top, pipe.rect_top)
            pipe.update()
            display_score(score)
            game_active=collision_sprite()
            clock.tick(60)
            pygame.display.update()
        else:
            display_screen.blit(gameoverscreen,(0,0))
            end_score=test_font_2.render(f"Score:{score}",False,"#ccffff")
            end_score_rect=end_score.get_rect(center=(150,250))
            highscoree=test_font_2.render(f"Highscore:{highscore(score)}",False,"#ccffff")
            highscoree_rect=highscoree.get_rect(center=(150,300))
            display_screen.blit(end_score,end_score_rect)
            display_screen.blit(highscoree,highscoree_rect)
            pygame.display.update()
            

