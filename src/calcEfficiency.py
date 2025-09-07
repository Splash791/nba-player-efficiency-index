# src/calcEfficiency.py
import os
import sys
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("❌ DATABASE_URL not set in .env", file=sys.stderr)
    sys.exit(1)

engine = create_engine(DATABASE_URL, future=True)

def calculate_efficiency(row):
    """Calculate simple player efficiency for a row."""
    # Normalize column names to lowercase for safety
    row = {k.lower(): (v if v is not None else 0) for k, v in row.items()}

    pts = row.get("pts", 0)
    reb = row.get("reb", 0)
    ast = row.get("ast", 0)
    stl = row.get("stl", 0)
    blk = row.get("blk", 0)
    tov = row.get("tov", 0)

    efficiency = pts + reb + ast + stl + blk - tov
    return efficiency

def update_efficiency(season="2022-23"):
    """Fetch all players for a season and calculate/update efficiency."""
    with engine.begin() as conn:
        # Pull all player stats for the season
        df = pd.read_sql(
            text("SELECT * FROM player_season_stats WHERE season = :season"),
            conn,
            params={"season": season}
        )

        if df.empty:
            print(f"⚠️ No player stats found for season {season}")
            return

        # Normalize column names to lowercase
        df.columns = [c.lower() for c in df.columns]

        # Calculate efficiency
        df["efficiency"] = df.apply(calculate_efficiency, axis=1)

        # Upsert into player_efficiency table
        for _, row in df.iterrows():
            conn.execute(
                text("""
                    INSERT INTO player_efficiency (player_id, season, efficiency)
                    VALUES (:player_id, :season, :efficiency)
                    ON CONFLICT (player_id, season) DO UPDATE
                    SET efficiency = EXCLUDED.efficiency
                """),
                {
                    "player_id": row["player_id"],
                    "season": row["season"],
                    "efficiency": row["efficiency"],
                }
            )

    print(f"✅ Inserted/Updated efficiency for {len(df)} players in {season}")

def main():
    season = "2022-23"
    update_efficiency(season)

if __name__ == "__main__":
    main()
