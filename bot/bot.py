from blackjack import game
import os
import tqdm
import random
from bot import visualize

NUM_ROUNDS = 10000000

rules = game.Rules()
shoe = game.Shoe(rules.num_decks, rules.reshuffle_at)
count = game.Count()
states = []
N = {}
Q = {}


def get_state(hand1, upcard):
    hand_score = hand1.score()
    is_soft = hand1.is_soft()
    dealer_score = game.CARD_SCORES[upcard]

    return hand_score, is_soft, dealer_score

def policy(state):
    choice = ""

    if random.random() <= e:
        choice = random.choice(["hit", "stand"])
        states.append((state, choice))
        return choice

    Q_hit = Q.get((state, "hit"), 0)
    Q_stand = Q.get((state, "stand"), 0)

    if Q_hit > Q_stand:
        choice = "hit"
        states.append((state, choice))
        return choice

    elif Q_hit < Q_stand:
        choice = "stand"
        states.append((state, choice))
        return choice

    else:
        choice = random.choice(["hit", "stand"])
        states.append((state, choice))
        return choice


def agent():
    total_outcome = 0
    current_round = 0
    global e
    global states
    live = visualize.LiveView()

    for i in tqdm.tqdm(range(NUM_ROUNDS)):
        current_round += current_round
        if current_round < NUM_ROUNDS / 2:
            e = 0.1
        elif current_round >= NUM_ROUNDS / 2:
            e = 0.01
        round = game.Round(rules, shoe, count, get_state, policy)
        outcome = round.play()
        for state in states:
            N[state] = N.get(state, 0) + 1
            Q[state] = Q.get(state, 0) + (outcome - Q.get(state, 0)) / N[state]
        states = []
        total_outcome += outcome
        average_outcome = total_outcome / NUM_ROUNDS
        if shoe.shuffle():
            count.reset()
        live.update(Q, i)
    live.finish(Q, NUM_ROUNDS)

    os.system("cls")
    print(f"-=OUTCOME=-")
    print(f"Average Profit: ${average_outcome:,}")
    print(f"Total Profit: ${total_outcome:,}")

if __name__ == "__main__":
    agent()