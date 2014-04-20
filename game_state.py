class GameState(object):
    """ Contains the information that is public to all players.
    """
    def __init__(self, players, pot, board):
        self.players = players
        self.pot = pot
        self.board = board
        self.big_blind = 2
        self.small_blind = 1

    def __str__(self):
        result = ""
        for player in self.players:
            result += str(player) + '\n'
        result += str(self.pot) + '\n'
        result += str(self.board) + '\n'
        return result

    def reset_callers(self):
        """ Reset the callers during a round of betting.
        """
        for player in self.players:
            player.caller = False
