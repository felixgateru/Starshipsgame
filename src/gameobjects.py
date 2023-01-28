import pygame, random, os

FRAME_WIDTH = 600
FRAME_HEIGHT = 400
STARSHIP_SPEED = 20
INITIAL_METEOR_POSITION = 10
MAX_METEOR_SPEED = 5
class GameObject:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = None
        self.width = 0
        self.height = 0

    def load_image(self, filename):
        self.image = pygame.image.load(filename).convert()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    
    def rect(self):
        """Generates a rectangle indicating the objects dimensions and location"""
        return pygame.Rect(self.x, self.y, self.width,self.height)
    
    def draw(self):
        """ draw the game object at the
            current x, y coordinates """
        self.game.display_surface.blit(self.image, (self.x, self.y))

    

class Starship(GameObject):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.x = FRAME_WIDTH/2
        self.y =FRAME_HEIGHT-60
        self.load_image("resources\starship.png") 
    
    def move_right(self):
        self.x =self.x + STARSHIP_SPEED
        if self.x +self.width > FRAME_WIDTH:
            self.x = FRAME_WIDTH - self.width
        
    
    def move_left(self):
        self.x = self.x - STARSHIP_SPEED
        if self.x < 0:
            self.x = 0
        
    
    def move_up(self):
        self.y = self.y - STARSHIP_SPEED
        if self.y < (FRAME_HEIGHT*0.75):
            self.y = FRAME_HEIGHT *0.75
        
    
    def move_down(self):
        self.y = self.y + STARSHIP_SPEED
        if self.y + self.height > FRAME_HEIGHT:
            self.y = FRAME_HEIGHT - self.height
        
    
    def __str__(self):
        return(f'Starship, {self.x}, {self.y}')


class Meteor(GameObject):
    def __init__(self,game):
        super().__init__()
        self.game = game
        self.r1= random.randint(0,FRAME_WIDTH/4)
        self.r2 = random.randint(FRAME_WIDTH/4 , FRAME_WIDTH/2)
        self.r3 = random.randint(FRAME_WIDTH/2, FRAME_WIDTH*0.75)
        self.r4 = random.randint(FRAME_WIDTH*0.75, FRAME_WIDTH)
        self.x = random.choice([self.r1,self.r2,self.r3,self.r4])
        self.y = INITIAL_METEOR_POSITION
        self.speed = random.randint(1, MAX_METEOR_SPEED)
        self.load_image(os.path.join("resources","meteor.png"))
    
    def move_down(self):
        self.y = self.y + self.speed
        if self.y > FRAME_HEIGHT:
            self.y = INITIAL_METEOR_POSITION
            self.r1= random.randint(0,FRAME_WIDTH/4)
            self.r2 = random.randint(FRAME_WIDTH/4 , FRAME_WIDTH/2)
            self.r3 = random.randint(FRAME_WIDTH/2, FRAME_WIDTH*0.75)
            self.r4 = random.randint(FRAME_WIDTH*0.75, FRAME_WIDTH)
            self.x = random.choice([self.r1,self.r2,self.r3,self.r4])
    
    def __str__(self):
        return(f"Meteor , {self.x}, {self.y}")


class Bullet(GameObject):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.x = 0
        self.y =0
        self.load_image(os.path.join("resources","laser.png"))
        self.speed = 10
    
    def move_up(self):
        self.y = self.y - self.speed
        if self.y < 0:
            self.game.bullets.pop(-1)

