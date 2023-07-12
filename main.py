import pygame
from db import *
from ressources import *

# Initialize Pygame
pygame.init()

# Window dimensions
width = 400
height = 600

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
SPECIAL_BLUE = (28, 76, 189)
DARK_BLUE = (10, 40, 95)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
GREY2 = (105, 105, 105)
GREY3 = (32, 32, 32)

# Create the window
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("PokéGuess")
pygame.display.set_icon(game_icon)

# Random pokemon generation
pokemon = info_pokemon()

# Hint on the random pokemon
hint = [f"Ce pokémon est de type {pokemon[2]}",
        f"Ce pokémon mesure {pokemon[4]} m et fait {pokemon[3]} kg", f"Ce pokémon peut utiliser {pokemon[5]}", f"C'était {pokemon[0]}  !"]
pokemon_evolution_statut = True
if pokemon[1] == None:
    hint_evolution = "Ce pokémon n'a pas d'évolution ou a atteint "
    pokemon_evolution_statut = False
else:
    hint_evolution = f"Ce pokémon évolue en {pokemon[1]}"

# Load the font
start_game_font = pygame.font.Font("fonts/pokemon_classic.ttf", 16)
hint_font = pygame.font.Font("fonts/pokemon_classic.ttf", 10)
reminder_font = pygame.font.Font("fonts/pokemon_classic.ttf", 14)
input_text_font = pygame.font.Font("fonts/pokemon_classic.ttf", 12)
pokemon_name_font = pygame.font.Font("fonts/pokemon_classic.ttf", 12)
player_name_font = pygame.font.Font("fonts/pokemon_classic.ttf", 12)            
result_state_font = pygame.font.Font("fonts/pokemon_classic.ttf", 22)
autocompletion_font = pygame.font.Font("fonts/pokemon_classic.ttf", 12)
game_title_font = pygame.font.Font("fonts/pokemon_classic.ttf", 36)

# Game state display
victory_text = result_state_font.render("Victoire !", True, BLACK)
defeat_text = result_state_font.render("Défaite !", True, BLACK)
victory_text_shadow = result_state_font.render("Victoire !", True, WHITE)
defeat_text_shadow = result_state_font.render("Défaite !", True, WHITE)

# Pokemon name display
pokemon_name_display = pokemon_name_font.render(pokemon[0], True, BLACK)

# Load the start background images
start_background = pygame.Surface((width, height))
start_background.blit(battle_background, (0, 0))

# Load the random pokemon image
pokemon_image = pygame.image.load(f"images/gen1_images/{pokemon[6]}.png")
pokemon_image_transform = pygame.transform.scale(pokemon_image, (200, 100))

# Positioning of the "Start Game" button
start_button_rect = pygame.Rect(100, 450, 200, 50)

# Constants
player_name = "Sasha"
victory = False
clock = pygame.time.Clock()

# Display game menu function
def display_start_menu():
    window.blit(main_background, (0, 0))
    text_pokeguess = game_title_font.render("PokéGuess", True, WHITE)
    text_pokeguess_shadow = game_title_font.render("PokéGuess", True, (SPECIAL_BLUE)) 
    text_pokeguess_rect = text_pokeguess.get_rect(center=(width/2, height/10))
    text_pokeguess_shadow_rect = text_pokeguess_rect.copy()
    text_pokeguess_shadow_rect.move_ip(5, 5)
    window.blit(text_pokeguess_shadow, text_pokeguess_shadow_rect)
    window.blit(text_pokeguess, text_pokeguess_rect)
    start_button_surface = pygame.Surface((200, 50), pygame.SRCALPHA)
    text_start_game = start_game_font.render("Press to start", True, BLACK)
    text_start_game_rect = text_start_game.get_rect(center=(100, 25))
    start_button_surface.blit(text_start_game, text_start_game_rect)
    window.blit(start_button_surface, (100, 450))
    start_song.play(loops=-1)

# Function that verifies the player's input
def verify(player_input):
    global victory
    if player_input.lower() == pokemon[0].lower():
        victory = True
        return True
    else:
        return False

# Game function
def game():
    game_state = True
    defeat = False
    text_display = ""
    reminder_list = ["Proposer un pokémon", "Veuillez proposer un pokémon !", "Ce n'est pas ce pokémon !"] # List with reminder string
    reminder = reminder_list[0]
    hint_statut = hint[0]
    hint_evolution_2 = "sa dernière évolution !"
    hint_statut_2 = ""
    text = ""
    input_window = True
    while input_window:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    k_text = text
                    text = ''

                    if verify(k_text): # Check if player's input is equal to the random pokemon
                        battle_song.stop()
                        victory_sound_effect.play()

                  
                    elif len(k_text) <= 0: # Check if the player has made a guess
                        reminder = reminder_list[1]

                    elif len(k_text) > 0:
                        if hint_statut == hint[0]: 
                            reminder = reminder_list[2] 
                            hint_statut = hint[2]  
                        elif hint_statut == hint[2]:
                            hint_statut = hint[1]
                        elif hint_statut == hint[1]:
                            hint_statut = hint_evolution

                            if pokemon_evolution_statut:
                                hint_statut_2 = ""
                            else : 
                                hint_statut_2 = hint_evolution_2
                        else :
                            defeat = True
                            battle_song.stop()
                            defeat_sound_effect.play()
                
                elif event.key == pygame.K_BACKSPACE: # Retrieve the player's inputs
                    text = text[:-1]
                else:
                    
                    if len(text) == 0: # Capitalize the player's input at the beginning
                        text += event.unicode.upper()
                    else:
                        text += event.unicode.lower()
                    
                    
                    auto_completion = get_autocomplete_results(text) # Store the fonction in the variable "auto_completion"
        window.blit(battle_background, (0, 0))

        
        # if len(text_display) < len(hint_statut):
        #     text_display = hint_statut[:len(text_display) + 1]

        # clock.tick(35) # Limit the refresh rate to 35 FPS

        # Text display (hint, reminder ...)
        hint_display = hint_font.render(hint_statut, True, WHITE)
        hint_display_shadow = hint_font.render(hint_statut,   True, GREY2)
        hint_display_2 = hint_font.render(hint_statut_2, True, WHITE)
        hint_display_2_shadow = hint_font.render(hint_statut_2, True, GREY2)
        window.blit(hint_display_shadow, (26, 201))
        window.blit(hint_display, (25, 200))
        window.blit(hint_display_2_shadow, (25+1, 220+1))
        window.blit(hint_display_2, (25, 220))
    
        hint_reminder = reminder_font.render(reminder, True, DARK_BLUE)
        hint_reminder_shadow = reminder_font.render(reminder, True, WHITE)
        text_width = hint_reminder.get_width()
        text_height = hint_reminder.get_height()
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        window.blit(hint_reminder_shadow, (x+2, y+2))
        window.blit(hint_reminder, (x, y))

         # Text display (pokemon name, player name ...)
        pokemon_name_q_mark = autocompletion_font.render("???", True, BLACK)
        pokemon_name_display_end = hint_font.render(hint[3], True, WHITE)
        pokemon_name_display_end_shadow = hint_font.render(hint[3], True, GREY2)
        window.blit(pokemon_name_q_mark, (45, 30))
        player_name_display = player_name_font.render(player_name, True, (0, 0, 0))
        window.blit(player_name_display, (245, 125))
        

        # Final game state display (=VICTORY)
        if victory:
            game_state = False 
            window.blit(battle_background, (0, 0))
            window.blit(pokemon_name_display, (40, 30))
            window.blit(pokemon_name_display_end_shadow, (25+1, 200+1))
            window.blit(pokemon_name_display_end, (25, 200))
            window.blit(victory_text_shadow, (width // 2 - victory_text.get_width() //
                        2 + 3, height // 1.6 - victory_text.get_height() // 2))
            window.blit(victory_text, (width // 2 - victory_text.get_width() //
                        2, height // 1.6 - victory_text.get_height() // 2))
            window.blit(pokemon_image_transform, (185, 10))
            window.blit(player_name_display, (245, 125))

        # Final game state display (=DEFEAT)
        if defeat:
            game_state = False 
            window.blit(battle_background, (0, 0))
            window.blit(pokemon_name_display, (40, 30))
            window.blit(pokemon_name_display_end_shadow, (25+1, 200+1))
            window.blit(pokemon_name_display_end, (25, 200))
            window.blit(defeat_text_shadow, (width // 2 - victory_text.get_width() //
                        2 + 3, height // 1.6 - victory_text.get_height() // 2))
            window.blit(defeat_text, (width // 2 - defeat_text.get_width() //
                        2, height // 1.6 - defeat_text.get_height() // 2))
            window.blit(pokemon_image_transform, (185, 10))
            window.blit(player_name_display, (245, 125))

        if text != "" and  game_state is True:  # Autocompletion function
            for i, pokemon in enumerate(auto_completion):
                text_autocompletion_shadow = autocompletion_font.render(
                    pokemon, True,  WHITE)
                text_autocompletion = autocompletion_font.render(
                    pokemon, True,  GREY)
                window.blit(text_autocompletion_shadow, (125, 325 + i * 18))
                window.blit(text_autocompletion, (125 + 1, 325 + i * 18 + 1))

        if game_state is True :
            input_text = input_text_font.render(text, True, BLACK) # Player input display
            input_text_ombre = input_text_font.render(text, True, WHITE)
        elif game_state is False :
            input_text = input_text_font.render("", True, BLACK) # Player input display
            input_text_ombre = input_text_font.render("", True, WHITE)


        window.blit(input_text_ombre, (125+1, 325+1))
        window.blit(input_text, (125, 325))
        pygame.display.update()

# Main function
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
             
                if start_button_rect.collidepoint(event.pos): # Retrieve the position of the mouse click
                    start_song.stop() 
                    click_sound_effect.play()
                    pygame.time.wait(1)
                    battle_song.play(loops=-1)
                    game() # Call the game function
        display_start_menu()
        pygame.display.flip()

main()
