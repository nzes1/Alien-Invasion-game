
class Settings():
    """A class to store all settings for the game """
    
    def __init__(self):
        """Intialize the game's static settings """
        #Screen Settings
        self.screen_Width = 1080
        self.screen_height = 650
        self.bg_color = (230,230,230)
        
        #Ship settings
        self.ship_limit = 3
        
        #Bullet Settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 3
        
        #Alien settings
        self.fleet_drop_speed = 10
        
        #How quickly the game  speeds up
        self.speedup_scale = 1.1
        
        #How quickly the alien point value increases
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game. """
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 5
        self.alien_speed_factor = 1
        
        #Fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
        
        #Scoring
        self.alien_points = 50
        
    def increase_speed(self):
        """Increase speed settings and alien point values. """
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
        