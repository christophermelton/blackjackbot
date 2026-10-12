import game
import os

NUM_HANDS = 1000000

def decide_hit_or_stand(g):
    return True

def main():
    counts = {}
    total_profit = 0
    total_games = 0

    for _ in range(NUM_HANDS):
        g = game.Game([], [], 0, 0)
        g.play_hand(decide_hit_or_stand)

        counts[g.winstate] = counts.get(g.winstate, 0) + 1
        total_profit += game.PAYOUT_MULTS[g.winstate] - 1
        total_games += 1

    os.system("cls")
    print(f"{counts}\n")
    print("-=RESULTS=-")
    print(f"Games: {total_games:,}")
    print(f"Player blackjacks: {counts["p_blackjack"]:,}")
    #print(f"Wins: {counts["win"]:,}")
    print(f"Shoves: {counts["shove"]:,}")
    print(f"Dealer blackjacks: {counts["d_blackjack"]:,}")
    #print(f"Losses: {counts["lose"]:,}")
    print(f"Player busts: {counts["p_bust"]:,}")
    #print(f"Dealer busts: {counts["d_bust"]:,}")
    print(f"Average profit per hand: ${total_profit / NUM_HANDS:,}")
    print(f"Total profit: ${total_profit:,}")

main()