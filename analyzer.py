"""
analyzer.py
───────────
Core analysis functions for YouTube trending data.
All functions accept a pandas DataFrame and return
either a transformed DataFrame or a plain dict/value.
"""

import pandas as pd


# ── Load ───────────────────────────────────────────────────────────────────

def load(path: str) -> pd.DataFrame:
    """Load a JSON data file into a clean DataFrame."""
    df = pd.read_json(path)
    df["published_at"] = pd.to_datetime(df["published_at"], utc=True, errors="coerce")
    return df


# ── Top-N helpers ──────────────────────────────────────────────────────────

def top_videos_by_views(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return the top N videos ranked by view count."""
    return (
        df.nlargest(n, "views")
          [["rank", "title", "channel", "category", "views", "likes", "comments"]]
          .reset_index(drop=True)
    )


def top_channels(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Rank channels by total trending appearances, total views,
    and average engagement rate.
    """
    agg = (
        df.groupby("channel")
          .agg(
              appearances=("video_id", "count"),
              total_views=("views", "sum"),
              avg_like_rate=("like_rate", "mean"),
              avg_comment_rate=("comment_rate", "mean"),
          )
          .sort_values(["appearances", "total_views"], ascending=False)
          .head(n)
          .reset_index()
    )
    agg["avg_like_rate"]    = agg["avg_like_rate"].round(2)
    agg["avg_comment_rate"] = agg["avg_comment_rate"].round(3)
    return agg


def category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Summarise trending videos by content category."""
    return (
        df.groupby("category")
          .agg(
              video_count=("video_id", "count"),
              total_views=("views", "sum"),
              avg_views=("views", "mean"),
              avg_like_rate=("like_rate", "mean"),
          )
          .sort_values("video_count", ascending=False)
          .reset_index()
    )


def engagement_stats(df: pd.DataFrame) -> dict:
    """Return high-level engagement summary statistics."""
    return {
        "total_videos":      len(df),
        "total_views":       int(df["views"].sum()),
        "avg_views":         int(df["views"].mean()),
        "median_views":      int(df["views"].median()),
        "avg_like_rate":     round(df["like_rate"].mean(), 2),
        "avg_comment_rate":  round(df["comment_rate"].mean(), 3),
        "most_viewed_title": df.loc[df["views"].idxmax(), "title"],
        "most_viewed_views": int(df["views"].max()),
    }


def views_vs_engagement(df: pd.DataFrame) -> pd.DataFrame:
    """Return a clean frame suitable for scatter / bubble plots."""
    return df[["title", "channel", "category", "views", "likes",
               "comments", "like_rate", "comment_rate"]].copy()


def top_videos_by_likes(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return the top N videos by like count."""
    return (
        df.nlargest(n, "likes")
          [["rank", "title", "channel", "category", "views", "likes", "like_rate"]]
          .reset_index(drop=True)
    )


def channel_diversity(df: pd.DataFrame) -> dict:
    """How concentrated is trending content? (fewer unique channels = more dominant)"""
    total    = len(df)
    unique   = df["channel"].nunique()
    top1_pct = round(df["channel"].value_counts().iloc[0] / total * 100, 1)
    return {
        "total_videos":   total,
        "unique_channels": unique,
        "channel_diversity_ratio": round(unique / total, 2),
        "top_channel_share_pct": top1_pct,
    }
