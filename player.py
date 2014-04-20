import card_set
import chip_stack
import hand_scorer

class Player(object):
    def __init__(self, name, starting_stack_amount):
        self.name = name
        self.stack = chip_stack.ChipStack(starting_stack_amount)
        self.hole = card_set.Hole()
        self.game_state = None

        # Set a player's activity state during a round.
        self.active = True

        # Set a player's calling state during a round.
        self.caller = False

        # Whether a player's out of money and can't play any more games.
        self.bust = False

        # How much I have in the pot this round so far.
        self.bet_amount = 0

    def __str__(self):
        result = ""
        result += "Name: %s\n" % self.name
        result += str(self.stack) + "\n"
        result += str(self.hole) + "\n"
        return result

    def reset_for_hand(self):
        self.active = True

    def reset_for_round(self):
        self.caller = False
        self.bet_amount = 0

    def set_active(self, bool):
        self.active = bool

    def set_game_state(self, game_state):
        self.game_state = game_state

    def accept_card(self, card):
        self.hole.add_card(card)

    def muck_cards(self):
        self.hole.reset()

    def act(self):
        """ A naive player that always calls. This is where the poker AI
        would go. One could also have some user input code here."""
        self.call()
        print 'Pot is now: %d' % (self.game_state.pot.amount)

    def call(self):
        if self.game_state.current_bet:
            to_call = self.game_state.current_bet.amount - self.bet_amount
            bet_amount = self.game_state.current_bet.amount
        else:
            to_call = 0
            bet_amount = 0
        print '%s calls the bet of %d with %s' % (self.name,
                                                  bet_amount,
                                                  to_call)
        self.stack.emit(self.game_state.pot, to_call)
        self.caller = True

    def bet(self, amount):
        print '%s bets %d' % (self.name, amount)
        self.bet_amount = amount
        self.stack.emit(self.game_state.pot, amount)
        self.game_state.current_bet = Bet(self, amount)
        self.game_state.reset_callers()

    def fold(self):
        self.active = False
        self.muck_cards()

    def best_hand(self):
        return hand_scorer.HandScorer(
            card_set.Hand(self.game_state.board, self.hole)).best_hand()


class Bet(object):

    def __init__(self, player, amount):
        self.player = player
        self.amount = amount
