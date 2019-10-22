import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet """
    def __init__(self, game_Settings, screen):
        """Initialize the alien ad set its starting position """
        super(Alien, self).__init__()
        self.screen = screen
        self.game_settings = game_Settings
        
        #Load the alien image and set its rect attribute
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()
        
        #Start each new alien near the top left corner of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #Store the aliens exact position
        self.x = float(self.rect.x)
        
    def blit_image(self):
        """Draw the alien at its current location """
        self.screen.blit(self.image, self.rect)
        
    def check_edges(self):
        """Return true if alien is at the edge of screen, either right or left. """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        
    def update(self):
        """Move the alien to the right or left """
        self.x += (self.game_settings.alien_speed_factor
                   *self.game_settings.fleet_direction)     
        #The fleet direction value is either 1(for moving right) or 
        # -1(for moving left) 
        self.rect.x = self.x