import random

suits = ['Club', 'Spade', 'Diamond', 'Heart']
values = [ '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

class Card(object):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __cmp__(self, card):
        return values.index(self.value) - values.index(card.value)

    def __str__(self):
        return str([self.value, self.suit])

    def __add__(self, num):
        try:
            return Card(values[values.index(self.value) + num], self.suit)
        except IndexError:
            return NullCard()

class NullCard(Card):
    def __init__(self):
        pass

    def __cmp__(self, card):
        return False

class CardSet(object):
    def __init__(self, card_list=[]):
        self.card_list = card_list

    def add_card(self, card):
        self.card_list.append(card)

    def reset(self):
        self.card_list = []

    def __add__(self, card_set):
        return CardSet(self.card_list + card_set.card_list)

    def __str__(self):
        result = ""
        for card in self.card_list:
            result += str(card) + '\n'
        return result


class Deck(CardSet):
    def __init__(self, num_decks):
        CardSet.__init__(self)
        self.num_decks = num_decks
        self.reset()

    def deal(self):
        return self.card_list.pop()

    def reset(self):
        CardSet.reset(self)
        for i in range(self.num_decks):
            for suit in suits:
                for value in values:
                    self.card_list.append(Card(value, suit))
        random.shuffle(self.card_list)
        assert len(self.card_list) == 52 * self.num_decks


class Hand(CardSet):
    def __init__(self, board, hole):
        CardSet.__init__(self, (board + hole).card_list)

class DealableCardSet(CardSet):
    def __init__(self, deck):
        CardSet.__init__(self, [])
        self.deck = deck

class Board(DealableCardSet):
    def __init__(self, deck):
        DealableCardSet.__init__(self, deck)
        self.round_order = [lambda: None, self.flop, self.turn, self.river]
        self.next_round = 0

    def deal_next_round(self):
        self.round_order[self.next_round]()
        self.next_round = (self.next_round + 1) % len(self.round_order)

    def burn(self):
        """ Throw away a dealt card.
        """
        self.deck.deal()

    def flop(self):
        assert len(self.card_list) == 0
        self.burn()
        for x in range(3):
            self.add_card(self.deck.deal())

    def turn(self):
        assert len(self.card_list) == 3
        self.burn()
        self.add_card(self.deck.deal())

    def river(self):
        assert len(self.card_list) == 4
        self.burn()
        self.add_card(self.deck.deal())

class Hole(CardSet):
    def __init__(self):
        CardSet.__init__(self, [])
