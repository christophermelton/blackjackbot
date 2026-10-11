import random
import os

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

player_cards = {}
dealer_cards = {}
player_score = 0
dealer_score = 0

def get_random_card():
    x = CARD_IDS[random.randint(2,14)]
    return x    

def deal_card(w):
    if w == "p":
        who = player_cards
    if w == "d":
        who = dealer_cards
    where = len(who)
    card = get_random_card()
    who[where] = card
    return

def hit_or_stand(who):
    global dealer_score
    if who == "p":
        while True:
            choice = input("Hit or stand? ")
            choice = choice.lower()
            if choice == "hit":
                deal_card("p")
                print_game()
                update_score()
                return True
            if choice == "stand":
                return False
    if who == "d":
        while True:
            update_score()
            if dealer_score < 17:
                deal_card("d")
                return True
            elif dealer_score >= 17:
                return False

def print_game():
    # clear terminal
    os.system("cls")

    # print player cards
    print(f"-=PLAYER=-")
    for i in range(len(player_cards)):
        print(f"{player_cards[i]} ", end="")
    print(f"")

    # print dealer cards
    print(f"-=DEALER=-")
    for i in range(len(dealer_cards)):
        print(f"{dealer_cards[i]} ", end="")
    print(f"")

def update_score():
    global player_score
    global dealer_score
    p_score = 0
    d_score = 0
    p_num_aces = 0
    d_num_aces = 0

    for i in player_cards.values():
        p_score += CARD_SCORES[i]
        if i == "A":
            p_num_aces += 1

    while True:
            if p_score > 21 and p_num_aces != 0:
                p_num_aces -= 1
                p_score -= 10
            else:
                break

    for i in dealer_cards.values():
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
    player_score = p_score
    dealer_score = d_score
    return

def does_bust(w, score):
    global player_score
    global dealer_score

    if w == "p":
        who = player_score
    if w == "d":
        who = dealer_score
        
    if who > 21:
        return True
    return False
    
def main():
    player_bust = False

    # deal cards
    for i in range(2):
        deal_card("p")
        deal_card("d")

    update_score()
    
    print_game()

    if player_score == 21:
        print(f"BLACKJACK!!!")

    # players turn
    while True:
        if does_bust("p", player_score) != True:
            
            if hit_or_stand("p") == False:
                break
        else:
            player_bust = True
            break
        
    # dealers turn
    if player_bust == False:
        while True:
            update_score()

            if does_bust("d", dealer_score) != True:
                print_game()

                if hit_or_stand("d") == False:
                    break
            else:
                print_game()
                break

    print(f"-=OUTCOME=-\nPlayer Score: {player_score}\nDealer Score: {dealer_score}")

    if dealer_score > 21:
        print(f"Dealer busts")
    elif player_score > 21:
        print(f"You bust :(")
    elif dealer_score > player_score:
        print(f"You lose :(")
    elif dealer_score == player_score:
        print(f"Shove")
    elif dealer_score < player_score:
        print(f"YOU WIN :)")

    return

main()