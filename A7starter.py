
#Isabella Ruiz + Jai 
# Starter code for an adventure type game.
# University of Utah, David Johnson, 2017.
# This code, or code derived from this code, may not be shared without permission.

import sys, pygame, math

# Define some words to act as a key into a dictionary of character-related data. I could
# use "image" as a key, but sometimes it is nice to avoid "".
IMAGE = 0
RECT = 1
POSITION = 2
VISIBLE = 3
PHRASE = 4

def bounce_rect_between_two_positions( rect, start_pos, end_pos, num_frame, frame_count ):
    if frame_count%num_frame < num_frame/2:
        new_pos_x = start_pos[0] + (end_pos[0] - start_pos[0]) * (frame_count%(num_frame/2))/(num_frame/2)
        new_pos_y = start_pos[1] + (end_pos[1] - start_pos[1]) * (frame_count%(num_frame/2))/(num_frame/2)
    else:
        new_pos_x = end_pos[0] + (start_pos[0] - end_pos[0]) * (frame_count%(num_frame/2))/(num_frame/2)
        new_pos_y = end_pos[1] + (start_pos[1] - end_pos[1]) * (frame_count%(num_frame/2))/(num_frame/2)

    rect.center = (new_pos_x, new_pos_y)

 
# Draw characters
def draw_characters( character_dict, screen, screen_x, screen_y, frame_count):
    # The mouser moves across the map by adding 1 to the x coordinate. Since POSITION is a tuple, we
    # cannot modify just the x coordinate, we need to rebuild the tuple.
#       character_data["mouser"][POSITION] = (character_data["mouser"][POSITION][0] + 1, character_data["mouser"][POSITION][1])
    # The mouser rectangle has to be shifted from the big map to the screen by offsetting by the screen corner.
    # This shifted rectangle is also how the catto might interact with the mouser since we care about
    # where they are on screen relative to each other.

    for dic in list(character_dict.values()):
        dic[RECT].center = (dic[POSITION][0] - screen_x, dic[POSITION][1] - screen_y)
        sprite = dic[IMAGE][frame_count%len(dic[IMAGE])]
        if dic[VISIBLE]:
            screen.blit(sprite, dic[RECT])    

def can_catto_move(x, y, world, tile_size):
    screen_coord = [x, y]
    mini_coordinates = map_position_to_minimap_index(screen_coord,tile_size)
    color = world.get_at((mini_coordinates[0],mini_coordinates[1]))
    if color == (127, 127, 127, 255) or color == (93, 93, 93, 255) or color == (159, 157, 157, 255):
        return False
    else:
        return True

def door_work(x, y, world, tile_size):
    screen_coord = [x, y]
    mini_coordinates = map_position_to_minimap_index(screen_coord,tile_size)
    color = world.get_at((mini_coordinates[0],mini_coordinates[1]))
    if color == (103, 85, 55, 255) or color == (65, 45, 11, 255):
        return False
    else:
        return True



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

# So ur proffessor makes no sense and I would never make a game this way but pretty much
# the minimap is a guide for the code to draw tiles. So if the upper right hand pixel is blue,
# you can assign blue to a certain tile. That way, when the code reads the mini map, when it reads
# blue, it writes the tile you assoisiated with blue. Ya'll have to make a mini map that corrisponds
# to the map you want. So bottom left hand corner will be purple for example, and centers can be blue or
# somthin, idk.
def load_tiles_and_make_dict_and_rect():
    # Load the tiles
    DARK_WALL = pygame.image.load("images/DARK_WALL.png").convert_alpha() # (206, 206, 46, 255)
    tile_rect = DARK_WALL.get_rect()
    LIGHT_WALL = pygame.image.load("images/LIGHT_WALL.png").convert_alpha() # (126, 206, 46, 255)
    CARPET = pygame.image.load("images/CARPET.png").convert_alpha() # (14,64,14,255)
    RIGHT_DOOR = pygame.image.load("images/RIGHT_DOOR.png").convert_alpha() # (117,94,21,255)
    LEFT_DOOR = pygame.image.load("images/LEFT_DOOR.png").convert_alpha() # (117,94,21,255)
    DARK_GRASS = pygame.image.load("images/DARK_GRASS.png").convert_alpha() # (0, 176, 255, 255)
    LIGHT_GRASS = pygame.image.load("images/LIGHT_GRASS.png").convert_alpha() # (0, 176, 255, 255)
    RIGHT_WINDOW_CLOSED = pygame.image.load("images/RIGHT_WINDOW_CLOSED.png").convert_alpha() # (39, 39, 21, 255)
    LEFT_WINDOW_CLOSED = pygame.image.load("images/LEFT_WINDOW_CLOSED.png").convert_alpha() # (39, 39, 21, 255)
    RIGHT_WINDOW_OPEN = pygame.image.load("images/RIGHT_WINDOW_OPEN.png").convert_alpha() # (39, 39, 21, 255)
    LEFT_WINDOW_OPEN = pygame.image.load("images/LEFT_WINDOW_OPEN.png").convert_alpha() # (39, 39, 21, 255)
    WATER = pygame.image.load("images/WATER.png").convert_alpha() # (39, 39, 21, 255)
    DOOR_HANDLE = pygame.image.load("images/DOOR_HANDLE.png").convert_alpha() # (39, 39, 21, 255)
    OPEN = pygame.image.load("images/OPEN.png").convert_alpha()
    THING = pygame.image.load("images/THING.png").convert_alpha()
    THING2 = pygame.image.load("images/THING2.png").convert_alpha()
    WHITE = pygame.image.load("images/WHITE.png").convert_alpha()
    BLUE = pygame.image.load("images/BLUE.png").convert_alpha()

    # The previous entries are associated with the minmap that came with this file. When you make ur
    # own minimap you have to reassign these colors.


    # Make a dictionary of the tiles for easy access
    tiles = {}
    tiles[(93, 93, 93, 255)] = DARK_WALL
    tiles[(159, 157, 157, 255)] = LIGHT_WALL
    tiles[(25, 44, 155, 255)] = CARPET
    tiles[(125, 79, 0, 255)] = RIGHT_DOOR
    tiles[(148, 102, 23, 255)] = LEFT_DOOR
    tiles[(22, 90, 17, 255)] = DARK_GRASS
    tiles[(11, 113, 3, 255)] = LIGHT_GRASS
    tiles[(153, 217, 334, 255)] = WATER
    tiles[(103, 85, 55, 255)] = RIGHT_WINDOW_CLOSED
    tiles[(65, 45, 11, 255)] = LEFT_WINDOW_CLOSED
    tiles[(103, 85, 55, 255)] = RIGHT_WINDOW_OPEN
    tiles[(65, 45, 11, 255)] = LEFT_WINDOW_OPEN
    tiles[(166, 154,  48, 255)] = DOOR_HANDLE
    tiles[(52, 52,  52, 255)] = OPEN
    tiles[(24, 44,  150, 255)] = THING
    tiles[(127, 127, 127, 255)] = THING2
    tiles[(255, 255, 255, 255)] = WHITE
    tiles[(0, 162,  232, 255)] = BLUE

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

#speed from terrain
def speed_from_terrain(catto_rect, world, screen_x, screen_y, tile_size):
    screen_coord = [screen_x, screen_y]
    mini_coordinates = map_position_to_minimap_index(screen_coord,tile_size)
    color = world.get_at((mini_coordinates[0],mini_coordinates[1]))
    print(mini_coordinates)
    #print(color)

    if color == (25, 44, 155, 255) or color == (24, 44,  150, 255):
        return 150
    else:
        return 30

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
    map_tile_width = 30 # we get to decide - it is not based on the map size
    map_tile_height = 20
    tile_size = 32 # the dimensions of the tile in pixels
    screen_size = width, height = (map_tile_width*tile_size, map_tile_height*tile_size)
    screen = pygame.display.set_mode(screen_size)

    # When we have moved across a portion of a tile, an extra tile is visible
    # on the edge. Always draw an extra tile to fill in the space.
    map_tile_width += 3
    map_tile_height += 3
    
    
    # Get a font
    myfont = pygame.font.SysFont("monospace", 24)

    # create the catto character
    # We treat the catto differently than all the other sprite characters as it doesn't move
    catto = load_piskell_sprite("images/Catto",2)
    catto_rect = catto[0].get_rect()
    # Place the catto at the center of the screen
    catto_rect.center = (width/2, height/2)

    # Put all the characters in a dictionary so we can pass to functions easily
    character_data = {}
    
    # add in a mouser character
    mouser_image1 = load_piskell_sprite("images/mouser",2)
    mouser_rect1 = mouser_image1[0].get_rect()
    mouser_pos1 = (9000,3400)
    mouser1 = {IMAGE:mouser_image1, RECT:mouser_rect1, POSITION:mouser_pos1, VISIBLE:True, PHRASE:"I KILLE YOU"}  
    character_data["mouser1"] = mouser1

    mouser_image2 = load_piskell_sprite("images/mouser",2)
    mouser_rect2 = mouser_image2[0].get_rect()
    mouser_pos2 = (10800,4200)
    mouser2 = {IMAGE:mouser_image2, RECT:mouser_rect2, POSITION:mouser_pos2, VISIBLE:True, PHRASE:"I KILLE YOU"}  
    character_data["mouser2"] = mouser2

    mouser_image3 = load_piskell_sprite("images/mouser",2)
    mouser_rect3 = mouser_image3[0].get_rect()
    mouser_pos3 = (10800,3400)
    mouser3 = {IMAGE:mouser_image3, RECT:mouser_rect3, POSITION:mouser_pos3, VISIBLE:True, PHRASE:"I KILLE YOU"}  
    character_data["mouser3"] = mouser3

    mouser_image4 = load_piskell_sprite("images/mouser",2)
    mouser_rect4 = mouser_image4[0].get_rect()
    mouser_pos4 = (10000,2800)
    mouser4= {IMAGE:mouser_image4, RECT:mouser_rect4, POSITION:mouser_pos4, VISIBLE:True, PHRASE:"I KILLE YOU"}  
    character_data["mouser4"] = mouser4


    mouser_image5 = load_piskell_sprite("images/mouser",2)
    mouser_rect5 = mouser_image5[0].get_rect()
    mouser_pos5 = (10000,4500)
    mouser5 = {IMAGE:mouser_image5, RECT:mouser_rect5, POSITION:mouser_pos5, VISIBLE:True, PHRASE:"I KILLE YOU"}  
    character_data["mouser5"] = mouser5

    mouser_image6 = load_piskell_sprite("images/mouser",2)
    mouser_rect6 = mouser_image6[0].get_rect()
    mouser_pos6 = (10000,3700)
    mouser6 = {IMAGE:mouser_image6, RECT:mouser_rect6, POSITION:mouser_pos6, VISIBLE:True, PHRASE:"I KILLE YOU"}  
    character_data["mouser6"] = mouser6

    mouser_image7 = load_piskell_sprite("images/mouser",2)
    mouser_rect7 = mouser_image7[0].get_rect()
    mouser_pos7 = (9000,4500)
    mouser7 = {IMAGE:mouser_image7, RECT:mouser_rect7, POSITION:mouser_pos7, VISIBLE:True, PHRASE:"I KILLE YOU"}  
    character_data["mouser7"] = mouser7

    mouser_image8 = load_piskell_sprite("images/mouser",2)
    mouser_rect8 = mouser_image8[0].get_rect()
    mouser_pos8 = (6000,3400)
    mouser8 = {IMAGE:mouser_image8, RECT:mouser_rect8, POSITION:mouser_pos8, VISIBLE:True, PHRASE:"I KILLE YOU"}  
    character_data["mouser8"] = mouser8

    mouser_image9 = load_piskell_sprite("images/mouser",2)
    mouser_rect9 = mouser_image9[0].get_rect()
    mouser_pos9 = (7000,3900)
    mouser9 = {IMAGE:mouser_image9, RECT:mouser_rect9, POSITION:mouser_pos9, VISIBLE:True, PHRASE:"I KILLE YOU"}  
    character_data["mouser9"] = mouser9

    mouser_image10 = load_piskell_sprite("images/mouser",2)
    mouser_rect10 = mouser_image10[0].get_rect()
    mouser_pos10 = (8000,4420)
    mouser10 = {IMAGE:mouser_image10, RECT:mouser_rect10, POSITION:mouser_pos10, VISIBLE:True, PHRASE:"I KILLE YOU"}  
    character_data["mouser10"] = mouser10

    mouser_image11 = load_piskell_sprite("images/mouser",2)
    mouser_rect11 = mouser_image11[0].get_rect()
    mouser_pos11 = (8000,4000)
    mouser11 = {IMAGE:mouser_image11, RECT:mouser_rect11, POSITION:mouser_pos11, VISIBLE:True, PHRASE:"I KILLE YOU"}  
    character_data["mouser11"] = mouser11

    mouser_image12 = load_piskell_sprite("images/mouser",2)
    mouser_rect12 = mouser_image12[0].get_rect()
    mouser_pos12 = (7000,3000)
    mouser12 = {IMAGE:mouser_image12, RECT:mouser_rect12, POSITION:mouser_pos12, VISIBLE:True, PHRASE:"I KILLE YOU"}  
    character_data["mouser12"] = mouser12

    mouser_image13 = load_piskell_sprite("images/mouser",2)
    mouser_rect13 = mouser_image13[0].get_rect()
    mouser_pos13 = (7000, 4700)
    mouser13 = {IMAGE:mouser_image13, RECT:mouser_rect13, POSITION:mouser_pos13, VISIBLE:True, PHRASE:"I KILLE YOU"}  
    character_data["mouser13"] = mouser13
    
    # add in a crown item
    crown_image = load_piskell_sprite("images/crown",2)
    # Note that we can add characters to the character dictionary without making a lot of variables
    character_data["crown"] = {IMAGE:crown_image, RECT:crown_image[0].get_rect(), POSITION:(3900, 3800), VISIBLE:True, PHRASE:"STOP THIEF"}

    king_image = load_piskell_sprite("images/king",2)
    # Note that we can add characters to the character dictionary without making a lot of variables
    character_data["king"] = {IMAGE:king_image, RECT:king_image[0].get_rect(), POSITION:(5295,3210), VISIBLE:False, PHRASE:"FUCK! BLUB BLURB *DEATH*"}

    merchant_image = load_piskell_sprite("images/merchant",2)
    # Note that we can add characters to the character dictionary without making a lot of variables
    character_data["merchant"] = {IMAGE:merchant_image, RECT:merchant_image[0].get_rect(), POSITION:(11450, 1620), VISIBLE:True, PHRASE:"Good Luck with the Rope, nonsuspisous cat!"}


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

    # capture mouser variable
    game_state = {}
    
    # Need to set all state variables here so that they are in the dictionary
    game_state["got merchant"] = False
    game_state["got king"] = False
    game_state["got crown"] = False
    

    # Load the minimap that defines the world.
    world = pygame.image.load("images/testMap2.png").convert_alpha()
    world_rect = world.get_rect()
    world2 = pygame.image.load("images/testMap1.png").convert_alpha()
    world2_rect = world2.get_rect()
    gameover = pygame.image.load("images/GAME_OVER.png").convert_alpha()
    gamover_rect = gameover.get_rect()

    # Define where the catto is positioned on the big map
    screen_x, screen_y = (11895,1720)

    # Get the tiles that define different terrain types
    tiles, tile_rect = load_tiles_and_make_dict_and_rect()

    Level = world

    #character Import
    mouse = load_piskell_sprite("images/mouser", 2)
    mouse_rect = mouse[0].get_rect()
   
    # Loop while the player is still active
    while playing:
        # start the next frame
        screen.fill((100,120,120)) # If we see this color, something is wrong with the tiles
        
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False



        # Clamp the screen offsets to allowable values
        screen_x = clamp(0, screen_x, ((world.get_width() - 1) - (map_tile_width - 1)) * tile_size + tile_size-1)
        screen_y = clamp(0, screen_y, ((world.get_height() - 1) - (map_tile_height - 1)) * tile_size + tile_size-1)

        print(screen_x)
        print(screen_y)

        x = screen_x + catto_rect.center[0]
        y = screen_y + catto_rect.center[1]

        #speed terrain
        speed = speed_from_terrain(catto_rect, world, x, y, tile_size)

        #Door Function


        # Allow continuous motion on a held-down key
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            is_facing_right = False
            if game_state["got merchant"] == True:
                if can_catto_move(x - 20, y, world, tile_size):
                    screen_x += -speed
            else:
                if can_catto_move(x - 20, y, world, tile_size) and door_work(x - 20, y, world, tile_size):
                    screen_x += -speed
        if keys[pygame.K_RIGHT]:
            is_facing_right = True
            if game_state["got merchant"] == True:
                if can_catto_move(x + 20, y, world, tile_size):
                    screen_x += speed
            else:
                if can_catto_move(x + 20, y, world, tile_size) and door_work(x + 20, y, world, tile_size):
                    screen_x += speed  
        if keys[pygame.K_UP]:
            if game_state["got merchant"] == True:
                if can_catto_move(x, y - 20, world, tile_size):
                    screen_y += -speed
            else:
                if can_catto_move(x, y - 20, world, tile_size) and door_work(x, y - 20, world, tile_size):
                    screen_y += -speed
        if keys[pygame.K_DOWN]:
            if game_state["got merchant"] == True:
                if can_catto_move(x, y + 20, world, tile_size):
                    screen_y += speed
            else:
                if can_catto_move(x, y + 20, world, tile_size) and door_work(x, y + 20, world, tile_size):
                    screen_y += speed


        # scale down from position on the big map to pixel on the minimap
        minimap_offset_x, minimap_offset_y =  map_position_to_minimap_index( (screen_x, screen_y), tile_size)
                # Draw the map
        for y in range(0,map_tile_height-1):
            # offset y
            y_index = y + minimap_offset_y
            for x in range(0, map_tile_width-1):
                # offset x
                x_index = x + minimap_offset_x
                pixelColor = Level.get_at((x_index,y_index))
                # The tile is draw at the pixel location scaled up, then shifted by the partial tile amount.
                tile_rect.topleft = (-(screen_x%tile_size) + x * tile_size, -(screen_y%tile_size) + y * tile_size)
                # Colors in pygame are not really tuples but we can force it to be a tuple.
                # Draw the tile that corresponds to the pixel color we found.
                screen.blit(tiles[tuple(pixelColor)], tile_rect)

        # Draw items. They move with the map.
        draw_characters(character_data, screen, screen_x, screen_y, frame_count)

        King_dead = False
        # Character interacting with enviornment
        if game_state["got crown"] == True:
            character_data["king"][VISIBLE] = True
            
        # interact with mouser
        if character_data["mouser1"][VISIBLE] and catto_rect.colliderect(character_data["mouser1"][RECT]):
            playing = False;
        if character_data["mouser2"][VISIBLE] and catto_rect.colliderect(character_data["mouser2"][RECT]):
            playing = False;
        if character_data["mouser3"][VISIBLE] and catto_rect.colliderect(character_data["mouser3"][RECT]):
            playing = False;
        if character_data["mouser4"][VISIBLE] and catto_rect.colliderect(character_data["mouser4"][RECT]):
            playing = False;
        if character_data["mouser5"][VISIBLE] and catto_rect.colliderect(character_data["mouser5"][RECT]):
            playing = False;
        if character_data["mouser6"][VISIBLE] and catto_rect.colliderect(character_data["mouser6"][RECT]):
            playing = False;
        if character_data["mouser7"][VISIBLE] and catto_rect.colliderect(character_data["mouser7"][RECT]):
            playing = False;
        if character_data["mouser8"][VISIBLE] and catto_rect.colliderect(character_data["mouser8"][RECT]):
            playing = False;
        if character_data["mouser9"][VISIBLE] and catto_rect.colliderect(character_data["mouser9"][RECT]):
            playing = False;
        if character_data["mouser10"][VISIBLE] and catto_rect.colliderect(character_data["mouser10"][RECT]):
            playing = False;
        if character_data["mouser11"][VISIBLE] and catto_rect.colliderect(character_data["mouser11"][RECT]):
            playing = False;
        if character_data["mouser12"][VISIBLE] and catto_rect.colliderect(character_data["mouser12"][RECT]):
            playing = False;
        if character_data["mouser13"][VISIBLE] and catto_rect.colliderect(character_data["mouser13"][RECT]):
            playing = False;
            
        if character_data["merchant"][VISIBLE] and catto_rect.colliderect(character_data["merchant"][RECT]): 
            character_data ["merchant"][VISIBLE] = False;
            say_phrases.append((character_data['merchant'][PHRASE], frame_count + 150))
            game_state["got merchant"] = True
        if character_data["king"][VISIBLE] and catto_rect.colliderect(character_data["king"][RECT]): 
            character_data ["king"][VISIBLE] = False;
            break
            King_dead = True
            say_phrases.append((character_data['king'][PHRASE], frame_count + 150))
            game_state["got king"] = True
        if character_data["crown"][VISIBLE] and catto_rect.colliderect(character_data["crown"][RECT]): 
            character_data ["crown"][VISIBLE] = False;
            say_phrases.append((character_data['crown'][PHRASE], frame_count + 150))
            game_state["got crown"] = True

        #FIght me
        if character_data["king"][VISIBLE] == False and King_dead == True:
            print(gameover)
        
        # The catto stays in the center of the screen
        catto_sprite = catto[frame_count%len(catto)]
        if is_facing_right:
            catto_sprite = pygame.transform.flip(catto_sprite, True, False)
        screen.blit(catto_sprite, catto_rect)

        fps = clock.get_fps()
        # Render text to the screen
        label = myfont.render("FPS:" + str(int(fps)), True, (255,255,0))
        screen.blit(label, (20,20))
        
        render_phrases(say_phrases, frame_count, screen, myfont)

        # Bring drawn changes to the front
        pygame.display.update()

        frame_count += 1

        # 60 fps
        clock.tick(30)

    # loop is over    
    pygame.quit()
    sys.exit()




# Start the program
main()
