#!/usr/bin/python

from card_set import *
from hand_scorer import *

def main():
    for hand in types:
        print 'hand: %s' % hand
        eval('tester(' + hand + '())')

def tester(hole):
    deck = Deck(1)
    print str(HandScorer(Hand(Board(deck), hole)).best_hand())

def pair():
    hole = Hole()
    hole.add_card(Card('8', 'Club'))
    hole.add_card(Card('8', 'Diamond'))
    hole.add_card(Card('6', 'Heart'))
    hole.add_card(Card('7', 'Spade'))
    hole.add_card(Card('9', 'Diamond'))
    hole.add_card(Card('10', 'Spade'))
    hole.add_card(Card('Q', 'Diamond'))
    return hole

def three_of_a_kind():
    hole = Hole()
    hole.add_card(Card('8', 'Club'))
    hole.add_card(Card('8', 'Diamond'))
    hole.add_card(Card('8', 'Heart'))
    hole.add_card(Card('7', 'Spade'))
    hole.add_card(Card('10', 'Diamond'))
    hole.add_card(Card('10', 'Spade'))
    hole.add_card(Card('Q', 'Diamond'))
    return hole

def four_of_a_kind():
    hole = Hole()
    hole.add_card(Card('8', 'Club'))
    hole.add_card(Card('8', 'Diamond'))
    hole.add_card(Card('8', 'Heart'))
    hole.add_card(Card('8', 'Spade'))
    hole.add_card(Card('10', 'Diamond'))
    hole.add_card(Card('10', 'Spade'))
    hole.add_card(Card('Q', 'Diamond'))
    return hole

def two_pair():
    hole = Hole()
    hole.add_card(Card('2', 'Club'))
    hole.add_card(Card('2', 'Diamond'))
    hole.add_card(Card('8', 'Heart'))
    hole.add_card(Card('8', 'Club'))
    hole.add_card(Card('10', 'Diamond'))
    hole.add_card(Card('10', 'Spade'))
    hole.add_card(Card('Q', 'Diamond'))
    return hole

def straight():
    hole = Hole()
    hole.add_card(Card('A', 'Club'))
    hole.add_card(Card('9', 'Club'))
    hole.add_card(Card('10', 'Club'))
    hole.add_card(Card('J', 'Club'))
    hole.add_card(Card('Q', 'Club'))
    hole.add_card(Card('K', 'Heart'))
    hole.add_card(Card('A', 'Heart'))
    return hole

def straight_flush():
    hole = Hole()
    hole.add_card(Card('A', 'Heart'))
    hole.add_card(Card('9', 'Club'))
    hole.add_card(Card('10', 'Club'))
    hole.add_card(Card('J', 'Club'))
    hole.add_card(Card('Q', 'Club'))
    hole.add_card(Card('K', 'Club'))
    hole.add_card(Card('A', 'Club'))
    return hole

def full_house():
    hole = Hole()
    hole.add_card(Card('A', 'Heart'))
    hole.add_card(Card('A', 'Club'))
    hole.add_card(Card('A', 'Diamond'))
    hole.add_card(Card('J', 'Club'))
    hole.add_card(Card('J', 'Heart'))
    hole.add_card(Card('K', 'Club'))
    hole.add_card(Card('10', 'Club'))
    return hole

def flush():
    hole = Hole()
    hole.add_card(Card('A', 'Heart'))
    hole.add_card(Card('9', 'Club'))
    hole.add_card(Card('2', 'Club'))
    hole.add_card(Card('J', 'Club'))
    hole.add_card(Card('3', 'Club'))
    hole.add_card(Card('K', 'Club'))
    hole.add_card(Card('4', 'Club'))
    return hole

def high_card():
    hole = Hole()
    hole.add_card(Card('8', 'Heart'))
    hole.add_card(Card('9', 'Club'))
    hole.add_card(Card('2', 'Club'))
    hole.add_card(Card('J', 'Diamond'))
    hole.add_card(Card('3', 'Diamond'))
    hole.add_card(Card('K', 'Club'))
    hole.add_card(Card('4', 'Club'))
    return hole

if __name__ == '__main__':
    main()
