import random
from typing import List, Dict

"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""


def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves

def avoid_the_walls(my_head: dict, board_height: int, board_width: int, possible_moves: List[str]) -> List[str]:
  
  if my_head["x"] == 0:  # my head is at the left wall
      possible_moves.remove("left")
  elif my_head["x"] == board_width - 1:  # my head is at the right wall
      possible_moves.remove("right")
  if my_head["y"] == 0:  # my head is at the bottom wall
      possible_moves.remove("down")
  elif my_head["y"] == board_height - 1:  # my head is at the top wall
      possible_moves.remove("up")

  return possible_moves

def avoid_my_body(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:

  print("----------In body----------")
  print(my_body)
  for i in range(2, len(my_body)):
    if my_body[i]["x"] == my_head["x"] - 1 and my_body[i]["y"] == my_head["y"]:  # current body part is left of my head
      if "left" in possible_moves:
        possible_moves.remove("left")
        print("Removed left")
    elif my_body[i]["x"] == my_head["x"] + 1 and my_body[i]["y"] == my_head["y"]:  # current body part is right of my head
      if "right" in possible_moves:
        possible_moves.remove("right")
        print("Removed right")
    elif my_body[i]["y"] == my_head["y"] - 1 and my_body[i]["x"] == my_head["x"]:  # current body part is below my head
      if "down" in possible_moves:
        possible_moves.remove("down")
        print("Removed down")
    elif my_body[i]["y"] == my_head["y"] + 1 and my_body[i]["x"] == my_head["x"]:  # current body part is above my head
      if "up" in possible_moves:
        possible_moves.remove("up")
        print("Removed up")
  print("----------")
  return possible_moves

def avoid_all_snakes(my_head: Dict[str, int], snakes: List[dict], possible_moves: List[str]) -> List[str]:

  for snake in snakes:
    for i in range(0, len(snake['body'])):
      if snake['body'][i]["x"] == my_head["x"] - 1 and snake['body'][i]["y"] == my_head["y"]:  # current body part is left of my head
        if "left" in possible_moves:
          possible_moves.remove("left")
          print("Removed left")
      elif snake['body'][i]["x"] == my_head["x"] + 1 and snake['body'][i]["y"] == my_head["y"]:  # current body part is right of my head
        if "right" in possible_moves:
          possible_moves.remove("right")
          print("Removed right")
      elif snake['body'][i]["y"] == my_head["y"] - 1 and snake['body'][i]["x"] == my_head["x"]:  # current body part is below my head
        if "down" in possible_moves:
          possible_moves.remove("down")
          print("Removed down")
      elif snake['body'][i]["y"] == my_head["y"] + 1 and snake['body'][i]["x"] == my_head["x"]:  # current body part is above my head
        if "up" in possible_moves:
          possible_moves.remove("up")
          print("Removed up")
  return possible_moves

def choose_move(data: dict, board_height: int, board_width: int) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]

    # TODO: uncomment the lines below so you can see what this data looks like in your output!
    # print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    # print(f"All board data this turn: {data}")
    # print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]

    # Don't allow your Battlesnake to move back in on it's own neck
    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)

    # TODO: Using information from 'data', find the edges of the board and don't let your Battlesnake move beyond them
    possible_moves = avoid_the_walls(my_head, board_height, board_width, possible_moves)

    # TODO Using information from 'data', don't let your Battlesnake pick a move that would hit its own body
    possible_moves = avoid_my_body(my_head, my_body, possible_moves)

    # TODO: Using information from 'data', don't let your Battlesnake pick a move that would collide with another Battlesnake

    possible_moves = avoid_all_snakes(my_head, data['board']['snakes'], possible_moves)

    # TODO: Using information from 'data', make your Battlesnake move towards a piece of food on the board

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    #move = possible_moves[0]
    move = random.choice(possible_moves)
    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move
