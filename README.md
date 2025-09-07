# NBA Player Efficiency Index

A Python project to fetch NBA player stats for the 2022-2023 seaoson, calculate efficiency ratings, and store the data in a PostgreSQL database.

<img width="455" height="361" alt="Screenshot 2025-09-07 at 11 58 22 AM" src="https://github.com/user-attachments/assets/d3ca4ef1-9d0a-41bd-a23f-b763708ed70a" />

## Features

- Fetch NBA player statistics for a given season using the `nba_api`.
- Store player, team, and season stats in PostgreSQL.
- Calculate player efficiency based on points, rebounds, assists, steals, blocks, turnovers, and minutes.
- Query efficiency stats with player names and seasons.

## Tech Stack

- Python 3.9+
- PostgreSQL
- SQLAlchemy
- Pandas
- `nba_api`
- `python-dotenv`
