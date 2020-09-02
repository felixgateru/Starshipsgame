import pygame
from gameobjects import Starship, Meteor
REFRESH_RATE = 30
FRAME_WIDTH = 600
FRAME_HEIGHT = 400
BACKGROUND = (0,0,0)
INITIAL_NUMBER_OF_METEORS = 8
MAX_NUMBER_Of_CYCLES = 1000
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
        self.starship.draw()
        self.meteors = [Meteor(self) for _ in range(0, INITIAL_NUMBER_OF_METEORS)]

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
        

    
    def play(self):
        is_running = True
        starship_collided = False
        count = 0


        while is_running  and not starship_collided:
            count +=1

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
            
            if count%NEW_MOTOR_CYCLE_INTERVAL == 0:
                self.meteors.append(Meteor(self))

            for meteor in self.meteors:
                meteor.move_down()

            self.display_surface.fill(BACKGROUND)

            self.starship.draw()
            for i in self.meteors:
                i.draw()

            if self._check_for_collision():
                print("collision!")
            
            if count == MAX_NUMBER_Of_CYCLES:
                print("winner")
                break
                

            pygame.display.update()
            self.clock.tick(REFRESH_RATE)
        
        pygame.quit()



        


