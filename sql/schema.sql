CREATE TABLE IF NOT EXISTS seasons (
    season_id SERIAL PRIMARY KEY,
    season TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    player_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS player_season_stats (
    season TEXT NOT NULL REFERENCES seasons(season),
    player_id INTEGER NOT NULL REFERENCES players(player_id),
    team_abbr TEXT,
    gp INTEGER,
    min_total NUMERIC,
    fga NUMERIC, fgm NUMERIC,
    fg3a NUMERIC, fg3m NUMERIC,
    fta NUMERIC, ftm NUMERIC,
    oreb NUMERIC, dreb NUMERIC, reb NUMERIC,
    ast NUMERIC, stl NUMERIC, blk NUMERIC,
    tov NUMERIC, pts NUMERIC,
    ts_pct NUMERIC,
    PRIMARY KEY (season, player_id)
);

CREATE INDEX IF NOT EXISTS idx_pss_season ON player_season_stats(season);
