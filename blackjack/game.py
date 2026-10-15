import random
from dataclasses import dataclass

CARD_IDS = {
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "T",
    11: "J",
    12: "Q",
    13: "K",
    14: "A",
}
CARD_SCORES = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11,
}
DECK = list(CARD_SCORES) * 4

@dataclass(frozen=True)
class Rules:
    # shoe
    num_decks: int = 6
    reshuffle_at: float = 0.25

    # dealer
    dealer_hits_soft_17: bool = True

    # player
    blackjack_payout: float = 1.5
    max_splits: int = 4
    can_split_aces: bool = False

class Shoe:
    def __init__(self, num_decks, reshuffle_at):
        self.cards = DECK * num_decks
        self.full_shoe = len(self.cards)
        random.shuffle(self.cards)
        self.num_decks = num_decks
        self.reshuffle_at = reshuffle_at

    def deal(self):
        return self.cards.pop()

    def shuffle(self):
        if len(self.cards) <= self.full_shoe * self.reshuffle_at:
            self.cards = DECK * self.num_decks
            random.shuffle(self.cards)
            return True
        return False

class Count:
    def __init__(self):
        self.count = 0

    def view(self, card_dealt):
        if card_dealt in("A", "K", "Q", "J", "T"):
            self.count -= 1
        if card_dealt in("6", "5", "4", "3", "2"):
            self.count += 1
        return self.count

    def reset(self):
        self.count = 0

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def score(self):
        self.h_score = 0
        self.num_aces = 0

        for card in self.cards:
            if card == "A":
                self.num_aces += 1

        for card in self.cards:
            self.h_score += CARD_SCORES[card]

        while self.num_aces >= 1 and self.h_score > 21:
            self.num_aces -= 1
            self.h_score -= 10
        return self.h_score

    def is_bust(self):
        self.score()
        if self.h_score > 21:
            return True
        else:
            return False

    def is_soft(self):
        self.score()
        if self.num_aces == 0:
            return False
        else:
            return True
        
    def is_blackjack(self):
        self.score()
        if len(self.cards) == 2 and self.h_score == 21:
            return True
        else:
            return False

    def upcard(self):
        return self.cards[0]

    def holecard(self):
        return self.cards[1]

class Round:
    def __init__(self, rules, shoe, count, decision):
        self.rules = rules
        self.shoe = shoe
        self.count = count
        self.decision = decision
        self.hand_1 = Hand()
        self.hand_d = Hand()

        for card in range(2):
            self.hand_1.add_card(self.shoe.deal())
            self.count.view(self.hand_1.cards[card])
            self.hand_d.add_card(self.shoe.deal())
        self.count.view(self.hand_d.upcard())

    def check_blackjack(self):
        if self.hand_1.is_blackjack() and self.hand_d.is_blackjack():
            self.count.view(self.hand_d.holecard())
            return 0
        
        elif self.hand_1.is_blackjack():
            self.count.view(self.hand_d.holecard())
            return self.rules.blackjack_payout
        
        elif self.hand_d.is_blackjack():
            self.count.view(self.hand_d.holecard())
            return -1

        else:
            return None

    def choice(self):
        while True:
            if self.hand_1.is_bust():
                break

            answer = self.decision(self.hand_1, self.hand_d.upcard(), self.count.count)

            if answer == "hit":
                card = self.shoe.deal()
                self.hand_1.add_card(card)
                self.count.view(card)

            elif answer == "stand":
                break

    def dealer_hits(self):
        score = self.hand_d.score()
        if score < 17:
            return True
        if score == 17 and self.hand_d.is_soft() and self.rules.dealer_hits_soft_17:
            return True
        return False

    def dealer_turn(self):
        while self.dealer_hits():
            card = self.shoe.deal()
            self.hand_d.add_card(card)
            self.count.view(card)

    def who_wins(self):
        score_1 = self.hand_1.score()
        score_d = self.hand_d.score()

        if self.hand_1.is_bust():
            return -1

        elif self.hand_d.is_bust():
            return 1

        elif score_1 == score_d:
            return 0

        elif score_1 > score_d:
            return 1

        elif score_1 < score_d:
            return -1

    def play(self):
        blackjack = self.check_blackjack()

        if blackjack != None:
            return blackjack

        self.choice()
        if not self.hand_1.is_bust():
            self.dealer_turn()
        self.count.view(self.hand_d.holecard())
        return self.who_wins()