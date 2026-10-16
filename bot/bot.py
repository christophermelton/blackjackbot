from blackjack import game
import os
import tqdm

NUM_ROUNDS = 1

rules = game.Rules()
shoe = game.Shoe(rules.num_decks, rules.reshuffle_at)
count = game.Count()
states = []

def get_state(hand1, upcard):
    hand_score = hand1.score()
    is_soft = hand1.is_soft()
    dealer_score = game.CARD_SCORES[upcard]

    return hand_score, is_soft, dealer_score

def policy(state):
    choice = ""

    if state[0] >= 20:
        choice = "stand"
        states.append(state)
        print(states)
        print(choice)

        return choice
    choice = "hit"
    states.append(state)
    print(states)
    print(choice)
    
    return choice

def agent():
    total_outcome = 0
    global states

    for _ in (range(NUM_ROUNDS)):
        round = game.Round(rules, shoe, count, get_state, policy)
        outcome = round.play()
        states = []
        total_outcome += outcome
        average_outcome = total_outcome / NUM_ROUNDS
        if shoe.shuffle():
            count.reset()

    #os.system("cls")
    print(f"-=OUTCOME=-")
    print(f"Average Profit: ${average_outcome:,}")
    print(f"Total Profit: ${total_outcome:,}")

if __name__ == "__main__":
    agent()