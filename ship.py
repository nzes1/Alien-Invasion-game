import pygame
from pygame.sprite import Sprite



class Ship(Sprite):
    """the ship class to modify the players ship"""
    def __init__(self, game_settings, screen):
        """initialize the ship and set its starting position"""
        super(Ship,self).__init__()
        self.screen = screen
        self.game_settings = game_settings
        
        #load the ship image and get its rectangle
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        #start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx # X-cordinate of the ship's center
        self.rect.bottom = self.screen_rect.bottom # y-cordinate of the ship's bottom
        
        #Store a decimal value for the ship's center
        self.center = float(self.rect.centerx)
        
        #Ship movement flags
        self.moving_right = False
        self.moving_left = False
        
    def update(self):
        """Update the ship's position based on the movement flag."""
        #update the ship's center value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.game_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0: # Prevent the ship from moving past the left edge of the screen
            self.center -= self.game_settings.ship_speed_factor
            
        #Update rect value/object from sef.center
        self.rect.centerx = self.center
        
    def blitimage(self):
        """Draw  the ship at its current location """
        self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        """Center the ship on the screen. """
        self.center = self.screen_rect.centerx
    