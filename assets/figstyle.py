"""
Shared matplotlib style for every illustrative figure in this repository.

Every figure script in this repo imports from here so all charts look like
one consistent visual system: same palette, same type scale, same source
note style. Data in every figure is invented and pedagogical — none of it
comes from the Hub-Racial-Brasil, analytics-case-studies, or
futebol-brasileiro-analises projects.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl

# Palette: a neutral, print-safe qualitative set. Two "group" colors (used
# whenever a figure compares two groups — e.g. Group A vs Group B) plus a
# neutral gray and an accent for highlighting a single quantity.
COLOR_GROUP_A = "#2E5C8A"      # steel blue
COLOR_GROUP_B = "#C2622D"      # burnt orange
COLOR_NEUTRAL = "#6B7280"      # gray
COLOR_ACCENT = "#1F8A70"       # teal (highlights, CIs, fitted lines)
COLOR_GRID = "#E5E7EB"
COLOR_TEXT = "#1F2937"

FIGSIZE_STANDARD = (7.2, 4.5)
FIGSIZE_WIDE = (9.0, 4.2)
FIGSIZE_SQUARE = (5.5, 5.5)

DPI = 200


def apply_style():
    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "axes.edgecolor": COLOR_NEUTRAL,
        "axes.labelcolor": COLOR_TEXT,
        "axes.grid": True,
        "grid.color": COLOR_GRID,
        "grid.linewidth": 0.8,
        "xtick.color": COLOR_TEXT,
        "ytick.color": COLOR_TEXT,
        "text.color": COLOR_TEXT,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "legend.fontsize": 10,
    })


def add_note(fig, text):
    """Small caption-style note at the bottom-left of the figure, used for
    'dados ilustrativos / illustrative data' disclaimers."""
    fig.text(0.01, 0.01, text, fontsize=8, color=COLOR_NEUTRAL, ha="left", va="bottom")


def save(fig, path, note=None):
    if note:
        add_note(fig, note)
    fig.tight_layout(rect=(0, 0.03, 1, 1) if note else None)
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
