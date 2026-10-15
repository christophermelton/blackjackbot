from blackjack import game
import os
import tqdm

NUM_ROUNDS = 10

rules = game.Rules()
shoe = game.Shoe(rules.num_decks, rules.reshuffle_at)
count = game.Count()

def get_state(hand1, upcard):
    hand_score = hand1.score()
    is_soft = hand1.is_soft()
    dealer_score = game.CARD_SCORES[upcard]

    return hand_score, is_soft, dealer_score

def action(state):
    return "stand"

def agent():
    total_outcome = 0

    for _ in (range(NUM_ROUNDS)):
        round = game.Round(rules, shoe, count, get_state, action)
        outcome = round.play()
        total_outcome += outcome
        average_outcome = total_outcome / NUM_ROUNDS
        print(get_state(round.hand_1, round.hand_d.upcard()))
        if shoe.shuffle():
            count.reset()

    #os.system("cls")
    print(f"-=OUTCOME=-")
    print(f"Average Profit: ${average_outcome:,}")
    print(f"Total Profit: ${total_outcome:,}")

if __name__ == "__main__":
    agent()