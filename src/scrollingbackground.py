import os
import pygame


class ScrollingBackGround:
    def __init__(self, screenHeight) -> None:
        self.img = pygame.image.load(os.path.join("resources","space-1.jpg"))
        self.coord = [0,0]
        self.coord2 = [0,-screenHeight]
        self.y_original = self.coord[1]
        self.y2_original = self.coord2[1]
    
    def show(self, surface) -> None:
        surface.blit(self.img, self.coord)
        surface.blit(self.img, self.coord2)
    
    def updateCoords(self,speed_y, time):
        distance_y = speed_y * time
        self.coord[1] += distance_y
        self.coord2[1] += distance_y

        if self.coord2[1] >= 0:
            self.coord[1] = self.y_original
            self.coord2[1] = self.y2_original
