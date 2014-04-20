import chip_stack
import card_set
import game_state
import hand_scorer

class Game(object):

    def __init__(self, players):
        assert len(players) > 1
        self.deck = card_set.Deck(1)
        self.board = card_set.Board(self.deck)

        self.players = players

        # Arbitrarily set player 0 as initial dealer
        self.order = self.players

        self.pot = chip_stack.ChipStack(0)

        self.game_state = game_state.GameState(self.players,
                                               self.pot,
                                               self.board)

    def play(self, num_hands):
        for player in self.players:
            player.set_game_state(self.game_state)

        for x in range(num_hands):
            self.deck.reset()
            self.deal()
            self.play_hand()
            if len(self.remaining_players()) < 2:
                break
            [player.reset_for_hand() for player in self.players]

    def update_deal_order(self, new_dealer=False):
        """ Update deal_order, taking into account busted
        and folded players. new_dealer=True indicates that there is a new
        hand and that the button goes to the next player. """

        # Remove busted players and reactivate the rest
        self.order = [x for x in self.order if not x.bust]
        [x.set_active(True) for x in self.order]
        # Rotate the list if there is a new dealer
        if new_dealer:
            self.order = self.order[-1:] + self.order[:-1]

    def good(self):
        """ 'good' means that all players have either called or folded.
        """
        return not any([x.active and not x.caller for x in self.order])

    def active_players(self):
        return [x for x in self.order if x.active]

    def remaining_players(self):
        return [x for x in self.order if not x.bust]

    def deal(self):
        """ Deal two cards to each player.
        """
        for x in range(2):
            for player in self.order:
                player.accept_card(self.deck.deal())

    def play_hand(self):
        """ Play a single hand.
        """
        print '---HAND---'
        print 'Player state:'
        for player in self.players:
            print str(player)
        rounds = ['first', 'flop', 'river', 'turn']
        for round in rounds:
            if len(self.active_players()) > 1:
                self.board.deal_next_round()
            else:
                break
            print "Board is:\n%s" % self.board
            self.play_round(round)
            [player.reset_for_round() for player in self.players]
            self.game_state.current_bet = None

        for player in self.active_players():
            print '%s has a %s' % (player.name, player.best_hand())
        winner = self.find_winning_player()

        print str(winner.name) + ' wins the pot of size: ' + str(self.pot)

        winner.stack.absorb_entire_stack(self.pot)

        # Kick out busted players
        for player in self.active_players():
            if player.stack.amount == 0:
                player.bust = True

        # Clean up
        [player.muck_cards() for player in self.players]
        self.board.reset()
        self.update_deal_order(True)

    def play_round(self, round):
        """ Do a round of betting/folding.
        """
        print 'Round of betting: %s' % round
        if round == 'first':
            self.order[0].bet(self.game_state.small_blind)
            self.order[1].bet(self.game_state.big_blind)
            if len(self.order) > 2:
                [x.act() for x in self.order[2:]]

        while not self.good():
            [x.act() for x in self.order if x.active and not x.caller]

    def find_winning_player(self):
        """ Look at each player's hand, find which is the best.
        """
        # Currently ignores if there is a tie.
        winner = reduce(lambda x,y : (x.best_hand() > y.best_hand() and
                                      [x] or [y])[0],
                        self.active_players())
        return winner
