import game
import os
import tqdm

NUM_ROUNDS = 10000000

rules = game.Rules()
shoe = game.Shoe(rules.num_decks, rules.reshuffle_at)
count = game.Count()

def always_stand(hand, upcard, running_count):
    return "stand"

def play():
    total_outcome = 0

    for _ in tqdm.tqdm(range(NUM_ROUNDS)):
        round = game.Round(rules, shoe, count, always_stand)
        outcome = round.play()
        total_outcome += outcome
        average_outcome = total_outcome / NUM_ROUNDS
        if shoe.shuffle():
            count.reset()

    os.system("cls")
    print(f"-=OUTCOME=-")
    print(f"Average Profit: ${average_outcome}")
    print(f"Total Profit: ${total_outcome}")

play()