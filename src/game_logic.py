import random

CHOICES = ["snake", "water", "gun"]

def get_random_choice():
    return random.choice(CHOICES)

def determine_result(player, computer):
    if player == computer:
        return "tie"
    if (player == "snake" and computer == "water") or \
       (player == "water" and computer == "gun") or \
       (player == "gun" and computer == "snake"):
        return "win"
    return "lose"
