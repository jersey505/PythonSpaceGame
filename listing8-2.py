import time, random, math

WIDTH = 800
HEIGHT = 800

PLAYER_NAME = "Player"
FRIEND1_NAME = "Friend 1"
FRIEND2_NAME = "Frind 2"
current_room = 31

top_left_x = 100
top_left_y = 150

DEMO_OBJECTS = [images.floor, images.pillar, images.soil]

LANDER_SECTOR = random.randint(1, 24)
LANDER_X = random.randint(2, 11)
LANDER_Y = random.randint(2, 11)

TILE_SIZE = 30

player_y, player_x = 2, 5
game_over = False

PLAYER = {
    "left": [images.spacesuit_left, images.spacesuit_left_1,
             images.spacesuit_left_2, images.spacesuit_left_3,
             images.spacesuit_left_4
             ],
    "right": [images.spacesuit_right, images.spacesuit_right_1,
              images.spacesuit_right_2, images.spacesuit_right_3,
              images.spacesuit_right_4
              ],
    "up": [images.spacesuit_back, images.spacesuit_back_1,
           images.spacesuit_back_2, images.spacesuit_back_3,
           images.spacesuit_back_4
           ],
    "down": [images.spacesuit_front, images.spacesuit_front_1,
             images.spacesuit_front_2, images.spacesuit_front_3,
             images.spacesuit_front_4
             ]
}

player_direction = "down"
player_frame = 0
player_image = PLAYER[player_direction][player_frame]
player_offset_x, player_offset_y = 0, 0

PLAYER_SHADOW = {
    "left": [images.spacesuit_left_shadow, images.spacesuit_left_1_shadow,
             images.spacesuit_left_2_shadow, images.spacesuit_left_3_shadow,
             images.spacesuit_left_4_shadow
             ],
    "right": [images.spacesuit_right_shadow, images.spacesuit_right_1_shadow,
              images.spacesuit_right_2_shadow,
              images.spacesuit_right_3_shadow, images.spacesuit_right_4_shadow
              ],
    "up": [images.spacesuit_back_shadow, images.spacesuit_back_1_shadow,
           images.spacesuit_back_2_shadow, images.spacesuit_back_3_shadow,
           images.spacesuit_back_4_shadow
           ],
    "down": [images.spacesuit_front_shadow, images.spacesuit_front_1_shadow,
             images.spacesuit_front_2_shadow, images.spacesuit_front_3_shadow,
             images.spacesuit_front_4_shadow
             ]
}

player_image_shadow = PLAYER_SHADOW["down"][0]

PILLARS = [
    images.pillar, images.pillar_95, images.pillar_80,
    images.pillar_60, images.pillar_50
]

wall_transparency_frame = 0

BLACK = (0, 0, 0)
BLUE = (0, 155, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (128, 0, 0)

MAP_WIDTH = 5
MAP_HEIGHT = 10
MAP_SIZE = MAP_WIDTH * MAP_HEIGHT

GAME_MAP = [["Room 0 - where unused objects are kept", 0, 0, False, False]]

outdoor_rooms = range(1, 26)
for planetsectors in range(1, 26):
    GAME_MAP.append(["The dusty planet surface", 13, 13, True, True])

GAME_MAP += [
    ["The airlock", 13, 5, True, False],
    ["The engineering lab", 13, 13, False, False],
    ["Poodle Mission Control", 9, 13, False, True],
    ["The viewing gallery", 9, 15, False, False],
    ["The crew's bathroom", 5, 5, False, False],
    ["The airlock entry bay", 7, 11, True, True],
    ["Left elbow room", 9, 7, True, False],
    ["Right elbow room", 7, 13, True, True],
    ["The science lab", 13, 13, False, True],
    ["The greenhouse", 13, 13, True, False],
    [PLAYER_NAME + "'s sleeping quarters", 9, 11, False, False],
    ["West corridor", 15, 5, True, True],
    ["The briefing room", 7, 13, False, True],
    ["The crew's community room", 11, 13, True, False],
    ["Main Mission Control", 14, 14, False, False],
    ["The sick bay", 12, 7, True, False],
    ["West corridor", 9, 7, True, False],
    ["Utilities control room", 9, 9, False, True],
    ["Systems engineering bay", 9, 11, False, False],
    ["Security portal to Mission Control", 7, 7, True, False],
    [FRIEND1_NAME + "'s sleeping quarters", 9, 11, True, True],
    [FRIEND2_NAME + "'s sleeping quarters", 9, 11, True, True],
    ["The pipeworks", 13, 11, True, False],
    ["The chief scientist's office", 9, 7, True, True],
    ["The robot workshop", 9, 11, True, False]
]


assert len(GAME_MAP) - 1 == MAP_SIZE, "Map size and GAME_MAP don't match"

objects = {
    0: [images.floor, None, "The floor is shiny and clean"],
    1: [images.pillar, images.full_shadow, "The wall is smooth and cold"],
    2: [images.soil, None, "It's like a desert. Or should that be dessert?"],
    3: [images.pillar_low, images.half_shadow, "The wall is smooth and cold"],
    4: [images.bed, images.half_shadow, "A tidy and comfortable bed"],
    5: [images.table, images.half_shadow, "It's made from strong plastic."],
    6: [images.chair_left, None, "A chair with a soft cushion"],
    7: [images.chair_right, None, "A chair with a soft cushion"],
    8: [images.bookcase_tall, images.full_shadow,
        "Bookshelves, stacked with reference books"],
    9: [images.bookcase_small, images.half_shadow,
        "Bookshelves, stacked with reference books"],
    10: [images.cabinet, images.half_shadow,
         "A small locker, for storing personal items"],
    11: [images.desk_computer, images.half_shadow,
         "A computer. Use it to run life support diagnostics"],
    12: [images.plant, images.plant_shadow, "A spaceberry plant, grown here"],
    13: [images.electrical1, images.half_shadow,
         "Electrical systems used for powering the space station"],
    14: [images.electrical2, images.half_shadow,
         "Electrical systems used for powering the space station"],
    15: [images.cactus, images.cactus_shadow, "Ouch! Careful on the cactus!"],
    16: [images.shrub, images.shrub_shadow,
         "A space lettuce. A bit limp, but amazing it's growing here!"],
    17: [images.pipes1, images.pipes1_shadow, "Water purification pipes"],
    18: [images.pipes2, images.pipes2_shadow,
         "Pipes for the life support systems"],
    19: [images.pipes3, images.pipes3_shadow,
         "Pipes for the life support systems"],
    20: [images.door, images.door_shadow, "Safety door. Opens automatically \
for astronauts in functioning spacesuits."],
    21: [images.door, images.door_shadow, "The airlock door. \
For safety reasons, it requires two person operation."],
    22: [images.door, images.door_shadow, "A locked door. It needs " \
         + PLAYER_NAME + "'s access card"],
    23: [images.door, images.door_shadow, "A locked door. It needs " \
         + FRIEND1_NAME + "'s access card"],
    24: [images.door, images.door_shadow, "A locked door. It needs " \
         + FRIEND2_NAME + "'s access card"],
    25: [images.door, images.door_shadow,
         "A locked door. It is opened from Main Mission Control"],
    26: [images.door, images.door_shadow,
         "A locked door in the engineering bay."],
    27: [images.map, images.full_shadow,
         "The screen says the crash site was Sector: " \
         + str(LANDER_SECTOR) + " // X: " + str(LANDER_X) + \
         " // Y: " + str(LANDER_Y)],
    28: [images.rock_large, images.rock_large_shadow,
         "A rock. Its coarse surface feels like a whetstone", "the rock"],
    29: [images.rock_small, images.rock_small_shadow,
         "A small but heavy piece of Martian rock"],
    30: [images.crater, None, "A crater in the planet surface"],
    31: [images.fence, None,
         "A fine gauze fence. It helps protect the station from dust storms"],
    32: [images.contraption, images.contraption_shadow,
         "One of the scientific experiments. It gently vibrates"],
    33: [images.robot_arm, images.robot_arm_shadow,
         "A robot arm, used for heavy lifting"],
    34: [images.toilet, images.half_shadow, "A sparkling clean toilet"],
    35: [images.sink, None, "A sink with running water", "the taps"],
    36: [images.globe, images.globe_shadow,
         "A giant globe of the planet. It gently glows from inside"],
    37: [images.science_lab_table, None,
         "A table of experiments, analyzing the planet soil and dust"],
    38: [images.vending_machine, images.full_shadow,
         "A vending machine. It requires a credit.", "the vending machine"],
    39: [images.floor_pad, None,
         "A pressure sensor to make sure nobody goes out alone."],
    40: [images.rescue_ship, images.rescue_ship_shadow, "A rescue ship!"],
    41: [images.mission_control_desk, images.mission_control_desk_shadow, \
         "Mission Control stations."],
    42: [images.button, images.button_shadow,
         "The button for opening the time-locked door in engineering."],
    43: [images.whiteboard, images.full_shadow,
         "The whiteboard is used in brainstorms and planning meetings."],
    44: [images.window, images.full_shadow,
         "The window provides a view out onto the planet surface."],
    45: [images.robot, images.robot_shadow, "A cleaning robot, turned off."],
    46: [images.robot2, images.robot2_shadow,
         "A planet surface exploration robot, awaiting set-up."],
    47: [images.rocket, images.rocket_shadow, "A one-person craft in repair"],
    48: [images.toxic_floor, None, "Toxic floor - do not walk on!"],
    49: [images.drone, None, "A delivery drone"],
    50: [images.energy_ball, None, "An energy ball - dangerous!"],
    51: [images.energy_ball2, None, "An energy ball - dangerous!"],
    52: [images.computer, images.computer_shadow,
         "A computer workstation, for managing space station systems."],
    53: [images.clipboard, None,
         "A clipboard. Someone has doodled on it.", "the clipboard"],
    54: [images.bubble_gum, None,
         "A piece of sticky bubble gum. Spaceberry flavour.", "bubble gum"],
    55: [images.yoyo, None, "A toy made of fine, strong string and plastic. \
Used for antigrav experiments.", PLAYER_NAME + "'s yoyo"],
    56: [images.thread, None,
         "A piece of fine, strong string", "a piece of string"],
    57: [images.needle, None,
         "A sharp needle from a cactus plant", "a cactus needle"],
    58: [images.threaded_needle, None,
         "A cactus needle, spearing a length of string", "needle and string"],
    59: [images.canister, None,
         "The air canister has a leak.", "a leaky air canister"],
    60: [images.canister, None,
         "It looks like the seal will hold!", "a sealed air canister"],
    61: [images.mirror, None,
         "The mirror throws a circle of light on the walls.", "a mirror"],
    62: [images.bin_empty, None,
         "A rarely used bin, made of light plastic", "a bin"],
    63: [images.bin_full, None,
         "A heavy bin full of water", "a bin full of water"],
    64: [images.rags, None,
         "An oily rag. Pick it up by one corner if you must!", "an oily rag"],
    65: [images.hammer, None,
         "A hammer. Maybe good for cracking things open...", "a hammer"],
    66: [images.spoon, None, "A large serving spoon", "a spoon"],
    67: [images.food_pouch, None,
         "A dehydrated food pouch. It needs water.", "a dry food pack"],
    68: [images.food, None,
         "A food pouch. Use it to get 100% energy.", "ready-to-eat food"],
    69: [images.book, None, "The book has the words 'Don't Panic' on the \
cover in large, friendly letters", "a book"],
    70: [images.mp3_player, None,
         "An MP3 player, with all the latest tunes", "an MP3 player"],
    71: [images.lander, None, "The Poodle, a small space exploration craft. \
Its black box has a radio sealed inside.", "the Poodle lander"],
    72: [images.radio, None, "A radio communications system, from the \
Poodle", "a communications radio"],
    73: [images.gps_module, None, "A GPS Module", "a GPS module"],
    74: [images.positioning_system, None, "Part of a positioning system. \
Needs a GPS module.", "a positioning interface"],
    75: [images.positioning_system, None,
         "A working positioning system", "a positioning computer"],
    76: [images.scissors, None, "Scissors. They're too blunt to cut \
anything. Can you sharpen them?", "blunt scissors"],
    77: [images.scissors, None,
         "Razor-sharp scissors. Careful!", "sharpened scissors"],
    78: [images.credit, None,
         "A small coin for the station's vending systems",
         "a station credit"],
    79: [images.access_card, None,
         "This access card belongs to " + PLAYER_NAME, "an access card"],
    80: [images.access_card, None,
         "This access card belongs to " + FRIEND1_NAME, "an access card"],
    81: [images.access_card, None,
         "This access card belongs to " + FRIEND2_NAME, "an access card"]
}

items_player_may_carry = list(range(53, 82))
items_player_may_stand_on = items_player_may_carry + [0, 39, 2, 48]

scenery = {
    26: [[39, 8, 2]],
    27: [[33, 5, 5], [33, 1, 1], [33, 1, 8], [47, 5, 2],
         [47, 3, 10], [47, 9, 8], [42, 1, 6]],
    28: [[27, 0, 3], [41, 4, 3], [41, 4, 7]],
    29: [[7, 2, 6], [6, 2, 8], [12, 1, 13], [44, 0, 1],
         [36, 4, 10], [10, 1, 1], [19, 4, 2], [17, 4, 4]],
    30: [[34, 1, 1], [35, 1, 3]],
    31: [[11, 1, 1], [19, 1, 8], [46, 1, 3]],
    32: [[48, 2, 2], [48, 2, 3], [48, 2, 4], [48, 3, 2], [48, 3, 3],
         [48, 3, 4], [48, 4, 2], [48, 4, 3], [48, 4, 4]],
    33: [[13, 1, 1], [13, 1, 3], [13, 1, 8], [13, 1, 10], [48, 2, 1],
         [48, 2, 7], [48, 3, 6], [48, 3, 3]],
    34: [[37, 2, 2], [32, 6, 7], [37, 10, 4], [28, 5, 3]],
    35: [[16, 2, 9], [16, 2, 2], [16, 3, 3], [16, 3, 8], [16, 8, 9], [16, 8, 2], [16, 1, 8],
         [16, 1, 3], [12, 8, 6], [12, 9, 4], [12, 9, 8],
         [15, 4, 6], [12, 7, 1], [12, 7, 11]],
    36: [[4, 3, 1], [9, 1, 7], [8, 1, 8], [8, 1, 9],
         [5, 5, 4], [6, 5, 7], [10, 1, 1], [12, 1, 2]],
    37: [[48, 3, 1], [48, 3, 2], [48, 7, 1], [48, 5, 2], [48, 5, 3],
         [48, 7, 2], [48, 9, 2], [48, 9, 3], [48, 11, 1], [48, 11, 2]],
    38: [[43, 0, 2], [6, 2, 2], [6, 3, 5], [6, 4, 7], [6, 2, 9], [45, 1, 10]],
    39: [[38, 1, 1], [7, 3, 4], [7, 6, 4], [5, 3, 6], [5, 6, 6],
         [6, 3, 9], [6, 6, 9], [45, 1, 11], [12, 1, 8], [12, 1, 4]],
    40: [[41, 5, 3], [41, 5, 7], [41, 9, 3], [41, 9, 7],
         [13, 1, 1], [13, 1, 3], [42, 1, 12]],
    41: [[4, 3, 1], [10, 3, 5], [4, 5, 1], [10, 5, 5], [4, 7, 1],
         [10, 7, 5], [12, 1, 1], [12, 1, 5]],
    44: [[46, 4, 3], [46, 4, 5], [18, 1, 1], [19, 1, 3],
         [19, 1, 5], [52, 4, 7], [14, 1, 8]],
    45: [[48, 2, 1], [48, 2, 2], [48, 3, 3], [48, 3, 4], [48, 1, 4], [48, 1, 1]],
    46: [[10, 1, 1], [4, 1, 2], [8, 1, 7], [9, 1, 8], [8, 1, 9], [5, 4, 3], [7, 3, 2]],
    47: [[9, 1, 1], [9, 1, 2], [10, 1, 3], [12, 1, 7], [5, 4, 4], [6, 4, 7], [4, 1, 8]],
    48: [[17, 4, 1], [17, 4, 2], [17, 4, 3], [17, 4, 4], [17, 4, 5], [17, 4, 6], [17, 4, 7],
         [17, 8, 1], [17, 8, 2], [17, 8, 3], [17, 8, 4],
         [17, 8, 5], [17, 8, 6], [17, 8, 7], [14, 1, 1]],
    49: [[14, 2, 2], [14, 2, 4], [7, 5, 1], [5, 5, 3], [48, 3, 3], [48, 3, 4]],
    50: [[45, 4, 8], [11, 1, 1], [13, 1, 8], [33, 2, 1], [46, 4, 6]]
}

checksum = 0
check_counter = 0
for key, room_scenery_list in scenery.items():
    for scenery_item_list in room_scenery_list:
        checksum += (scenery_item_list[0] * key
                     + scenery_item_list[1] * (key + 1)
                     + scenery_item_list[2] * (key + 2))
        check_counter += 1
print(check_counter, "scenery items")
assert check_counter == 161, "Expected 161 scenery items"
assert checksum == 200095, "Error in scenery data"
print("Scenery checksum: " + str(checksum))

for room in range(1, 26):
    if room != 13:
        scenery_item = random.choice([16, 28, 29, 30])
        scenery[room] = [[scenery_item, random.randint(2, 10),
                          random.randint(2, 10)]]


for room_coordinate in range(0, 13):
    for room_number in [1, 2, 3, 4, 5]:
        scenery[room_number] += [[31, 0, room_coordinate]]
    for room_number in [1, 6, 11, 16, 21]:
        scenery[room_number] += [[31, room_coordinate, 0]]
    for room_number in [5, 10, 15, 20, 25]:
        scenery[room_number] += [[31, room_coordinate, 12]]

del scenery[21][-1]
del scenery[25][-1]



def get_floor_type():
    if current_room in outdoor_rooms:
        return 2
    else:
        return 0


def generate_map():

    global room_map, room_width, room_height, room_name, hazard_map
    global top_left_x, top_left_y, wall_transparency_frame
    room_data = GAME_MAP[current_room]
    room_name = room_data[0]
    room_height = room_data[1]
    room_width = room_data[2]

    floor_type = get_floor_type()
    if current_room in range(1, 21):
        bottom_edge = 2
        side_edge = 2
    if current_room in range(21, 26):
        bottom_edge = 1
        side_edge = 2
    if current_room > 25:
        bottom_edge = 1
        side_edge = 1


    room_map = [[side_edge] * room_width]

    for y in range(room_height - 2):
        room_map.append([side_edge]
                        + [floor_type] * (room_width - 2) + [side_edge])

    room_map.append([bottom_edge] * room_width)

    # Add doorways.
    middle_row = int(room_height / 2)
    middle_column = int(room_width / 2)

    if room_data[4]:
        room_map[middle_row][room_width - 1] = floor_type
        room_map[middle_row + 1][room_width - 1] = floor_type
        room_map[middle_row - 1][room_width - 1] = floor_type

    if current_room % MAP_WIDTH != 1:
        room_to_left = GAME_MAP[current_room - 1]

        if room_to_left[4]:
            room_map[middle_row][0] = floor_type
            room_map[middle_row + 1][0] = floor_type
            room_map[middle_row - 1][0] = floor_type

    if room_data[3]:
        room_map[0][middle_column] = floor_type
        room_map[0][middle_column + 1] = floor_type
        room_map[0][middle_column - 1] = floor_type

    if current_room <= MAP_SIZE - MAP_WIDTH:
        room_below = GAME_MAP[current_room + MAP_WIDTH]

        if room_below[3]:
            room_map[room_height - 1][middle_column] = floor_type
            room_map[room_height - 1][middle_column + 1] = floor_type
            room_map[room_height - 1][middle_column - 1] = floor_type

    if current_room in scenery:
        for this_scenery in scenery[current_room]:
            scenery_number = this_scenery[0]
            scenery_y = this_scenery[1]
            scenery_x = this_scenery[2]
            room_map[scenery_y][scenery_x] = scenery_number

            image_here = objects[scenery_number][0]
            image_width = image_here.get_width()
            image_width_in_tiles = int(image_width / TILE_SIZE)

            for tile_number in range(1, image_width_in_tiles):
                room_map[scenery_y][scenery_x + tile_number] = 255

    center_y = int(HEIGHT / 2)
    center_x = int(WIDTH / 2)
    room_pixel_width = room_width * TILE_SIZE
    room_pixel_height = room_height * TILE_SIZE
    top_left_x = center_x - 0.5 * room_pixel_width
    top_left_y = (center_y - 0.5 * room_pixel_height) + 110




def game_loop():
    def start_room():
        show_text("You are in: " + room_name, 0)

    global player_x, player_y, current_room
    global from_player_x, from_player_y
    global player_image, player_image_shadow
    global selected_item, item_carrying, energy
    global player_offset_x, player_offset_y
    global player_frame, player_direction

    if game_over:
        return

    if player_frame > 0:
        player_frame += 1
        time.sleep(0.05)
        if player_frame == 5:
            player_frame = 0
            player_offset_x = 0
            player_offset_y = 0


    old_player_x = player_x
    old_player_y = player_y


    if player_frame == 0:
        if keyboard.d:
            from_player_x = player_x
            from_player_y = player_y
            player_x += 1
            player_direction = "right"
            player_frame = 1
        elif keyboard.a:
            from_player_x = player_x
            from_player_y = player_y
            player_x -= 1
            player_direction = "left"
            player_frame = 1
        elif keyboard.w:
            from_player_x = player_x
            from_player_y = player_y
            player_y -= 1
            player_direction = "up"
            player_frame = 1
        elif keyboard.s:
            from_player_x = player_x
            from_player_y = player_y
            player_y += 1
            player_direction = "down"
            player_frame = 1


    if player_x == room_width:
        current_room += 1
        generate_map()
        player_x = 0
        player_y = int(room_height / 2)
        player_frame = 0
        start_room()
        return

    if player_x == -1:
        current_room -= 1
        generate_map()
        player_x = room_width - 1
        player_y = int(room_height / 2)
        player_frame = 0
        start_room()
        return

    if player_y == room_height:
        current_room += MAP_WIDTH
        generate_map()
        player_y = 0
        player_x = int(room_width / 2)
        player_frame = 0
        start_room()
        return

    if player_y == -1:
        current_room -= MAP_WIDTH
        generate_map()
        player_y = room_height - 1
        player_x = int(room_width / 2)
        player_frame = 0
        start_room()
        return


    if room_map[player_y][player_x] not in items_player_may_stand_on:

        player_x = old_player_x
        player_y = old_player_y
        player_frame = 0

    if player_direction == "right" and player_frame > 0:
        player_offset_x = -1 + (0.25 * player_frame)
    if player_direction == "left" and player_frame > 0:
        player_offset_x = 1 - (0.25 * player_frame)
    if player_direction == "up" and player_frame > 0:
        player_offset_y = 1 - (0.25 * player_frame)
    if player_direction == "down" and player_frame > 0:
        player_offset_y = -1 + (0.25 * player_frame)




def draw_image(image, y, x):
    screen.blit(
        image,
        (top_left_x + (x * TILE_SIZE),
         top_left_y + (y * TILE_SIZE) - image.get_height())
    )


def draw_shadow(image, y, x):
    screen.blit(
        image,
        (top_left_x + (x * TILE_SIZE),
         top_left_y + (y * TILE_SIZE))
    )


def draw_player():
    player_image = PLAYER[player_direction][player_frame]
    draw_image(player_image, player_y + player_offset_y,
               player_x + player_offset_x)
    player_image_shadow = PLAYER_SHADOW[player_direction][player_frame]
    draw_shadow(player_image_shadow, player_y + player_offset_y,
                player_x + player_offset_x)


def draw():
    if game_over:
        return


    box = Rect((0, 150), (800, 600))
    screen.draw.filled_rect(box, RED)
    box = Rect((0, 0), (800, top_left_y + (room_height - 1) * 30))
    screen.surface.set_clip(box)
    floor_type = get_floor_type()

    for y in range(room_height):
        for x in range(room_width):
            draw_image(objects[floor_type][0], y, x)

            if room_map[y][x] in items_player_may_stand_on:
                draw_image(objects[room_map[y][x]][0], y, x)


    if current_room == 26:
        draw_image(objects[39][0], 8, 2)
        image_on_pad = room_map[8][2]
        if image_on_pad > 0:
            draw_image(objects[image_on_pad][0], 8, 2)

    for y in range(room_height):
        for x in range(room_width):
            item_here = room_map[y][x]

            if item_here not in items_player_may_stand_on + [255]:
                image = objects[item_here][0]

                if (current_room in outdoor_rooms
                    and y == room_height - 1
                    and room_map[y][x] == 1) or \
                        (current_room not in outdoor_rooms
                         and y == room_height - 1
                         and room_map[y][x] == 1
                         and x > 0
                         and x < room_width - 1):

                    image = PILLARS[wall_transparency_frame]

                draw_image(image, y, x)

                if objects[item_here][1] is not None:
                    shadow_image = objects[item_here][1]
                    if shadow_image in [images.half_shadow,
                                        images.full_shadow]:
                        shadow_width = int(image.get_width() / TILE_SIZE)
                        for z in range(0, shadow_width):
                            draw_shadow(shadow_image, y, x + z)
                    else:
                        draw_shadow(shadow_image, y, x)

        if (player_y == y):
            draw_player()

    screen.surface.set_clip(None)


def adjust_wall_transparency():
    global wall_transparency_frame

    if (player_y == room_height - 2
            and room_map[room_height - 1][player_x] == 1
            and wall_transparency_frame < 4):
        wall_transparency_frame += 1

    if ((player_y < room_height - 2
         or room_map[room_height - 1][player_x] != 1)
            and wall_transparency_frame > 0):
        wall_transparency_frame -= 1


def show_text(text_to_show, line_number):
    if game_over:
        return
    text_lines = [15, 50]
    box = Rect((0, text_lines[line_number]), (800, 35))
    screen.draw.filled_rect(box, BLACK)
    screen.draw.text(text_to_show,
                     (20, text_lines[line_number]), color=GREEN)


generate_map()
clock.schedule_interval(game_loop, 0.03)
