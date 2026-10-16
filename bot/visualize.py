"""
DISCLAIMER
THIS SCRIPT WAS WRITTEN BY CLAUDE (AI)
I USE THIS SCRIPT TO VISUALIZE MY WORK
"""
import os

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

UPCARDS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]   # 11 = ace
HARD_TOTALS = range(4, 22)
SOFT_TOTALS = range(12, 22)
COLOR = {"H": 1, "?": 0.5, "S": 0}   # green, yellow, red
ROWS = [(HARD_TOTALS, False, "hard totals"), (SOFT_TOTALS, True, "soft totals")]
TOTAL_CELLS = (len(HARD_TOTALS) + len(SOFT_TOTALS)) * len(UPCARDS)


def policy_letter(Q, state):
    q_hit = Q.get((state, "hit"), 0)
    q_stand = Q.get((state, "stand"), 0)
    if q_hit > q_stand:
        return "H"
    if q_hit < q_stand:
        return "S"
    return "?"


def basic_letter(state):
    """Hit/stand basic strategy: 6 decks, dealer hits soft 17, no doubling, splitting or surrender."""
    total, soft, upcard = state
    if soft:
        if total <= 17:
            return "H"
        if total == 18:
            return "H" if upcard >= 9 else "S"
        return "S"
    if total <= 11:
        return "H"
    if total == 12:
        return "S" if 4 <= upcard <= 6 else "H"
    if total <= 16:
        return "S" if upcard <= 6 else "H"
    return "S"


def make_grid(letter_fn, totals, soft):
    return [[letter_fn((total, soft, upcard)) for upcard in UPCARDS] for total in totals]


def upcard_label(upcard):
    return "A" if upcard == 11 else str(upcard)


def setup_axes(ax, totals, title):
    ax.set_xticks(range(len(UPCARDS)))
    ax.set_xticklabels([upcard_label(u) for u in UPCARDS])
    ax.set_yticks(range(len(totals)))
    ax.set_yticklabels(list(totals))
    ax.set_xlabel("Dealer upcard")
    ax.set_ylabel("Your total")
    ax.set_title(title)


def draw_letters(ax, grid):
    ax.imshow([[COLOR[letter] for letter in line] for line in grid], cmap="RdYlGn", vmin=0, vmax=1)
    return [[ax.text(c, r, letter, ha="center", va="center") for c, letter in enumerate(line)]
            for r, line in enumerate(grid)]


def build_figure():
    """Learned policy on the left, basic strategy on the right; return the figure and the parts that change."""
    fig, axes = plt.subplots(
        2, 2, figsize=(9.5, 11.5), gridspec_kw={"height_ratios": [len(HARD_TOTALS), len(SOFT_TOTALS)]}
    )
    panels = []
    for (learned_ax, basic_ax), (totals, soft, name) in zip(axes, ROWS):
        basic = make_grid(basic_letter, totals, soft)
        basic_texts = draw_letters(basic_ax, basic)
        setup_axes(basic_ax, totals, f"Basic strategy: {name}")

        blank = [["?"] * len(UPCARDS) for _ in totals]
        texts = draw_letters(learned_ax, blank)
        image = learned_ax.get_images()[0]
        outlines = [[learned_ax.add_patch(Rectangle((c - 0.5, r - 0.5), 1, 1, fill=False,
                                                    edgecolor="black", linewidth=2.5, visible=False))
                     for c in range(len(UPCARDS))] for r in range(len(totals))]
        setup_axes(learned_ax, totals, f"Learned: {name}")
        panels.append({"totals": totals, "soft": soft, "basic": basic, "basic_texts": basic_texts,
                       "image": image, "texts": texts, "outlines": outlines})
    heading = fig.suptitle("Learned policy vs basic strategy")
    fig.text(0.5, 0.01, "Outlined squares differ from basic strategy", ha="center")
    fig.tight_layout(rect=(0, 0.02, 1, 0.95))
    return fig, panels, heading


def show_basic_letters(panels, visible):
    """The basic strategy side never changes, so the live window skips its letters to redraw faster."""
    for panel in panels:
        for row in panel["basic_texts"]:
            for text in row:
                text.set_visible(visible)


def fill_figure(panels, Q):
    """Write the current policy into the learned grids; return how many cells match basic strategy."""
    matches = 0
    for panel in panels:
        grid = make_grid(lambda state: policy_letter(Q, state), panel["totals"], panel["soft"])
        panel["image"].set_data([[COLOR[letter] for letter in line] for line in grid])
        for r, line in enumerate(grid):
            for c, letter in enumerate(line):
                panel["texts"][r][c].set_text(letter)
                same = letter == panel["basic"][r][c]
                panel["outlines"][r][c].set_visible(not same)
                matches += same
    return matches


def save_figure(fig, filename):
    folder = os.path.dirname(filename)
    if folder:
        os.makedirs(folder, exist_ok=True)
    fig.savefig(filename)


def show_policy(Q, filename="data/policy.png"):
    """Save the learned policy next to basic strategy as one image."""
    fig, panels, heading = build_figure()
    matches = fill_figure(panels, Q)
    heading.set_text(f"Learned policy vs basic strategy\n{matches} of {TOTAL_CELLS} cells match")
    save_figure(fig, filename)
    plt.close(fig)


class LiveView:
    """A window that redraws the policy every `every` rounds while training runs."""

    def __init__(self, every=50_000):
        self.every = every
        plt.ion()
        self.fig, self.panels, self.heading = build_figure()
        show_basic_letters(self.panels, False)
        plt.show(block=False)
        plt.pause(0.001)

    def update(self, Q, rounds):
        """Call once per round; it only redraws every `every` rounds."""
        if rounds % self.every:
            return
        self.redraw(Q, rounds)

    def redraw(self, Q, rounds):
        matches = fill_figure(self.panels, Q)
        self.heading.set_text(f"Learned policy after {rounds:,} rounds\n{matches} of {TOTAL_CELLS} cells match basic strategy")
        self.fig.canvas.draw_idle()
        plt.pause(0.001)

    def finish(self, Q, rounds, filename="data/policy.png"):
        """Draw the final policy, save it, and keep the window open until you close it."""
        show_basic_letters(self.panels, True)
        self.redraw(Q, rounds)
        save_figure(self.fig, filename)
        plt.ioff()
        plt.show()
