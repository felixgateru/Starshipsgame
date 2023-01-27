import pygame
import os
from pygame import mixer
from src.gameobjects import Starship, Meteor, Bullet
from src.scrollingbackground import ScrollingBackGround
from src.menu import *


class Game:
    def __init__(self):
        print("Initialising the game:")
        pygame.init()
        self.refresh_rate = 30
        self.frame_width = 600
        self.frame_height = 400
        self.black_colour = (0, 0, 0)
        self.white_colour = (255, 255, 255)
        self.background_speed = 200
        self.initial_no_meteors = 8
        self.max_cycles = 100000
        self.new_meteor_cyle_interval = 100
        self.background_Object = ScrollingBackGround(self.frame_height+60)
        self.background_time = pygame.time.Clock().tick(self.refresh_rate)/2500.0
        print("Initialising the display:")
        self.game_surface = pygame.Surface(
            (self.frame_width, self.frame_height))
        self.display_surface = pygame.display.set_mode(
            (self.frame_width, self.frame_height))
        pygame.mouse.set_visible(0)
        pygame.display.set_caption("StarShips GO!")
        self.clock = pygame.time.Clock()
        self.starship = Starship(self)
        self.bullets = []
        self.score = 0
        self.starship.draw()
        self.meteors = [Meteor(self)
                        for _ in range(0, self.initial_no_meteors)]
        self.meteor_count = len(self.meteors)
        mixer.music.load(os.path.join("resources", "background.mp3"))
        mixer.music.play(-1)
        self.bullet_sound = mixer.Sound(os.path.join("resources", "laser.wav"))
        self.running = True
        self.playing = False
        self.font_name = pygame.font.get_default_font()
        self.START_KEY = False
        self.BACK_KEY = False
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

    def reset_keys(self):
        self.BACK_KEY, self.START_KEY, self.UP_KEY, self.DOWN_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.white_colour)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.game_surface.blit(text_surface, text_rect)

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
        text_font = pygame.font.Font("freesansbold.ttf", 18)
        text_surface = text_font.render(
            message, True, (0, 0, 255), self.white_colour)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (self.frame_width/2, self.frame_height/2)
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
        text_font = pygame.font.Font("freesansbold.ttf", 24)
        text = "Score:" + score
        text_surface = text_font.render(text, True, (255, 255, 255), (0, 0, 0))
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (
            self.frame_width-text_rectangle.width/2, text_rectangle.height/2 + 5)

        self.display_surface.blit(text_surface, text_rectangle)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Received exit event", event)
                print("Exiting the game", '.'*23)
                self.running = False
                self.playing = False
                self.curr_menu.run_display = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print("Received exit event", event)
                    print("Exiting the game", '.'*23)
                    self.running = False
                    self.playing = False
                elif event.key == pygame.K_UP:
                    self.starship.move_up()
                elif event.key == pygame.K_DOWN:
                    self.starship.move_down()
                elif event.key == pygame.K_RIGHT:
                    self.starship.move_right()
                elif event.key == pygame.K_LEFT:
                    self.starship.move_left()
                elif event.key == pygame.K_w:
                    self.UP_KEY = True
                elif event.key == pygame.K_s:
                    self.DOWN_KEY = True
                elif event.key == pygame.K_RETURN:
                    self.START_KEY = True
                elif event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                elif event.key == pygame.K_p:
                    self._pause()
                elif event.key == pygame.K_SPACE:
                    self.bullet = Bullet(self)
                    self.bullet_sound.play()
                    self.bullet.x = self.starship.x - 5 + self.starship.width/2
                    self.bullet.y = self.starship.y + self.starship.height/2
                    self.bullets.append(self.bullet)

    def gameplay(self):
        # self.playing = True
        starship_collided = False
        count = 0
        chances = 0

        while self.playing:  # and not starship_collided:
            count += 1
            self.background_Object.updateCoords(
                self.background_speed, self.background_time)
            self.check_events()
            while len(self.meteors) < self.meteor_count:
                x = Meteor(self)
                self.meteors.append(x)

            if count % self.new_meteor_cyle_interval == 0:
                self.meteors.append(Meteor(self))
                self.meteor_count = len(self.meteors)
                self.score += 10

            for meteor in self.meteors:
                meteor.move_down()

            self.background_Object.show(self.display_surface)

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
                explosion_sound = mixer.Sound(
                    os.path.join("resources", "explosion.wav"))
                explosion_sound.play()
                if chances == 0:
                    self.meteors.clear()
                    self._display_message(
                        "You have 2 chances.Press space  to continue:")

                elif chances == 1:
                    self._display_message(
                        "You have 1 more chance. Press space to continue:")

                    self.meteors.clear()

                elif chances == 2:
                    self._display_message("Game over.")

                    self._display_message("Your Score:"+str(self.score))

                    self.playing = False
                    self.runnng =False

                chances += 1

            self._display_score(str(self.score))

            if count == self.max_cycles:
                print("winner")
                self._display_message("You win")
                break

            pygame.display.update()
            self.reset_keys()
            self.clock.tick(self.refresh_rate)

       # pygame.quit()
        print("The game has ended")
        print("The game has ended")
