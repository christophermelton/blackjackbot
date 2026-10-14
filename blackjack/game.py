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

class Round:
    def __init__(self):
        return