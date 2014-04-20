import card_set

types = ['straight_flush', 'four_of_a_kind', 'full_house',
         'flush', 'straight', 'three_of_a_kind', 'two_pair',
         'pair', 'high_card']

def find_value(card):
    return card_set.values.index(card.value)

class HandScorer(object):

    def __init__(self, hand):
        self.hand = hand

    def find_sets(self):
        """ Find card sets by creating a histogram of card values.
        """
        card_hist = {}
        for card in self.hand.card_list:
            if card.value not in card_hist.keys():
                card_hist[card.value] = 1
            else:
                card_hist[card.value] += 1

        # Remove trivial sets
        sets = dict([x for x in card_hist.items() if x[1] != 1])

        kickers = [x[0] for x in card_hist.items() if x[1] == 1]

        return sets, kickers

    def find_set_score(self, set_length, num_sets):
        sets, kickers = self.find_sets()
        my_sets = []
        for key, value in sets.iteritems():
            if value == set_length:
                my_sets.append(key)
        if len(my_sets) >= num_sets:
            # Find the score of the set
            set_score = [card_set.values.index(x) for x in my_sets]
            set_score.sort(reverse=True)
            set_score = set_score[0:num_sets]

            # Find the scores for the hand kickers
            kickers_score = [card_set.values.index(x) for x in kickers]

            # Extend the kickers with the left-over sets
            all_set_score = [card_set.values.index(x) for x in sets]
            kickers_score.extend(all_set_score[num_sets:])

            kickers_score.sort(reverse=True)
            kickers_score = kickers_score[0:5-set_length*num_sets]
            return set_score + kickers_score
        else:
            return -1

    def find_runs(self, cards, run_length):
        # Remove duplicates
        hand_set = list(set(cards))
        hand_length = len(hand_set)
        hand_set.sort()
        runs = []
        for i in range(hand_length - run_length + 1):
            for j in range(run_length - 1):
                if hand_set[i+j] + 1 != hand_set[i+j+1]:
                    break
                if j == run_length - 2:
                    runs.append(hand_set[i:i+run_length])

        return runs

    def find_run_score(self, cards, run_length):
        runs = self.find_runs(cards, run_length)
        if len(runs) > 0:
            maxes = []
            for set in runs:
                maxes.append(max([find_value(x) for x in set]))
            return [max(maxes)]
        else:
            return -1

    def find_flush(self, cards):
        card_hist = {}
        for card in cards:
            if card.suit not in card_hist.keys():
                card_hist[card.suit] = [card]
            else:
                card_hist[card.suit] += [card]
        flush = [v for v in card_hist.values() if len(v) >= 5]
        if flush:
            return flush[0]
        else:
            return flush

    def find_flush_score(self, cards):
        flush = self.find_flush(cards)
        if flush:
            flush_score = max([find_value(card) for card in flush])
            return [flush_score]
        return -1

    def full_house(self):
        full_house_score = -1
        pair_score = self.find_set_score(2,1)
        three_of_a_kind_score = self.find_set_score(3,1)
        if pair_score != -1 and three_of_a_kind_score != -1:
            full_house_score = [three_of_a_kind_score[0], pair_score[0]]
        return full_house_score

    def straight_flush(self):
        flush = self.find_flush(self.hand.card_list)
        if flush != -1:
            scores = self.find_run_score(flush, 5)
            if scores != -1:
                return [max(scores)]
        return -1

    def high_card(self):
        card_list = [find_value(x) for x in
                     self.hand.card_list]
        card_list.sort(reverse=True)
        return card_list[:5]

    def best_hand(self):
        """ Return the HandRank object for the Hand containing the best
        containing the hand type and score for the best available hand.
        """
        hands = {
            'high_card': self.high_card,
            'pair' : lambda: self.find_set_score(2, 1),
            'two_pair' : lambda: self.find_set_score(2, 2),
            'three_of_a_kind' : lambda: self.find_set_score(3, 1),
            'four_of_a_kind' : lambda: self.find_set_score(4, 1),
            'straight' : lambda: self.find_run_score(self.hand.card_list, 5),
            'flush' : lambda: self.find_flush_score(self.hand.card_list),
            'full_house' : self.full_house,
            'straight_flush' : self.straight_flush
        }

        for type in types:
            scores = hands[type]()
            if scores != -1:
                return HandRank(type, scores)
        # we shouldn't get here
        return HandRank('high_card', 0)


class HandRank(object):
    def __init__(self, type, scores):
        self.type = type
        self.scores = scores

    def __cmp__(self, other):
        result = cmp(types.index(other.type), types.index(self.type))
        if result:
            return result
        else:
            assert len(self.scores) == len(other.scores)
            for ss, os in zip(self.scores, other.scores):
                if ss != os:
                    return ss - os
            return 0

    def __str__(self):
        return '%s with a score of %s' % (self.type, self.scores)
