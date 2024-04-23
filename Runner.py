import random
import time
from Player import Player
from Board import Board

"""
Function that is the game.
"""
def runner():
  demo_board = Board()
  print(f"Please widen your terminal so this board fits:\n\n{demo_board.get_board()}")
  time.sleep(3)
  print("Based on the game Battleship.")
  time.sleep(0.5)
  print("Info at en.wikipedia.org/wiki/Battleship_(game) .")
  time.sleep(0.5)
  print("Ships based on Hasbro 2002's designations.\n")

  time.sleep(2)

  ship_list = [
    {"name": "Carrier", "size": "5"},
    {"name": "Battleship", "size": "4"},
    {"name": "Destroyer", "size": "3"},
    {"name": "Submarine", "size": "3"},
    {"name": "Patrol Boat", "size": "2"}
  ]

  human_name = input("What is your name?: ")
  human_player = Player(human_name)

  print(f"Hello {human_name}. ", end="", flush=True)
  time.sleep(1.5)
  print("Today you are playing against", end="", flush=True)
  for _ in range(3):
    time.sleep(0.5)
    print(".", end="", flush=True)
  time.sleep(1)
  computer_player = Player(["Hal", "Mr. Roboto", "The Machine"][random.randint(0, 2)])
  print(f" {computer_player.name}.\n\n", flush=True)
  time.sleep(1)

  board_facts = [
    "Let's learn about the board.",
    "~ = Water.",
    "$ = Ship.",
    "X = Strike that did not hit a ship.",
    "* = Strike that hit a ship.\n",
    "For the coordinates:",
    "x = horizontal, 0 to 9, left to right.",
    "y = vertical, 0 to 9, top to bottom."
  ]
  for fact in board_facts:
    print(fact)
    time.sleep(0.5)
  time.sleep(3.5)

  # Human placing ships.

  print("\nPlease place your ships.")
  time.sleep(1)
  print("Note: If the ship is horizontal, the coordinate is the leftmost coordinate.")
  time.sleep(0.5)
  print("      If the ship is vertical, the coordinate is the top coordinate.")
  time.sleep(4)
  for ship in ship_list:
    print(f"\n\nYour current board:\n\n{human_player.get_board()}")
    time.sleep(1)
    print(f"Place your {ship['name']}, which has a size of {ship['size']}.")
    while True:
      coord = input("(x, y) coordinate separated by a comma, no parentheses.: ")
      direction = input("Direction of the ship. h = horizontal, v = vertical.: ")
      info = human_player.place_ship(tuple(coord.replace(" ", "").split(",")),
        ship["size"],
        direction)
      if info["ship_placed"]:
        break
      print("Error: ", end="")
      if not info["valid_coord"]:
        print("Invalid coordinate.")
      elif not info["valid_direction"]:
        print("Invalid direction.")
      elif not info["fits_on_board"]:
        print("Ship doesn't fit on board.")
      elif not info["no_conflicts"]:
        print("Ship conflicts with a ship already on the board.")
      print()
      time.sleep(1)
    time.sleep(1)

  print("\nWhat your board looks like with all ships placed:\n\n")
  print(human_player.get_board())
  time.sleep(2)

  # Computer placing ships.

  print(f"\nNow it's time for {computer_player.name} to place its ships.", end="", flush=True)
  for ship in ship_list:
    time.sleep(0.5)
    while True:
      coord = (f"{random.randint(0, 9)}", f"{random.randint(0, 9)}")
      direction = ["h", "v"][random.randint(0, 1)]
      info = computer_player.place_ship(coord, ship["size"], direction)
      if info["ship_placed"]:
        break
    print(".", end="", flush=True)
  
  time.sleep(1)
  print(f"\n\n{computer_player.name} has placed its ships.\n")

  time.sleep(1)
  print("Now, it's time to play.\n")

  time.sleep(1)
  reminders = [
    "Reminder:",
    "~ = Water.",
    "$ = Ship.",
    "X = Strike that did not hit a ship.",
    "* = Strike that hit a ship.\n",
    "For the coordinates:",
    "x = horizontal, 0 to 9, left to right.",
    "y = vertical, 0 to 9, top to bottom."
  ]
  for reminder in reminders:
    print(reminder)
    time.sleep(0.5)
  time.sleep(2.5)
  print()

  computer_target = []
  computer_init_target_sorrounding = {"t": False, "b": False, "r": False, "l": False}
  computer_target_direction = "u"
  computer_target_boundaries = {"tl": False, "br": False}

  while True:
    # Human strike.

    print(f"{human_player.name}, it's your turn.\n")
    time.sleep(1)
    print(f"What {computer_player.name}'s board looks like:\n\n{computer_player.get_board(True)}\n")
    time.sleep(2)

    while True:
      human_strike_coord = input("Enter the coordinate you want to strike, (x, y), separated by a comma, no parentheses.: ")
      human_strike_info = computer_player.place_strike(tuple(human_strike_coord.replace(" ", "").split(",")))

      if human_strike_info["strike_placed"]:
        human_strike_coord = tuple(int(num) for num in human_strike_coord.replace(" ", "").split(","))
        print(f"The strike on {human_strike_coord} has been placed", end="", flush=True)
        time.sleep(0.5)
        print(", and you've hit a ship!" if human_strike_info["is_hit"] else ", but it was water.",
          flush=True)
        if human_strike_info["all_ships_hit"]:
          end(human_player, computer_player)
          return
        break
      
      print("Error: ", end="")
      if not human_strike_info["valid_coord"]:
        print("Invalid coordinate.")
      elif not human_strike_info["available_coord"]:
        print("Coordinate has already been struck.")
      print()
    print()
    time.sleep(2)

    # Computer strike.

    print(f"Now {computer_player.name} is placing its strike.")
    time.sleep(1)
    computer_strike_info = computer_strike_coord = None
    # If the computer has no target, place random strike.
    if len(computer_target) in [0, 5]:
      if len(computer_target) == 5:
        computer_target = []
        computer_target_direction = "u"
        computer_target_boundaries = {"tl": False, "br": False}
      coord = calc_random_strike_coord(human_player)
      computer_strike_info = human_player.place_strike((str(coord[0]), str(coord[1])))
      computer_strike_coord = coord
      if computer_strike_info["is_hit"]:
        computer_target.append(computer_strike_coord)
    # If the computer has a target but doesn't know its direction, check sorrounding coordinates for ships.
    elif len(computer_target) == 1:
      computer_init_target = computer_target[0]
      while not computer_strike_coord:
        if all(value == True for value in computer_init_target_sorrounding.values()):
          computer_target = []
          computer_init_target_sorrounding = {k: False for k in computer_init_target_sorrounding.keys()}
          coord = calc_random_strike_coord(human_player)
          computer_strike_info = human_player.place_strike((str(coord[0]), str(coord[1])))
          computer_strike_coord = coord
          if computer_strike_info["is_hit"]:
            computer_target.append(computer_strike_coord)
        else:
          coord = computer_init_target
          direction_checked = None
          if not computer_init_target_sorrounding["t"]:
            direction_checked = "t"
            coord = (coord[0], coord[1] - 1)
          elif not computer_init_target_sorrounding["r"]:
            direction_checked = "r"
            coord = (coord[0] + 1, coord[1])
          elif not computer_init_target_sorrounding["b"]:
            direction_checked = "b"
            coord = (coord[0], coord[1] + 1)
          elif not computer_init_target_sorrounding["l"]:
            direction_checked = "l"
            coord = (coord[0] - 1, coord[1])
          computer_init_target_sorrounding[direction_checked] = True
          info = human_player.place_strike((str(coord[0]), str(coord[1])))
          if info["strike_placed"]:
            computer_strike_coord, computer_strike_info = coord, info
            if computer_strike_info["is_hit"]:
              computer_init_target_sorrounding = {k: False for k in computer_init_target_sorrounding.keys()}
              computer_target_direction = "v" if direction_checked in ["t", "b"] else "h"
              if direction_checked in ["t", "l"]:
                computer_target.insert(0, computer_strike_coord)
              elif direction_checked in ["b", "r"]:
                computer_target.append(computer_strike_coord)
    # If the computer has a target and has an idea of its direction, use the known information to place strike.
    elif 2 <= len(computer_target) <= 4:
      while not computer_strike_coord:
        if all(value == True for value in computer_target_boundaries.values()):
          computer_target = []
          computer_target_boundaries = {"tl": False, "br": False}
          computer_target_direction = "u"
          coord = calc_random_strike_coord(human_player)
          computer_strike_info = human_player.place_strike((str(coord[0]), str(coord[1])))
          computer_strike_coord = coord
          if computer_strike_info["is_hit"]:
            computer_target.append(computer_strike_coord)
        else:
          coord = None
          add_to_front_or_end = None
          if not computer_target_boundaries["tl"]:
            add_to_front_or_end = "f"
            coord = computer_target[0]
            if computer_target_direction == "h":
              coord = ((coord[0] - 1), coord[1])
            elif computer_target_direction == "v":
              coord = (coord[0], (coord[1] - 1))
          elif not computer_target_boundaries["br"]:
            add_to_front_or_end = "e"
            coord = computer_target[-1]
            if computer_target_direction == "h":
              coord = ((coord[0] + 1), coord[1])
            elif computer_target_direction == "v":
              coord = (coord[0], (coord[1] + 1))
          info = human_player.place_strike((str(coord[0]), str(coord[1])))
          if not info["is_hit"]:
            if add_to_front_or_end == "f":
              computer_target_boundaries["tl"] = True
            else:
              computer_target_boundaries["br"] = True
          else:
            if add_to_front_or_end == "f":
              computer_target.insert(0, coord)
            else:
              computer_target.append(coord)
          if info["strike_placed"]:
            computer_strike_coord = coord
            computer_strike_info = info
    print(f"{computer_player.name} has placed its strike on {computer_strike_coord}", end="", flush=True)
    time.sleep(0.5)
    print(", which was one of your ships." if computer_strike_info["is_hit"] else ", which was water.", flush=True)
    if computer_strike_info["all_ships_hit"]:
      end(computer_player, human_player)
      return
    time.sleep(1)
    print()
    print(f"What your board looks like:\n\n{human_player.get_board()}")
    time.sleep(3)

# -------------------------------------------------- #

"""
Function for ending the game.

Parameter(s):
  winner = the winner of the game.
"""
def end(winner, loser):
  time.sleep(1)
  print()
  if winner.name not in ["Hal", "Mr. Roboto", "The Machine"]:
    print(f"Congratulations {winner.name}!")
    time.sleep(1)
    print(f"You have beat {loser.name}.")
  else:
    print(f"Sorry {loser.name}, {winner.name} is victorius.")
    time.sleep(1)
    print("Maybe next time you'll win.")
  
  time.sleep(1)
  print()
  # Text represented by character generated with https://www.patorjk.com/software/taag/, font Isometric3.
  gg_credits_lines = [
    "      ___           ___",
    "     /  /\\         /  /\\",
    "    /  /:/_       /  /:/_",
    "   /  /:/ /\\     /  /:/ /\\",
    "  /  /:/_/::\\   /  /:/_/::\\",
    " /__/:/__\\/\\:\\ /__/:/__\\/\\:\\",
    " \\  \\:\\ /~~/:/ \\  \\:\\ /~~/:/",
    "  \\  \\:\\  /:/   \\  \\:\\  /:/",
    "   \\  \\:\\/:/     \\  \\:\\/:/",
    "    \\  \\::/       \\  \\::/",
    "     \\__\\/         \\__\\/",
    "",
    "Game coded in Python by Junchen Wang.",
    "Website: chen858858.github.io .",
    "GitHub: github.com/Chen858858 .",
    "",
    "Initial release April 2024.",
    "",
    "This game's repository: github.com/Chen858858/battleship-python-apr-2024 ."

  ]
  for line in gg_credits_lines:
    print(line)
    time.sleep(0.5)

# -------------------------------------------------- #

"""
Calculates a random coordinate for the computer to strike. For optimization, it checks the x columns to see which was has been struck the least.

Parameters(s):
  human_player = The human player object.

Return:
  Coordinate to strike.
"""
def calc_random_strike_coord(human_player):
  strike_coords = human_player.get_strike_coords()
  strike_coords_by_x = {x: 0 for x in range(0, 10)}
  for coord in strike_coords:
    strike_coords_by_x[coord[0]] += 1
  x = min(strike_coords_by_x, key=strike_coords_by_x.get)
  while True:
    coord = (x, random.randint(0, 9))
    if coord not in strike_coords:
      return coord

# -------------------------------------------------- #

runner()