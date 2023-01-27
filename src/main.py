import pygame
import os
from pygame import mixer
import time
from src.gameobjects import Starship, Meteor, Bullet
REFRESH_RATE = 30
FRAME_WIDTH = 600
FRAME_HEIGHT = 400
BACKGROUND = (0,0,0)
INITIAL_NUMBER_OF_METEORS = 8
MAX_NUMBER_Of_CYCLES = 100000
NEW_MOTOR_CYCLE_INTERVAL = 100

class Game:
    def __init__(self):
        print("Initialising the game:")
        pygame.init()

        print("Initialising the display:")
        self.display_surface = pygame.display.set_mode((FRAME_WIDTH,FRAME_HEIGHT))
        pygame.display.set_caption("StarShips GO!")
        self.clock = pygame.time.Clock()
        self.starship = Starship(self)
        self.bullets = []
        self.score = 0 
        self.starship.draw()
        self.meteors = [Meteor(self) for _ in range(0, INITIAL_NUMBER_OF_METEORS)]
        self.meteor_count = len(self.meteors)
        mixer.music.load(os.path.join("resources","background.mp3"))
        mixer.music.play(-1)
        self.bullet_sound = mixer.Sound(os.path.join("resources","laser.wav"))
    def _check_for_collision(self):
        """ Checks to see if any of the meteors have collided with the starship """
        result = False
        for meteor in self.meteors:
            if self.starship.rect().colliderect(meteor.rect()):
                result = True
                break
        return result

    def _pause(self):
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = False
                        break
        
                        
    def _display_message(self, message):
        text_font = pygame.font.Font("freesansbold.ttf",18)
        text_surface = text_font.render(message,True, (0,0,255),(255,255,255))
        text_rectangle = text_surface.get_rect()
        text_rectangle.center=(FRAME_WIDTH/2, FRAME_HEIGHT/2)
        paused = True
        while paused:
            self.display_surface.blit(text_surface, text_rectangle)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = False
                        break
        
        
        self.display_surface.blit(text_surface, text_rectangle)
            
    
    def _display_score(self, score):
        text_font = pygame.font.Font("freesansbold.ttf",24)
        text = "Score:"+ score 
        text_surface = text_font.render(text,True, (0,0,255),(0,0,0))
        text_rectangle = text_surface.get_rect()
        text_rectangle.center=(FRAME_WIDTH-text_rectangle.width/2, text_rectangle.height/2 + 5)
        
        self.display_surface.blit(text_surface, text_rectangle)

    
    def play(self):
        is_running = True
        starship_collided = False
        count = 0
        chances =0


        while is_running  and not starship_collided:
            count += 1
            
            



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Received exit event", event)
                    print("Exiting the game",'.'*23)
                    is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        print("Received exit event", event)
                        print("Exiting the game",'.'*23)
                        is_running  = False
                    elif event.key == pygame.K_UP:
                        print(U"Up up up")
                        self.starship.move_up()
                    elif event.key == pygame.K_DOWN:
                        self.starship.move_down()
                    elif event.key == pygame.K_RIGHT:
                        self.starship.move_right()
                    elif event.key == pygame.K_LEFT:
                        self.starship.move_left()
                    elif event.key == pygame.K_SPACE:
                        self._pause()
                    elif event.key == pygame.K_s:
                        self.bullet = Bullet(self)
                        
                        self.bullet_sound.play()
                        self.bullet.x = self.starship.x - 5 + self.starship.width/2 
                        self.bullet.y = self.starship.y + self.starship.height/2
                        self.bullets.append(self.bullet)
            
            while len(self.meteors) < self.meteor_count:
                x = Meteor(self)
                self.meteors.append(x)

            if count%NEW_MOTOR_CYCLE_INTERVAL == 0:
                self.meteors.append(Meteor(self))
                self.meteor_count = len(self.meteors)
                self.score += 10

            for meteor in self.meteors:
                meteor.move_down()

            self.display_surface.fill(BACKGROUND)

            self.starship.draw()
            for i in self.meteors:
                i.draw()
            
            for i in self.bullets:
                i.move_up()
                i.draw()
            
            for meteor in self.meteors:
                for bullet in self.bullets:
                    if meteor.rect().colliderect(bullet.rect()):
                        self.meteors.remove(meteor)
                        self.bullets.remove(bullet)
                        self.score += 20 
            if self._check_for_collision():
                explosion_sound= mixer.Sound("resources\explosion.wav")
                explosion_sound.play()
                if chances == 0:
                    self.meteors.clear()
                    self._display_message("You have 2 chances.Press space  to continue:")
                    
                                     
                elif chances == 1:
                    self._display_message("You have 1 more chance. Press space to continue:")
                    
                    self.meteors.clear()

                elif chances == 2:
                    self._display_message("Game over.")
                    
                    self._display_message("Your Score:"+str(self.score))
                    
                    is_running = False
                
                chances +=1

            self._display_score(str(self.score))
            
            if count == MAX_NUMBER_Of_CYCLES:
                print("winner")
                self._display_message("You win")
                break
                

            pygame.display.update()
            self.clock.tick(REFRESH_RATE)
        
        pygame.quit()



        


