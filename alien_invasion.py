
import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import Game_stats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as g_functions

def run_game():
    #initialize the pygame, settings and a screen object
    pygame.init()

    # creating a screen object
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.screen_Width, game_settings.screen_height))
    pygame.display.set_caption("ALIEN INVASION")
    
    #Make the play button.
    play_button = Button(game_settings, screen, "PLAY")
    
    #Create an instance to store game statistics and create a scoreboard
    stats = Game_stats(game_settings)
    scoreboard = Scoreboard(game_settings, screen, stats)
    
    #Make a ship by using an instance of the Ship class, a group of bullets and a group of aliens
    ship = Ship(game_settings, screen)
    bullets = Group()
    aliens = Group()
    
    #Create the fleet of aliens
    g_functions.create_fleet(game_settings, screen, ship, aliens)

    #start the main loop for the game
    while True:
        g_functions.check_events(game_settings, screen, stats, scoreboard, play_button, ship,
            aliens, bullets)
        
        if stats.game_active:
            #update ship's position before updating the screen
            ship.update()
            g_functions.update_bullets(game_settings, screen, stats, scoreboard, ship, aliens, bullets)
            g_functions.update_aliens(game_settings, stats, scoreboard, screen, ship, aliens, bullets)
        g_functions.update_screen(game_settings, screen, stats, scoreboard, ship, aliens, bullets,
            play_button)
        
        
#calling the function
run_game()
