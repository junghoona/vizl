"""Matplotlib plotting layer for simple_eda, matching the reference dashboard.

Drawing internals (theme rcParams, gradients, glow, arcs) live in ._style;
this module holds only the public chart functions.
"""

import numpy as np

from . import _style as s

theme = s.theme


def line_plot(df, x, y, smooth=True):
    """Smooth line(s) with round caps, glow, and a gradient fill under each."""
    fig, ax = s.new_fig()
    cols = [y] if isinstance(y, str) else list(y)
    palette = [s.CORAL, s.PERIWINKLE,
               s.THEME["coral"][2], s.THEME["periwinkle"][2]]
    xn, is_num = s.xvals(df, x)
    for i, col in enumerate(cols):
        color = palette[i % len(palette)]
        yv = df[col].to_numpy(dtype=float)
        xs, ys = s.smooth(xn, yv) if smooth else (xn, yv)
        s.gradient_fill(ax, xs, ys, color)
        s.glow(ax, xs, ys, color)
        ax.plot(xs, ys, color=color, linewidth=3.0,
                solid_capstyle="round", label=col, zorder=3)
        ax.plot(xn, yv, "o", color=color, markersize=6, zorder=4)
    if not is_num:
        ax.set_xticks(xn)
        ax.set_xticklabels(df[x].tolist())
    s.title(ax, y if isinstance(y, str) else " vs ".join(cols))
    if len(cols) > 1:
        ax.legend(loc="upper left")
    return fig, ax


def area_plot(df, x, y):
    """Filled wave/area chart that fades to transparent toward the baseline."""
    fig, ax = s.new_fig()
    xn, is_num = s.xvals(df, x)
    yv = df[y].to_numpy(dtype=float)
    xs, ys = s.smooth(xn, yv)
    s.gradient_fill(ax, xs, ys, s.PERIWINKLE)
    s.glow(ax, xs, ys, s.PERIWINKLE)
    ax.plot(xs, ys, color=s.PERIWINKLE, linewidth=3.0,
            solid_capstyle="round", zorder=3)
    if not is_num:
        ax.set_xticks(xn)
        ax.set_xticklabels(df[x].tolist())
    s.title(ax, y)
    return fig, ax


def bar_plot(df, category, value):
    """Vertical rounded bars filled with the coral-to-periwinkle gradient.

    Each bar represents one row of `df`: its position/label along the
    x-axis is `category`, and its height (also annotated above the bar)
    is `value`.
    """
    fig, ax = s.new_fig()
    cats, vals = df[category].tolist(), df[value].to_numpy(dtype=float)
    xs = range(len(cats))
    for xi, v in zip(xs, vals):
        s.vbar(ax, xi, v, 0.6, s.BLEND_CMAP)
        ax.text(xi, v + vals.max() * 0.03, f"{v:g}", ha="center",
                va="bottom", fontsize=10, color=s.THEME["text"])
    ax.set_xticks(list(xs))
    ax.set_xticklabels(cats)
    ax.set_xlim(-0.7, len(cats) - 0.3)
    ax.set_ylim(0, vals.max() * 1.15)
    ax.set_xlabel(category)
    ax.set_ylabel(value)
    s.title(ax, f"{value} by {category}")
    return fig, ax


def hbar_plot(df, category, value):
    """Horizontal capsule bars filled with the coral-to-periwinkle gradient.

    Each bar represents one row of `df`: its position/label along the
    y-axis is `category`, and its length (also annotated past the bar
    end) is `value`.
    """
    fig, ax = s.new_fig()
    cats, vals = df[category].tolist(), df[value].to_numpy(dtype=float)
    ys = range(len(cats))
    for yi, v in zip(ys, vals):
        s.hbar(ax, yi, v, 0.55, s.BLEND_CMAP)
        ax.text(v + vals.max() * 0.02, yi, f"{v:g}", ha="left",
                va="center", fontsize=10, color=s.THEME["text"])
    ax.set_yticks(list(ys))
    ax.set_yticklabels(cats)
    ax.set_ylim(-0.7, len(cats) - 0.3)
    ax.set_xlim(0, vals.max() * 1.15)
    ax.invert_yaxis()
    ax.set_xlabel(value)
    ax.set_ylabel(category)
    s.title(ax, f"{value} by {category}")
    return fig, ax


def donut_plot(df, column, agg="mean", label=None):
    """Gradient progress ring for the `agg` of `column` in `df` (0-100%).

    Ties the ring to a dataset column so the chart states what it
    represents: a top title (the label) and a subtitle name the metric,
    and the centered "NN%" is `df[column].agg(...)`, clipped to [0, 100].
    e.g. donut_plot(df, "uptime_pct", agg="mean", label="Uptime").
    """
    value = float(getattr(df[column], agg)())
    label = label or f"{agg} of {column}"
    fig, ax = s.new_fig((5, 5))
    ax.set_aspect("equal")
    ax.axis("off")
    s.arc(ax, 0, 360, r=1.0, lw=22, color=s.THEME["grid"], alpha=0.35)
    frac = max(0.0, min(value, 100.0)) / 100.0
    s.arc(ax, -90, -90 + 360 * frac, r=1.0, lw=22, cmap=s.BLEND_CMAP)
    ax.text(0, 0.05, f"{value:.0f}%", ha="center", va="center",
            fontsize=32, fontweight="bold", color=s.THEME["text"])
    ax.text(0, -0.22, label, ha="center", va="center",
            fontsize=11, color=s.THEME["muted"])
    s.title(ax, label)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    return fig, ax


def gauge_plot(value, label=""):
    """Semicircular gauge with a gradient arc, a needle, and a pill label."""
    fig, ax = s.new_fig((5.5, 3.4))
    ax.set_aspect("equal")
    ax.axis("off")
    s.arc(ax, 180, 0, r=1.0, lw=22, color=s.THEME["grid"], alpha=0.35)
    frac = max(0.0, min(value, 100.0)) / 100.0
    s.arc(ax, 180, 180 - 180 * frac, r=1.0, lw=22, cmap=s.BLEND_CMAP)
    theta = np.radians(180 - 180 * frac)
    ax.plot([0, 0.82 * np.cos(theta)], [0, 0.82 * np.sin(theta)],
            color=s.THEME["text"], linewidth=3,
            solid_capstyle="round", zorder=5)
    ax.scatter([0], [0], s=90, color=s.THEME["text"], zorder=6)
    pill = dict(boxstyle="round,pad=0.4", facecolor=s.THEME["grid"],
                edgecolor="none", alpha=0.6)
    ax.text(0, -0.35, f"{value:.0f}%", ha="center", va="center",
            fontsize=20, fontweight="bold", color=s.THEME["text"], bbox=pill)
    if label:
        ax.text(0, -0.65, label, ha="center", va="center",
                fontsize=10, color=s.THEME["muted"])
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-0.3, 1.3)
    return fig, ax
