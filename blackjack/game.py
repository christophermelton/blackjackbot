import random

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

PAYOUT_MULTS = {
    "p_blackjack": 2.5,
    "win": 2.0,
    "d_bust": 2.0,
    "shove": 1.0,
    "d_blackjack": 0.0,
    "lose": 0.0,
    "p_bust": 0.0
}

def get_random_card():
        x = CARD_IDS[random.randint(2,14)]
        return x  

class Game:
    def __init__(self, player_cards, dealer_cards, player_score, dealer_score):
        self.player_cards = player_cards
        self.dealer_cards = dealer_cards
        self.player_score = player_score
        self.dealer_score = dealer_score
        self.winstate = 0

    def deal_card(self, w):
        if w == "p":
            who = self.player_cards
        if w == "d":
            who = self.dealer_cards
        card = get_random_card()
        who.append(card)
        return

    def hit_or_stand(self, who, choice=None):
        self.dealer_score
        if who == "p":
            while True:
                if choice == True:
                    self.deal_card("p")
                    self.update_score()
                    return True
                if choice == False:
                    return False
        if who == "d":
            while True:
                self.update_score()
                if self.dealer_score < 17:
                    self.deal_card("d")
                    return True
                elif self.dealer_score >= 17:
                    return False

    def gamestate(self):
        return self.player_cards, self.dealer_cards, self.player_score, self.dealer_score
    
    def update_score(self):
        self.player_score
        self.dealer_score
        p_score = 0
        d_score = 0
        p_num_aces = 0
        d_num_aces = 0

        for i in self.player_cards:
            p_score += CARD_SCORES[i]
            if i == "A":
                p_num_aces += 1

        while True:
                if p_score > 21 and p_num_aces != 0:
                    p_num_aces -= 1
                    p_score -= 10
                else:
                    break

        for i in self.dealer_cards:
                d_score += CARD_SCORES[i]
                if i == "A":
                    d_num_aces += 1

        while True:
            if d_score > 21 and d_num_aces != 0:
                d_num_aces -= 1
                d_score -= 10
            else:
                break
        
        # set scores
        self.player_score = p_score
        self.dealer_score = d_score
        return

    def does_bust(self, w):
        if w == "p":
            who = self.player_score
        if w == "d":
            who = self.dealer_score
            
        if who > 21:
            return True
        return False

    def outcome(self):
        if self.player_score > 21:
            # player busts
            self.winstate = "p_bust"
        elif self.dealer_score > 21:
            # dealer busts
            self.winstate = "d_bust"
        elif self.dealer_score > self.player_score:
            # dealer beats player
            self.winstate = "lose"
        elif self.dealer_score == self.player_score:
            # shove
            self.winstate = "shove"
        elif self.dealer_score < self.player_score:
            # player wins
            self.winstate = "win"
        return self.gamestate(), self.winstate
        
    def play_hand(self, choice):
        self.player_bust = False

        # deal cards
        for i in range(2):
            self.deal_card("p")
            self.deal_card("d")

        self.update_score()

        if self.player_score == 21 and self.dealer_score == 21:
            self.winstate = "shove"
            return
        elif self.player_score == 21:
            self.winstate = "p_blackjack"
            return
        elif self.dealer_score == 21:
            self.winstate = "d_blackjack"
            return

        # players turn
        while True:
            if self.does_bust("p") != True:
                if self.hit_or_stand("p", choice(self)) == False:
                    break
            else:
                self.player_bust = True
                break
            
        # dealers turn
        if self.player_bust == False:
            while True:
                self.update_score()

                if self.does_bust("d") != True:

                    if self.hit_or_stand("d") == False:
                        break
                else:
                    break
        self.outcome()
        return