# Spend the Next Token Where Verification Cannot Reach

Team _hans, ARC Prize 2026 (ARC-AGI-2 and Paper Track).

**Paper:** [paper/paper.pdf](paper/paper.pdf)

We built a program-synthesis agent around one open-weight model, Qwen3.8-Flash-Next (125B parameters, 6B active), and ran it on Kaggle's four L4 GPUs. The agent writes Python in a persistent interpreter and may only submit a program that reproduces every training pair.

For a long time more tokens per task meant a higher score. Then it stopped: with the harness fixed, doubling serving throughput moved the public leaderboard from 69.2 to 70.1. The paper traces the plateau to *train-consistent wrong* answers, programs that fit every training pair but get the test wrong. It argues that no check against the training pairs can catch them, and measures what does: an independent second run rescues 39.5% of doubted wrong answers, against about 20% for a retry in the same conversation. A token budget built on this scored 73.89 on the public leaderboard, up from 70.14.

## Contents

| Path | What it is |
|---|---|
| `paper/paper.pdf` | Technical report (26 pages): main text plus appendices with every experiment |
| `paper/*.tex` | LaTeX source (`paper.tex` + `app_*.tex` appendices) |
| `figures/` | Figures, plus `make_figures.py` that draws them from the numbers in the paper |

## Links

- Kaggle writeup (Paper Track): https://www.kaggle.com/competitions/arc-prize-2026-paper-track/writeups/spend-the-next-token-where-verification-cannot-rea
- Submission notebook (full harness and serving code): https://www.kaggle.com/code/deepdreamer/fnext-w4a16-arc-submit

Much of our code and this paper was written with help from Claude (Claude Code); all numbers come from our own runs.
