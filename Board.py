class Board():

  # Contains ships' coordinates.
  ship_coords = []
  # Contains strikes' coordinates.
  strike_coords = []
  # Contains hits' coordinates.
  hit_coords = []
  
  def __init__(self):
    pass

  # -------------------------------------------------- #

  """
  Returns the board as a string.

  Parameter(s):
    censored = if the other player requests the board, don't show the ships.
  
  Board key:
    ~ = Water; $ = Ship; X = Missed strike; * = Successful strike, hit.
  """
  def get_board(self, censored = False):
    board_string = "   "
    
    for x in range(10):
      board_string += f" {x} "
    board_string += "\n"

    for y in range(10):
      board_string += f" {y} "
      for x in range(10):
        if (x, y) in self.hit_coords:
          board_string += " * "
          continue
        if (x, y) in self.strike_coords:
          board_string += " X "
          continue
        if (x, y) in self.ship_coords and not censored:
          board_string += " $ "
          continue
        board_string += " ~ "
      board_string += "\n"

    return board_string

  # -------------------------------------------------- #

  """
  Places ship.

  Parameter(s):
    coord = if horizontal, leftmost coordinate; if vertical, highest coordinate.
    size = length of the ship.
    direction = horizontal or vertical.

  Return:
    Info, if there are errors or successes.
  """
  def place_ship(self, coord, size, direction):
    info = {
      "valid_coord": False,
      "valid_size": False,
      "valid_direction": False,
      "fits_on_board": False,
      "no_conflicts": False,
      "ship_placed": False
    }

    # Checks if the coordinate is valid.
    if not self.check_coord(coord):
      return info
    info["valid_coord"] = True
    (x, y) = coord
    x, y = int(x), int(y)

    # Checks if the size is valid.
    if not size.isdigit():
      return info
    info["valid_size"] = True
    size = int(size)

    # Checks if the direction is valid.
    direction = direction.lower()
    if direction not in ["h", "v"]:
      return info
    info["valid_direction"] = True

    # Checks if the ship fits on the board.
    if direction == "h":
      if (x + size - 1) > 9:
        return info
    else:
      if (y + size - 1) > 9:
        return info
    info["fits_on_board"] = True

    # Checks if the ship will not conflict with ships already placed.
    this_ship_coords = []
    for offset in range(size):
      this_ship_coords.append((
        x + (offset if direction == "h" else 0),
        y + (offset if direction == "v" else 0)
      ))
    for coord in this_ship_coords:
      if coord in self.ship_coords:
        return info
    info["no_conflicts"] = True

    self.ship_coords = sorted(self.ship_coords + this_ship_coords)
    info["ship_placed"] = True
    return info

  # -------------------------------------------------- #
  
  """
  Places strike.

  Parameter(s):
    coord = strike coordinate.

  Return:
    Info, if there are errors or successes.
  """
  def place_strike(self, coord):
    info = {
      "valid_coord": False,
      "available_coord": False,
      "strike_placed": False,
      "is_hit": False,
      "all_ships_hit": False
    }

    # Checks if the coordinate is valid.
    if not self.check_coord(coord):
      return info
    info["valid_coord"] = True

    (x, y) = coord
    x, y = int(x), int(y)

    # Checks if the coordinate has not already been struck.
    if (x, y) in self.strike_coords:
      return info
    info["available_coord"] = True

    self.strike_coords = sorted(self.strike_coords + [(x, y)])
    info["strike_placed"] = True

    # Checks if the coordinate is a ship.
    if (x, y) not in self.ship_coords:
      return info
    self.hit_coords = sorted(self.hit_coords + [(x, y)])
    info["is_hit"] = True

    # Checks if all the ships have been hit.
    if len(self.hit_coords) == len(self.ship_coords):
      info["all_ships_hit"] = True

    return info

  # -------------------------------------------------- #

  """
  Returns the strike coordinates.

  Return:
    Strike coordinates.
  """
  def get_strike_coords(self):
    return self.strike_coords

  # -------------------------------------------------- #

  """
  Checks if coordinate is valid.

  Parameters(s):
    coord = coordinate to check.

  Return:
    If coordinate is valid.
  """
  def check_coord(self, coord):
    if type(coord) is not tuple:
      return False
    if len(coord) != 2:
      return False
    (x, y) = coord
    if not x.isdigit() or not y.isdigit():
      return False
    x, y = int(x), int(y)
    if x < 0 or x > 9 or y < 0 or y > 9:
      return False
    return True
    
  


