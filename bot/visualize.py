"""
DISCLAIMER
THIS SCRIPT WAS WRITTEN BY CLAUDE (AI)
I USE THIS SCRIPT TO VISUALIZE MY WORK
"""
import os

import matplotlib.pyplot as plt

UPCARDS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]   # 11 = ace
HARD_TOTALS = range(4, 22)
SOFT_TOTALS = range(12, 22)
COLOR = {"H": 1, "?": 0.5, "S": 0}   # green, yellow, red
PANELS = [(HARD_TOTALS, False, "Hard totals"), (SOFT_TOTALS, True, "Soft totals")]


def policy_letter(Q, state):
    q_hit = Q.get((state, "hit"), 0)
    q_stand = Q.get((state, "stand"), 0)
    if q_hit > q_stand:
        return "H"
    if q_hit < q_stand:
        return "S"
    return "?"


def make_grid(Q, totals, soft):
    return [[policy_letter(Q, (total, soft, upcard)) for upcard in UPCARDS] for total in totals]


def upcard_label(upcard):
    return "A" if upcard == 11 else str(upcard)


def build_figure():
    """Create the hard and soft grids once; return the figure and the parts that change."""
    fig, axes = plt.subplots(
        2, 1, figsize=(6, 11), gridspec_kw={"height_ratios": [len(HARD_TOTALS), len(SOFT_TOTALS)]}
    )
    panels = []
    for ax, (totals, soft, title) in zip(axes, PANELS):
        blank = [[COLOR["?"]] * len(UPCARDS) for _ in totals]
        image = ax.imshow(blank, cmap="RdYlGn", vmin=0, vmax=1)
        texts = [[ax.text(c, r, "?", ha="center", va="center") for c in range(len(UPCARDS))]
                 for r in range(len(totals))]
        ax.set_xticks(range(len(UPCARDS)))
        ax.set_xticklabels([upcard_label(u) for u in UPCARDS])
        ax.set_yticks(range(len(totals)))
        ax.set_yticklabels(list(totals))
        ax.set_xlabel("Dealer upcard")
        ax.set_ylabel("Your total")
        ax.set_title(title)
        panels.append({"totals": totals, "soft": soft, "image": image, "texts": texts})
    heading = fig.suptitle("Learned policy")
    fig.tight_layout()
    return fig, panels, heading


def fill_figure(panels, Q):
    """Write the current policy into the existing squares and letters."""
    for panel in panels:
        grid = make_grid(Q, panel["totals"], panel["soft"])
        panel["image"].set_data([[COLOR[letter] for letter in line] for line in grid])
        for text_row, line in zip(panel["texts"], grid):
            for text, letter in zip(text_row, line):
                text.set_text(letter)


def save_figure(fig, filename):
    folder = os.path.dirname(filename)
    if folder:
        os.makedirs(folder, exist_ok=True)
    fig.savefig(filename)


def show_policy(Q, filename="data/policy.png"):
    """Save the hard and soft policy grids as one image."""
    fig, panels, heading = build_figure()
    fill_figure(panels, Q)
    save_figure(fig, filename)
    plt.close(fig)


class LiveView:
    """A window that redraws the policy every `every` rounds while training runs."""

    def __init__(self, every=50_000):
        self.every = every
        plt.ion()
        self.fig, self.panels, self.heading = build_figure()
        plt.show(block=False)
        plt.pause(0.001)

    def update(self, Q, rounds):
        """Call once per round; it only redraws every `every` rounds."""
        if rounds % self.every:
            return
        self.redraw(Q, rounds)

    def redraw(self, Q, rounds):
        fill_figure(self.panels, Q)
        self.heading.set_text(f"Learned policy after {rounds:,} rounds")
        self.fig.canvas.draw_idle()
        plt.pause(0.001)

    def finish(self, Q, rounds, filename="data/policy.png"):
        """Draw the final policy, save it, and keep the window open until you close it."""
        self.redraw(Q, rounds)
        save_figure(self.fig, filename)
        plt.ioff()
        plt.show()
