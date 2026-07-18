🔗 [Live App](https://netflix-analysed-gmoexu2le5twdmaaiuvqhe.streamlit.app/)
# Netflix Analysed 🎬

**YOU WATCHED. WE ANALYSED.**

A Streamlit web app that analyzes personal Netflix viewing history data and surfaces insights across viewing patterns, content preferences, behavior, and fun stats — all from a CSV export of your own watch history.

## What it does

Upload your Netflix viewing history CSV, pick a profile, and explore your data across three categories:

### ⏱️ Time-Series Analysis (The "When")
- **Peak Viewing Hours** — distribution of watch time across the 24-hour clock
- **Monthly Trends** — total hours watched per month
- **Weekly Rhythm** — weekday vs. weekend viewing split
- **Streak Finder** — longest run of consecutive days watched

### 🎭 Content & Genre Deep-Dives (The "What")
- **Series vs. Movies Split** — proportion of episodic content vs. feature films
- **Rewatch Leaderboard** — most-watched series and movie
- **Genre Distribution** — breakdown of viewing by genre

### 📱 Behavioral & Device Insights (The "How")
- **Device Dominance** — which device gets the most screen time
- **Cost Per Hour** — how much a given month of viewing "cost" based on your subscription fee
- **Bollywood Scale** — split between Indian and international content

## Tech Stack

- **Python** — core language
- **Pandas** — data cleaning, filtering, aggregation, and analysis
- **Matplotlib** — chart generation
- **Streamlit** — interactive web app / frontend

## Project Structure

```
Netflix_Project/
├── Netflix_Backend.py    # All data processing and analysis functions
├── Netflix_Frontend.py   # Streamlit UI, layout, and state management
└── README.md
```

The backend and frontend are fully decoupled — `Netflix_Backend.py` contains no Streamlit code and can be tested or reused independently of the UI.

## How It Works

1. User uploads a Netflix viewing history CSV (exported from Netflix's account activity page)
2. App reads the available profiles from the data and lets the user select one
3. Once confirmed, the app processes the data for that profile and displays four clickable sections
4. Each section runs the relevant backend function(s) and renders the result as a chart or stat

## Running Locally

```bash
pip install streamlit pandas matplotlib
streamlit run Netflix_Frontend.py
```

## CSV Format

The app expects a CSV with the following columns (standard Netflix viewing activity export format):

| Column | Description |
|---|---|
| `Profile Name` | Netflix profile the session belongs to |
| `Start Time` | Timestamp of when viewing started |
| `Duration` | Length of the session (HH:MM:SS) |
| `Title` | Title of the content watched |
| `Attributes` | Additional metadata (e.g. autoplay, download) |
| `Device Type` | Device used to watch |
| `Country` | Country the session occurred in |

## Notes

- Genre tagging currently relies on a manually curated title-to-genre mapping and will label unrecognized titles as unmatched — this is a known limitation for datasets with titles outside the current mapping.
- Built as a personal data analysis / portfolio project to practice pandas fundamentals (filtering, grouping, datetime handling, string operations) and building an interactive data app end-to-end.

## Possible Future Additions

- Content-based recommendation system using cosine similarity
- Expanded, more complete genre mapping
- Binge session detection
- Support for multi-year year-over-year comparisons
