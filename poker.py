#!/usr/bin/python

import player
import game

def main():
    players = [player.Player('Jack', 100),
               player.Player('Jill', 100),
               player.Player('Doyle', 200),
               player.Player('Phil', 500),
               ]
    poker_game = game.Game(players)

    num_hands = 1000

    poker_game.play(num_hands)

if __name__ == "__main__":
    main()
