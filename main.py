"""
main.py
───────
Entry point — runs the full YouTube Trending analysis pipeline.

Usage:
    python main.py                       # mock data, US region
    python main.py --api-key YOUR_KEY   # live data
    python main.py --region IN           # different region (with API key)
"""

import argparse
import json
from pathlib import Path

from data_fetcher import generate_mock_data, fetch_live_data, save as save_data
from analyzer import (
    load, top_videos_by_views, top_channels, category_breakdown,
    engagement_stats, views_vs_engagement, top_videos_by_likes, channel_diversity
)
from visualizer import (
    chart_top_videos, chart_top_channels, chart_category_donut,
    chart_engagement_heatmap, chart_views_vs_likes, chart_summary_dashboard
)


def run(api_key: str | None = None, region: str = "US", count: int = 50):
    print("\n" + "═" * 55)
    print("  📺  YouTube Trending Analysis")
    print("═" * 55)

    # ── 1. Fetch / load data ──────────────────────────────────
    data_path = Path("data") / f"trending_{region}.json"

    if api_key:
        print(f"\n🌐  Fetching live data (region={region}) ...")
        raw = fetch_live_data(api_key, region, count)
        save_data(raw, region)
    elif data_path.exists():
        print(f"\n📂  Loading existing data from {data_path} ...")
    else:
        print(f"\n🎲  Generating mock data (region={region}, n={count}) ...")
        raw = generate_mock_data(count, region)
        save_data(raw, region)

    df = load(str(data_path))
    print(f"    Loaded {len(df)} videos.\n")

    # ── 2. Analyse ────────────────────────────────────────────
    print("🔍  Running analysis...")
    stats   = engagement_stats(df)
    df_top  = top_videos_by_views(df, 10)
    df_ch   = top_channels(df, 10)
    df_cat  = category_breakdown(df)
    df_eng  = views_vs_engagement(df)
    df_div  = channel_diversity(df)

    # Print summary to console
    print("\n── Engagement Summary ──────────────────────────")
    for k, v in stats.items():
        label = k.replace("_", " ").title()
        val   = f"{v:,}" if isinstance(v, int) else v
        print(f"  {label:<25} {val}")

    print("\n── Channel Diversity ───────────────────────────")
    for k, v in df_div.items():
        label = k.replace("_", " ").title()
        print(f"  {label:<30} {v}")

    print("\n── Top 5 Videos by Views ───────────────────────")
    for _, row in df_top.head(5).iterrows():
        views_m = f"{row['views']/1e6:.1f}M"
        print(f"  #{int(row['rank'])}  {row['title'][:48]:<50} {views_m}")

    print("\n── Top 5 Channels ──────────────────────────────")
    for _, row in df_ch.head(5).iterrows():
        print(f"  {row['channel']:<22} appearances={int(row['appearances'])}  "
              f"total_views={int(row['total_views']):,}")

    # ── 3. Visualise ──────────────────────────────────────────
    print("\n📊  Generating charts...")
    chart_summary_dashboard(stats, df_top, df_cat)
    chart_top_videos(df_top)
    chart_top_channels(df_ch)
    chart_category_donut(df_cat)
    chart_engagement_heatmap(df_ch)
    chart_views_vs_likes(df_eng)

    # ── 4. Export results JSON ────────────────────────────────
    results = {
        "summary":    stats,
        "diversity":  df_div,
        "top_videos": df_top.to_dict(orient="records"),
        "top_channels": df_ch.to_dict(orient="records"),
        "categories": df_cat.to_dict(orient="records"),
    }
    out = Path("data") / f"results_{region}.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n✅  Results saved → {out}")

    print("\n" + "═" * 55)
    print("  ✅  Analysis complete! Charts saved to charts/")
    print("═" * 55 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--region",  default="US")
    parser.add_argument("--count",   default=50, type=int)
    args = parser.parse_args()
    run(args.api_key, args.region, args.count)
