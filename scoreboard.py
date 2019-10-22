import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """A class to report scoring information. """
    
    def __init__(self, game_settings, screen, stats):
        """Initialize scorekeeping attributes. """
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.game_settings = game_settings
        self.stats = stats
        
        #Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont('None', 30)
        
        #Prepare the initial score images
        self.prepare_score()
        self.prepare_high_score()
        self.prepare_level()
        self.prepare_ships()
        
    def prepare_score(self):
        """Turn the score to a rendered image"""
        rounded_score = int(round(self.stats.score, -1))
        score_string = "Score: " + "{:,}".format(rounded_score)
        
        self.score_image = self.font.render(score_string, True, self.text_color,
            self.game_settings.bg_color)
        
        #Display the score on the top right corner of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
    def prepare_high_score(self):
        """Turn the high score to a rendered image. """
        high_score = int(round(self.stats.high_score, -1))
        high_score_string = "High Score:"  +"{:,}".format(high_score)
        
        self.high_score_image = self.font.render(high_score_string, True, self.text_color,
            self.game_settings.bg_color)
        
        #center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prepare_level(self):
        """Turn the level to a rendered image. """
        level_image_string = "Level: " +str(self.stats.level)
        self.level_image = self.font.render(level_image_string, True,
            self.text_color, self.game_settings.bg_color)
        
        #Position the level below score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
        
    def prepare_ships(self):
        """Show how many ships are left. """
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.game_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
        
    def show_score(self):
        """ Draw scores and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        
        #Draw ships
        self.ships.draw(self.screen)
        
    