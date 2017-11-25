# Starter code for an adventure type game.
# University of Utah, David Johnson, 2017.
# This code, or code derived from this code, may not be shared without permission.

import sys, pygame, math

# Define some words to act as a key into a dictionary of character-related data. I could
# use "image" as a key, but sometimes it is nice to avoid "".
CASTLE = 0
RECT = 1
POSITION = 2
VISIBLE = 3
PHRASE = 4

# This function loads a series of sprite images stored in a folder with a
# consistent naming pattern: sprite_# or sprite_##. It returns a list of the images.
def load_piskell_sprite(sprite_folder_name, number_of_frames):
    frame_counts = []
    padding = math.ceil(math.log(number_of_frames-1,10))
    for frame in range(number_of_frames):
        folder_and_file_name = sprite_folder_name + "/sprite_" + str(frame).rjust(padding,'0') +".png"
        frame_counts.append(pygame.image.load(folder_and_file_name).convert_alpha())
                             
    return frame_counts

# This loads known images that correspond to tile types. It then puts those tiles
# in a dictionary with the minimap pixel color as a key - those key colors are also
# preset. A more general function would take a list of color, filename tuples and
# make the dictionary, but then calling the function would be as long as this function.
def load_tiles_and_make_dict_and_rect():
    # Load the tiles
    BOTTOM_LEFT_CORNER = pygame.image.load("CASTLE.BOTTOM_LEFT_CORNER.png").convert_alpha() # (206, 206, 46, 255)
    tile_rect = sand.get_rect()
    BOTTOM_STRAIGHT_CORNER = pygame.image.load("CASTLE.BOTTOM_RIGHT_CORNER.png").convert_alpha() # (126, 206, 46, 255)
    BOTTOM_STRAIGHT = pygame.image.load("CASTLE.BOTTOM_STRAIGHT.png").convert_alpha() # (14,64,14,255)
    CENTER = pygame.image.load("CASTLE.CENTER.png").convert_alpha() # (117,94,21,255)
    LEFT_DOOR = pygame.image.load("CASTLE.LEFT_DOOR.png").convert_alpha() # (0, 176, 255, 255)
    LEFT_STRAIGHT = pygame.image.load("CASTLE.LEFT_STRAIGHT.png").convert_alpha()# (39, 39, 21, 255)
    RIGHT_DOOR = pygame.image.load("CASTLE.RIGHT_DOOR.png").convert_alpha()
    RIGHT_STRAIGHT = pygame.image.load("CASTLE.RIGHT_STRAIGHT.png").convert_alpha()
    RIGHT_WINDOW_CLOSE = pygame.image.load("CASTLE.RIGHT_WINDOW_CLOSE.png").convert_alpha()
    RIGHT_WINDOW_OPEN = pygame.image.load("CASTLE.RIGHT_WINDOW_OPEN.png").convert_alpha()
    TOP_LEFT_CORNER = pygame.image.load("CASTLE.TOP_LEFT_CORNER.png").convert_alpha()
    TOP_RIGHT_CORNER = pygame.image.load("CASTLE.TOP_RIGHT_CORNER.png").convert_alpha()
    TOP_STRAIGHT = pygame.image.load("CASTLE.TOP_STRAIGHT.png").convert_alpha()

    # Make a dictionary of the tiles for easy access
    tiles = {}
    tiles[(206, 206, 46, 255)] = sand
    tiles[(126, 206, 46, 255)] = plains
    tiles[(39, 39, 21, 255)] = rocks
    tiles[(0, 176, 255, 255)] = water
    tiles[(117,94,21,255)] = dirt
    tiles[(14,64,14,255)] = swamp

    return (tiles, tile_rect)

# Clamp the value parameter to be on the range from min_allowed to max_allowed.
# The clamped value is returned, while the original value is not changed.
def clamp(min_allowed, value, max_allowed):
    return max(min_allowed, min(value, max_allowed))


# Check for overlap between non-transparent pixels in sprite and the pixels in image that are
# in the rectangle and a certain color.
def pixel_collision( sprite, sprite_rect, image, color):
    # Figure out where the upper-left corner of the sprite_rect is
    x_offset, y_offset = sprite_rect.topleft
    for row_pos in range(sprite.get_height()):
        for col_pos in range(sprite.get_width()):
            if sprite.get_at((col_pos, row_pos))[3] > 0 and image.get_at((col_pos+x_offset,row_pos+y_offset)) == color:
                return True
    return False

# Take an x,y pos on the map and return a (x_index, y_index) tuple that says which pixel index they would be over
def map_position_to_minimap_index( pos, tile_size ):
    return (int(pos[0]/tile_size), int(pos[1]/tile_size))

# Simple way of getting some character phrases on the screen. The go away when the frame count is higher than
# the phrase's count. say_phrases is a list of the form [("phrase", cutoff_frame_count)]
def render_phrases( say_phrases, frame_count, screen, myfont):
    phrase_position = screen.get_height() - 80
    for index in range(len(say_phrases)):
        if say_phrases[index][1] > frame_count:
            label = myfont.render(say_phrases[index][0], True, (255,255,0))
            screen.blit(label, (screen.get_width()//2 - 100, phrase_position))
            phrase_position += 20

# The main loop handles most of the game    
def main():

    # Initialize pygame                                 
    pygame.init()

    # The map tile width/height specifies how big the window is in tiles
    map_tile_width = 150 # we get to decide - it is not based on the map size
    map_tile_height = 150
    tile_size = 3 # the dimensions of the tile in pixels
    screen_size = width, height = (map_tile_width*tile_size, map_tile_height*tile_size)
    screen = pygame.display.set_mode(screen_size)

    # When we have moved across a portion of a tile, an extra tile is visible
    # on the edge. Always draw an extra tile to fill in the space.
    map_tile_width += 3
    map_tile_height += 3
    
    # Get a font
    myfont = pygame.font.SysFont("monospace", 24)

    # create the hero character
    # We treat the hero differently than all the other sprite characters as it doesn't move
    hero = load_piskell_sprite("./Catto",2)
    hero_rect = hero[0].get_rect()
    # Place the hero at the center of the screen
    hero_rect.center = (width/2, height/2)

    # Put all the characters in a dictionary so we can pass to functions easily
    character_data = {}
    # add in a king
    king_image = pygame.image.load("king/sprite_king0.png").convert_alpha()
    king_rect = king_image.get_rect()
    king_pos = (1700,1200)
    # This is our standard character data - it is a dictionary of
    # an {IMAGE, RECT, POSITION, VISIBLE, optional PHRASE}. The ALL CAPS keys are defined at
    # the top of this file. They are really numbers. Words make more sense to read but I get
    # frustrated having to put quotes around the words. So the variables act as the word and the
    # value in the variable acts as the key.
    king = {IMAGE:king_image, RECT:king_rect, POSITION:king_pos, VISIBLE:True, PHRASE:"NOooooo!"}
    # Add the king list to the character dictionary.    
    character_data["king"] = king

    # add in a treasure item
    rope_image = pygame.image.load("merchant/sprite_merchant0.png").convert_alpha()
    # Note that we can add characters to the character dictionary without making a lot of variables
    character_data["rope"] = {IMAGE:rope_image, RECT:rope_image.get_rect(), POSITION:(1000, 500), VISIBLE:False, PHRASE:"Use this rope wisely!"}

    # Add a place to hold screen phrases
    say_phrases = []
    
    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # Counts how many times the game loop has repeated. Used to animate sprites
    frame_count = 0;

    # variable to show if we are still playing the game
    playing = True

    # variable to show which way I am moving
    is_facing_right = True # False means left

    # capture king variable
    game_state = {}
    
    # Need to set all state variables here so that they are in the dictionary
    game_state["got king"] = False

    # Load the minimap that defines the world.
    world = pygame.image.load("images/testMap2.png").convert_alpha()
    world_rect = world.get_rect()

    # Define where the hero is positioned on the big map
    screen_x, screen_y = (1200,1200)

    # Get the tiles that define different terrain types
    tiles, tile_rect = load_tiles_and_make_dict_and_rect()

    # Loop while the player is still active
    while playing:
        # start the next frame
        screen.fill((100,120,120)) # If we see this color, something is wrong with the tiles
        
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False

        # Set the speed of the hero, which is the speed the screen corner moves.
        speed = 15

        # Allow continuous motion on a held-down key
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            is_facing_right = False
            screen_x += -speed
        if keys[pygame.K_RIGHT]:
            is_facing_right = True
            screen_x += speed
        if keys[pygame.K_UP]:
            screen_y += -speed
        if keys[pygame.K_DOWN]:
            screen_y += speed

        # Clamp the screen offsets to allowable values
        screen_x = clamp(0, screen_x, ((world.get_width() - 1) - (map_tile_width - 1)) * tile_size + tile_size-1)
        screen_y = clamp(0, screen_y, ((world.get_height() - 1) - (map_tile_height - 1)) * tile_size + tile_size-1)

        # scale down from position on the big map to pixel on the minimap
        minimap_offset_x, minimap_offset_y =  map_position_to_minimap_index( (screen_x, screen_y), tile_size)
        
        # Draw the map
        for y in range(0,map_tile_height):
            # offset y
            y_index = y + minimap_offset_y
            for x in range(0, map_tile_width):
                # offset x
                x_index = x + minimap_offset_x
                pixelColor = world.get_at((x_index,y_index))
                # The tile is draw at the pixel location scaled up, then shifted by the partial tile amount.
                tile_rect.topleft = (-(screen_x%tile_size) + x * tile_size, -(screen_y%tile_size) + y * tile_size)
                # Colors in pygame are not really tuples but we can force it to be a tuple.
                # Draw the tile that corresponds to the pixel color we found.
                screen.blit(tiles[tuple(pixelColor)], tile_rect)

        # Draw items. They move with the map.

        # The king moves across the map by adding 1 to the x coordinate. Since POSITION is a tuple, we
        # cannot modify just the x coordinate, we need to rebuild the tuple.
        character_data["king"][POSITION] = (character_data["king"][POSITION][0] + 1, character_data["king"][POSITION][1])
        # The king rectangle has to be shifted from the big map to the screen by offsetting by the screen corner.
        # This shifted rectangle is also how the hero might interact with the king since we care about
        # where they are on screen relative to each other.
        character_data["king"][RECT].center = (character_data["king"][POSITION][0] - screen_x, character_data["king"][POSITION][1] - screen_y)
        if character_data["king"][VISIBLE]:
            screen.blit(character_data["king"][IMAGE], character_data["king"][RECT])

        # interact with king
        if character_data["king"][VISIBLE] and hero_rect.colliderect(character_data["king"][RECT]):
            character_data["king"][VISIBLE] = False;
            say_phrases.append((character_data["king"][PHRASE], frame_count + 150))
            game_state["got king"] = True # Not really used in the starter code
            
        # The hero stays in the center of the screen
        hero_sprite = hero[frame_count%len(hero)]
        if is_facing_right:
            hero_sprite = pygame.transform.flip(hero_sprite, True, False)
        screen.blit(hero_sprite, hero_rect)

        fps = clock.get_fps()
        # Render text to the screen
        label = myfont.render("FPS:" + str(int(fps)), True, (255,255,0))
        screen.blit(label, (20,20))
        
        render_phrases(say_phrases, frame_count, screen, myfont)

        # Bring drawn changes to the front
        pygame.display.update()

        frame_count += 1

        # 60 fps
        clock.tick(60)

    # loop is over    
    pygame.quit()
    sys.exit()




# Start the program
main()
