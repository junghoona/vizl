"""Private theming/drawing helpers for simple_eda.plots (not public API)."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_rgb
from matplotlib.path import Path
from matplotlib.patches import FancyBboxPatch, PathPatch
from matplotlib.collections import LineCollection

THEME = {
    "bg": "#2E1F4E",
    "text": "#FFF7FF",
    "muted": "#B9AEDD",
    "grid": "#4A3B6E",
    "coral": ["#FCA99B", "#FB7C85", "#F76481"],
    "periwinkle": ["#8B7FF0", "#6758E9", "#5546C8"],
}
CORAL = THEME["coral"][1]
PERIWINKLE = THEME["periwinkle"][1]


def _cmap(colors):
    return LinearSegmentedColormap.from_list("simple_eda", colors)


BLEND_CMAP = _cmap(THEME["coral"] + THEME["periwinkle"])


def theme():
    """Apply the dark-indigo rcParams theme (called by every plot function)."""
    plt.rcParams.update({
        "figure.facecolor": THEME["bg"],
        "axes.facecolor": THEME["bg"],
        "savefig.facecolor": THEME["bg"],
        "axes.edgecolor": THEME["grid"],
        "axes.linewidth": 0.8,
        "axes.labelcolor": THEME["muted"],
        "text.color": THEME["text"],
        "xtick.color": THEME["muted"],
        "ytick.color": THEME["muted"],
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "axes.grid.axis": "y",
        "grid.color": THEME["grid"],
        "grid.alpha": 0.35,
        "grid.linewidth": 0.8,
        "lines.linewidth": 3.0,
        "lines.solid_capstyle": "round",
        "lines.solid_joinstyle": "round",
        "legend.frameon": False,
        "legend.labelcolor": THEME["muted"],
        "font.size": 11,
    })


def new_fig(figsize=(7, 4.5)):
    theme()
    return plt.subplots(figsize=figsize)


def title(ax, text, subtitle=None):
    ax.set_title(text, loc="left", fontsize=15, fontweight="bold",
                 color=THEME["text"], pad=20 if subtitle else 12)
    if subtitle:
        ax.text(0.0, 1.03, subtitle, transform=ax.transAxes, fontsize=10,
                 color=THEME["muted"], ha="left", va="bottom")


def smooth(x, y, n=300):
    """Catmull-Rom interpolation for spline-like curves (no scipy needed)."""
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if len(x) < 3:
        return x, y
    t = np.arange(len(x))
    ti = np.linspace(0, len(x) - 1, n)
    xi = np.interp(ti, t, x)
    yp = np.pad(y, 1, mode="edge")
    idx = np.clip(ti.astype(int), 0, len(x) - 2)
    frac = ti - idx
    p0, p1, p2, p3 = yp[idx], yp[idx + 1], yp[idx + 2], yp[idx + 3]
    f2, f3 = frac ** 2, frac ** 3
    yi = (2 * p1 + (-p0 + p2) * frac
          + (2 * p0 - 5 * p1 + 4 * p2 - p3) * f2
          + (-p0 + 3 * p1 - 3 * p2 + p3) * f3)
    return xi, 0.5 * yi


def glow(ax, x, y, color, lw=3.0):
    for w, a in ((lw * 3.2, 0.05), (lw * 2.2, 0.09), (lw * 1.4, 0.16)):
        ax.plot(x, y, color=color, linewidth=w, alpha=a,
                solid_capstyle="round", zorder=2)


def gradient_fill(ax, x, y, color, baseline=0.0):
    """Fill under a curve, fading to transparent toward the baseline."""
    z = np.zeros((100, 1, 4))
    z[..., :3] = to_rgb(color)
    z[:, 0, 3] = np.linspace(0.32, 0.0, 100)
    top = max(float(np.max(y)), baseline + 1e-9)
    im = ax.imshow(z, extent=[x.min(), x.max(), baseline, top],
                    origin="upper", aspect="auto", zorder=1)
    verts = np.column_stack([np.concatenate([x, x[::-1]]),
                              np.concatenate([y, np.full_like(y, baseline)])])
    im.set_clip_path(PathPatch(Path(verts), transform=ax.transData))


def vbar(ax, xpos, val, width, cmap):
    z = np.linspace(0, 1, 200).reshape(-1, 1)
    extent = [xpos - width / 2, xpos + width / 2, 0, val]
    im = ax.imshow(z, cmap=cmap, extent=extent,
                    origin="lower", aspect="auto", zorder=2)
    box = FancyBboxPatch((xpos - width / 2, 0), width, val,
                          boxstyle=f"round,pad=0,rounding_size={width * 0.4}",
                          transform=ax.transData,
                          facecolor="none", edgecolor="none")
    im.set_clip_path(box)


def hbar(ax, ypos, val, height, cmap):
    z = np.linspace(0, 1, 200).reshape(1, -1)
    extent = [0, val, ypos - height / 2, ypos + height / 2]
    im = ax.imshow(z, cmap=cmap, extent=extent,
                    origin="lower", aspect="auto", zorder=2)
    box = FancyBboxPatch((0, ypos - height / 2), val, height,
                          boxstyle=f"round,pad=0,rounding_size={height * 0.5}",
                          transform=ax.transData,
                          facecolor="none", edgecolor="none")
    im.set_clip_path(box)


def arc(ax, theta0, theta1, r, lw, cmap=None, color=None, alpha=1.0, n=200):
    theta = np.radians(np.linspace(theta0, theta1, n))
    xy = np.column_stack([r * np.cos(theta), r * np.sin(theta)])
    pts = xy.reshape(-1, 1, 2)
    lc = LineCollection(np.concatenate([pts[:-1], pts[1:]], axis=1),
                         linewidths=lw, alpha=alpha, capstyle="round")
    if cmap is not None:
        lc.set_array(np.linspace(0, 1, len(pts) - 1))
        lc.set_cmap(cmap)
    else:
        lc.set_color(color)
    ax.add_collection(lc)


def xvals(df, x):
    xv = df[x].to_numpy()
    is_num = np.issubdtype(xv.dtype, np.number)
    return (xv, True) if is_num else (np.arange(len(xv)), False)
