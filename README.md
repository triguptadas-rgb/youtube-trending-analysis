# 📺 YouTube Trending Videos Analysis

A Python data analysis project that fetches, analyses, and visualises YouTube trending videos — covering top videos, dominant channels, category distribution, and engagement patterns.

> Works out of the box with **mock data** — no API key required to run!

---

## 📊 Sample Charts

| Summary Dashboard | Top Videos |
|---|---|
| `charts/00_summary_dashboard.png` | `charts/01_top_videos_by_views.png` |

| Channel Bubble Chart | Category Breakdown |
|---|---|
| `charts/02_top_channels_bubble.png` | `charts/03_category_breakdown.png` |

| Engagement Heatmap | Views vs Like Rate |
|---|---|
| `charts/04_engagement_heatmap.png` | `charts/05_views_vs_like_rate.png` |

---

## ✨ Features

- 🎲 **Demo mode** — realistic mock data, zero setup required
- 🌐 **Live mode** — plug in a free YouTube Data API key for real trending data
- 📊 **6 charts** — dashboard, bar charts, bubble chart, donut, heatmap, scatter
- 🗂️ **Multi-region** — analyse US, IN, GB, JP, BR, and more
- 📓 **Jupyter Notebook** — interactive, cell-by-cell exploration
- 📁 **JSON export** — all results saved for downstream use

---

## 🗂️ Project Structure

```
yt-trending-analysis/
├── main.py            # Run the full pipeline in one command
├── data_fetcher.py    # Mock data generator + YouTube API fetcher
├── analyzer.py        # All analysis functions (pure pandas)
├── visualizer.py      # All chart functions (matplotlib + seaborn)
├── analysis.ipynb     # Jupyter Notebook walkthrough
├── requirements.txt
├── .gitignore
├── data/              # Generated JSON files (auto-created)
└── charts/            # Generated PNG charts (auto-created)
```

---

## 🚀 Quick Start

### 1. Clone & install

```bash
git clone https://github.com/YOUR_USERNAME/yt-trending-analysis.git
cd yt-trending-analysis
pip install -r requirements.txt
```

### 2. Run with mock data (no API key needed)

```bash
python main.py
```

Charts will be saved to `charts/` and a results JSON to `data/results_US.json`.

### 3. Run with live YouTube data

1. Get a free API key at [console.cloud.google.com](https://console.cloud.google.com)
2. Enable the **YouTube Data API v3**
3. Run:

```bash
python main.py --api-key YOUR_KEY --region US
```

### 4. Open the Jupyter Notebook

```bash
jupyter notebook analysis.ipynb
```

---

## 🌍 Supported Regions

Pass any of these with `--region`:

| Code | Country       | Code | Country     |
|------|---------------|------|-------------|
| US   | United States | IN   | India       |
| GB   | United Kingdom| JP   | Japan       |
| BR   | Brazil        | DE   | Germany     |
| FR   | France        | KR   | South Korea |

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| `pandas` | Data loading, cleaning, aggregation |
| `matplotlib` | All chart rendering |
| `seaborn` | Heatmap |
| `google-api-python-client` | YouTube Data API v3 (optional) |

---

## 📌 Analysis Covered

- **Top videos** by views, likes, and engagement rate
- **Top channels** by trending appearances and total views
- **Category breakdown** — which content types dominate trending
- **Engagement heatmap** — multi-metric channel comparison
- **Views vs like rate** scatter — do more views mean more engagement?
- **Channel diversity** — how concentrated is trending content?

---

## 🔮 Ideas to Extend This

- [ ] Compare trending across multiple regions side-by-side
- [ ] Track the same videos over multiple days (time-series)
- [ ] Add sentiment analysis on video titles
- [ ] Build a Streamlit dashboard for interactive exploration
- [ ] Predict view count from title length and publish time

---

## ⚠️ API Key Safety

**Never commit your API key to GitHub.** The `.gitignore` excludes `secrets.py` — store your key there if you prefer not to pass it via CLI.

```python
# secrets.py  (never committed)
API_KEY = "YOUR_KEY_HERE"
```

---

## 📄 License

MIT — free to use and build on.

---

Built with 📺 and Python.
