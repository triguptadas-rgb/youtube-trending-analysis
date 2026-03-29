"""
visualizer.py
─────────────
All chart-generation functions for the YouTube Trending analysis.
Each function saves a PNG to the charts/ directory and returns the path.
"""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import pandas as pd
from pathlib import Path

CHARTS_DIR = Path("charts")
CHARTS_DIR.mkdir(exist_ok=True)

# ── Global style ────────────────────────────────────────────────────────────
PALETTE   = ["#FF0000", "#CC0000", "#990000", "#FF3333", "#FF6666",
             "#FF9999", "#FFB3B3", "#FFCCCC", "#FFE0E0", "#FFF0F0"]
BG        = "#0F0F0F"
SURFACE   = "#1A1A1A"
TEXT      = "#FFFFFF"
MUTED     = "#AAAAAA"
ACCENT    = "#FF0000"
GRID      = "#2A2A2A"

def _base_style():
    plt.rcParams.update({
        "figure.facecolor":  BG,
        "axes.facecolor":    SURFACE,
        "axes.edgecolor":    GRID,
        "axes.labelcolor":   TEXT,
        "axes.titlecolor":   TEXT,
        "axes.titlesize":    14,
        "axes.labelsize":    11,
        "xtick.color":       MUTED,
        "ytick.color":       MUTED,
        "text.color":        TEXT,
        "grid.color":        GRID,
        "grid.linewidth":    0.6,
        "font.family":       "DejaVu Sans",
        "figure.dpi":        120,
    })

def _save(fig, name: str) -> Path:
    path = CHARTS_DIR / name
    fig.savefig(path, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  📊 Saved → {path}")
    return path


# ── 1. Top 10 videos by views (horizontal bar) ─────────────────────────────

def chart_top_videos(df_top: pd.DataFrame) -> Path:
    _base_style()
    fig, ax = plt.subplots(figsize=(12, 6))

    titles = [t[:52] + "…" if len(t) > 52 else t for t in df_top["title"]]
    views  = df_top["views"] / 1_000_000

    colors = [PALETTE[i % len(PALETTE)] for i in range(len(df_top))]
    bars = ax.barh(titles[::-1], views[::-1], color=colors[::-1], height=0.65, edgecolor="none")

    for bar, v in zip(bars, views[::-1]):
        ax.text(bar.get_width() + 0.15, bar.get_y() + bar.get_height() / 2,
                f"{v:.1f}M", va="center", color=MUTED, fontsize=9)

    ax.set_xlabel("Views (Millions)", color=MUTED)
    ax.set_title("Top 10 Trending Videos by Views", pad=14, fontweight="bold")
    ax.xaxis.set_major_formatter(mtick.FormatStrFormatter("%.0fM"))
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    ax.spines[["top", "right", "left"]].set_visible(False)
    fig.tight_layout()
    return _save(fig, "01_top_videos_by_views.png")


# ── 2. Top channels (bubble chart) ─────────────────────────────────────────

def chart_top_channels(df_ch: pd.DataFrame) -> Path:
    _base_style()
    fig, ax = plt.subplots(figsize=(11, 6))

    sizes = (df_ch["total_views"] / df_ch["total_views"].max() * 1200) + 100
    sc = ax.scatter(
        df_ch["appearances"],
        df_ch["total_views"] / 1_000_000,
        s=sizes,
        c=range(len(df_ch)),
        cmap="Reds",
        alpha=0.85,
        edgecolors="none",
    )

    for _, row in df_ch.iterrows():
        ax.annotate(
            row["channel"],
            (row["appearances"], row["total_views"] / 1_000_000),
            textcoords="offset points", xytext=(6, 4),
            fontsize=8, color=TEXT,
        )

    ax.set_xlabel("Trending Appearances", color=MUTED)
    ax.set_ylabel("Total Views (Millions)", color=MUTED)
    ax.set_title("Top Channels — Appearances vs Total Views\n(bubble size = total views)",
                 pad=14, fontweight="bold")
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%.0fM"))
    ax.grid(linestyle="--", alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return _save(fig, "02_top_channels_bubble.png")


# ── 3. Category breakdown (donut) ──────────────────────────────────────────

def chart_category_donut(df_cat: pd.DataFrame) -> Path:
    _base_style()
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))

    # Left: donut by video count
    top = df_cat.nlargest(7, "video_count")
    other_count = df_cat["video_count"].sum() - top["video_count"].sum()
    if other_count > 0:
        other_row = pd.DataFrame([{"category": "Other", "video_count": other_count,
                                   "total_views": 0, "avg_views": 0, "avg_like_rate": 0}])
        top = pd.concat([top, other_row], ignore_index=True)

    colors_d = PALETTE[:len(top)]
    wedges, texts, autotexts = axes[0].pie(
        top["video_count"],
        labels=top["category"],
        autopct="%1.0f%%",
        colors=colors_d,
        pctdistance=0.82,
        wedgeprops=dict(width=0.52, edgecolor=BG, linewidth=2),
        startangle=140,
    )
    for t in texts: t.set(color=MUTED, fontsize=8)
    for at in autotexts: at.set(color=TEXT, fontsize=8, fontweight="bold")
    axes[0].set_title("Video Count by Category", fontweight="bold", pad=10)

    # Right: horizontal bar by avg views
    df_cat_s = df_cat.sort_values("avg_views", ascending=True).tail(8)
    axes[1].barh(df_cat_s["category"], df_cat_s["avg_views"] / 1_000_000,
                 color=ACCENT, alpha=0.85, height=0.6)
    axes[1].set_xlabel("Avg Views (Millions)", color=MUTED)
    axes[1].set_title("Avg Views per Category", fontweight="bold", pad=10)
    axes[1].xaxis.set_major_formatter(mtick.FormatStrFormatter("%.0fM"))
    axes[1].grid(axis="x", linestyle="--", alpha=0.3)
    axes[1].spines[["top", "right", "left"]].set_visible(False)

    fig.suptitle("Category Analysis", fontsize=15, fontweight="bold", y=1.01)
    fig.tight_layout()
    return _save(fig, "03_category_breakdown.png")


# ── 4. Engagement heatmap (channel × metric) ───────────────────────────────

def chart_engagement_heatmap(df_ch: pd.DataFrame) -> Path:
    _base_style()
    fig, ax = plt.subplots(figsize=(10, 6))

    heat_df = df_ch.set_index("channel")[["appearances", "avg_like_rate", "avg_comment_rate"]].copy()
    heat_df.columns = ["Trending\nAppearances", "Avg Like\nRate (%)", "Avg Comment\nRate (%)"]
    heat_norm = (heat_df - heat_df.min()) / (heat_df.max() - heat_df.min())

    sns.heatmap(
        heat_norm,
        annot=heat_df.round(2),
        fmt="g",
        cmap="Reds",
        ax=ax,
        linewidths=0.5,
        linecolor=BG,
        cbar_kws={"label": "Normalised score"},
        annot_kws={"size": 9},
    )
    ax.set_title("Channel Engagement Heatmap\n(normalised 0–1 per metric)",
                 pad=14, fontweight="bold")
    ax.set_ylabel("")
    ax.tick_params(axis="x", rotation=0)
    ax.tick_params(axis="y", rotation=0)
    fig.tight_layout()
    return _save(fig, "04_engagement_heatmap.png")


# ── 5. Views vs Like Rate scatter ──────────────────────────────────────────

def chart_views_vs_likes(df: pd.DataFrame) -> Path:
    _base_style()
    fig, ax = plt.subplots(figsize=(11, 6))

    cats = df["category"].unique()
    cmap = plt.cm.get_cmap("Reds", len(cats))
    cat_color = {c: cmap(i) for i, c in enumerate(cats)}

    for cat, grp in df.groupby("category"):
        ax.scatter(grp["views"] / 1_000_000, grp["like_rate"],
                   label=cat, color=cat_color[cat],
                   alpha=0.75, s=55, edgecolors="none")

    ax.set_xlabel("Views (Millions)", color=MUTED)
    ax.set_ylabel("Like Rate (%)", color=MUTED)
    ax.set_title("Views vs Like Rate — by Category", pad=14, fontweight="bold")
    ax.xaxis.set_major_formatter(mtick.FormatStrFormatter("%.0fM"))
    ax.grid(linestyle="--", alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=7, framealpha=0.15, labelcolor=TEXT,
              loc="upper right", ncol=2)
    fig.tight_layout()
    return _save(fig, "05_views_vs_like_rate.png")


# ── 6. Summary dashboard ────────────────────────────────────────────────────

def chart_summary_dashboard(stats: dict, df_top: pd.DataFrame, df_cat: pd.DataFrame) -> Path:
    _base_style()
    fig = plt.figure(figsize=(14, 8))
    fig.suptitle("YouTube Trending — Summary Dashboard", fontsize=17,
                 fontweight="bold", y=0.98)

    gs = fig.add_gridspec(2, 3, hspace=0.45, wspace=0.35)

    # KPI tiles (top row, left 3 cells)
    kpis = [
        ("Total Videos",     f"{stats['total_videos']}"),
        ("Total Views",      f"{stats['total_views']/1e9:.2f}B"),
        ("Avg Like Rate",    f"{stats['avg_like_rate']}%"),
    ]
    for i, (label, val) in enumerate(kpis):
        ax = fig.add_subplot(gs[0, i])
        ax.set_facecolor("#2A0000")
        ax.text(0.5, 0.58, val, ha="center", va="center",
                fontsize=22, fontweight="bold", color=ACCENT, transform=ax.transAxes)
        ax.text(0.5, 0.28, label, ha="center", va="center",
                fontsize=10, color=MUTED, transform=ax.transAxes)
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_edgecolor("#550000")

    # Top 5 videos bar (bottom left, spanning 2 cols)
    ax2 = fig.add_subplot(gs[1, :2])
    top5 = df_top.head(5)
    labels = [t[:38] + "…" if len(t) > 38 else t for t in top5["title"]]
    ax2.barh(labels[::-1], top5["views"][::-1] / 1e6,
             color=PALETTE[:5][::-1], height=0.55, edgecolor="none")
    ax2.set_xlabel("Views (M)", color=MUTED, fontsize=9)
    ax2.set_title("Top 5 by Views", fontsize=11, fontweight="bold")
    ax2.xaxis.set_major_formatter(mtick.FormatStrFormatter("%.0fM"))
    ax2.grid(axis="x", linestyle="--", alpha=0.3)
    ax2.spines[["top", "right", "left"]].set_visible(False)
    ax2.tick_params(labelsize=8)

    # Category pie (bottom right)
    ax3 = fig.add_subplot(gs[1, 2])
    top_cat = df_cat.nlargest(5, "video_count")
    ax3.pie(top_cat["video_count"], labels=top_cat["category"],
            colors=PALETTE[:5], autopct="%1.0f%%",
            wedgeprops=dict(width=0.5, edgecolor=BG, linewidth=1.5),
            textprops={"fontsize": 7, "color": MUTED},
            pctdistance=0.78, startangle=120)
    ax3.set_title("Top Categories", fontsize=11, fontweight="bold")

    return _save(fig, "00_summary_dashboard.png")
