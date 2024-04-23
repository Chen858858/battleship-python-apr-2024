from Board import Board

class Player():

  name = ""
  player_board = None

  # -------------------------------------------------- #

  def __init__(self, name):
    self.name = name
    self.player_board = Board()

  # -------------------------------------------------- #
  
  def get_board(self, censored = False):
    return self.player_board.get_board(censored)

  # -------------------------------------------------- #

  def place_ship(self, coord, size, direction):
    return self.player_board.place_ship(coord, size, direction)

  # -------------------------------------------------- #

  def place_strike(self, coord):
    return self.player_board.place_strike(coord)

  # -------------------------------------------------- #

  def get_strike_coords(self):
    return self.player_board.strike_coords