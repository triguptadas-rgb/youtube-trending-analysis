"""
data_fetcher.py
───────────────
Fetches YouTube trending videos via the YouTube Data API v3.
Falls back to realistic mock data when no API key is provided.

Usage:
    python data_fetcher.py                  # uses mock data
    python data_fetcher.py --api-key YOUR_KEY --region US
"""

import json
import random
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# ── Try importing the Google API client (optional) ─────────────────────────
try:
    from googleapiclient.discovery import build
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False

# ── Constants ──────────────────────────────────────────────────────────────
OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

CATEGORIES = {
    "1":  "Film & Animation",
    "2":  "Autos & Vehicles",
    "10": "Music",
    "15": "Pets & Animals",
    "17": "Sports",
    "20": "Gaming",
    "22": "People & Blogs",
    "23": "Comedy",
    "24": "Entertainment",
    "25": "News & Politics",
    "26": "Howto & Style",
    "27": "Education",
    "28": "Science & Technology",
    "29": "Nonprofits & Activism",
}

CHANNELS = [
    "MrBeast", "T-Series", "PewDiePie", "Cocomelon", "SET India",
    "5-Minute Crafts", "WWE", "Zee Music Company", "Canal KondZilla",
    "Like Nastya", "Vlad and Niki", "Ryan's World", "Dude Perfect",
    "Mark Rober", "Veritasium", "Kurzgesagt", "MKBHD", "Linus Tech Tips",
    "Nas Daily", "Yes Theory", "Cody Ko", "David Dobrik", "Emma Chamberlain",
    "Charli D'Amelio", "Ninja", "Pokimane", "Valkyrae", "Dream",
    "Lex Fridman", "Andrew Huberman", "Ali Abdaal", "Thomas Frank",
]

TITLE_TEMPLATES = [
    "I Spent {n} Days in {place} and This Happened",
    "Reacting to the World's {adj} {thing}",
    "Why {thing} is Actually {adj}",
    "{n} Things You Didn't Know About {thing}",
    "I Tried {thing} for {n} Days — Here's What Happened",
    "The Truth About {thing} Nobody Talks About",
    "How {thing} Changed My Life Forever",
    "{thing}: A Complete {n}-Hour Deep Dive",
    "I Built {thing} From Scratch in {n} Hours",
    "Exposing the {adj} Side of {thing}",
    "Rating Every {thing} I've Ever Tried",
    "My {adj} Journey to Become a {thing}",
    "This {thing} Cost Me ${n},000 — Was It Worth It?",
    "Testing {adj} {thing} So You Don't Have To",
    "The Most {adj} {thing} of 2024",
]

FILL = {
    "n":     [3, 7, 10, 24, 30, 100, 1000],
    "place": ["Antarctica", "Tokyo", "the Amazon", "Mars (simulation)", "Area 51", "Dubai", "North Korea"],
    "adj":   ["Expensive", "Dangerous", "Unusual", "Underrated", "Overrated", "Satisfying", "Viral", "Shocking"],
    "thing": ["AI", "YouTube", "the Internet", "a Tiny House", "Street Food", "Formula 1", "Chess", "Crypto",
              "a Budget PC", "the Stock Market", "a $1 Meal", "Zero Waste", "Cold Showers", "No Sleep"],
}


def _random_title() -> str:
    template = random.choice(TITLE_TEMPLATES)
    for key, options in FILL.items():
        placeholder = "{" + key + "}"
        if placeholder in template:
            template = template.replace(placeholder, str(random.choice(options)), 1)
    return template


def generate_mock_data(n: int = 50, region: str = "US") -> list[dict]:
    """Generate realistic-looking trending video records."""
    random.seed(42)
    videos = []
    base_date = datetime.now()

    for rank in range(1, n + 1):
        pub_days_ago = random.randint(1, 14)
        published_at = (base_date - timedelta(days=pub_days_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")

        # Engagement metrics — top-ranked videos get higher numbers
        scale = max(0.1, 1 - (rank / n) * 0.85)
        views    = int(random.uniform(500_000, 50_000_000) * scale)
        likes    = int(views * random.uniform(0.02, 0.08))
        comments = int(views * random.uniform(0.002, 0.015))

        cat_id = random.choice(list(CATEGORIES.keys()))

        videos.append({
            "rank":          rank,
            "video_id":      f"mock_{rank:04d}",
            "title":         _random_title(),
            "channel":       random.choice(CHANNELS),
            "category_id":   cat_id,
            "category":      CATEGORIES[cat_id],
            "views":         views,
            "likes":         likes,
            "comments":      comments,
            "like_rate":     round(likes / views * 100, 2),
            "comment_rate":  round(comments / views * 100, 3),
            "published_at":  published_at,
            "days_since_pub": pub_days_ago,
            "region":        region,
        })

    return videos


def fetch_live_data(api_key: str, region: str = "US", max_results: int = 50) -> list[dict]:
    """Fetch real trending videos from the YouTube Data API v3."""
    if not GOOGLE_API_AVAILABLE:
        raise ImportError(
            "google-api-python-client is required for live data.\n"
            "Install it with: pip install google-api-python-client"
        )

    youtube = build("youtube", "v3", developerKey=api_key)
    response = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode=region,
        maxResults=max_results,
    ).execute()

    videos = []
    for rank, item in enumerate(response.get("items", []), start=1):
        snippet = item["snippet"]
        stats   = item.get("statistics", {})
        views   = int(stats.get("viewCount", 0))
        likes   = int(stats.get("likeCount", 0))
        comments = int(stats.get("commentCount", 0))
        cat_id  = snippet.get("categoryId", "0")

        videos.append({
            "rank":          rank,
            "video_id":      item["id"],
            "title":         snippet.get("title", ""),
            "channel":       snippet.get("channelTitle", ""),
            "category_id":   cat_id,
            "category":      CATEGORIES.get(cat_id, "Other"),
            "views":         views,
            "likes":         likes,
            "comments":      comments,
            "like_rate":     round(likes / views * 100, 2) if views else 0,
            "comment_rate":  round(comments / views * 100, 3) if views else 0,
            "published_at":  snippet.get("publishedAt", ""),
            "days_since_pub": None,
            "region":        region,
        })

    return videos


def save(videos: list[dict], region: str = "US"):
    path = OUTPUT_DIR / f"trending_{region}.json"
    with open(path, "w") as f:
        json.dump(videos, f, indent=2)
    print(f"✅  Saved {len(videos)} videos → {path}")
    return path


# ── CLI entry point ────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch YouTube trending data")
    parser.add_argument("--api-key", default=None, help="YouTube Data API v3 key")
    parser.add_argument("--region",  default="US",  help="Region code (default: US)")
    parser.add_argument("--count",   default=50, type=int, help="Number of videos")
    args = parser.parse_args()

    if args.api_key:
        print(f"🌐  Fetching live data for region={args.region} ...")
        data = fetch_live_data(args.api_key, args.region, args.count)
    else:
        print(f"🎲  No API key provided — generating mock data (region={args.region}) ...")
        data = generate_mock_data(args.count, args.region)

    save(data, args.region)
