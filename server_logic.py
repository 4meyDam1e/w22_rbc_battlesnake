import random
from typing import List, Dict
from xmlrpc.client import boolean
"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the "neck" direction
from the list of possible moves!
"""


def avoid_the_walls(my_head: dict, board_width: int, board_height: int, possible_moves: List[str]) -> List[str]:
  if my_head["x"] == 0:  # my head is at the left wall
    possible_moves.remove("left")
  elif my_head["x"] == board_width - 1:  # my head is at the right wall
    possible_moves.remove("right")
  if my_head["y"] == 0:  # my head is at the bottom wall
    possible_moves.remove("down")
  elif my_head["y"] == board_height - 1:  # my head is at the top wall
    possible_moves.remove("up")
  return possible_moves


def is_in_snake(coord: Dict[str, int], snakes: List[dict]) -> boolean:
  for snake in snakes:
    for i in range(snake["length"]):
      if coord == snake["body"][i]:
        return True
  return False


def avoid_all_snakes(my_head: Dict[str, int], snakes: List[dict], possible_moves: List[str]) -> List[str]:
  # print("-----------------------\nIn avoid_all_snakes()")
  if is_in_snake({"x": my_head["x"], "y": my_head["y"] + 1}, snakes): # above my head
    if "up" in possible_moves:
      # print("REMOVING UP")
      possible_moves.remove("up")
  if is_in_snake({"x": my_head["x"] - 1, "y": my_head["y"]}, snakes): # left of my head
    if "left" in possible_moves:
      # print("REMOVING LEFT")
      possible_moves.remove("left")
  if is_in_snake({"x": my_head["x"], "y": my_head["y"] - 1}, snakes): # below my head
    if "down" in possible_moves:
      # print("REMOVING DOWN")
      possible_moves.remove("down")
  if is_in_snake({"x": my_head["x"] + 1, "y": my_head["y"]}, snakes): # right of my head
    if "right" in possible_moves:
      # print("REMOVING RIGHT")
      possible_moves.remove("right")
  # print("------------------")
  return possible_moves


def find_closest_food(my_head: Dict[str, int], board_width: int, board_height: int, food_list: List[dict]) -> Dict[str, int]:
  min_distance = board_width + board_height
  closest_food = {"x": 0, "y": 0}
  for food in food_list:
    curr_food_distance = abs(food["x"] - my_head["x"]) + abs(food["y"] - my_head["y"])
    if curr_food_distance < min_distance:
      min_distance = curr_food_distance
      closest_food = food
  return closest_food


def move_to_coord(possible_moves: List[str], my_head: Dict[str, int], coord: Dict[str, int]) -> str:
  move = random.choice(possible_moves)
  if my_head["x"] != coord["x"]:
    if coord["x"] > my_head["x"]:
      if "right" in possible_moves:
        return "right"
    else:
      if "left" in possible_moves:
        return "left"

  if my_head["y"] != coord["y"]:
    if coord["y"] > my_head["y"]:
      if "up" in possible_moves:
        return "up"
    else:
      if "down" in possible_moves:
        return "down"
  return move


def coords_around_move(move: str, my_head: Dict[str, int]) -> List[Dict[str, int]]:
  coords = []
  if move == "left":
    next_coord = {"x": my_head["x"] - 1, "y": my_head["y"]}
    coords.append({"x": next_coord["x"], "y": next_coord["y"] + 1})  #up
    coords.append({"x": next_coord["x"] - 1, "y": next_coord["y"]})  #left
    coords.append({"x": next_coord["x"], "y": next_coord["y"] - 1})  #down
  elif move == "right":
    next_coord = {"x": my_head["x"] + 1, "y": my_head["y"]}
    coords.append({"x": next_coord["x"], "y": next_coord["y"] - 1})  #down
    coords.append({"x": next_coord["x"] + 1, "y": next_coord["y"]})  #right
    coords.append({"x": next_coord["x"], "y": next_coord["y"] + 1})  #up
  elif move == "up":
    next_coord = {"x": my_head["x"], "y": my_head["y"] + 1}
    coords.append({"x": next_coord["x"] + 1, "y": next_coord["y"]})  #right
    coords.append({"x": next_coord["x"], "y": next_coord["y"] + 1})  #up
    coords.append({"x": next_coord["x"] - 1, "y": next_coord["y"]})  #left
  elif move == "down":
    next_coord = {"x": my_head["x"], "y": my_head["y"] - 1}
    coords.append({"x": next_coord["x"] - 1, "y": next_coord["y"]})  #left
    coords.append({"x": next_coord["x"], "y": next_coord["y"] - 1})  #down
    coords.append({"x": next_coord["x"] + 1, "y": next_coord["y"]})  #right
  return coords


def kill_safe(coords: List[Dict[str, int]], snakes: List[Dict[str, int]], my_length: int) -> bool:
  for coord in coords:
    for snake in snakes:
      if snake["body"][0] == coord:#(snake["body"][0]["x"] == (coord["x"]) and snake["body"][0]["y"] == (coord["y"])):
        if (snake["length"] >= my_length):
          # print("SAFE: FALSE")
          return False
  # print("SAFE: TRUE")
  return True


def flood_fill(x: int, y: int, visited: List[str], count: int, board_width: int, board_height: int, snakes: List[dict]) -> int:
  coord = "(" + str(x) + ", " + str(y) + ")"
  #print("COORDINATE: " + coord)
  if ((coord in visited) or  # coordinate already visited
      (x < 0) or  # coordinate out of bounds to the left
      (y < 0) or  # coordinate out of bounds below
      (x >= board_width) or  # coordinate out of bounds to the right
      (y >= board_height) or  # coordinate out of bounds above
      (is_in_snake({"x": x, "y": y}, snakes))):  # coordinate is on a snake
    #print("RETURNING 0")
    return 0

  visited.append(coord)
  #print("VISITED AFTER ADDING: ", end = "")
  #print(visited)
  count_up = flood_fill(x, y + 1, visited, count, board_width, board_height, snakes)
  count_left = flood_fill(x - 1, y, visited, count, board_width, board_height, snakes)
  count_down = flood_fill(x, y - 1, visited, count, board_width, board_height, snakes)
  count_right = flood_fill(x + 1, y, visited, count, board_width, board_height, snakes)
  return count_up + count_left + count_down + count_right + 1


def get_flood_fill_value(move: str, my_head: str, board_width: int, board_height: int, snakes: List[dict]) -> int:
  if move == "up":
    x = my_head["x"]
    y = my_head["y"] + 1
  elif move == "left":
    x = my_head["x"] - 1
    y = my_head["y"]
  elif move == "down":
    x = my_head["x"]
    y = my_head["y"] - 1
  elif move == "right":
    x = my_head["x"] + 1
    y = my_head["y"]
  
  return flood_fill(x, y, [], 0, board_width, board_height, snakes)


def get_largest_snake_length(snakes: List[dict], my_id: str):
  max_length = 0

  for snake in snakes:
    if my_id != snake['id']:
      current_length = snake['length']
      if current_length > max_length:
        max_length = current_length

  return max_length + 3


def prioritize_kill(possible_moves: List[str], snakes: List[dict],my_head:Dict[str, int], my_length:int) -> List[str]:
  kill_moves= []
  for move in possible_moves:
    coords = coords_around_move(move, my_head)
    for coord in coords:
      for snake in snakes:
        if (snake['body'][0]['x'] == (coord['x']) and snake['body'][0]['y'] == (coord['y'])):
          if (snake["length"] < my_length):
            kill_moves.append(move)
  return kill_moves


def choose_move(data: dict) -> str:
  my_head = data["you"][
    "head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
  my_body = data["you"][
    "body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
  my_length = data["you"]["length"]
  my_health = data["you"]["health"]
  my_id = data["you"]["id"]
  snakes = data["board"]["snakes"]


  # TODO: uncomment the lines below so you can see what this data looks like in your output!
  # print(f"~~~ Turn: {data["turn"]}  Game Mode: {data["game"]["ruleset"]["name"]} ~~~")
  # print(f"All board data this turn: {data}")
  # print("----------------------")
  # print(f"My Battlesnakes head this turn is: {my_head}")
  # print(f"My Battlesnakes body this turn is: {my_body}")

  possible_moves = ["up", "down", "left", "right"]

  # Don"t allow your Battlesnake to move back in on it"s own neck
  #possible_moves = avoid_my_neck(my_head, my_body, possible_moves)

  # TODO: Using information from "data", find the edges of the board and don"t let your Battlesnake move beyond them
  board_width = data["board"]["width"]
  board_height = data["board"]["height"]
  possible_moves = avoid_the_walls(my_head, board_width, board_height,
                                    possible_moves)

  # TODO Using information from "data", don"t let your Battlesnake pick a move that would hit its own body
  #possible_moves = avoid_my_body(my_head, my_body, possible_moves)

  # TODO: Using information from "data", don"t let your Battlesnake pick a move that would collide with another Battlesnake
  possible_moves = avoid_all_snakes(my_head, snakes, possible_moves)

  # TODO: Using information from "data", make your Battlesnake move towards a piece of food on the board
  closest_food = find_closest_food(my_head, board_width, board_height, data["board"]["food"])
  # print("CLOSEST FOOD: ")
  # print(closest_food)
  
  kill_moves = prioritize_kill(possible_moves, snakes, my_head, my_length)
  if len(kill_moves) > 0:
    move = random.choice(kill_moves)
  else:
    # CHASING TAIL
    if my_health < 50 or my_length <= get_largest_snake_length(snakes, my_id):
      move = move_to_coord(possible_moves, my_head, closest_food)
    else:
      if len(snakes) > 2:
        move = move_to_coord(possible_moves, my_head, my_body[-1]) 
      else:
        for snake in snakes:
          if snake["id"] != my_id:
            move = move_to_coord(possible_moves, my_head, snake["body"][0])
      # move = move_to_coord(possible_moves, my_head, my_body[-1]) 
      # move = random.choice(possible_moves)
    # print("CURRENT CHOSEN MOVE:" + move)

  risky_kill_moves = []
  safe_from_kill = kill_safe(coords_around_move(move, my_head), snakes, my_length)
  risky_block_moves_to_ff_value = {}
  risky_kill_moves_to_ff_value = {}
  ff_value = get_flood_fill_value(move, my_head, board_width, board_height, snakes)
  # print("FLOOD FILL VALUE: ", end = "")
  # print(ff_value)
  safe_from_block = ff_value >= my_length

  while (not safe_from_block) or (not safe_from_kill):
    # print(f"BLOCK_SAFE: {safe_from_block} KILL_SAFE: {safe_from_kill}")
    if not safe_from_block:
      risky_block_moves_to_ff_value[move] = ff_value
    if not safe_from_kill:
      risky_kill_moves_to_ff_value[move] = ff_value
      # risky_kill_moves.append(move)
    possible_moves.remove(move)
    if move in kill_moves:
      kill_moves.remove(move)

    if len(possible_moves) == 0:
      if len(risky_kill_moves_to_ff_value) <= 1 and len(risky_block_moves_to_ff_value) > 0:
        move = max(risky_block_moves_to_ff_value, key = risky_block_moves_to_ff_value.get)
      else:
        # move = random.choice(risky_kill_moves)
        move = max(risky_kill_moves_to_ff_value, key = risky_kill_moves_to_ff_value.get)
      break
        
    if len(kill_moves) > 0:
      move = random.choice(kill_moves)
    else:
      # CHASING TAIL
      if my_health < 50 or my_length <= get_largest_snake_length(snakes, my_id):
        move = move_to_coord(possible_moves, my_head, closest_food)
      else:
        if len(snakes) > 2:
          move = move_to_coord(possible_moves, my_head, my_body[-1]) 
        else:
          for snake in snakes:
            if snake["id"] != my_id:
              move = move_to_coord(possible_moves, my_head, snake["body"][0])
        # move = move_to_coord(possible_moves, my_head, my_body[-1]) 
        # move = random.choice(possible_moves)
      # print("CURRENT CHOSEN MOVE:" + move)
    safe_from_kill = kill_safe(coords_around_move(move, my_head), snakes, my_length)
    ff_value = get_flood_fill_value(move, my_head, board_width, board_height, snakes)
    # print("FLOOD FILL VALUE: ", end = "")
    # print(ff_value)
    safe_from_block = ff_value >= my_length
    

  #coords = coords_around_move(move, my_head)
  #print("COORDS AROUND MOVE: ")
  #print(coords)
  # TODO: Explore new strategies for picking a move that are better than random

  # if len(possible_moves) == 0:
  #   move = random.choice(risky_moves)

  # print(
  #     f"{data["game"]["id"]} MOVE {data["turn"]}: {move} picked from all valid options in {possible_moves}"
  # )
  # print("FINAL CHOSEN MOVE:" + move)
  # print("----------------------")
  return move
