"""Figures for the ARC Prize 2026 paper-track writeup (team _hans).

All numbers are copied from our run records (see writeup.md); Figure 2 is a schematic.
Run: python make_figures.py  -> figures/*.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)

# Reference palette (light surface); categorical slots validated with validate_palette.js
SURF = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#8a8984"
GRID = "#e6e5e1"
BLUE = "#2a78d6"
BLUE_L = "#9ec5f4"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
NEUTRAL = "#c9c8c2"

def _register_avenir():
    """matplotlib only indexes the first (Bold) face of Avenir Next.ttc; extract Regular + Demi Bold."""
    src = "/System/Library/Fonts/Avenir Next.ttc"
    cache = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".fonts")
    try:
        from fontTools.ttLib import TTCollection
        from matplotlib import font_manager as fm
        os.makedirs(cache, exist_ok=True)
        coll = TTCollection(src)
        for idx, name in ((7, "AvenirNext-Regular.ttf"), (2, "AvenirNext-DemiBold.ttf")):
            out = os.path.join(cache, name)
            if not os.path.exists(out):
                coll.fonts[idx].save(out)
            fm.fontManager.addfont(out)
        return ["Avenir Next", "Avenir Next Demi Bold"]
    except Exception:
        return []


_FAMS = _register_avenir()

plt.rcParams.update({
    "font.family": ["Avenir Next", "Helvetica Neue", "DejaVu Sans"],
    "font.weight": "normal",
    "font.size": 10,
    "axes.edgecolor": GRID,
    "axes.labelcolor": INK2,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": SURF,
    "axes.facecolor": SURF,
    "savefig.facecolor": SURF,
})


W = 6.4   # inches; 1280 px at dpi 200, shown ~612 px wide in the Kaggle column -> 10 pt ~ 13 px


PDF_MODE = os.environ.get("FIG_PDF") == "1"   # PDF: no "Figure N." prefix (LaTeX numbers the figures)
if PDF_MODE:
    OUT = os.path.join(OUT, "pdf")
    os.makedirs(OUT, exist_ok=True)


def title(fig, text, sub=None, y=0.975):
    if PDF_MODE and text.startswith("Figure "):
        text = text.split(". ", 1)[1]
    fig.text(0.035, y, text, fontsize=12.5, fontweight="demibold", color=INK, va="top")
    if sub:
        fig.text(0.035, y - 0.052 * (6.0 / fig.get_figheight()), sub, fontsize=9.5, color=INK2,
                 va="top", linespacing=1.35)


def note(fig, text, y=0.012):
    fig.text(0.035, y, text, fontsize=8.5, color=MUTED, va="bottom", linespacing=1.35)


# ---------------------------------------------------------------- Figure 1
def fig1():
    vers = ["v1", "v2", "v13", "v30", "v31", "v32", "v33", "v34"]
    dates = ["10-01", "10-02", "10-14", "10-26", "10-27", "10-28", "10-31", "11-01"]
    subs = [[22.92], [46.39], [71.81, 68.75, 65.56, 70.83], [70.14], [70.28],
            [70.97, 72.64, 66.81], [73.89], [77.64]]
    tps = [120, 215, 315, 462, 498, 639, 639, 713]
    x = list(range(len(vers)))

    fig, (a, b) = plt.subplots(2, 1, figsize=(W, 5.6), sharex=True,
                               gridspec_kw={"height_ratios": [3, 1.5], "hspace": 0.1})
    fig.subplots_adjust(left=0.115, right=0.975, top=0.83, bottom=0.135)
    title(fig, "Figure 1. Doubling throughput barely moved the score",
          "Public leaderboard per submission (top) and Kaggle generation\n"
          "throughput (bottom). v13 to v32 use the same harness.")

    a.axvspan(1.6, 5.4, color="#f0efec", zorder=0)
    a.text(3.5, 36, "same harness:\n2× throughput,\nLB 69.2 → 70.1", ha="center",
           va="center", fontsize=9, color=INK2, linespacing=1.3)
    for xi, s in zip(x, subs):
        late = vers[xi] == "v34"
        hi = vers[xi] in ("v33", "v34")
        col = ORANGE if hi else BLUE
        if len(s) > 1:
            a.scatter([xi] * len(s), s, s=22, facecolors="none", edgecolors=MUTED,
                      linewidths=1.1, zorder=3)
        m = sum(s) / len(s)
        a.scatter([xi], [m], s=60, color=SURF if late else col, edgecolors=col,
                  linewidths=2, zorder=4)
        lab = f"{m:.1f}"
        dy = {"v13": -7.5, "v30": 5.5, "v31": -6, "v32": 5.5}.get(vers[xi], 0)
        ha, dx = ("left", 0.17) if not dy else ("center", 0)
        a.text(xi + dx, m + dy, lab, fontsize=9, color=INK, va="center", ha=ha)
    a.text(2, 76.5, "mean of 4", fontsize=8, color=MUTED, ha="center")
    a.text(5, 61.5, "mean of 3", fontsize=8, color=MUTED, ha="center")
    a.annotate("budget\nmechanism v2", xy=(6, 73.89), xytext=(5.9, 84),
               fontsize=8.5, color=INK2, ha="center", va="center",
               arrowprops=dict(arrowstyle="-", color=MUTED, lw=1))
    a.annotate("48 lanes,\nscored after\nthe deadline", xy=(7, 77.64), xytext=(6.95, 56),
               fontsize=8.5, color=INK2, ha="center", va="center",
               arrowprops=dict(arrowstyle="-", color=MUTED, lw=1))
    a.set_ylim(15, 90)
    a.set_ylabel("Public LB score")
    a.grid(axis="y", color=GRID, lw=0.8)
    a.set_axisbelow(True)

    cols = [BLUE_L] * 6 + [ORANGE, ORANGE]
    b.bar(x, tps, width=0.6, color=cols, edgecolor=SURF, linewidth=1.5)
    for xi, t in zip(x, tps):
        b.text(xi, t + 30, f"{t}", ha="center", fontsize=8.5, color=INK)
    b.set_ylim(0, 900)
    b.set_yticks([0, 400, 800])
    b.set_ylabel("tok/s")
    b.grid(axis="y", color=GRID, lw=0.8)
    b.set_axisbelow(True)
    b.set_xticks(x)
    b.set_xticklabels([f"{v}\n{d}" for v, d in zip(vers, dates)], fontsize=8.5)
    note(fig, "v2: over a full-depth run (KV-bound). v32 to v34: first 30 min of Kaggle probes.\n"
              "One submission has an SD of about 2.7.")
    fig.savefig(os.path.join(OUT, "fig1_throughput_vs_lb.png"), dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------- Figure 3 (budget schematic)
def fig_budget():
    fig, axes = plt.subplots(2, 1, figsize=(W, 6.4), sharex=True,
                             gridspec_kw={"hspace": 0.42})
    fig.subplots_adjust(left=0.12, right=0.975, top=0.815, bottom=0.17)
    title(fig, "Figure 4. Budget mechanism v2 (schematic)",
          "Four lanes over the 12-hour run. Bar = one task's chain;\n"
          "dashed outline = time it was given but never used.")

    def lane_bar(ax, lane, x0, x1, color, label="", edge=None, fill=True, ls="-", lx=None):
        ax.add_patch(Rectangle((x0, lane - 0.33), x1 - x0, 0.66, facecolor=color if fill else "none",
                               edgecolor=edge or SURF, lw=1.4 if edge else 1.8,
                               linestyle=ls, zorder=3))
        if label:
            ink = SURF if color in (BLUE, ORANGE) else (INK if fill else MUTED)
            ax.text(lx if lx is not None else (x0 + x1) / 2, lane, label, ha="center",
                    va="center", fontsize=8, color=ink, zorder=4)

    ax = axes[0]
    ax.set_title("Time bank (v32): hard tasks cut early, time left idle", loc="left",
                 fontsize=10, color=INK, fontweight="demibold")
    lane_bar(ax, 4, 0, 46, BLUE_L, "hard task")
    ax.plot([46, 46], [3.55, 4.45], color=INK, lw=2.2, zorder=5)
    ax.text(47.5, 4.0, "cut", fontsize=8, color=INK, va="center")
    lane_bar(ax, 4, 64, 76, BLUE_L, "easy")
    lane_bar(ax, 3, 0, 14, BLUE_L, "easy")
    lane_bar(ax, 3, 14, 30, BLUE_L, "easy")
    lane_bar(ax, 3, 30, 58, BLUE_L, "medium")
    lane_bar(ax, 3, 58, 70, BLUE_L, "late")
    lane_bar(ax, 3, 70, 99, NEUTRAL, "unused", fill=False, edge=MUTED, ls="--", lx=89)
    lane_bar(ax, 2, 0, 46, BLUE_L, "hard task")
    ax.plot([46, 46], [1.55, 2.45], color=INK, lw=2.2, zorder=5)
    ax.text(47.5, 2.0, "cut", fontsize=8, color=INK, va="center")
    lane_bar(ax, 2, 52, 64, BLUE_L, "late")
    lane_bar(ax, 2, 64, 99, NEUTRAL, "unused", fill=False, edge=MUTED, ls="--", lx=89)
    lane_bar(ax, 1, 0, 20, BLUE_L, "easy")
    lane_bar(ax, 1, 20, 66, BLUE_L, "medium")
    ax.axvline(78, color=MUTED, lw=1, ls=":", zorder=2)
    ax.text(79.5, 1.0, "last task ends\n0.5–2.4 h early", fontsize=8, color=INK2, va="center",
            ha="left", linespacing=1.2)

    ax = axes[1]
    ax.set_title("Budget v2: base share, floors for hard tasks, second chains",
                 loc="left", fontsize=10, color=INK, fontweight="demibold")
    lane_bar(ax, 4, 0, 46, BLUE_L, "hard task: base")
    lane_bar(ax, 4, 46, 70, BLUE, "floor 160k")
    lane_bar(ax, 4, 70, 82, BLUE_L, "easy")
    lane_bar(ax, 4, 82, 99, ORANGE, "2nd chain")
    lane_bar(ax, 3, 0, 14, BLUE_L, "easy")
    lane_bar(ax, 3, 14, 30, BLUE_L, "easy")
    lane_bar(ax, 3, 30, 58, BLUE_L, "medium")
    lane_bar(ax, 3, 58, 70, BLUE_L, "late")
    lane_bar(ax, 3, 70, 99, ORANGE, "2nd chain: doubted")
    lane_bar(ax, 2, 0, 46, BLUE_L, "hard task: base")
    lane_bar(ax, 2, 46, 66, BLUE, "floor")
    lane_bar(ax, 2, 66, 80, BLUE_L, "late")
    lane_bar(ax, 2, 80, 99, ORANGE, "2nd chain")
    lane_bar(ax, 1, 0, 20, BLUE_L, "easy")
    lane_bar(ax, 1, 20, 66, BLUE_L, "medium")
    lane_bar(ax, 1, 66, 99, ORANGE, "2nd chain: long, doubted")

    for ax in axes:
        ax.set_xlim(0, 100)
        ax.set_ylim(0.3, 4.7)
        ax.set_yticks([1, 2, 3, 4])
        ax.set_yticklabels(["lane 4", "lane 3", "lane 2", "lane 1"], fontsize=8.5)
        ax.tick_params(axis="y", length=0)
        ax.spines["left"].set_visible(False)
    axes[1].set_xticks([0, 25, 50, 75, 100])
    axes[1].set_xticklabels(["0 h", "3 h", "6 h", "9 h", "12 h"], fontsize=8.5)
    note(fig, "Hard = first answer doubted at P0/P1, or nothing passes training by 60k tokens.\n"
              "A 2nd chain is a fresh conversation that stops at its first train-passing program;\n"
              "its answer replaces attempt 2. Doubted tasks with long first chains go first,\n"
              "tasks with nothing train-passing go last.")
    fig.savefig(os.path.join(OUT, "fig3_budget_v2.png"), dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------- Figure 2 (TCW)
def fig_tcw():
    fig, (a, c, b) = plt.subplots(3, 1, figsize=(W, 9.4),
                                  gridspec_kw={"height_ratios": [1.55, 1.25, 1], "hspace": 0.5})
    fig.subplots_adjust(left=0.33, right=0.95, top=0.868, bottom=0.08)
    title(fig, "Figure 3. Train-consistent errors and what rescues them",
          "Most lost test inputs come from programs that pass every training pair;\n"
          "late fits are often wrong; an independent run rescues twice as many\n"
          "as a same-chain retry.")

    # (b) accuracy of the first train-passing program vs tokens spent before it
    bins = ["<10k", "10–20k", "20–40k", "40–80k", "≥80k"]
    fin = [(31, 33, 80.4, 98.3), (38, 54, 57.2, 80.9), (80, 105, 67.2, 83.3), (65, 118, 46.1, 63.8),
           (12, 42, 17.2, 43.6)]
    tb = [(38, 43, 75.5, 94.9), (110, 137, 72.8, 86.1), (158, 212, 68.3, 79.9), (113, 206, 48.0, 61.5),
          (16, 94, 10.8, 25.9)]
    xx = list(range(len(bins)))
    for series, col, lab, off in ((tb, BLUE_L, "time bank, 6 runs (692 fits)", -0.08),
                                  (fin, BLUE, "final harness, 3 runs (352 fits)", 0.08)):
        ys = [100 * r / n for r, n, lo, hi in series]
        lo = [y - l for y, (_, _, l, _) in zip(ys, series)]
        hi = [h - y for y, (_, _, _, h) in zip(ys, series)]
        c.errorbar([x + off for x in xx], ys, yerr=[lo, hi], color=col, lw=2, marker="o", ms=5,
                   capsize=2.5, elinewidth=1, label=lab, zorder=3)
    for x, (r, n, _, _) in zip(xx, fin):
        c.text(x + 0.16, 100 * r / n + (4 if x != 1 else -9), f"{100 * r / n:.0f}%", fontsize=8.5,
               color=INK, va="center")
    c.set_xticks(xx)
    c.set_xticklabels(bins, fontsize=8.5)
    c.set_xlabel("generated tokens before the first train-passing program", fontsize=8.5)
    c.set_ylim(0, 105)
    c.set_yticks([0, 25, 50, 75, 100])
    c.set_yticklabels(["0", "25", "50", "75", "100%"], fontsize=8.5)
    c.set_title("First train-passing program right on test (95% CI)", loc="right", fontsize=9.5,
                color=INK, x=1.0)
    c.legend(fontsize=8, frameon=False, loc="lower left")
    pos = c.get_position()
    c.set_position([0.12, pos.y0, 0.95 - 0.12, pos.height])
    c.grid(axis="y", color=GRID, lw=0.8)
    c.set_axisbelow(True)

    cls = ["Doubted; attempt 2\nalso wrong", "Confident; attempt 2\nalso wrong",
           "Wrong output size;\nattempt 2 also wrong", "Confident; no attempt 2",
           "No train-passing\nprogram", "Other"]
    n = [36, 12, 9, 3, 8, 3]
    tcw = [True, True, True, True, False, False]
    y = list(range(len(cls)))[::-1]
    a.barh(y, n, color=[BLUE if t else NEUTRAL for t in tcw], height=0.64, edgecolor=SURF, lw=1.5)
    for yi, v in zip(y, n):
        a.text(v + 0.8, yi, str(v), va="center", fontsize=9, color=INK)
    a.set_yticks(y)
    a.set_yticklabels(cls, fontsize=8.5, linespacing=1.15)
    a.set_xlim(0, 44)
    a.set_title("Lost test inputs by class (budget v2, 2 offline runs, 71 lost)",
                loc="right", fontsize=9.5, color=INK, x=1.0)
    a.text(17, 1.0, "blue = train-consistent\nwrong: 60 of 71", fontsize=8.5, color=INK2,
           va="center", linespacing=1.25)
    a.grid(axis="x", color=GRID, lw=0.8)
    a.set_axisbelow(True)
    a.tick_params(axis="y", length=0)

    src = ["Same-chain attempt 2", "Explorer proposals\nmerged in context", "Independent run\nof the same task"]
    r = [20.2, 27.4, 39.5]
    yb = [2, 1, 0]
    b.barh(yb, r, color=[NEUTRAL, BLUE_L, BLUE], height=0.62, edgecolor=SURF, lw=1.5)
    for yi, v in zip(yb, r):
        b.text(v + 0.8, yi, f"{v:.0f}%" if v != 39.5 else "39.5%", va="center", fontsize=9, color=INK)
    b.set_yticks(yb)
    b.set_yticklabels(src, fontsize=8.5, linespacing=1.15)
    b.set_xlim(0, 44)
    b.set_xticks([0, 10, 20, 30, 40])
    b.set_xticklabels(["0", "10", "20", "30", "40%"])
    b.set_title("Rescue rate of doubted wrong attempt-1 answers (attempt 1 fixed)",
                loc="right", fontsize=9.5, color=INK, x=1.0)
    b.grid(axis="x", color=GRID, lw=0.8)
    b.set_axisbelow(True)
    b.tick_params(axis="y", length=0)
    note(fig, "Primary chains on augmented public evaluation. Doubted attempt-1 answers are right\n"
              "37% of the time, undoubted 92%. First two rescue bars: 168 replayed states.")
    fig.savefig(os.path.join(OUT, "fig2_tcw.png"), dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------- Figure 4
def fig4():
    steps = ["Naive: 512 experts, BF16 KV, 2 lanes",
             "Load-time pruning to 384 experts, 8 lanes",
             "v13: 320 experts pre-pruned, FP8 PLE, FR-Spec",
             "v30: 32 lanes, FP8 KV, bf16 DeltaNet state, host KV tier",
             "v32: int4 KV, prefix-cache fixes, server think budget",
             "v34: 48 lanes, FP8 indexer, memory-access fix"]
    kv = ["0.11M", "0.35M", "0.47M", "~0.9M", "1.4M", "1.65M"]
    tps = [120, 215, 315, 462, 639, 713]
    y = list(range(len(steps)))[::-1]
    fig, b = plt.subplots(figsize=(W, 5.0))
    fig.subplots_adjust(left=0.035, right=0.975, top=0.80, bottom=0.15)
    title(fig, "Figure 5. Serving on 4×L4: 120 → 713 tok/s",
          "Each row adds to the one above it. Bar = generation throughput;\n"
          "label = KV pool size in tokens. Prefix-cache hits rose from 72% to 96%.")
    yb = [v - 0.14 for v in y]
    b.barh(yb, tps, color=[BLUE_L] * 5 + [BLUE], height=0.36, edgecolor=SURF, lw=1, zorder=2)
    for yi, v, s, k in zip(y, tps, steps, kv):
        b.text(0, yi + 0.27, s, va="center", fontsize=8.5, color=INK, zorder=3)
        b.text(v + 12, yi - 0.14, f"{v} tok/s · KV {k}", va="center", fontsize=8.5,
               color=INK2, zorder=3)
    b.set_ylim(-0.6, len(steps) - 0.45)
    b.set_xlim(0, 1000)
    b.set_xticks([0, 200, 400, 600, 800])
    b.set_xticklabels(["0", "200", "400", "600", "800 tok/s"], fontsize=8.5)
    b.set_yticks([])
    b.spines["left"].set_visible(False)
    b.grid(axis="x", color=GRID, lw=0.8)
    b.set_axisbelow(True)
    note(fig, "Kaggle probes. Row 2 is KV-bound over a full-depth run.\n"
              "MTP drafting (3 tokens, ~2.8 accepted) in every row.")
    fig.savefig(os.path.join(OUT, "fig4_serving.png"), dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------- Figure 2 (concept)
def fig_concept():
    from matplotlib.patches import Ellipse, FancyArrowPatch, Circle
    GREEN = "#1f9d6a"
    RED = ORANGE
    fig = plt.figure(figsize=(W, 5.3))
    ax = fig.add_axes([0.0, 0.0, 1.0, 0.86])
    ax.set_xlim(0, 100)
    ax.set_ylim(-7, 72)
    ax.axis("off")
    title(fig, "Figure 2. Why checks against training cannot catch a TCW answer",
          "H is the set of programs that reproduce every training pair. The agent\n"
          "stops at the first member of H it finds; which one it finds is the problem.",
          y=0.975)

    # the version space H
    ax.add_patch(Ellipse((52, 40), 60, 34, facecolor="#eef4fb", edgecolor=BLUE_L, lw=1.6, zorder=1))
    ax.text(52, 54.2, "H: programs that pass every training pair", ha="center", fontsize=9,
            color=BLUE, fontweight="demibold")
    ax.text(52, 50.6, "any check against training says ✓ for all of them", ha="center",
            fontsize=8.5, color=INK2)
    import random
    rnd = random.Random(7)
    others = [(30, 40), (34, 31), (47, 46), (57, 30), (70, 33), (79, 47), (62, 47), (39, 45),
              (52, 36), (68, 26), (78, 37)]
    for (x, y) in others:
        ax.add_patch(Circle((x, y), 0.9, color=NEUTRAL, zorder=2))
    p1 = (41, 36)
    pst = (66, 40)
    near = (46.5, 31.5)
    ax.add_patch(Circle(near, 0.9, color=NEUTRAL, zorder=2))

    # search path into H (dropped readings)
    path = [(5, 60), (10, 55), (6, 49), (12, 45), (9, 39), (16, 36), (21, 41), (26, 36), (31, 37)]
    xs, ys = zip(*(path + [p1]))
    ax.plot(xs, ys, color=MUTED, lw=1, ls=(0, (2, 2)), zorder=2)
    for (x, y) in path:
        ax.plot(x, y, marker="x", color=MUTED, ms=4.5, mew=1.2, zorder=3)
    ax.text(2, 70, "long search: each dropped reading (×) is one\nmore chance to fit a few training pairs by accident",
            fontsize=8.5, color=INK2, va="top", linespacing=1.25)

    # p1 and p*
    ax.add_patch(Circle(p1, 1.7, color=RED, zorder=4))
    ax.text(p1[0] - 2.5, p1[1] + 3.2, "p1: found first,\nwrong on test", ha="center", fontsize=8.5,
            color=RED, fontweight="demibold", linespacing=1.15)
    ax.add_patch(Circle(pst, 1.7, color=GREEN, zorder=4))
    ax.text(pst[0] + 3.2, pst[1] + 0.2, "p*: right", ha="left", va="center", fontsize=8.5, color=GREEN,
            fontweight="demibold")

    # same-chain retry
    ax.add_patch(FancyArrowPatch(p1, near, connectionstyle="arc3,rad=0.5", arrowstyle="-|>",
                                 mutation_scale=9, color=INK2, lw=1.1, zorder=5, shrinkA=6, shrinkB=4))
    ax.annotate("same-chain retry\nstays near p1: ~20% rescued", xy=(46, 30.5), xytext=(22, 14),
                fontsize=8.5, color=INK2, ha="center", va="center", linespacing=1.2,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))

    # independent run
    start = (95, 64)
    ax.plot(*start, marker="o", ms=5, mfc=SURF, mec=BLUE, mew=1.4, zorder=5)
    ax.add_patch(FancyArrowPatch(start, pst, connectionstyle="arc3,rad=-0.25", arrowstyle="-|>",
                                 mutation_scale=10, color=BLUE, lw=1.4, zorder=5, shrinkA=4, shrinkB=7))
    ax.text(97, 69.5, "independent run (fresh context):\n39.5% of doubted wrong answers rescued",
            ha="right", va="top", fontsize=8.5, color=BLUE, linespacing=1.2)

    # self-review note
    ax.text(97, 22.5, "self-review only has a prior:\ndoubted answers right 37%,\nundoubted 92%",
            ha="right", va="top", fontsize=8.5, color=INK2, linespacing=1.25)

    # test outputs
    def mini(x0, y0, col, cells):
        s = 1.55
        for r in range(4):
            for c in range(4):
                fc = "#222222"
                if (r, c) in cells:
                    fc = cells[(r, c)]
                ax.add_patch(Rectangle((x0 + c * s, y0 + (3 - r) * s), s, s, facecolor=fc,
                                       edgecolor="#444444", lw=0.4, zorder=6))
        ax.add_patch(Rectangle((x0, y0), 4 * s, 4 * s, facecolor="none", edgecolor=col, lw=1.6, zorder=7))
    gA = {(1, 0): "#0074D9", (1, 1): "#0074D9", (1, 2): "#0074D9", (1, 3): "#0074D9", (0, 2): "#AAAAAA",
          (2, 2): "#AAAAAA", (3, 2): "#AAAAAA"}
    gB = {(1, 0): "#0074D9", (1, 1): "#0074D9", (0, 2): "#AAAAAA", (1, 2): "#AAAAAA",
          (2, 2): "#AAAAAA", (3, 2): "#AAAAAA"}
    mini(53.5, 4.5, RED, gA)
    mini(66.5, 4.5, GREEN, gB)
    ax.text(63.4, 9.2, "≠", ha="center", va="center", fontsize=15, color=INK)
    ax.text(63.4, 2.0, "two train-passing programs, two test outputs:\nthe disagreement is the only evidence left",
            ha="center", va="top", fontsize=8.5, color=INK, linespacing=1.2)
    ax.add_patch(FancyArrowPatch(p1, (56.6, 11.2), connectionstyle="arc3,rad=0.15", arrowstyle="-|>",
                                 mutation_scale=8, color=RED, lw=1, zorder=5, shrinkA=6, shrinkB=2))
    ax.add_patch(FancyArrowPatch(pst, (69.6, 11.2), connectionstyle="arc3,rad=-0.1", arrowstyle="-|>",
                                 mutation_scale=8, color=GREEN, lw=1, zorder=5, shrinkA=6, shrinkB=2))
    fig.savefig(os.path.join(OUT, "fig2_concept.png"), dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------- PDF-only: offline resource curve
def fig_tokens_offline():
    fig, ax = plt.subplots(figsize=(W, 3.9))
    fig.subplots_adjust(left=0.11, right=0.97, top=0.76, bottom=0.17)
    title(fig, "Offline: score rises with tokens per task (early harness)",
          "Public evaluation (120 tasks), Kaggle-equivalent budgets, early harness (Duck v15), one run each.")
    pts = [(22.3, 44.0, "22k tokens/task\n44.0 (rep. 44.3)"), (40.2, 77.5, "40k: 77.5"),
           (68.0, 97.33, "68k, 32k think cap: 97.3")]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    ax.plot(xs[:2], ys[:2], color=BLUE, lw=2, zorder=2)
    ax.plot(xs[1:], ys[1:], color=BLUE, lw=1.5, ls="--", zorder=2)
    ax.scatter(xs, ys, s=55, color=BLUE, zorder=3)
    ax.scatter([22.3], [44.33], s=30, facecolors="none", edgecolors=BLUE, zorder=3)
    ax.scatter([40.2], [65.0], s=55, color=ORANGE, zorder=3)
    for (x, y, lab), dx, dy, ha in zip(pts, [1.2, -1.2, -1.2], [-7, 4.5, 3.5], ["left", "right", "right"]):
        ax.text(x + dx, y + dy, lab, fontsize=8.5, color=INK, ha=ha, va="center", linespacing=1.2)
    ax.text(41.4, 65.0, "40k with history compaction: 65.0", fontsize=8.5, color=ORANGE, va="center")
    ax.set_xlim(15, 75)
    ax.set_ylim(30, 108)
    ax.set_xlabel("Kaggle-equivalent generated tokens per task (thousands)")
    ax.set_ylabel("Score / 120")
    ax.grid(color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    note(fig, "Solid: same harness and caps; dashed: different think cap. ~+17 points per +10k tokens between 22k and 40k.")
    fig.savefig(os.path.join(OUT, "fig_tokens_offline.png"), dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------- Cover
ARC = ["#000000", "#0074D9", "#FF4136", "#2ECC40", "#FFDC00",
       "#AAAAAA", "#F012BE", "#FF851B", "#7FDBFF", "#870C25"]


def draw_grid(ax, g, x0, y0, cell, border="#555555"):
    h, w = len(g), len(g[0])
    for r in range(h):
        for c in range(w):
            ax.add_patch(Rectangle((x0 + c * cell, y0 + (h - 1 - r) * cell), cell, cell,
                                   facecolor=ARC[g[r][c]], edgecolor="#2b2b2b", lw=0.8))
    ax.add_patch(Rectangle((x0, y0), w * cell, h * cell, facecolor="none", edgecolor=border, lw=1.4))


def extend(g, stop_at_wall):
    out = [row[:] for row in g]
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v not in (0, 5):
                for cc in range(c + 1, len(row)):
                    if stop_at_wall and g[r][cc] == 5:
                        break
                    out[r][cc] = v
    return out


def cover():
    fig = plt.figure(figsize=(16, 9), dpi=100)
    fig.patch.set_facecolor("#101418")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 90)
    ax.axis("off")
    ax.set_facecolor("#101418")

    ax.text(8, 74, "Spend the next token\nwhere verification\ncannot reach", fontsize=46,
            color="#f4f3ef", fontweight="demibold", va="top", linespacing=1.15)
    ax.text(8, 36, "A program-synthesis agent on Qwen3.8-Flash-Next, 4×L4.\n"
            "Two programs fit every training pair. Only an independent\nderivation tells them apart.",
            fontsize=17, color="#b9b8b1", va="top", linespacing=1.45)
    ax.text(8, 10, "ARC Prize 2026 · ARC-AGI-2 · team _hans", fontsize=14, color="#7f7e78")

    def g(n=6):
        return [[0] * n for _ in range(n)]

    t1 = g(); t1[1][0] = 1; t1[4][1] = 2
    t2 = g(); t2[0][2] = 3; t2[3][0] = 4; t2[5][3] = 6
    te = g(); te[1][0] = 1; te[3][1] = 2
    for r in range(0, 5):
        te[r][3] = 5
    cell = 2.6
    X = 98
    ax.text(X, 82, "training pairs", fontsize=13, color="#b9b8b1")
    for i, t in enumerate([t1, t2]):
        y0 = 62 - i * 19
        draw_grid(ax, t, X, y0, cell)
        ax.annotate("", xy=(X + 20.5, y0 + 7.8), xytext=(X + 16.5, y0 + 7.8),
                    arrowprops=dict(arrowstyle="->", color="#b9b8b1", lw=1.6))
        draw_grid(ax, extend(t, True), X + 22, y0, cell)
        ax.text(X + 39.5, y0 + 7.8, "✓", fontsize=20, color="#2ECC40", va="center")
    ax.text(X, 37, "test input", fontsize=13, color="#b9b8b1")
    draw_grid(ax, te, X, 18, cell)
    ax.annotate("", xy=(X + 20.5, 30), xytext=(X + 16.5, 25),
                arrowprops=dict(arrowstyle="->", color="#b9b8b1", lw=1.6))
    ax.annotate("", xy=(X + 20.5, 13), xytext=(X + 16.5, 21),
                arrowprops=dict(arrowstyle="->", color="#b9b8b1", lw=1.6))
    small = 1.75
    draw_grid(ax, extend(te, False), X + 22, 25, small, border="#e34948")
    ax.text(X + 34, 30.2, "fits training,\nwrong on test", fontsize=11, color="#e7a3a2", va="center")
    draw_grid(ax, extend(te, True), X + 22, 6, small, border="#2ECC40")
    ax.text(X + 34, 11.2, "independent\nre-derivation", fontsize=11, color="#9fe0a8", va="center")
    fig.savefig(os.path.join(OUT, "cover.png"), dpi=100, facecolor="#101418")
    plt.close(fig)


if __name__ == "__main__":
    import sys
    fig1(); fig_concept(); fig_tcw(); fig_budget(); fig4()
    if PDF_MODE:
        fig_tokens_offline()
    if "--cover" in sys.argv:
        cover()
    print("wrote", sorted(os.listdir(OUT)))
