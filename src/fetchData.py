# src/fetchData.py
import os
import sys
import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load env vars
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("❌ DATABASE_URL not set in .env", file=sys.stderr)
    sys.exit(1)

engine = create_engine(DATABASE_URL, future=True)

def fetch_season_stats(season="2022-23"):
    """Fetch player stats for a given NBA season."""
    print(f"📥 Fetching data for {season}...")
    stats = leaguedashplayerstats.LeagueDashPlayerStats(season=season).get_data_frames()[0]
    print(f"✅ Retrieved {len(stats)} rows for {season}")
    return stats

def insert_data(df, season):
    """Insert season and player stats into database."""
    with engine.begin() as conn:
        # Insert season
        conn.execute(
            text("INSERT INTO seasons (season) VALUES (:season) ON CONFLICT DO NOTHING"),
            {"season": season}
        )

        for _, row in df.iterrows():
            player_id = int(row["PLAYER_ID"])
            player_name = row["PLAYER_NAME"]

            # Skip missing player names
            if pd.isna(player_name) or str(player_name).strip() == "":
                print(f"⚠️ Skipping player_id {player_id} because name is missing")
                continue

            # Insert player
            conn.execute(
                text("""
                    INSERT INTO players (player_id, player_name)
                    VALUES (:player_id, :player_name)
                    ON CONFLICT (player_id) DO NOTHING
                """),
                {"player_id": player_id, "player_name": player_name}
            )

            # Insert player stats
            conn.execute(
                text("""
                    INSERT INTO player_season_stats
                    (player_id, season, team_abbr, gp, min_total, fga, fgm, fg3a, fg3m,
                     fta, ftm, oreb, dreb, reb, ast, stl, blk, tov, pts, ts_pct)
                    VALUES (:player_id, :season, :team_abbr, :gp, :min_total, :fga, :fgm, :fg3a, :fg3m,
                            :fta, :ftm, :oreb, :dreb, :reb, :ast, :stl, :blk, :tov, :pts, :ts_pct)
                    ON CONFLICT (season, player_id) DO NOTHING
                """),
                {
                    "player_id": row["PLAYER_ID"],
                    "season": season,
                    "team_abbr": row["TEAM_ABBREVIATION"],
                    "gp": row["GP"],
                    "min_total": row["MIN"],
                    "fga": row["FGA"],
                    "fgm": row["FGM"],
                    "fg3a": row["FG3A"],
                    "fg3m": row["FG3M"],
                    "fta": row["FTA"],
                    "ftm": row["FTM"],
                    "oreb": row["OREB"],
                    "dreb": row["DREB"],
                    "reb": row["REB"],
                    "ast": row["AST"],
                    "stl": row["STL"],
                    "blk": row["BLK"],
                    "tov": row["TOV"],
                    "pts": row["PTS"],
                    "ts_pct": row.get("TS_PCT", None),  # handle missing TS_PCT
                }
            )

    print(f"✅ Inserted {len(df)} player rows for {season}")

def main():
    season = "2022-23"
    df = fetch_season_stats(season)
    insert_data(df, season)
    print("Columns in DataFrame:", df.columns.tolist())

if __name__ == "__main__":
    main()
