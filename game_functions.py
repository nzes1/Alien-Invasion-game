import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


#A function to manage keydown events

def check_keydown_events(event, game_settings, screen, ship, bullets):
    """ Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        #Move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        #Move the ship to the left
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        #Create a new bullet and add it to the bullets group
        if len(bullets) < game_settings.bullets_allowed:
            new_bullet = Bullet(game_settings, screen, ship)
            bullets.add(new_bullet)
    elif event.key == pygame.K_q:
        #Quit when Q is pressed
        sys.exit()
    
#A function to manage keyup events
def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
        
def check_events(game_settings, screen, stats, scoreboard, play_button, ship, aliens,
    bullets):
    """ Respond to keypresses and mouse events """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(game_settings, screen, stats, scoreboard, play_button, ship,
                aliens,bullets, mouse_x, mouse_y)
            
        elif event.type == pygame.KEYDOWN:
            #Call the check_keydown_events function
            check_keydown_events(event, game_settings, screen, ship, bullets)
          
        elif event.type == pygame.KEYUP:
            #Call the check_keyup_events function
            check_keyup_events(event, ship)
                
def check_play_button(game_settings, screen, stats, scoreboard, play_button, ship, aliens, 
        bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks play. """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #Reset the game settings
        game_settings.initialize_dynamic_settings()
        
        #Hide the mouse cursor
        pygame.mouse.set_visible(False)
        #Reset the game statistics
        stats.reset_stats()
        stats.game_active = True
        
        #Reset the scoreboard images
        scoreboard.prepare_score()
        scoreboard.prepare_high_score()
        scoreboard.prepare_level()
        scoreboard.prepare_ships()
        
        #Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        
        #Create a new fleet and center the ship
        create_fleet(game_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(game_settings, screen, stats, scoreboard, ship, aliens, bullets, play_button):
    """update images on the screen and flip to new screen """
    screen.fill(game_settings.bg_color)
    
    #Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
        
    ship.blitimage()
    aliens.draw(screen)
    
    #Draw the score information
    scoreboard.show_score()
    
    #Draw the play button if the game is inactive
    if not stats.game_active:   #Will only execute when game_active is False
        play_button.draw_button()
    
    #make the most recently screen drawn visible
    pygame.display.flip()
    
def update_bullets(game_settings, screen, stats, scoreboard, ship, aliens, bullets):
    """Update the bullets position and get rid of old bullets """
    #Update bullet position
    bullets.update()
        
    #Get rid of old bullets that have dissappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            
    check_bullet_alien_collisions(game_settings, screen, stats, scoreboard, ship, aliens, bullets)
        
def check_bullet_alien_collisions(game_settings, screen, stats, scoreboard, ship,
        aliens, bullets):
    """Respond to bullet-alien collisions. """
    #Remove any aliens and bullets that have collided
   
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += game_settings.alien_points * len(aliens)
            scoreboard.prepare_score()
        
        check_high_score(stats, scoreboard)
        
    if len(aliens) == 0:
        #Destroy existing bullets, speed up game and create a new fleet
        #If the entire fleet is destroyed, start a new level
        bullets.empty()
        game_settings.increase_speed()
        
        #Increase level
        stats.level += 1
        scoreboard.prepare_level()
        
        create_fleet(game_settings, screen, ship, aliens)
    
        
def get_number_aliens_x(game_settings, alien_width):
    """Determine the number of aliens that fit in a row """
    available_space_x = game_settings.screen_Width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width  ))
    return number_aliens_x
             
def create_alien(game_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row """
    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + (2 * alien.rect.height * row_number)
    aliens.add(alien)
    
def create_fleet(game_settings, screen, ship, aliens):
    """Create a full fleet of aliens """ 
    #Create an alien and find the number of aliens in a row
    #Spacing betwen each alien is equal to one alien width
    alien = Alien(game_settings, screen)
    number_aliens_x = get_number_aliens_x(game_settings, alien.rect.width)
    number_rows = get_number_rows(game_settings, ship.rect.height, alien.rect.height)
  
    #Create the fleet of aliens
    for row_number in range (number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(game_settings, screen, aliens, alien_number, row_number)
            

def get_number_rows(game_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen """
    available_space_y = (game_settings.screen_height - (3 *  alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def check_fleet_edges(game_settings, aliens):
    """Respond appropriately if any aiens have reached the edges. """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_settings, aliens)
            break
        
def change_fleet_direction(game_settings, aliens):
    """Drop the entire fleet and change the fleet's direction """
    for alien in aliens.sprites():
        alien.rect.y += game_settings.fleet_drop_speed
        
    game_settings.fleet_direction *= -1
     
def ship_hit(game_settings, stats, scoreboard, screen, ship, aliens, bullets):
    """Respond to a ship being hit by an alien """
    if stats.ships_left > 0:
        #Decreament the number of ships left
        stats.ships_left -= 1
        
        #Update Scoreboard
        scoreboard.prepare_ships()
        
        #Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        
        #Create a new fleet and center the ship
        create_fleet(game_settings, screen, ship, aliens)
        ship.center_ship()
        
        #Pause the game for a moment
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(game_settings, stats, scoreboard, screen, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #Treate this the same as if the ship got hit
            ship_hit(game_settings, stats, scoreboard, screen, ship, aliens, bullets)
            break  
        
def update_aliens(game_settings, stats,scoreboard, screen, ship, aliens, bullets):
    """Check if the fleet is at an edge, 
        and then update the positions of all aliens in the fleet 
     """
    check_fleet_edges(game_settings, aliens)
    aliens.update()
    
    #Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_settings, stats, scoreboard, screen, ship, aliens, bullets)
        
    #Look for aliens hitting the bottom of the screen
    check_aliens_bottom(game_settings, stats, scoreboard, screen, ship, aliens, bullets)

def check_high_score(stats, scoreboard):
    """Check to see if ther is a new high score. """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prepare_high_score()
