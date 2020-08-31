import pygame
from gameobjects import Starship, Meteor
REFRESH_RATE = 30
FRAME_WIDTH = 600
FRAME_HEIGHT = 400
BACKGROUND = (125,0,125)
INITIAL_NUMBER_OF_METEORS = 8

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

    
    def play(self):
        is_running = True

        while is_running:
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
                    
                    self.display_surface.fill(BACKGROUND)

                    self.starship.draw()
                    for i in self.meteors:
                        i.draw()
                    
                
            
            
            
            
            pygame.display.update()
            self.clock.tick(REFRESH_RATE)
        
        pygame.quit()
        


